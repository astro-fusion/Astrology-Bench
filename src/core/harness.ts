/**
 * @file src/core/harness.ts
 * @description Core execution engine for the BPHS-Bench evaluation framework.
 *
 * The harness orchestrates the full benchmark lifecycle:
 *  1. Iterates through every TestCase in the dataset.
 *  2. Constructs an AgentPayload (chartState context + layman prompt).
 *  3. Calls the agent (mock or real) and measures wall-clock latency.
 *  4. Delegates response parsing to the parser module.
 *  5. Computes per-case EvaluationResult records.
 *  6. Aggregates a BenchmarkSummary with the final score percentage.
 *
 * To integrate a real AI agent, replace `mockAgentCall` with your own
 * async function that accepts an `AgentPayload` and returns a `string`.
 *
 * Scoring formula:
 *   Final Bench Score % = (Exact Matches / Total Test Cases Run) × 100
 */

import { tryParseAgentScore } from "./parser.js";
import type {
  AgentPayload,
  BenchmarkSummary,
  EvaluationResult,
  TestCase,
} from "../types/index.js";

// ---------------------------------------------------------------------------
// Agent Interface
// ---------------------------------------------------------------------------

/**
 * Type signature for any agent callable by the harness.
 *
 * Replace `mockAgentCall` with a real implementation matching this signature
 * to benchmark an actual AI model.
 */
export type AgentCallable = (payload: AgentPayload) => Promise<string>;

// ---------------------------------------------------------------------------
// Mock Agent
// ---------------------------------------------------------------------------

/**
 * A deterministic mock agent used when no real agent is integrated.
 *
 * The mock simulates a realistic range of AI output formats to exercise
 * the parser under varied response conditions. It does NOT use gold scores;
 * instead it returns a pseudo-random response so the benchmark produces
 * both PASSes and FAILs for demonstration purposes.
 *
 * Distribution of mock formats:
 *  - ~30%: bare digit          ("3")
 *  - ~20%: fraction notation   ("3/5")
 *  - ~20%: labelled response   ("Score: 3")
 *  - ~15%: prose embedding     ("I would rate this a 3.")
 *  - ~15%: "out of 5" phrasing ("3 out of 5")
 *
 * @param payload - The evaluation payload (used only for seeding variety).
 * @returns A mock response string simulating realistic AI output.
 */
async function mockAgentCall(payload: AgentPayload): Promise<string> {
  // Seed pseudo-randomness from the test case ID character codes so output
  // is reproducible for the same dataset across runs.
  const seed = payload.testCaseId
    .split("")
    .reduce((acc, c) => acc + c.charCodeAt(0), 0);

  // Generate a score in [1–5] from the seed (not gold-aligned intentionally).
  const mockScore = (seed % 5) + 1;

  // Simulate a small async delay (10–50ms) to mimic real network latency.
  const delayMs = 10 + (seed % 40);
  await new Promise<void>((resolve) => setTimeout(resolve, delayMs));

  // Rotate through realistic response format templates.
  const formatIndex = seed % 5;
  switch (formatIndex) {
    case 0:
      return `${mockScore}`;
    case 1:
      return `${mockScore}/5`;
    case 2:
      return `Score: ${mockScore}`;
    case 3:
      return `I would rate this a ${mockScore} based on the planetary configuration provided.`;
    case 4:
      return `${mockScore} out of 5`;
    default:
      return `${mockScore}`;
  }
}

// ---------------------------------------------------------------------------
// Payload Construction
// ---------------------------------------------------------------------------

/**
 * Builds the `AgentPayload` for a given test case.
 *
 * The `context` field carries the full `ChartState` object so that a real
 * agent can read every planetary indicator. The `prompt` is passed verbatim
 * as specified in the test case definition.
 *
 * @param testCase - The test case to build a payload for.
 * @returns A structured payload ready for agent invocation.
 */
function buildPayload(testCase: TestCase): AgentPayload {
  return {
    context: testCase.chartState,
    prompt: testCase.prompt,
    testCaseId: testCase.id,
  };
}

// ---------------------------------------------------------------------------
// Single-Case Evaluation
// ---------------------------------------------------------------------------

/**
 * Evaluates a single test case against the provided agent.
 *
 * Measures wall-clock execution time for the agent call + parsing phase.
 * Parsing failures are captured as `parsedScore: null` with `passed: false`.
 *
 * @param testCase - The test case to evaluate.
 * @param agent - The agent callable to invoke.
 * @returns A fully populated `EvaluationResult`.
 */
async function evaluateTestCase(
  testCase: TestCase,
  agent: AgentCallable
): Promise<EvaluationResult> {
  const payload = buildPayload(testCase);
  const startMs = performance.now();

  // Invoke the agent and capture the raw string response.
  const rawResponse = await agent(payload);

  const endMs = performance.now();
  const executionTimeMs = Math.round(endMs - startMs);

  // Attempt to parse the response into a [1–5] integer.
  const parsedScore = tryParseAgentScore(rawResponse);

  const delta =
    parsedScore !== null ? Math.abs(parsedScore - testCase.goldScore) : null;

  const passed = parsedScore === testCase.goldScore;

  return {
    testCaseId: testCase.id,
    tier: testCase.tier,
    topic: testCase.topic,
    goldScore: testCase.goldScore,
    rawResponse,
    parsedScore,
    delta,
    passed,
    evaluatedAt: new Date().toISOString(),
    executionTimeMs,
  };
}

// ---------------------------------------------------------------------------
// Summary Aggregation
// ---------------------------------------------------------------------------

/**
 * Computes a `BenchmarkSummary` from an array of `EvaluationResult` records.
 *
 * @param results - All individual evaluation results.
 * @param startedAt - ISO timestamp when the run started.
 * @param completedAt - ISO timestamp when the run completed.
 * @param totalExecutionTimeMs - Wall-clock duration of the entire run.
 * @returns Aggregated benchmark metrics.
 */
function computeSummary(
  results: EvaluationResult[],
  startedAt: string,
  completedAt: string,
  totalExecutionTimeMs: number
): BenchmarkSummary {
  const totalCases = results.length;
  const exactMatches = results.filter((r) => r.passed).length;
  const parseErrors = results.filter((r) => r.parsedScore === null).length;
  const failures = totalCases - exactMatches;

  const finalScorePercent =
    totalCases > 0 ? (exactMatches / totalCases) * 100 : 0;

  // Compute mean absolute delta across successfully parsed results only.
  const parsedResults = results.filter((r) => r.delta !== null);
  const meanAbsoluteDelta =
    parsedResults.length > 0
      ? parsedResults.reduce((sum, r) => sum + (r.delta ?? 0), 0) /
        parsedResults.length
      : 0;

  return {
    totalCases,
    exactMatches,
    failures,
    parseErrors,
    finalScorePercent,
    meanAbsoluteDelta,
    results,
    startedAt,
    completedAt,
    totalExecutionTimeMs,
  };
}

// ---------------------------------------------------------------------------
// Public API — Main Runner
// ---------------------------------------------------------------------------

/**
 * Runs a benchmark evaluation suite.
 *
 * Iterates through every test case in the provided dataset, evaluates each
 * against the provided agent (defaults to `mockAgentCall`), and returns
 * a complete `BenchmarkSummary`.
 *
 * @param dataset - The array of test cases to evaluate.
 * @param agent - Optional agent callable. Defaults to `mockAgentCall`.
 *                Swap this for your real AI agent in production use.
 * @returns A fully populated `BenchmarkSummary` with all results.
 *
 * @example
 * // Run with mock agent (default):
 * const summary = await runBenchmark(myDataset);
 *
 * // Run with a real agent:
 * const summary = await runBenchmark(myDataset, async (payload) => {
 *   const response = await myAIClient.generate(payload);
 *   return response.text;
 * });
 */
export async function runBenchmark(
  dataset: ReadonlyArray<TestCase>,
  agent: AgentCallable = mockAgentCall
): Promise<BenchmarkSummary> {
  const startedAt = new Date().toISOString();
  const runStartMs = performance.now();

  // Evaluate all test cases sequentially to avoid rate-limiting issues with
  // real agents. Switch to Promise.all for parallel execution if needed.
  const results: EvaluationResult[] = [];
  for (const testCase of dataset) {
    const result = await evaluateTestCase(testCase, agent);
    results.push(result);
  }

  const runEndMs = performance.now();
  const completedAt = new Date().toISOString();
  const totalExecutionTimeMs = Math.round(runEndMs - runStartMs);

  return computeSummary(results, startedAt, completedAt, totalExecutionTimeMs);
}
