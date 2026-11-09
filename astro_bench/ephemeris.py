"""Swiss Ephemeris files for the oracle: pinned, verified, and never silently skipped.

Without ``.se1`` files pyswisseph falls back to the Moshier analytic ephemeris, whose
true lunar node differs from the file value by up to about 5e-3 deg; that put gold on the
wrong side of pada and sign edges (CORRECTIONS 2026-11-09). The generator and the oracle
call :func:`configure` first: it checks the pinned files and their sha256, points
``SE_EPHE_PATH`` at them and asserts the engine reports ``ephemeris_model == "swieph"``.

Files come from the official Swiss Ephemeris repository (aloistr/swisseph, ``ephe/``)
at :data:`EPHE_COMMIT`; ``scripts/fetch_ephe.py`` downloads them into ``ephe/``. They are
Astrodienst's Swiss Ephemeris data, dual-licensed AGPL-3.0 or Swiss Ephemeris
Professional License, the same licence family as pyswisseph; they are not committed.
"""

from __future__ import annotations

import hashlib
import os
from functools import lru_cache
from pathlib import Path

EPHE_REPO = "https://github.com/aloistr/swisseph"
EPHE_COMMIT = "94621aba9f3ff9c32cb721eac0380c30dbb153fe"
#: Files covering 1800-2399: planets, Moon (and so the nodes), main asteroids.
EPHE_FILES: dict[str, str] = {
    "sepl_18.se1": "ca1393ceab3a44fbc895887cf789c68819ae6a1cbc9b22225872dbe4ccd99a66",
    "semo_18.se1": "1ca07bd67c24374d77226180c20a4f9996cba013697894810518e7eb582ca4f7",
    "seas_18.se1": "a2cd8fc33807c78ca9a700c91c2e042258b12fc4796519e00781440b5ad8b2e2",
}
#: One id for the whole file set, recorded on every item and result.
EPHE_SET_SHA256 = hashlib.sha256(
    "".join(f"{k} {v}\n" for k, v in sorted(EPHE_FILES.items())).encode()).hexdigest()


class EphemerisError(RuntimeError):
    """The Swiss Ephemeris files are missing, altered, or not used by the engine."""


def ephe_dir() -> Path:
    """``$ASTRO_BENCH_EPHE`` or ``<checkout>/ephe``."""
    env = os.environ.get("ASTRO_BENCH_EPHE")
    return Path(env) if env else Path(__file__).resolve().parents[1] / "ephe"


def verify(directory: Path) -> None:
    for name, digest in EPHE_FILES.items():
        path = directory / name
        if not path.is_file():
            raise EphemerisError(
                f"{path} is missing: run `python scripts/fetch_ephe.py` (no silent Moshier)")
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise EphemerisError(f"{path} does not match its pinned sha256")


@lru_cache(maxsize=1)
def configure() -> str:
    """Use the pinned files and assert the engine computes from them; return the model."""
    directory = ephe_dir()
    verify(directory)
    os.environ["SE_EPHE_PATH"] = str(directory)
    import swisseph as swe
    from vedic_astrology_core.astrology.ephemeris import EphemerisEngine

    swe.set_ephe_path(str(directory))
    model = str(EphemerisEngine(node_model="true").ephemeris_model)
    if model != "swieph":
        raise EphemerisError(f"engine reports ephemeris_model={model!r}, expected 'swieph'")
    return model


__all__ = ["EPHE_COMMIT", "EPHE_FILES", "EPHE_SET_SHA256", "EphemerisError", "configure",
           "ephe_dir", "verify"]
