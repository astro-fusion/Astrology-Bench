"""Helpers importable as ``tests.helpers`` (used by the module:callable solver test)."""

from __future__ import annotations

import json

from astro_bench.schema import Item


def always_true(item: Item) -> str:
    return json.dumps({"answer": True, "citations": []})
