/**
 * @file src/index.ts
 * @description CLI entry point for the BPHS-Bench evaluation framework.
 *
 * Runs the full benchmark suite and renders a formatted Markdown table
 * directly to the terminal, followed by an aggregate summary block.
 *
 * Usage:
 *   npm run bench
 *
 * To integrate a real AI agent, replace the `agent` parameter in `runBenchmark`
 * with your own `AgentCallable` implementation.
 */

import { runBenchmark } from "./core/harness.js";
import type { BenchmarkSummary, EvaluationResult } from "./types/index.js";

// ---------------------------------------------------------------------------
// ANSI Colour Helpers (no external dependencies)
// ---------------------------------------------------------------------------

const ANSI = {
  reset: "\x1b[0m",
  bold: "\x1b[1m",
  dim: "\x1b[2m",
  green: "\x1b[32m",
  red: "\x1b[31m",
  yellow: "\x1b[33m",
  cyan: "\x1b[36m",
  magenta: "\x1b[35m",
  blue: "\x1b[34m",
  white: "\x1b[37m",
  bgGreen: "\x1b[42m",
  bgRed: "\x1b[41m",
} as const;

function bold(s: string): string {
  return `${ANSI.bold}${s}${ANSI.reset}`;
}
function cyan(s: string): string {
  return `${ANSI.cyan}${s}${ANSI.reset}`;
}
function green(s: string): string {
  return `${ANSI.green}${s}${ANSI.reset}`;
}
function red(s: string): string {
  return `${ANSI.red}${s}${ANSI.reset}`;
}
function yellow(s: string): string {
  return `${ANSI.yellow}${s}${ANSI.reset}`;
}
function magenta(s: string): string {
  return `${ANSI.magenta}${s}${ANSI.reset}`;
}
function dim(s: string): string {
  return `${ANSI.dim}${s}${ANSI.reset}`;
}

// ---------------------------------------------------------------------------
// Table Renderer
// ---------------------------------------------------------------------------

/** Column widths (characters) for the results table. */
const COL = {
  id: 15,
  tier: 10,
  topic: 40,
  gold: 14,
  ai: 10,
  delta: 7,
  result: 12,
  time: 10,
} as const;

/** Pads a string to a fixed width, truncating with "…" if needed. */
function pad(value: string, width: number): string {
  if (value.length > width) {
    return value.slice(0, width - 1) + "…";
  }
  return value.padEnd(width);
}

/** Renders the Markdown-compatible table header. */
function renderTableHeader(): string {
  const h = (label: string, width: number): string =>
    pad(label, width);

  const header = [
    h("Test Case ID", COL.id),
    h("Difficulty", COL.tier),
    h("Topic", COL.topic),
    h("Target Score", COL.gold),
    h("AI Score", COL.ai),
    h("Δ", COL.delta),
    h("Result", COL.result),
    h("Time (ms)", COL.time),
  ]
    .map((col) => bold(cyan(col)))
    .join(" │ ");

  const separator = [
    "─".repeat(COL.id),
    "─".repeat(COL.tier),
    "─".repeat(COL.topic),
    "─".repeat(COL.gold),
    "─".repeat(COL.ai),
    "─".repeat(COL.delta),
    "─".repeat(COL.result),
    "─".repeat(COL.time),
  ].join("─┼─");

  return `${header}\n${dim(separator)}`;
}

/** Renders a single result row with ANSI colouring. */
function renderResultRow(result: EvaluationResult): string {
  const passLabel = result.passed
    ? green("✔ PASS")
    : result.parsedScore === null
    ? yellow("✘ PARSE ERR")
    : red("✘ FAIL");

  const aiScore =
    result.parsedScore !== null ? String(result.parsedScore) : red("—");

  const delta =
    result.delta !== null
      ? result.delta === 0
        ? green("0")
        : red(`+${result.delta}`)
      : dim("—");

  const tierColour: Record<string, (s: string) => string> = {
    EASY: green,
    MEDIUM: yellow,
    HARD: magenta,
    VERY_HARD: red,
  };
  const tierFn = tierColour[result.tier] ?? ((s: string) => s);

  return [
    pad(result.testCaseId, COL.id),
    pad(tierFn(result.tier), COL.tier + 10), // +10 for ANSI escape overhead
    pad(result.topic, COL.topic),
    pad(String(result.goldScore), COL.gold),
    pad(aiScore, COL.ai + (result.parsedScore === null ? 10 : 0)),
    pad(delta, COL.delta + 10),
    pad(passLabel, COL.result + 10),
    pad(`${result.executionTimeMs}ms`, COL.time),
  ].join(" │ ");
}

// ---------------------------------------------------------------------------
// Summary Block Renderer
// ---------------------------------------------------------------------------

/** Returns a coloured grade label based on the final score percentage. */
function gradeLabel(score: number): string {
  if (score >= 90) return green("🏆  EXCELLENT");
  if (score >= 70) return cyan("✔   GOOD");
  if (score >= 50) return yellow("⚠   MODERATE");
  return red("✘   NEEDS WORK");
}

/** Renders the aggregate summary block beneath the results table. */
function renderSummary(summary: BenchmarkSummary): string {
  const score = summary.finalScorePercent.toFixed(1);
  const grade = gradeLabel(summary.finalScorePercent);

  const tierBreakdown = ["EASY", "MEDIUM", "HARD", "VERY_HARD"]
    .map((tier) => {
      const tierResults = summary.results.filter((r) => r.tier === tier);
      if (tierResults.length === 0) return null;
      const passed = tierResults.filter((r) => r.passed).length;
      return `  ${pad(tier, 10)} ${green(String(passed))}/${tierResults.length}`;
    })
    .filter(Boolean)
    .join("\n");

  return [
    "",
    dim("─".repeat(115)),
    "",
    bold("  BPHS-BENCH SUMMARY"),
    "",
    `  ${bold("Final Score:")}          ${bold(cyan(`${score}%`))}  ${grade}`,
    `  ${bold("Exact Matches:")}        ${green(String(summary.exactMatches))} / ${summary.totalCases}`,
    `  ${bold("Failures:")}             ${summary.failures > 0 ? red(String(summary.failures)) : green("0")}`,
    `  ${bold("Parse Errors:")}         ${summary.parseErrors > 0 ? yellow(String(summary.parseErrors)) : green("0")}`,
    `  ${bold("Mean Abs. Delta:")}      ${summary.meanAbsoluteDelta.toFixed(2)}`,
    `  ${bold("Total Runtime:")}        ${summary.totalExecutionTimeMs}ms`,
    "",
    bold("  BY TIER"),
    tierBreakdown,
    "",
    dim(`  Run started:   ${summary.startedAt}`),
    dim(`  Run completed: ${summary.completedAt}`),
    "",
    dim("─".repeat(115)),
    "",
  ].join("\n");
}

// ---------------------------------------------------------------------------
// CLI Banner
// ---------------------------------------------------------------------------

function renderBanner(): void {
  process.stdout.write("\n");
  process.stdout.write(
    bold(cyan("  ╔══════════════════════════════════════════════════╗\n"))
  );
  process.stdout.write(
    bold(cyan("  ║          BPHS-BENCH  v1.0.0                      ║\n"))
  );
  process.stdout.write(
    bold(cyan("  ║  Brihat Parashara Hora Shastra Evaluation Suite   ║\n"))
  );
  process.stdout.write(
    bold(cyan("  ╚══════════════════════════════════════════════════╝\n"))
  );
  process.stdout.write("\n");
  process.stdout.write(
    dim(
      "  Evaluating 10 test cases across EASY → MEDIUM → HARD → VERY_HARD tiers…\n"
    )
  );
  process.stdout.write("\n");
}

// ---------------------------------------------------------------------------
// Main Entry Point
// ---------------------------------------------------------------------------

async function main(): Promise<void> {
  renderBanner();

  // --- Run the benchmark suite ---
  // Pass a custom `AgentCallable` here to benchmark a real AI agent:
  //
  //   const summary = await runBenchmark(async (payload) => {
  //     const res = await myClient.generate({
  //       systemPrompt: JSON.stringify(payload.context),
  //       userPrompt: payload.prompt,
  //     });
  //     return res.text;
  //   });
  //
  const summary = await runBenchmark();

  // --- Render the results table ---
  process.stdout.write(renderTableHeader() + "\n");

  for (const result of summary.results) {
    process.stdout.write(renderResultRow(result) + "\n");
  }

  // --- Render the aggregate summary ---
  process.stdout.write(renderSummary(summary));

  // Exit with non-zero code if any cases failed (useful for CI pipelines).
  if (summary.failures > 0 || summary.parseErrors > 0) {
    process.exit(1);
  }
}

main().catch((err: unknown) => {
  const message = err instanceof Error ? err.message : String(err);
  process.stderr.write(`\n${red("[FATAL]")} Benchmark run aborted: ${message}\n`);
  process.exit(2);
});
