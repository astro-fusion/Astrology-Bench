"""The http_json solver against a local in-process HTTP server (no network)."""

from __future__ import annotations

import json
import threading
from collections.abc import Iterator
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any

import pytest
import yaml

from astro_bench.canon import Canon
from astro_bench.redact import to_solver_item
from astro_bench.runner import run
from astro_bench.schema import Item
from astro_bench.solvers import get_solver
from astro_bench.solvers.http_json import HttpJsonSolver, HttpSolverError, dig, fill


class Server:
    def __init__(self) -> None:
        self.requests: list[dict[str, Any]] = []
        self.fail_429 = 0
        outer = self

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self) -> None:  # noqa: N802
                body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                outer.requests.append({"headers": dict(self.headers), "body": body})
                if outer.fail_429 > 0:
                    outer.fail_429 -= 1
                    self.send_response(429)
                    self.send_header("Retry-After", "0")
                    self.end_headers()
                    return
                reply = {"answer": True, "citations": [], "confidence": 0.5}
                payload = json.dumps({"data": [{"text": json.dumps(reply)}]}).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)

            def log_message(self, *args: Any) -> None:
                pass

        self.httpd = HTTPServer(("127.0.0.1", 0), Handler)
        self.url = f"http://127.0.0.1:{self.httpd.server_address[1]}/answer"
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()


@pytest.fixture()
def server() -> Iterator[Server]:
    srv = Server()
    yield srv
    srv.httpd.shutdown()


def config(url: str, **extra: Any) -> dict[str, Any]:
    return {"url": url, "headers": {"Authorization": "Bearer ${BENCH_TEST_KEY}"},
            "body_template": {"sys": "{system}", "q": "{prompt}", "meta": {
                "id": "{item_id}", "conv": "{convention}", "mode": "{input_mode}"}},
            "reply_path": "data.0.text", "timeout_s": 5, **extra}


def test_posts_template_and_reads_reply(server: Server, small_items: list[Item],
                                        canon: Canon) -> None:
    item = next(i for i in small_items if i.level == 1)
    solver = HttpJsonSolver(config(server.url), environ={"BENCH_TEST_KEY": "s3cret"})
    view = to_solver_item(item)
    reply = solver(view)
    assert json.loads(reply)["answer"] is True
    sent = server.requests[0]
    assert sent["headers"]["Authorization"] == "Bearer s3cret"
    assert sent["body"]["meta"] == {"id": item.id, "conv": item.convention.words(),
                                    "mode": "chart"}
    assert item.prompt in sent["body"]["q"] and "Astro-Bench" in sent["body"]["sys"]
    assert "gold" not in json.dumps(sent["body"])


def test_missing_env_fails_at_start(server: Server) -> None:
    with pytest.raises(HttpSolverError, match="BENCH_TEST_KEY"):
        HttpJsonSolver(config(server.url), environ={})


def test_retries_on_429_and_rate_limits(server: Server, small_items: list[Item]) -> None:
    sleeps: list[float] = []
    server.fail_429 = 2
    solver = HttpJsonSolver(config(server.url, rate_limit_per_minute=60),
                            environ={"BENCH_TEST_KEY": "k"}, sleep=sleeps.append)
    view = to_solver_item(small_items[0])
    assert json.loads(solver(view))["answer"] is True
    assert len(server.requests) == 3
    solver(view)
    assert any(s > 0.5 for s in sleeps)  # throttled to one call per second


def test_429_without_retry_is_an_error(server: Server, small_items: list[Item]) -> None:
    server.fail_429 = 1
    solver = HttpJsonSolver(config(server.url, retry_on_429=False),
                            environ={"BENCH_TEST_KEY": "k"})
    with pytest.raises(HttpSolverError, match="429"):
        solver(to_solver_item(small_items[0]))


def test_reply_text_mode_and_cli_name(server: Server, tmp_path: Path,
                                      monkeypatch: pytest.MonkeyPatch,
                                      small_items: list[Item], canon: Canon) -> None:
    cfg = config(server.url, reply="text")
    del cfg["reply_path"]
    path = tmp_path / "solver.yaml"
    path.write_text(yaml.safe_dump(cfg))
    monkeypatch.setenv("BENCH_TEST_KEY", "k")
    solver = get_solver(f"http_json:{path}", small_items, canon)
    items = [i for i in small_items if i.answer_type == "bool"][:2]
    result = run(solver, items, canon, solver_name=f"http_json:{path}", kind="model")
    assert result.summary.overall.parse_error_rate == 1.0  # body is not the answer object


def test_helpers() -> None:
    assert fill({"a": ["x {prompt} y", 3]}, {"prompt": 'say "hi"'}) == {"a": ['x say "hi" y', 3]}
    assert dig({"a": [{"b": "c"}]}, "a.0.b") == "c"
    with pytest.raises(HttpSolverError):
        dig({"a": 1}, "a.b")
    with pytest.raises(HttpSolverError):
        HttpJsonSolver({"url": "http://x"})


PATH_MARKERS = ("/Users/", "/home/", "C:\\")


def test_result_records_no_filesystem_path(server: Server, tmp_path: Path,
                                           monkeypatch: pytest.MonkeyPatch,
                                           small_items: list[Item], canon: Canon) -> None:
    from astro_bench.runner import public_solver_name

    path = tmp_path / "my-endpoint.yaml"
    path.write_text(yaml.safe_dump(config(server.url)))
    monkeypatch.setenv("BENCH_TEST_KEY", "k")
    items = small_items[:2]
    for name in (f"http_json:{path}", f"nochart:http_json:{path}"):
        result = run(get_solver(name, items, canon), items, canon, solver_name=name,
                     kind="system", description="test endpoint")
        top = result.model_dump(mode="json", exclude={"per_item", "summary"})
        markers = (*PATH_MARKERS, str(tmp_path))
        leaked = {k: v for k, v in top.items()
                  if isinstance(v, str) and any(m in v for m in markers)}
        assert leaked == {}
        assert result.solver.endswith("http_json:my-endpoint")
        assert result.model == result.solver
    assert public_solver_name("http_json:C:\\cfg\\app.yml") == "http_json:app"
    assert public_solver_name("http_json:/home/u/x.yaml") == "http_json:x"
    assert public_solver_name("mock") == "mock"


def test_committed_results_contain_no_paths() -> None:
    import json as _json

    for path in sorted((Path(__file__).resolve().parents[1] / "results").glob("*.json")):
        data = _json.loads(path.read_text())
        for key, value in data.items():
            if isinstance(value, str):
                assert not any(m in value for m in PATH_MARKERS), (path.name, key)
