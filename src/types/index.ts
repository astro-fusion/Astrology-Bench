/**
 * @file src/types/index.ts
 * @description Core type definitions for the BPHS-Bench evaluation framework.
 *
 * All interfaces are intentionally explicit to enforce strict data contracts
 * across the benchmark harness, dataset, and parser layers.
 */

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
 *
 * Fields are intentionally typed as `string | number | string[] | undefined`
 * to accommodate the heterogeneous nature of astrological parameters across
 * different house queries (career, marriage, children, etc.).
 *
 * Each key maps to a BPHS-recognised astrological indicator:
 *  - Lordship positions (e.g., `10th_lord`, `7th_lord`)
 *  - Divisional chart states (D1, D5, D9)
 *  - Dasha contexts (Mahadasha, Antardasha, Pratyantar Dasha)
 *  - Ashtakavarga Bindu counts (numerical strength scores per house)
 *  - Yoga formations (Parivartana, Vipareeta, Harsha, Sarala)
 *  - Paksha Bala (lunar phase strength)
 *  - Shadbala planetary strength ratios
 *  - Transit overlays over natal placements
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
  /** Active Mahadasha lord (e.g. "Mars Mahadasha"). */
  current_dasha?: string;
  /** Active Pratyantar Dasha lord and state. */
  current_pratyantar_dasha_lord?: string;

  // --- Yoga Formations ---
  /** Description of any active Parivartana (mutual exchange) Yoga. */
  parivartana_yoga?: string;
  /** Description of any mutual exchange formation. */
  mutual_exchange?: string;
  /** Key planetary conjunction with degree proximity. */
  planetary_conjunction?: string;

  // --- Neecha Bhanga & Cancellation ---
  /** Whether Neecha Bhanga Raja Yoga is active and its trigger. */
  neecha_bhanga?: string;
  /** State of the dispositor planet that influences Neecha Bhanga. */
  dispositor_state?: string;

  // --- Ashtakavarga Bindu Counts (0–56 scale per house) ---
  /** Bindu strength of the 2nd house (wealth). */
  ashtakavarga_2nd_house_bindus?: number;
  /** Bindu strength of the 7th house (marriage/partnership). */
  ashtakavarga_7th_house_bindus?: number;
  /** Bindu strength of the 10th house (career/status). */
  ashtakavarga_10th_house_bindus?: number;
  /** Bindu strength of the 11th house (gains/fulfilment). */
  ashtakavarga_11th_house_bindus?: number;

  // --- Paksha Bala ---
  /** Lunar phase strength descriptor (e.g. "Weak New Moon phase"). */
  moon_paksha_bala?: string;

  // --- Shadbala ---
  /** Shadbala strength ratio for Mars (1.0 = minimum required). */
  shadbala_mars?: number;

  // --- Transit Overlays ---
  /** Current Saturn or other slow-planet transit description. */
  transit_state?: string;

  // --- Upapada Lagna (Marriage Potential Point) ---
  /** Sign of the Upapada Lagna. */
  upapada_lagna_sign?: string;
  /** Planets occupying the Upapada Lagna. */
  upapada_lagna_planets?: string[];

  // --- Extensibility ---
  /** Catch-all for any additional chart parameters not explicitly typed. */
  [key: string]: string | number | string[] | undefined;
}

// ---------------------------------------------------------------------------
// TestCase
// ---------------------------------------------------------------------------

/**
 * A single benchmark test case representing one evaluation unit.
 *
 * Combines the astrological context (`chartState`), the natural-language
 * prompt presented to the AI agent, and the immutable gold standard score
 * derived from classical rules.
 */
export interface TestCase {
  /**
   * Unique identifier.
   * Convention: `TC-{TIER_CODE}-{SEQUENTIAL_NUMBER}` (e.g., "TC-EASY-01").
   */
  id: string;

  /** Difficulty tier classification. */
  tier: Tier;

  /** Short descriptive label for the astrological topic being evaluated. */
  topic: string;

  /**
   * The layman-facing prompt shown to the AI agent.
   * Must always instruct the agent to reply with only a number (1–5).
   */
  prompt: string;

  /**
   * The immutable gold-standard expected score (1–5).
   */
  readonly goldScore: 1 | 2 | 3 | 4 | 5;

  /**
   * The interpretive logic or rule chain that justifies the goldScore.
   * Based on the source text specified in `reference`.
   */
  logic: string;

  /**
   * Precise citation for the interpretive rule.
   */
  reference: {
    book: string;
    chapter?: string;
    verse?: string;
  };

  /** Optional tags for filtering (e.g., "wealth", "marriage", "yogas"). */
  tags?: string[];

  /** The pre-calculated planetary state injected into the agent context. */
  chartState: ChartState;
}

// ---------------------------------------------------------------------------
// EvaluationResult
// ---------------------------------------------------------------------------

/**
 * The result of evaluating a single `TestCase` against an AI agent response.
 *
 * Captures the full audit trail from raw response to final pass/fail verdict.
 */
export interface EvaluationResult {
  /** The test case ID that was evaluated. */
  testCaseId: string;

  /** The difficulty tier of the evaluated test case. */
  tier: Tier;

  /** The topic label for human-readable reporting. */
  topic: string;

  /** The immutable gold standard score for this test case. */
  goldScore: 1 | 2 | 3 | 4 | 5;

  /** The raw unprocessed string returned by the AI agent. */
  rawResponse: string;

  /**
   * The integer parsed from `rawResponse` by the parser.
   * `null` if parsing failed (no valid 1–5 integer found).
   */
  parsedScore: number | null;

  /**
   * The absolute numerical delta between parsed and gold scores.
   * `null` if parsing failed.
   */
  delta: number | null;

  /** Whether the parsed score exactly matches the gold score. */
  passed: boolean;

  /** ISO 8601 timestamp of when this evaluation was completed. */
  evaluatedAt: string;

  /** Wall-clock execution time for this single evaluation in milliseconds. */
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

  /** Number of test cases that failed (wrong score or parse error). */
  failures: number;

  /** Number of test cases where the agent response could not be parsed. */
  parseErrors: number;

  /**
   * Final benchmark score as a percentage (0–100).
   * Formula: (exactMatches / totalCases) × 100
   */
  finalScorePercent: number;

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
 *
 * The `context` field provides the structured planetary state as a
 * serialized JSON block; the `prompt` is the natural-language question.
 */
export interface AgentPayload {
  /** Structured astrological context for the agent to interpret. */
  context: ChartState;

  /** The layman-facing question the agent must answer with a 1–5 score. */
  prompt: string;

  /** The test case ID for traceability in logs or agent telemetry. */
  testCaseId: string;
}
