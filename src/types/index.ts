/**
 * @file src/types/index.ts
 * @description Core type definitions for the Astro-Bench evaluation framework.
 */

// ---------------------------------------------------------------------------
// Source Type
// ---------------------------------------------------------------------------

/** Supported classical source texts. */
export type Source = "BPHS" | "Phaladeepika" | "Saravali" | "Jaimini" | "Synthesis";

// ---------------------------------------------------------------------------
// Tier Difficulty
// ---------------------------------------------------------------------------

/** Difficulty classification for each test case. */
export type Tier = "EASY" | "MEDIUM" | "HARD" | "VERY_HARD";

// ---------------------------------------------------------------------------
// ChartState
// ---------------------------------------------------------------------------

/**
 * A structured snapshot of a Vedic horoscope relevant to a single test case.
 */
export interface ChartState {
  /** Rising sign (Lagna) for the chart. */
  ascendant?: string;

  // --- Divisional Chart Positions (D1 = Rashi) ---
  "1st_lord"?: string;
  "2nd_house_sign"?: string;
  "2nd_lord"?: string;
  "5th_house_sign"?: string;
  "5th_house_planets"?: string[];
  "6th_lord"?: string;
  "7th_house_sign"?: string;
  "7th_lord"?: string;
  "7th_house_planets"?: string[];
  "8th_lord"?: string;
  "9th_lord"?: string;
  "10th_house_sign"?: string;
  "10th_lord"?: string;
  "10th_house_aspects"?: string;
  "11th_house_sign"?: string;
  "11th_lord"?: string;

  // --- D1 Karaka (Natural Significator) Positions ---
  "D1_5th_lord"?: string;
  "D1_7th_lord"?: string;
  "D1_jupiter_karaka"?: string;

  // --- D5 Panchamsha Chart ---
  "D5_panchamsha_5th_lord"?: string;
  "D5_jupiter_karaka"?: string;

  // --- D9 Navamsha Chart ---
  "D9_navamsha_7th_lord"?: string;

  // --- Dasha Context ---
  current_dasha?: string;
  current_pratyantar_dasha_lord?: string;

  // --- Yoga Formations ---
  parivartana_yoga?: string;
  mutual_exchange?: string;
  planetary_conjunction?: string;

  // --- Neecha Bhanga & Cancellation ---
  neecha_bhanga?: string;
  dispositor_state?: string;

  // --- Ashtakavarga Bindu Counts (0–56 scale per house) ---
  ashtakavarga_2nd_house_bindus?: number;
  ashtakavarga_7th_house_bindus?: number;
  ashtakavarga_10th_house_bindus?: number;
  ashtakavarga_11th_house_bindus?: number;

  // --- Paksha Bala ---
  moon_paksha_bala?: string;

  // --- Shadbala ---
  shadbala_mars?: number;

  // --- Transit Overlays ---
  transit_state?: string;

  // --- Upapada Lagna ---
  upapada_lagna_sign?: string;
  upapada_lagna_planets?: string[];

  /** Catch-all for any additional chart parameters. */
  [key: string]: string | number | string[] | undefined;
}

// ---------------------------------------------------------------------------
// TestCase
// ---------------------------------------------------------------------------

/**
 * A single benchmark test case representing one evaluation unit.
 */
export interface TestCase {
  /**
   * Unique identifier.
   * Convention: `{SOURCE_ID}-{SEQUENTIAL_NUMBER}` (e.g., "BPHS-01").
   */
  id: string;

  /** The classical source text this test case is derived from. */
  source: Source;

  /** Difficulty tier classification. */
  tier: Tier;

  /** Short descriptive label for the astrological topic being evaluated. */
  topic: string;

  /**
   * The layman-facing prompt shown to the AI agent.
   */
  prompt: string;

  /**
   * The immutable gold-standard expected score (1–5).
   */
  readonly goldScore: 1 | 2 | 3 | 4 | 5;

  /**
   * The interpretive logic or rule chain that justifies the goldScore.
   */
  logic: string;

  /**
   * Precise citation for the interpretive rule.
   */
  reference: {
    book: string;
    chapter?: string;
    verse?: string;
    quote?: string;
  };

  /** Optional tags for filtering. */
  tags?: string[];

  /** The pre-calculated planetary state injected into the agent context. */
  chartState: ChartState;
}

// ---------------------------------------------------------------------------
// EvaluationResult
// ---------------------------------------------------------------------------

/**
 * The result of evaluating a single `TestCase` against an AI agent response.
 */
export interface EvaluationResult {
  /** The test case ID that was evaluated. */
  testCaseId: string;

  /** The source of the evaluated test case. */
  source: Source;

  /** The difficulty tier of the evaluated test case. */
  tier: Tier;

  /** The topic label for human-readable reporting. */
  topic: string;

  /** The immutable gold standard score for this test case. */
  goldScore: 1 | 2 | 3 | 4 | 5;

  /** The raw unprocessed string returned by the AI agent. */
  rawResponse: string;

  /**
   * The integer parsed from `rawResponse`.
   */
  parsedScore: number | null;

  /**
   * The absolute numerical delta between parsed and gold scores.
   */
  delta: number | null;

  /**
   * Points awarded for this evaluation.
   * 1.0 = Exact Match (delta 0)
   * 0.5 = Near Match (delta 1)
   * 0.0 = Fail (delta >= 2 or Parse Error)
   */
  points: number;

  /** Whether the parsed score exactly matches the gold score. */
  passed: boolean;

  /** ISO 8601 timestamp of when this evaluation was completed. */
  evaluatedAt: string;

  /** Wall-clock execution time in milliseconds. */
  executionTimeMs: number;
}

// ---------------------------------------------------------------------------
// BenchmarkSummary
// ---------------------------------------------------------------------------

/**
 * Aggregate metrics computed after all test cases have been evaluated.
 */
export interface BenchmarkSummary {
  /** Total number of test cases in the run. */
  totalCases: number;

  /** Number of test cases that passed (exact match). */
  exactMatches: number;

  /** Total points accumulated across all cases. */
  totalPoints: number;

  /** Number of test cases that failed. */
  failures: number;

  /** Number of test cases where the agent response could not be parsed. */
  parseErrors: number;

  /**
   * Final benchmark score as a percentage (0–100).
   */
  finalScorePercent: number;

  /**
   * Weighted point-based score as a percentage (0–100).
   */
  weightedScorePercent: number;

  /** Mean absolute delta across all successfully parsed responses. */
  meanAbsoluteDelta: number;

  /** Individual result records for every evaluated test case. */
  results: EvaluationResult[];

  /** ISO 8601 timestamp when the benchmark run started. */
  startedAt: string;

  /** ISO 8601 timestamp when the benchmark run completed. */
  completedAt: string;

  /** Total wall-clock time for the entire benchmark run in milliseconds. */
  totalExecutionTimeMs: number;
}

// ---------------------------------------------------------------------------
// Agent Integration Contract
// ---------------------------------------------------------------------------

/**
 * The payload constructed by the harness and sent to the AI agent.
 */
export interface AgentPayload {
  /** Structured astrological context for the agent to interpret. */
  context: ChartState;

  /** The layman-facing question the agent must answer with a 1–5 score. */
  prompt: string;

  /** The test case ID for traceability. */
  testCaseId: string;
}
