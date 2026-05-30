/**
 * @file src/core/parser.ts
 * @description Fail-safe integer extractor for BPHS-Bench agent responses.
 *
 * AI agents rarely return a bare digit. Common formats encountered in practice:
 *   - "3"                          → trivial case
 *   - "The answer is 3"            → trailing digit in sentence
 *   - "3/5"                        → fraction notation
 *   - "Score: 3"                   → label prefix
 *   - "I would rate this a 3."     → embedded in prose
 *   - "Rating: 3 out of 5"         → verbose format
 *   - " 3 "                        → padded whitespace
 *   - "**3**"                      → markdown bold
 *   - "Answer:\n3"                 → newline-separated
 *
 * The parser applies a layered regex strategy to reliably extract the
 * *first* standalone integer in the range [1–5], ignoring all surrounding
 * prose, punctuation, or formatting noise.
 *
 * @throws {ParseError} when no valid 1-5 integer can be extracted.
 */

// ---------------------------------------------------------------------------
// Custom Error
// ---------------------------------------------------------------------------

/**
 * Thrown when the parser cannot extract a valid [1-5] integer from the input.
 * Carries the original raw response for upstream error reporting.
 */
export class ParseError extends Error {
  /** The raw response string that could not be parsed. */
  public readonly rawResponse: string;

  constructor(rawResponse: string) {
    const truncated =
      rawResponse.length > 120
        ? `${rawResponse.slice(0, 120)}…`
        : rawResponse;
    super(
      `[BPHSBench:ParseError] Could not extract a valid 1-5 integer from agent response: "${truncated}"`
    );
    this.name = "ParseError";
    this.rawResponse = rawResponse;
    // Preserve prototype chain for instanceof checks across ES5 transpilation.
    Object.setPrototypeOf(this, new.target.prototype);
  }
}

// ---------------------------------------------------------------------------
// Validation Helper
// ---------------------------------------------------------------------------

/**
 * Returns `true` if `n` is a valid BPHS-Bench score (integer in [1, 5]).
 */
function isValidScore(n: number): n is 1 | 2 | 3 | 4 | 5 {
  return Number.isInteger(n) && n >= 1 && n <= 5;
}

// ---------------------------------------------------------------------------
// Extraction Strategies (ordered by specificity — most precise first)
// ---------------------------------------------------------------------------

/**
 * Strategy 1 — Standalone digit on its own line or fully isolated.
 *
 * Matches: "3", " 3 ", "\n3\n", "**3**"
 * Pattern: word boundary on both sides, digit in [1-5].
 */
const STRATEGY_ISOLATED_DIGIT = /(?<![0-9])[1-5](?![0-9])/;

/**
 * Strategy 2 — Fraction notation (e.g., "3/5", "4/5").
 *
 * Matches: "3/5", "2/5", "rating: 4/5"
 * Captures the numerator in group 1.
 */
const STRATEGY_FRACTION = /([1-5])\s*\/\s*5/i;

/**
 * Strategy 3 — Labelled response patterns.
 *
 * Matches: "Score: 3", "Rating: 4", "Answer: 2", "Result: 5"
 * Captures the digit in group 1.
 */
const STRATEGY_LABELLED = /(?:score|rating|answer|result|response)[:\s]+([1-5])\b/i;

/**
 * Strategy 4 — "Out of" phrasing (e.g., "3 out of 5").
 *
 * Matches: "3 out of 5", "I give it a 4 out of 5"
 * Captures the digit in group 1.
 */
const STRATEGY_OUT_OF = /([1-5])\s+out\s+of\s+5/i;

/**
 * Strategy 5 — Written number words as last-resort fallback.
 *
 * Matches: "one", "two", "three", "four", "five" (case-insensitive).
 * Returns the mapped integer value.
 */
const STRATEGY_WORD_NUMBERS: ReadonlyMap<RegExp, number> = new Map([
  [/\bone\b/i, 1],
  [/\btwo\b/i, 2],
  [/\bthree\b/i, 3],
  [/\bfour\b/i, 4],
  [/\bfive\b/i, 5],
]);

// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------

/**
 * Extracts the first valid BPHS-Bench score (integer 1–5) from an agent
 * response string using a layered regex strategy.
 *
 * Strategy execution order (first match wins):
 *  1. Fraction notation  — "3/5"
 *  2. Labelled response  — "Score: 3"
 *  3. "Out of 5" phrasing — "3 out of 5"
 *  4. Isolated digit     — standalone [1-5] with no adjacent digits
 *  5. Written number words — "three"
 *
 * @param rawResponse - The raw string returned by the AI agent.
 * @returns The parsed score as a number in [1, 5].
 * @throws {ParseError} If no valid score can be extracted.
 *
 * @example
 * parseAgentScore("The answer is 3")    // → 3
 * parseAgentScore("3/5")                // → 3
 * parseAgentScore("Score: 4")           // → 4
 * parseAgentScore("4 out of 5")         // → 4
 * parseAgentScore("**2**")              // → 2
 * parseAgentScore("three")             // → 3
 * parseAgentScore("definitely maybe")  // → throws ParseError
 */
export function parseAgentScore(rawResponse: string): number {
  // Normalise: strip leading/trailing whitespace, collapse multiple spaces.
  const cleaned = rawResponse.trim().replace(/\s+/g, " ");

  // --- Strategy 1: Fraction notation (highest signal, check first) ---
  const fractionMatch = cleaned.match(STRATEGY_FRACTION);
  if (fractionMatch != null && fractionMatch[1] != null) {
    const candidate = parseInt(fractionMatch[1], 10);
    if (isValidScore(candidate)) return candidate;
  }

  // --- Strategy 2: Labelled response ---
  const labelledMatch = cleaned.match(STRATEGY_LABELLED);
  if (labelledMatch != null && labelledMatch[1] != null) {
    const candidate = parseInt(labelledMatch[1], 10);
    if (isValidScore(candidate)) return candidate;
  }

  // --- Strategy 3: "out of 5" phrasing ---
  const outOfMatch = cleaned.match(STRATEGY_OUT_OF);
  if (outOfMatch != null && outOfMatch[1] != null) {
    const candidate = parseInt(outOfMatch[1], 10);
    if (isValidScore(candidate)) return candidate;
  }

  // --- Strategy 4: Isolated digit (broadest numeric match) ---
  const isolatedMatch = cleaned.match(STRATEGY_ISOLATED_DIGIT);
  if (isolatedMatch != null && isolatedMatch[0] != null) {
    const candidate = parseInt(isolatedMatch[0], 10);
    if (isValidScore(candidate)) return candidate;
  }

  // --- Strategy 5: Written number words (last resort) ---
  for (const [pattern, value] of STRATEGY_WORD_NUMBERS) {
    if (pattern.test(cleaned)) {
      return value;
    }
  }

  // All strategies exhausted — throw a typed error with the raw payload.
  throw new ParseError(rawResponse);
}

/**
 * Safe variant of `parseAgentScore` that returns `null` instead of throwing.
 *
 * Useful in contexts where parse failures should be collected rather than
 * propagated (e.g., batch evaluation loops that must continue on error).
 *
 * @param rawResponse - The raw string returned by the AI agent.
 * @returns The parsed score, or `null` if parsing fails.
 */
export function tryParseAgentScore(rawResponse: string): number | null {
  try {
    return parseAgentScore(rawResponse);
  } catch {
    return null;
  }
}
