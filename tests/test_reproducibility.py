"""Guard: published numbers must not depend on the Swiss Ephemeris build.

Measured on 2026-11-08 between pyswisseph 2.10.3.2 wheels for CPython 3.11 and 3.14
(the cause of a CI determinism failure): longitudes differ by up to 1e-9 deg for the
planets and 1.1e-5 deg for the true node; speeds by up to 5e-6 deg/day (Moon) and
1e-4 deg/day (true node). So the chart table carries no speed magnitude and no node
speed sign, true-node longitudes are published to 1 dp, and every committed value must
survive a perturbation by about twice those bounds.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from vedic_astrology_core.astrology.ayanamsa import get_zodiac_sign
from vedic_astrology_core.astrology.chart import get_nakshatra

from astro_bench.generators.common import NO_SPEED_SIGN, chart_of, lon_digits, planet_record
from astro_bench.io import item_files, load_items
from astro_bench.schema import Body, Item

ITEMS = Path(__file__).resolve().parents[1] / "items"
LON_NOISE = {"true_node": 2.5e-5, "other": 1e-7}  # about 2x and 100x the measured bounds
SPEED_NOISE = 1e-5


def _lon_noise(item: Item, body: str) -> float:
    if body in NO_SPEED_SIGN and item.convention.node == "true":
        return LON_NOISE["true_node"]
    return LON_NOISE["other"]


def _stable_round(value: float, noise: float, ndigits: int = 2) -> bool:
    return round(value - noise, ndigits) == round(value + noise, ndigits) == round(value, ndigits)


def test_body_has_no_speed_magnitude() -> None:
    assert set(Body.model_fields) == {"lon", "retrograde"}


@pytest.mark.skipif(not item_files(ITEMS), reason="no committed items")
def test_committed_values_survive_build_noise() -> None:
    unstable: list[str] = []
    for item in load_items(ITEMS):
        if item.input.birth is None or item.generator.name == "positions_from_golden_charts":
            continue
        chart = chart_of(item)
        table = item.input.chart
        if table is not None:
            for name, body in table.bodies.items():
                rec = planet_record(chart, name)
                lon, noise = float(rec["longitude"]), _lon_noise(item, name)
                digits = lon_digits(name, item.convention.node)
                if round(lon, digits) != body.lon or not _stable_round(lon, noise, digits):
                    unstable.append(f"{item.id} {name} lon")
                if name in NO_SPEED_SIGN:
                    if body.retrograde is not None:
                        unstable.append(f"{item.id} {name} speed sign published")
                elif abs(float(rec["longitude_speed"])) < SPEED_NOISE:
                    unstable.append(f"{item.id} {name} speed near zero")
        if item.task == "positions":
            for name in item.gold.answer:
                if name == "Lagna":
                    continue
                lon = float(planet_record(chart, name)["longitude"])
                noise = _lon_noise(item, name)
                deg = get_zodiac_sign(lon)[2]
                same_nak = {(get_nakshatra(x)["index"], get_nakshatra(x)["pada"])
                            for x in (lon - noise, lon + noise)}
                same_sign = {get_zodiac_sign(x)[0] for x in (lon - noise, lon + noise)}
                digits = lon_digits(name, item.convention.node)
                if not _stable_round(deg, noise, digits) or len(same_nak) > 1 or len(same_sign) > 1:
                    unstable.append(f"{item.id} {name} gold")
    assert unstable == []
