# Astro-Bench

A deterministic testing and evaluation framework for benchmarking AI-driven Vedic Astrology applications against strict text-based rules from classical sources of truth.

## Overview

Astro-Bench is designed to evaluate how accurately AI models interpret astrological configurations according to various classical texts. It supports multiple benchmark suites, each derived from a specific source of truth.

Currently supported benchmarks:
- **BPHS-Bench**: Based on *Brihat Parashara Hora Shastra*.

## Architecture

The framework operates as a **"Black Box" numerical evaluator**:

1. **Inject** raw, mathematically validated planetary states (`ChartState`) into the agent context.
2. **Prompt** the AI with non-technical layman questions.
3. **Parse** a single-digit integer response (1–5) from the agent output.
4. **Score** it against an immutable gold standard baseline.
5. **Report** a formatted markdown table with pass/fail results.

```
astro-bench/
├── src/
│   ├── benchmarks/           # Benchmark definitions
│   │   ├── index.ts          # Benchmark registry
│   │   └── bphs/             # BPHS specific dataset
│   ├── core/
│   │   ├── harness.ts        # Generic execution engine
│   │   └── parser.ts         # Fail-safe 1-5 integer extractor
│   ├── types/
│   │   └── index.ts          # Core interfaces
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
```

## Adding a New Benchmark

To add a new benchmark (e.g., *Phaladeepika-Bench*):

1. Create a new directory `src/benchmarks/phaladeepika/`.
2. Define your dataset in `dataset.ts` following the `TestCase` interface.
3. Register the new benchmark in `src/benchmarks/index.ts`.

```typescript
// src/benchmarks/index.ts
export const BENCHMARKS: BenchmarkDefinition[] = [
  {
    id: "bphs",
    // ...
  },
  {
    id: "phaladeepika",
    name: "Phaladeepika-Bench",
    description: "Evaluations based on Phaladeepika",
    dataset: PHALADEEPIKA_DATASET,
  }
];
```

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
