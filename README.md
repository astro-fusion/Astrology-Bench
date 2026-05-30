# Astro-Bench

A deterministic testing and evaluation framework for benchmarking AI-driven Vedic Astrology applications against strict text-based rules from classical sources of truth.

## Overview

Astro-Bench is designed to evaluate how accurately AI models interpret astrological configurations according to various classical texts. It supports multiple benchmark suites, each derived from a specific source of truth.

Currently supported benchmarks:
- **BPHS-Bench**: Foundational Parashari system (10 cases).
- **Phaladeepika-Bench**: Ashtakavarga and Predictive nuances (10 cases).
- **Saravali-Bench**: Conjunctions and nuanced Yogas (10 cases).
- **Unified Vedic-Bench**: A combined 30-case evaluation across all sources.

## Architecture

The framework operates as a **"Black Box" numerical evaluator**:

1. **Inject**: Raw, mathematically validated planetary states (`ChartState`) are injected into the agent context.
2. **Prompt**: The AI is prompted with non-technical layman questions.
3. **Reasoning**: Each test case contains structured **Interpretive Logic** and **Classical References** (Chapter/Verse) to justify the gold standard score.
4. **Parse**: A single-digit integer response (1–5) is extracted from the agent output.
5. **Score**: Points are awarded based on proximity to the gold standard:
   - **1.0 pt**: Exact Match
   - **0.5 pt**: Near Match (±1 delta)
   - **0.0 pt**: Fail
6. **Report**: Comprehensive metrics including **Weighted Scores**, **Source Breakdowns**, and **Tier Analysis**.

## Usage

### Run All Benchmarks (Combined)
```bash
npm run bench
```

### Run a Specific Benchmark
```bash
npm run bench bphs
npm run bench phaladeepika
npm run bench saravali
```

## Data Schema (TestCase)

Every evaluation unit follows a strict schema to ensure scientific rigor:

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | Unique identifier (e.g., `BPHS-01`) |
| `source` | `string` | The classical text source |
| `tier` | `Tier` | Difficulty (EASY, MEDIUM, HARD, VERY_HARD) |
| `logic` | `string` | The rule chain justifying the gold score |
| `reference` | `object` | Book, Chapter, and Verse citations |
| `goldScore` | `1-5` | The immutable target score |

## Benchmark Formula

$$\text{Weighted Score \%} = \left( \frac{\text{Total Points Accumulated}}{\text{Total Test Cases Run}} \right) \times 100$$

## Scoring Interpretation

| Score | Meaning |
|-------|---------|
| 1 | Very unfavourable / blocked |
| 2 | Below average / challenged |
| 3 | Moderate / mixed signals |
| 4 | Good / above average |
| 5 | Excellent / highly favourable |
