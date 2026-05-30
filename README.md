# Astro-Bench

A deterministic testing and evaluation framework for benchmarking AI-driven Vedic Astrology applications against strict text-based rules from classical sources of truth.

## Overview

Astro-Bench is designed to evaluate how accurately AI models interpret astrological configurations according to various classical texts. It supports multiple benchmark suites, each derived from a specific source of truth.

Currently supported benchmarks:
- **BPHS-Bench**: Based on *Brihat Parashara Hora Shastra*.
- **Saravali-Bench**: Based on Kalyana Varma's *Saravali*.

## Architecture

The framework operates as a **"Black Box" numerical evaluator**:

1. **Inject**: Raw, mathematically validated planetary states (`ChartState`) are injected into the agent context.
2. **Prompt**: The AI is prompted with non-technical layman questions.
3. **Reasoning**: Each test case contains structured **Interpretive Logic** and **Classical References** (Chapter/Verse) to justify the gold standard score.
4. **Parse**: A single-digit integer response (1–5) is extracted from the agent output using a fail-safe parser.
5. **Score**: The AI score is compared against the immutable gold standard baseline.
6. **Report**: A formatted markdown table with pass/fail results and aggregate metrics is generated.

```
astro-bench/
├── src/
│   ├── benchmarks/           # Benchmark definitions
│   │   ├── index.ts          # Benchmark registry
│   │   ├── bphs/             # BPHS dataset & logic
│   │   └── saravali/         # Saravali dataset & logic
│   ├── core/
│   │   ├── harness.ts        # Generic execution engine
│   │   └── parser.ts         # Fail-safe 1-5 integer extractor
│   ├── types/
│   │   └── index.ts          # Core interfaces (TestCase, ChartState)
│   └── index.ts              # CLI entry point
```

## Usage

### Run Default Benchmark (BPHS)
```bash
npm run bench
```

### Run a Specific Benchmark
```bash
npm run bench bphs
npm run bench saravali
```

## Data Schema (TestCase)

Every evaluation unit follows a strict schema to ensure scientific rigor:

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | Unique identifier (e.g., `TC-SAR-01`) |
| `tier` | `Tier` | Difficulty (EASY, MEDIUM, HARD, VERY_HARD) |
| `logic` | `string` | The rule chain justifying the gold score |
| `reference` | `object` | Book, Chapter, and Verse citations |
| `goldScore` | `1-5` | The immutable target score |
| `chartState` | `object` | The planetary data provided to the AI |

## Adding a New Benchmark

To add a new benchmark (e.g., *Phaladeepika-Bench*):

1. Create a new directory `src/benchmarks/phaladeepika/`.
2. Define your dataset in `dataset.ts` following the `TestCase` interface:

```typescript
const TC_EXAMPLE: TestCase = {
  id: "TC-PD-01",
  tier: "EASY",
  topic: "Health Baseline",
  prompt: "Rate my physical resilience on a scale of 1-5.",
  goldScore: 5,
  logic: "Lagna lord in Kendra with Subha-aspects...",
  reference: { book: "Phaladeepika", chapter: "4", verse: "1" },
  chartState: { /* ... */ }
};
```

3. Register the new benchmark in `src/benchmarks/index.ts`.

## Benchmark Formula

$$\text{Final Bench Score \%} = \left( \frac{\text{Exact Matches}}{\text{Total Test Cases Run}} \right) \times 100$$

## Scoring Interpretation

| Score | Meaning |
|-------|---------|
| 1 | Very unfavourable / blocked |
| 2 | Below average / challenged |
| 3 | Moderate / mixed signals |
| 4 | Good / above average |
| 5 | Excellent / highly favourable |
