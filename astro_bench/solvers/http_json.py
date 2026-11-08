"""Generic HTTP solver: ``http_json:<config.yaml>`` (ADR-002 decision 4).

Config keys::

    url: https://example.org/v1/answer       # required
    method: POST                              # default POST
    headers: {Authorization: "Bearer ${MY_API_KEY}"}   # ${VAR} read from the environment
    body_template: {question: "{prompt}", system: "{system}", meta: {id: "{item_id}"}}
    reply_path: data.answer.text              # dotted JSON path (list indexes allowed)
    reply: text                               # instead of reply_path: the raw body is the reply
    rate_limit_per_minute: 30                 # optional
    timeout_s: 60                             # default 60
    retry_on_429: true                        # default true; honours Retry-After
    max_retries: 5                            # default 5

Placeholders in ``body_template`` strings: ``{system}``, ``{prompt}`` (the rendered user
message), ``{convention}``, ``{input_mode}``, ``{item_id}``. The template is a YAML/JSON
structure; substitution happens inside string values, so the request is always valid
JSON. Credentials never live in the config: an unset ``${VAR}`` is an error at start-up.
"""

from __future__ import annotations

import json
import os
import re
import time
import urllib.error
import urllib.request
from collections.abc import Callable
from pathlib import Path
from typing import Any

import yaml

from ..prompts import render_user_message, system_prompt
from ..schema import SolverItem

_ENV = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")
PLACEHOLDERS = ("system", "prompt", "convention", "input_mode", "item_id")


class HttpSolverError(RuntimeError):
    """The HTTP solver is misconfigured or the endpoint failed."""


def resolve_env(value: str, environ: dict[str, str] | None = None) -> str:
    env = os.environ if environ is None else environ

    def repl(match: re.Match[str]) -> str:
        name = match.group(1)
        if not env.get(name):
            raise HttpSolverError(f"environment variable {name} is not set")
        return env[name]

    return _ENV.sub(repl, value)


def fill(template: Any, values: dict[str, str]) -> Any:
    """Substitute ``{name}`` placeholders inside every string of ``template``."""
    if isinstance(template, str):
        out = template
        for key, val in values.items():
            out = out.replace("{" + key + "}", val)
        return out
    if isinstance(template, dict):
        return {k: fill(v, values) for k, v in template.items()}
    if isinstance(template, list):
        return [fill(v, values) for v in template]
    return template


def dig(data: Any, path: str) -> Any:
    """Follow a dotted path (``choices.0.message.content``) into parsed JSON."""
    for part in path.split("."):
        if isinstance(data, list) and part.lstrip("-").isdigit():
            data = data[int(part)]
        elif isinstance(data, dict) and part in data:
            data = data[part]
        else:
            raise HttpSolverError(f"reply_path {path!r} not found at {part!r}")
    return data


class HttpJsonSolver:
    def __init__(self, config: dict[str, Any], *, environ: dict[str, str] | None = None,
                 sleep: Callable[[float], None] = time.sleep,
                 clock: Callable[[], float] = time.monotonic):
        if not config.get("url"):
            raise HttpSolverError("config needs a url")
        if not config.get("reply_path") and config.get("reply") != "text":
            raise HttpSolverError("config needs reply_path or reply: text")
        self.url = resolve_env(str(config["url"]), environ)
        self.method = str(config.get("method", "POST")).upper()
        self.headers = {"Content-Type": "application/json"}
        for key, value in (config.get("headers") or {}).items():
            self.headers[str(key)] = resolve_env(str(value), environ)
        self.body_template = config.get("body_template") or {
            "system": "{system}", "prompt": "{prompt}", "convention": "{convention}",
            "input_mode": "{input_mode}", "item_id": "{item_id}"}
        self.reply_path = config.get("reply_path")
        self.timeout = float(config.get("timeout_s", 60))
        self.retry_on_429 = bool(config.get("retry_on_429", True))
        self.max_retries = int(config.get("max_retries", 5))
        rpm = config.get("rate_limit_per_minute")
        self.min_interval = 60.0 / float(rpm) if rpm else 0.0
        self.sleep, self.clock = sleep, clock
        self._last: float | None = None
        self.name = "http_json"

    @classmethod
    def from_file(cls, path: str | Path, **kwargs: Any) -> HttpJsonSolver:
        config = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
        return cls(config, **kwargs)

    def body(self, item: SolverItem) -> bytes:
        values = {"system": system_prompt(), "prompt": render_user_message(item),
                  "convention": item.convention.words(), "input_mode": item.input_mode,
                  "item_id": item.id}
        return json.dumps(fill(self.body_template, values), ensure_ascii=False).encode()

    def _throttle(self) -> None:
        if self.min_interval and self._last is not None:
            wait = self.min_interval - (self.clock() - self._last)
            if wait > 0:
                self.sleep(wait)
        self._last = self.clock()

    def _send(self, data: bytes) -> str:
        for attempt in range(self.max_retries + 1):
            self._throttle()
            req = urllib.request.Request(self.url, data=data, headers=self.headers,
                                         method=self.method)
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:  # noqa: S310
                    return str(resp.read().decode("utf-8"))
            except urllib.error.HTTPError as exc:
                if exc.code == 429 and self.retry_on_429 and attempt < self.max_retries:
                    retry_after = exc.headers.get("Retry-After") if exc.headers else None
                    try:
                        delay = float(retry_after) if retry_after else 2.0 ** attempt
                    except ValueError:
                        delay = 2.0 ** attempt
                    self.sleep(delay)
                    continue
                raise HttpSolverError(f"HTTP {exc.code} from {self.url}") from exc
        raise HttpSolverError(f"gave up after {self.max_retries} retries")

    def __call__(self, item: SolverItem) -> str:
        text = self._send(self.body(item))
        if not self.reply_path:
            return text
        reply = dig(json.loads(text), str(self.reply_path))
        return reply if isinstance(reply, str) else json.dumps(reply)
