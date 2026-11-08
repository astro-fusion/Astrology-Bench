"""Pydantic models for items, model output, results and the canon (ADR-001)."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

AnswerType = Literal["bool", "category", "set", "positions", "citation", "likert"]
Tier = Literal["EASY", "MEDIUM", "HARD", "VERY_HARD"]
Split = Literal["dev", "test"]
Ayanamsa = Literal["lahiri", "raman", "krishnamurti"]
NodeModel = Literal["mean", "true"]
HouseSystem = Literal["whole_sign", "placidus"]
Verified = Literal["quoted", "paraphrased", "untraced"]


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


# --------------------------------------------------------------------------- items


class Convention(_Strict):
    ayanamsa: Ayanamsa = "lahiri"
    node: NodeModel = "mean"
    house: HouseSystem = "whole_sign"

    @property
    def key(self) -> str:
        """Short key such as ``lahiri/mean/whole_sign``."""
        return f"{self.ayanamsa}/{self.node}/{self.house}"

    def words(self) -> str:
        """The convention in plain words, for prompts."""
        ayan = {"lahiri": "Lahiri", "raman": "Raman", "krishnamurti": "Krishnamurti (KP)"}
        house = {"whole_sign": "whole-sign houses", "placidus": "Placidus houses"}
        return f"{ayan[self.ayanamsa]} ayanamsa, {self.node} node, {house[self.house]}"


class Birth(_Strict):
    utc: str
    lat: float
    lon: float
    place: str | None = None
    tz: str | None = None


class Body(_Strict):
    lon: float
    speed: float


class ChartTable(_Strict):
    lagna: float
    bodies: dict[str, Body]
    cusps: list[float] | None = None


class ItemInput(_Strict):
    birth: Birth | None = None
    chart: ChartTable | None = None
    #: Task parameters (planet, varga, house, target date, rule id, ...).
    query: dict[str, Any] = Field(default_factory=dict)


class Gold(_Strict):
    answer: Any


class GraderSpec(_Strict):
    name: Literal["exact", "jaccard", "positions", "citation", "likert"]
    tolerance_deg: float | None = None


class GeneratorInfo(_Strict):
    name: str
    version: str
    seed: int | None = None
    engine_commit: str
    index: int | None = None


class Item(_Strict):
    id: str
    schema_version: Literal[1] = 1
    level: int = Field(ge=0, le=4)
    task: str
    tier: Tier
    source: str
    canon_ids: list[str] = Field(default_factory=list)
    rule_id: str | None = None
    convention: Convention = Field(default_factory=Convention)
    split: Split
    input: ItemInput
    prompt: str
    answer_type: AnswerType
    #: Answer space for category / set items (used by baseline solvers and prompts).
    choices: list[str] | None = None
    gold: Gold
    grader: GraderSpec
    generator: GeneratorInfo


# --------------------------------------------------------------------------- output


class Citation(BaseModel):
    model_config = ConfigDict(extra="allow")

    text: str = ""
    chapter: str | None = None
    verse: str | None = None
    edition: str | None = None

    @field_validator("chapter", "verse", "text", mode="before")
    @classmethod
    def _stringify(cls, value: Any) -> Any:
        if value is None:
            return None
        return str(value)


class ModelOutput(BaseModel):
    model_config = ConfigDict(extra="allow")

    answer: Any = None
    citations: list[Citation] = Field(default_factory=list)
    confidence: float | None = None
    note: str | None = None

    @field_validator("citations", mode="before")
    @classmethod
    def _citations(cls, value: Any) -> Any:
        if value is None:
            return []
        if isinstance(value, dict):
            return [value]
        if isinstance(value, list):
            return [v for v in value if isinstance(v, dict)]
        return []

    @field_validator("confidence", mode="before")
    @classmethod
    def _confidence(cls, value: Any) -> Any:
        try:
            conf = float(value)
        except (TypeError, ValueError):
            return None
        return min(max(conf, 0.0), 1.0)

    @field_validator("note", mode="before")
    @classmethod
    def _note(cls, value: Any) -> Any:
        return None if value is None else str(value)


# --------------------------------------------------------------------------- results


class PerItem(_Strict):
    id: str
    level: int
    task: str
    tier: str
    source: str
    convention: str
    parse_error: bool
    answer_score: float
    citation_score: int | None = None
    fabricated: bool = False
    confidence: float | None = None
    answer: Any = None
    error: str | None = None


class Stat(_Strict):
    n: int
    answer_acc: float
    answer_ci: tuple[float, float]
    citation_n: int
    citation_mean: float | None = None
    fabricated_rate: float | None = None
    parse_error_rate: float
    brier: float | None = None
    ece: float | None = None


class Summary(_Strict):
    overall: Stat
    by_level: dict[str, Stat]
    by_task: dict[str, Stat]
    by_source: dict[str, Stat]
    by_convention: dict[str, Stat]
    by_tier: dict[str, Stat]


class RunResult(_Strict):
    run_id: str
    created_at: str
    model: str
    provider: str
    solver: str
    bench_version: str
    items_sha256: str
    split: str
    item_count: int
    convention_filter: str | None = None
    engine_commit: str
    per_item: list[PerItem]
    summary: Summary


# --------------------------------------------------------------------------- canon


class CanonText(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    title: str
    author: str | None = None
    translator: str | None = None
    edition_id: str | None = None
    edition: str | None = None
    year: int | None = None
    chapters: int = Field(ge=1)
    public_domain: bool = False
    url: str | None = None
    bibtex_key: str | None = None


class CanonRegistry(BaseModel):
    model_config = ConfigDict(extra="allow")

    texts: list[CanonText]


class AlsoIn(BaseModel):
    model_config = ConfigDict(extra="allow")

    text: str
    chapter: str
    verse: str | None = None

    @field_validator("chapter", "verse", mode="before")
    @classmethod
    def _stringify(cls, value: Any) -> Any:
        return None if value is None else str(value)


class CanonEntry(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    text: str
    edition: str | None = None
    chapter: str
    verse: str | None = None
    topic: str
    rule_key: str
    statement: str
    quote: str | None = None
    url: str | None = None
    verified: Verified
    verified_by: str | None = None
    verified_at: str | None = None
    also_in: list[AlsoIn] = Field(default_factory=list)

    @field_validator("chapter", "verse", "verified_at", mode="before")
    @classmethod
    def _stringify(cls, value: Any) -> Any:
        return None if value is None else str(value)

    @field_validator("also_in", mode="before")
    @classmethod
    def _also_in(cls, value: Any) -> Any:
        return [] if value is None else value
