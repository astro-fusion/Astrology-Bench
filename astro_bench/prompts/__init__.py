"""Prompt text and user-message rendering."""

from __future__ import annotations

from importlib import resources

from ..schema import Item


def system_prompt() -> str:
    """The system prompt shipped with the package (``prompts/system.md``)."""
    return resources.files(__package__).joinpath("system.md").read_text(encoding="utf-8")


def render_input(item: Item) -> str:
    """The item's birth data and chart table as plain text (empty when removed)."""
    lines: list[str] = []
    birth = item.input.birth
    if birth is not None:
        where = f" ({birth.place})" if birth.place else ""
        lines.append(
            f"Birth: {birth.utc} UTC, latitude {birth.lat:.4f}, "
            f"longitude {birth.lon:.4f} (east positive){where}"
        )
    chart = item.input.chart
    if chart is not None:
        lines.append(f"Sidereal chart ({item.convention.words()}):")
        lines.append(f"  Lagna (ascendant): {chart.lagna:.2f} deg")
        lines.append("  Body: sidereal longitude deg, speed deg/day (negative = retrograde)")
        for name, body in chart.bodies.items():
            lines.append(f"  {name}: {body.lon:.2f}, {body.speed:+.2f}")
        if chart.cusps:
            cusps = ", ".join(f"{i + 1}: {c:.2f}" for i, c in enumerate(chart.cusps))
            lines.append(f"  House cusps: {cusps}")
    return "\n".join(lines)


def render_user_message(item: Item) -> str:
    """The full user message: input block (if any) then the question."""
    block = render_input(item)
    return f"{block}\n\n{item.prompt}" if block else item.prompt


__all__ = ["render_input", "render_user_message", "system_prompt"]
