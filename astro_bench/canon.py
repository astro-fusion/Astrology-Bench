"""Load and query the canon: ``canon/REGISTRY.yaml`` plus ``canon/<text>.yaml`` entries.

Only entries with ``verified: quoted`` are gold (:meth:`Canon.gold_for`). Texts are
resolved by registry id, title or bibtex key, and a small table of common spellings
(:data:`TEXT_ALIASES`), all compared on lowercase alphanumerics only.
"""

from __future__ import annotations

import re
from collections import defaultdict
from collections.abc import Iterable
from pathlib import Path
from typing import Any

import yaml

from .schema import CanonEntry, CanonRegistry, CanonText


class CanonError(ValueError):
    """The canon files are malformed or inconsistent."""


def _key(name: str | None) -> str:
    return "".join(ch for ch in str(name or "").lower() if ch.isalnum())


#: Spellings a model (or a rule's ``source.text``) may use for a registry text.
#: Keys are normalised registry ids; values are normalised alternative names.
TEXT_ALIASES: dict[str, list[str]] = {
    "bphs": [
        "brihatparasharahorashastra",
        "brihatparasarahorasastra",
        "brhatparasarahorasastra",
        "brihatparasharahorasastra",
        "parasharahorashastra",
        "parashara",
        "parasara",
    ],
    "bj": ["brihatjataka", "brhajjataka", "brihajjataka", "brihatjatakam"],
    "brihatjataka": ["bj", "brhajjataka", "brihajjataka", "brihatjatakam"],
    "phaladeepika": ["phaladipika", "phaladeepikā", "phaladeepikam"],
    "saravali": ["saaravali", "saravalli"],
    "jaiminisutras": ["jaiminisutra", "jaiminisutram", "upadesasutras", "jaimini"],
    "js": ["jaiminisutras", "jaiminisutra", "jaiminisutram", "upadesasutras", "jaimini"],
    "brihatsamhita": ["brhatsamhita", "brihatsamhitha", "bs"],
    "bs": ["brihatsamhita", "brhatsamhita", "brihatsamhitha"],
}


def chapter_number(chapter: str | int | None) -> int | None:
    """The leading integer of a chapter label ("36", "Ch. 36", "036"), else None."""
    if chapter is None:
        return None
    match = re.search(r"\d+", str(chapter))
    return int(match.group()) if match else None


_RANGE = re.compile(r"^(?:(\d+)\.)?(\d+)\s*[-–]\s*(?:(\d+)\.)?(\d+)$")
_SINGLE = re.compile(r"^(?:(\d+)\.)?(\d+)$")


def verse_numbers(verse: str | int | None) -> set[str]:
    """Every verse named by a label, as strings.

    Plain verses: "3" -> {"3"}, "57-63" -> {"57", ..., "63"}, "3, 5" -> {"3", "5"}.
    Dotted Jaimini ``pada.sutra`` verses keep the pada: "1.11" -> {"1.11"},
    "1.2-3" and "1.2-1.3" -> {"1.2", "1.3"}. A label prefixed "v." or "verse" is accepted.
    """
    if verse is None:
        return set()
    found: set[str] = set()
    text = re.sub(r"(?i)\b(?:verses?|vv?|sl(?:oka)?s?|sutras?)\.?\s*", "", str(verse))
    for part in re.split(r"[,;/&]+|\s+and\s+", text):
        part = part.strip().rstrip(".")
        rng = _RANGE.match(part)
        if rng:
            pada, lo_s, pada2, hi_s = rng.groups()
            lo, hi = int(lo_s), int(hi_s)
            if pada2 is not None and pada2 != pada:
                found.update({f"{pada}.{lo}" if pada else str(lo), f"{pada2}.{hi}"})
                continue
            if lo <= hi and hi - lo < 200:
                prefix = f"{int(pada)}." if pada else ""
                found.update(f"{prefix}{n}" for n in range(lo, hi + 1))
            continue
        single = _SINGLE.match(part)
        if single:
            pada, num = single.groups()
            found.add(f"{int(pada)}.{int(num)}" if pada else str(int(num)))
    return found


class Canon:
    """The loaded canon, indexed by rule key and by (text, chapter)."""

    def __init__(self, registry: CanonRegistry, entries: Iterable[CanonEntry],
                 untraced: Iterable[dict[str, Any]] | None = None):
        self.registry = registry
        self.texts: dict[str, CanonText] = {t.id: t for t in registry.texts}
        self.entries: dict[str, CanonEntry] = {}
        self.by_rule_key: dict[str, list[CanonEntry]] = defaultdict(list)
        #: Rules searched for and not found (``untraced:`` lists); never gold.
        self.untraced: list[dict[str, Any]] = list(untraced or [])
        self.by_text_chapter: dict[tuple[str, int], list[CanonEntry]] = defaultdict(list)
        self._names: dict[str, str] = {}
        for text in registry.texts:
            for name in (text.id, text.title, text.bibtex_key, text.edition_id):
                if name:
                    self._names.setdefault(_key(name), text.id)
            for alias in TEXT_ALIASES.get(_key(text.id), []):
                self._names.setdefault(alias, text.id)
        problems: list[str] = []
        for entry in entries:
            if entry.id in self.entries:
                problems.append(f"duplicate canon id {entry.id}")
                continue
            text_id = self.resolve_text(entry.text)
            if text_id is None:
                problems.append(f"{entry.id}: text {entry.text!r} is not in REGISTRY.yaml")
                continue
            if not self.chapter_in_range(text_id, entry.chapter):
                problems.append(f"{entry.id}: chapter {entry.chapter} out of range")
            self.entries[entry.id] = entry
            for key in entry.keys:
                self.by_rule_key[key].append(entry)
            num = chapter_number(entry.chapter)
            if num is not None:
                self.by_text_chapter[(text_id, num)].append(entry)
        if problems:
            raise CanonError("; ".join(problems))

    # ----------------------------------------------------------------- loading

    @classmethod
    def load(cls, directory: str | Path) -> Canon:
        """Load ``REGISTRY.yaml`` and every other ``*.yaml`` in ``directory``."""
        root = Path(directory)
        reg_path = root / "REGISTRY.yaml"
        if not reg_path.exists():
            raise CanonError(f"{reg_path} not found")
        raw = yaml.safe_load(reg_path.read_text(encoding="utf-8")) or {}
        registry = CanonRegistry.model_validate(raw)
        entries: list[CanonEntry] = []
        untraced: list[dict[str, Any]] = []
        for path in sorted(root.glob("*.yaml")):
            if path.name == "REGISTRY.yaml":
                continue
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            for raw_entry in data.get("entries") or []:
                entries.append(CanonEntry.model_validate(raw_entry))
            untraced += [dict(u, file=path.name) for u in data.get("untraced") or []]
        return cls(registry, entries, untraced)

    @classmethod
    def empty(cls) -> Canon:
        """A canon with no texts (citation grading then marks every citation fabricated)."""
        return cls(CanonRegistry(texts=[]), [])

    @classmethod
    def load_or_empty(cls, directory: str | Path | None) -> Canon:
        """Load ``directory`` when it holds a registry, else :meth:`empty`."""
        if directory is None or not (Path(directory) / "REGISTRY.yaml").exists():
            return cls.empty()
        return cls.load(directory)

    # ----------------------------------------------------------------- queries

    def resolve_text(self, name: str | None) -> str | None:
        """Registry id for a text name, id, bibtex key or known spelling."""
        return self._names.get(_key(name)) if name else None

    def is_known_text(self, name: str | None) -> bool:
        return self.resolve_text(name) is not None

    def chapter_in_range(self, text: str | None, chapter: str | int | None) -> bool:
        """True when ``chapter`` is a number in 1..chapters of the registry text."""
        text_id = self.resolve_text(text)
        num = chapter_number(chapter)
        if text_id is None or num is None:
            return False
        return 1 <= num <= self.texts[text_id].chapters

    def gold_for(self, rule_key: str) -> list[CanonEntry]:
        """``verified: quoted`` entries whose ``rule_key`` or ``rule_keys`` name ``rule_key``."""
        entries = self.by_rule_key.get(rule_key, [])
        return sorted((e for e in entries if e.verified == "quoted"), key=lambda e: e.id)

    def quoted(self) -> list[CanonEntry]:
        """Every ``verified: quoted`` entry, sorted by id."""
        return sorted((e for e in self.entries.values() if e.verified == "quoted"),
                      key=lambda e: e.id)

    def rule_keys(self) -> set[str]:
        return set(self.by_rule_key)

    def entry(self, canon_id: str) -> CanonEntry | None:
        return self.entries.get(canon_id)

    def __len__(self) -> int:
        return len(self.entries)


__all__ = ["TEXT_ALIASES", "Canon", "CanonError", "chapter_number", "verse_numbers"]
