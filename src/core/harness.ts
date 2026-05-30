/**
 * @file src/core/harness.ts
 * @description Core execution engine for the Astro-Bench evaluation framework.
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

export type AgentCallable = (payload: AgentPayload) => Promise<string>;

// ---------------------------------------------------------------------------
// Mock Agent
// ---------------------------------------------------------------------------

async function mockAgentCall(payload: AgentPayload): Promise<string> {
  const seed = payload.testCaseId
    .split("")
    .reduce((acc, c) => acc + c.charCodeAt(0), 0);

  const mockScore = (seed % 5) + 1;
  const delayMs = 10 + (seed % 40);
  await new Promise<void>((resolve) => setTimeout(resolve, delayMs));

  const formatIndex = seed % 5;
  switch (formatIndex) {
    case 0: return `${mockScore}`;
    case 1: return `${mockScore}/5`;
    case 2: return `Score: ${mockScore}`;
    case 3: return `I would rate this a ${mockScore} based on the planetary configuration provided.`;
    case 4: return `${mockScore} out of 5`;
    default: return `${mockScore}`;
  }
}

// ---------------------------------------------------------------------------
// Payload Construction
// ---------------------------------------------------------------------------

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

async function evaluateTestCase(
  testCase: TestCase,
  agent: AgentCallable
): Promise<EvaluationResult> {
  const payload = buildPayload(testCase);
  const startMs = performance.now();

  const rawResponse = await agent(payload);

  const endMs = performance.now();
  const executionTimeMs = Math.round(endMs - startMs);

  const parsedScore = tryParseAgentScore(rawResponse);

  const delta =
    parsedScore !== null ? Math.abs(parsedScore - testCase.goldScore) : null;

  const passed = parsedScore === testCase.goldScore;

  // Award points based on proximity
  let points = 0;
  if (delta === 0) {
    points = 1.0;
  } else if (delta === 1) {
    points = 0.5;
  }

  return {
    testCaseId: testCase.id,
    source: testCase.source,
    tier: testCase.tier,
    topic: testCase.topic,
    goldScore: testCase.goldScore,
    rawResponse,
    parsedScore,
    delta,
    points,
    passed,
    evaluatedAt: new Date().toISOString(),
    executionTimeMs,
  };
}

// ---------------------------------------------------------------------------
// Summary Aggregation
// ---------------------------------------------------------------------------

function computeSummary(
  results: EvaluationResult[],
  startedAt: string,
  completedAt: string,
  totalExecutionTimeMs: number
): BenchmarkSummary {
  const totalCases = results.length;
  const exactMatches = results.filter((r) => r.passed).length;
  const totalPoints = results.reduce((sum, r) => sum + r.points, 0);
  const parseErrors = results.filter((r) => r.parsedScore === null).length;
  const failures = totalCases - exactMatches;

  const finalScorePercent =
    totalCases > 0 ? (exactMatches / totalCases) * 100 : 0;

  const weightedScorePercent =
    totalCases > 0 ? (totalPoints / totalCases) * 100 : 0;

  const parsedResults = results.filter((r) => r.delta !== null);
  const meanAbsoluteDelta =
    parsedResults.length > 0
      ? parsedResults.reduce((sum, r) => sum + (r.delta ?? 0), 0) /
        parsedResults.length
      : 0;

  return {
    totalCases,
    exactMatches,
    totalPoints,
    failures,
    parseErrors,
    finalScorePercent,
    weightedScorePercent,
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

export async function runBenchmark(
  dataset: ReadonlyArray<TestCase>,
  agent: AgentCallable = mockAgentCall
): Promise<BenchmarkSummary> {
  const startedAt = new Date().toISOString();
  const runStartMs = performance.now();

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
