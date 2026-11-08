"""inspect_ai tasks, one per level (install the ``[eval]`` extra).

    inspect eval astro_bench/inspect_tasks.py@level1 --model anthropic/claude-sonnet-5-5

Each sample's input is the rendered user message; the system prompt is
``prompts/system.md``; the scorer reuses the built-in parser and graders, so scores
equal ``astro-bench run`` scores for the same responses. Task parameters:
``items`` (default ``items/``), ``canon`` (default ``canon/``), ``convention``
(e.g. ``lahiri/mean/whole_sign``) and ``task`` (e.g. ``dasha``).
"""

from __future__ import annotations

from functools import lru_cache
from typing import Any

from .canon import Canon
from .io import load_items
from .prompts import render_user_message, system_prompt
from .runner import grade_response
from .schema import Item

try:  # inspect_ai is optional: the module imports without it, the tasks need it.
    from inspect_ai import Task, task
    from inspect_ai.dataset import MemoryDataset, Sample
    from inspect_ai.scorer import Score, Target, mean, scorer, stderr
    from inspect_ai.solver import TaskState, generate, system_message

    HAVE_INSPECT = True
except ImportError:  # pragma: no cover - exercised only without the extra
    HAVE_INSPECT = False

    def task(func: Any) -> Any:  # type: ignore[no-redef]
        return func


@lru_cache(maxsize=4)
def _canon(path: str) -> Canon:
    return Canon.load_or_empty(path)


def _require() -> None:
    if not HAVE_INSPECT:
        raise ImportError("inspect_ai is not installed: pip install 'astro-bench[eval]'")


def select(items_dir: str, level: int, convention: str | None, task_name: str | None
           ) -> list[Item]:
    items = [i for i in load_items(items_dir) if i.level == level]
    if convention:
        items = [i for i in items if i.convention.key == convention]
    if task_name:
        items = [i for i in items if i.task == task_name]
    return items


def to_sample(item: Item) -> Any:
    return Sample(id=item.id, input=render_user_message(item),
                  target=str(item.gold.answer),
                  metadata={"item": item.model_dump(mode="json", exclude_none=True)})


def astro_scorer(canon_dir: str = "canon") -> Any:
    _require()

    @scorer(metrics={"answer": [mean(), stderr()], "citation": [mean()],
                     "fabricated": [mean()], "parse_error": [mean()]})
    def _astro() -> Any:
        async def score(state: TaskState, target: Target) -> Score:
            item = Item.model_validate(state.metadata["item"])
            row = grade_response(item, state.output.completion, _canon(canon_dir))
            return Score(
                value={"answer": row.answer_score,
                       "citation": float(row.citation_score or 0),
                       "fabricated": float(row.fabricated),
                       "parse_error": float(row.parse_error)},
                answer=str(row.answer) if row.answer is not None else None,
                metadata=row.model_dump(mode="json"),
            )

        return score

    return _astro()


def _task(level: int, items: str, canon: str, convention: str | None, task_name: str | None
          ) -> Any:
    _require()
    samples = [to_sample(i) for i in select(items, level, convention, task_name)]
    return Task(
        dataset=MemoryDataset(samples, name=f"astro-bench-level{level}"),
        solver=[system_message(system_prompt()), generate()],
        scorer=astro_scorer(canon),
    )


@task
def level0(items: str = "items", canon: str = "canon", convention: str | None = None,
           task: str | None = None) -> Any:
    """Level 0: compute positions from birth data."""
    return _task(0, items, canon, convention, task)


@task
def level1(items: str = "items", canon: str = "canon", convention: str | None = None,
           task: str | None = None) -> Any:
    """Level 1: recognise nakshatra, varga, dasha, dignity, combustion, aspect, lordship, yogas."""
    return _task(1, items, canon, convention, task)


@task
def level2(items: str = "items", canon: str = "canon", convention: str | None = None,
           task: str | None = None) -> Any:
    """Level 2: cite the classical text, chapter and verse of a rule."""
    return _task(2, items, canon, convention, task)
