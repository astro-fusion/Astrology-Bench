# BPHS-Bench

A deterministic testing and evaluation framework for benchmarking AI-driven Vedic Astrology applications against the strict text-based rules of **Brihat Parashara Hora Shastra (BPHS)**.

## Architecture

The framework operates as a **"Black Box" numerical evaluator**:

1. **Inject** raw, mathematically validated planetary states (`ChartState`) into the agent context.
2. **Prompt** the AI with non-technical layman questions.
3. **Parse** a single-digit integer response (1–5) from the agent output.
4. **Score** it against an immutable gold standard baseline.
5. **Report** a formatted markdown table with pass/fail results.

```
bphs-bench/
├── package.json
├── tsconfig.json
├── README.md
└── src/
    ├── types/
    │   └── index.ts          # ChartState, TestCase, EvaluationResult interfaces
    ├── data/
    │   └── dataset.ts        # 10 golden test cases (Easy → Very Hard)
    ├── core/
    │   ├── harness.ts        # Core execution engine & scoring matrix
    │   └── parser.ts         # Fail-safe 1-5 integer extractor
    └── index.ts              # CLI entry point
```

## Benchmark Formula

$$\text{Final Bench Score \%} = \left( \frac{\text{Exact Matches}}{\text{Total Test Cases Run}} \right) \times 100$$

## Test Case Tiers

| Tier | Cases | Description |
|------|-------|-------------|
| EASY | 2 | Direct lordship, single-dimension interpretation |
| MEDIUM | 3 | Parivartana, Varga traps, combustion filters |
| HARD | 3 | Vipareeta Yogas, Varga subversion, multi-factor analysis |
| VERY_HARD | 2 | Dialectical contradictions, timing windows, Neecha Bhanga |

## Usage

```bash
npm install
npm run bench
```

## Integrating a Real Agent

Edit `src/core/harness.ts` and replace the `mockAgentCall` function with your actual AI agent invocation. The harness expects a plain string response containing the score somewhere in the output.

```typescript
// Replace this mock with your real agent call:
async function callAgent(payload: AgentPayload): Promise<string> {
  // e.g., call OpenAI, Gemini, or your custom BPHS AI
  const response = await myAIClient.chat(payload);
  return response.text;
}
```

## Scoring Interpretation

| Score | Meaning |
|-------|---------|
| 1 | Very unfavourable / blocked |
| 2 | Below average / challenged |
| 3 | Moderate / mixed signals |
| 4 | Good / above average |
| 5 | Excellent / highly favourable |
