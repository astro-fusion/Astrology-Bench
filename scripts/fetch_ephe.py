#!/usr/bin/env python3
"""Download the pinned Swiss Ephemeris files into ``ephe/`` and verify their sha256.

    python scripts/fetch_ephe.py [--dest ephe/]

Source: the official Swiss Ephemeris repository, https://github.com/aloistr/swisseph,
directory ``ephe/`` at the commit pinned in ``astro_bench/ephemeris.py``.

Licence: the files are part of the Swiss Ephemeris by Astrodienst AG, distributed under a
dual licence, the GNU Affero General Public License (AGPL-3.0) or the Swiss Ephemeris
Professional License (https://www.astro.com/swisseph/). pyswisseph, which the oracle
engine already depends on, is under the same licence family. The files are downloaded
for local computation and are not committed to this repository (``ephe/`` is ignored).
"""

from __future__ import annotations

import argparse
import hashlib
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from astro_bench.ephemeris import EPHE_COMMIT, EPHE_FILES, verify  # noqa: E402

RAW = "https://raw.githubusercontent.com/aloistr/swisseph/{commit}/ephe/{name}"


def fetch(dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    for name, digest in EPHE_FILES.items():
        path = dest / name
        if path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == digest:
            print(f"ok      {name}")
            continue
        url = RAW.format(commit=EPHE_COMMIT, name=name)
        with urllib.request.urlopen(url, timeout=120) as resp:  # noqa: S310
            data = resp.read()
        if hashlib.sha256(data).hexdigest() != digest:
            raise SystemExit(f"{name}: downloaded file does not match the pinned sha256")
        path.write_bytes(data)
        print(f"fetched {name} ({len(data)} bytes)")
    verify(dest)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dest", default=str(ROOT / "ephe"))
    fetch(Path(parser.parse_args().dest))


if __name__ == "__main__":
    main()
