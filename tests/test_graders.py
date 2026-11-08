from __future__ import annotations

import pytest

from astro_bench.graders import grade_exact, grade_jaccard, grade_positions
from astro_bench.score import brier, ece, wilson


@pytest.mark.parametrize(
    ("answer", "gold", "score"),
    [
        (True, True, 1.0), ("yes", True, 1.0), (False, True, 0.0), ("Mars", True, 0.0),
        ("Guru", "Jupiter", 1.0), ("mesha", "Aries", 1.0), ("Aswini", "Ashwini", 1.0),
        ("7", "7", 1.0), (7, "7", 1.0), ("8", "7", 0.0),
        ({"nakshatra": "rohini", "pada": "2"}, {"nakshatra": "Rohini", "pada": 2}, 1.0),
        ({"nakshatra": "Rohini", "pada": 3}, {"nakshatra": "Rohini", "pada": 2}, 0.0),
        ("Own", "own", 1.0), (None, "own", 0.0),
    ],
)
def test_exact(answer: object, gold: object, score: float) -> None:
    assert grade_exact(answer, gold) == score


@pytest.mark.parametrize(
    ("answer", "gold", "score"),
    [
        ([], [], 1.0), (["Mars"], [], 0.0), (["Mars", "Saturn"], ["Saturn", "Mars"], 1.0),
        (["Mars"], ["Mars", "Saturn"], 0.5), (["Kuja", "Shani", "Sun"], ["Mars", "Saturn"], 2 / 3),
        ("Mars, Saturn", ["Mars", "Saturn"], 1.0), ({"Mars": 1}, ["Mars"], 0.0),
    ],
)
def test_jaccard(answer: object, gold: object, score: float) -> None:
    assert grade_jaccard(answer, gold) == pytest.approx(score)


GOLD = {
    "Sun": {"sign": "Taurus", "deg_in_sign": 0.38, "nakshatra": "Krittika", "pada": 2},
    "Moon": {"sign": "Sagittarius", "deg_in_sign": 29.71, "nakshatra": "Uttara Ashadha",
             "pada": 1},
    "Lagna": {"sign": "Cancer"},
}


def test_positions_perfect_and_weights() -> None:
    assert grade_positions(GOLD, GOLD) == 1.0
    answer = {
        # sign right, nakshatra right, degree off by 2 -> 0.75
        "Sun": {"sign": "Taurus", "deg_in_sign": 2.38, "nakshatra": "Krittika"},
        # sign wrong (Capricorn 0.2 is within 1 deg across the boundary) -> 0.25 + 0.25
        "Moon": {"sign": "Capricorn", "deg_in_sign": 0.2, "nakshatra": "Uttara Ashadha"},
        "Ascendant": {"sign": "Karka"},
    }
    assert grade_positions(answer, GOLD) == pytest.approx((0.75 + 0.5 + 1.0) / 3)


def test_positions_tolerance_and_garbage() -> None:
    near = {"Sun": dict(GOLD["Sun"], deg_in_sign=1.0)}
    assert grade_positions(near, {"Sun": GOLD["Sun"]}, tolerance_deg=1.0) == 1.0
    assert grade_positions(near, {"Sun": GOLD["Sun"]}, tolerance_deg=0.5) == 0.75
    assert grade_positions("Sun in Taurus", GOLD) == 0.0
    assert grade_positions({}, GOLD) == 0.0


def test_wilson() -> None:
    assert wilson(0, 0) == (0.0, 0.0)
    lo, hi = wilson(50, 100)
    assert lo == pytest.approx(0.4038, abs=1e-3) and hi == pytest.approx(0.5962, abs=1e-3)
    assert wilson(10, 10)[1] == 1.0


def test_brier_and_ece() -> None:
    assert brier([], []) is None and ece([], []) is None
    assert brier([1.0, 0.0], [1.0, 0.0]) == 0.0
    assert brier([0.5, 0.5], [1.0, 0.0]) == 0.25
    assert ece([1.0, 0.0], [1.0, 0.0]) == 0.0
    # all in the 0.9 bin, half right: |0.9 - 0.5| = 0.4
    assert ece([0.9, 0.9], [1.0, 0.0]) == pytest.approx(0.4)
