/**
 * @file src/index.ts
 * @description CLI entry point for the Astro-Bench evaluation framework.
 */

import { runBenchmark } from "./core/harness.js";
import { BENCHMARKS, getBenchmark } from "./benchmarks/index.js";
import type { BenchmarkSummary, EvaluationResult } from "./types/index.js";
import type { BenchmarkDefinition } from "./benchmarks/index.js";

// ---------------------------------------------------------------------------
// ANSI Colour Helpers
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

function bold(s: string): string { return `${ANSI.bold}${s}${ANSI.reset}`; }
function cyan(s: string): string { return `${ANSI.cyan}${s}${ANSI.reset}`; }
function green(s: string): string { return `${ANSI.green}${s}${ANSI.reset}`; }
function red(s: string): string { return `${ANSI.red}${s}${ANSI.reset}`; }
function yellow(s: string): string { return `${ANSI.yellow}${s}${ANSI.reset}`; }
function magenta(s: string): string { return `${ANSI.magenta}${s}${ANSI.reset}`; }
function dim(s: string): string { return `${ANSI.dim}${s}${ANSI.reset}`; }

// ---------------------------------------------------------------------------
// Table Renderer
// ---------------------------------------------------------------------------

const COL = {
  id: 10,
  source: 14,
  tier: 10,
  topic: 35,
  gold: 7,
  ai: 6,
  pts: 6,
  result: 12,
  time: 10,
} as const;

function pad(value: string, width: number): string {
  if (value.length > width) return value.slice(0, width - 1) + "…";
  return value.padEnd(width);
}

function renderTableHeader(): string {
  const h = (label: string, width: number): string => pad(label, width);

  const header = [
    h("ID", COL.id),
    h("Source", COL.source),
    h("Difficulty", COL.tier),
    h("Topic", COL.topic),
    h("Gold", COL.gold),
    h("AI", COL.ai),
    h("Pts", COL.pts),
    h("Result", COL.result),
    h("Time", COL.time),
  ].map((col) => bold(cyan(col))).join(" │ ");

  const separator = [
    "─".repeat(COL.id),
    "─".repeat(COL.source),
    "─".repeat(COL.tier),
    "─".repeat(COL.topic),
    "─".repeat(COL.gold),
    "─".repeat(COL.ai),
    "─".repeat(COL.pts),
    "─".repeat(COL.result),
    "─".repeat(COL.time),
  ].join("─┼─");

  return `${header}\n${dim(separator)}`;
}

function renderResultRow(result: EvaluationResult): string {
  const passLabel = result.passed
    ? green("✔ PASS")
    : result.points === 0.5
    ? yellow("⚠ NEAR")
    : result.parsedScore === null
    ? yellow("✘ PARSE ERR")
    : red("✘ FAIL");

  const aiScore = result.parsedScore !== null ? String(result.parsedScore) : red("—");
  const points = result.points === 1.0 ? green("1.0") : result.points === 0.5 ? yellow("0.5") : red("0.0");

  const tierColour: Record<string, (s: string) => string> = {
    EASY: green,
    MEDIUM: yellow,
    HARD: magenta,
    VERY_HARD: red,
  };
  const tierFn = tierColour[result.tier] ?? ((s: string) => s);

  return [
    pad(result.testCaseId, COL.id),
    pad(result.source, COL.source),
    pad(tierFn(result.tier), COL.tier + 10),
    pad(result.topic, COL.topic),
    pad(String(result.goldScore), COL.gold),
    pad(aiScore, COL.ai + (result.parsedScore === null ? 10 : 0)),
    pad(points, COL.pts + 10),
    pad(passLabel, COL.result + 10),
    pad(`${result.executionTimeMs}ms`, COL.time),
  ].join(" │ ");
}

// ---------------------------------------------------------------------------
// Summary Block Renderer
// ---------------------------------------------------------------------------

function gradeLabel(score: number): string {
  if (score >= 90) return green("🏆  EXCELLENT");
  if (score >= 75) return cyan("✔   GOOD");
  if (score >= 55) return yellow("⚠   MODERATE");
  return red("✘   NEEDS WORK");
}

function renderSummary(summary: BenchmarkSummary, bench: BenchmarkDefinition): string {
  const weighted = summary.weightedScorePercent.toFixed(1);
  const exact = summary.finalScorePercent.toFixed(1);
  const grade = gradeLabel(summary.weightedScorePercent);

  const tierBreakdown = ["EASY", "MEDIUM", "HARD", "VERY_HARD"]
    .map((tier) => {
      const tierResults = summary.results.filter((r) => r.tier === tier);
      if (tierResults.length === 0) return null;
      const pts = tierResults.reduce((sum, r) => sum + r.points, 0);
      return `  ${pad(tier, 10)} ${green(pts.toFixed(1))}/${tierResults.length}`;
    })
    .filter(Boolean)
    .join("\n");

  const sourceBreakdown = ["BPHS", "Phaladeepika", "Saravali"]
    .map((source) => {
      const srcResults = summary.results.filter((r) => r.source === source);
      if (srcResults.length === 0) return null;
      const pts = srcResults.reduce((sum, r) => sum + r.points, 0);
      const score = (pts / srcResults.length) * 100;
      return `  ${pad(source, 15)} ${bold(score.toFixed(1))}% (${pts.toFixed(1)}/${srcResults.length})`;
    })
    .filter(Boolean)
    .join("\n");

  return [
    "",
    dim("─".repeat(120)),
    "",
    bold(`  ${bench.name.toUpperCase()} SUMMARY`),
    "",
    `  ${bold("Weighted Score:")}       ${bold(cyan(`${weighted}%`))}  ${grade}`,
    `  ${bold("Exact Matches:")}        ${summary.exactMatches} / ${summary.totalCases} (${exact}%)`,
    `  ${bold("Total Points:")}         ${summary.totalPoints.toFixed(1)} / ${summary.totalCases}`,
    `  ${bold("Failures:")}             ${summary.failures > 0 ? red(String(summary.failures)) : green("0")}`,
    `  ${bold("Mean Abs. Delta:")}      ${summary.meanAbsoluteDelta.toFixed(2)}`,
    `  ${bold("Total Runtime:")}        ${summary.totalExecutionTimeMs}ms`,
    "",
    bold("  BY SOURCE"),
    sourceBreakdown || "  (Single Source Run)",
    "",
    bold("  BY TIER (Points)"),
    tierBreakdown,
    "",
    dim(`  Run started:   ${summary.startedAt}`),
    dim(`  Run completed: ${summary.completedAt}`),
    "",
    dim("─".repeat(120)),
    "",
  ].join("\n");
}

// ---------------------------------------------------------------------------
// CLI Banner
// ---------------------------------------------------------------------------

function renderBanner(bench: BenchmarkDefinition): void {
  const line = "═".repeat(50);
  process.stdout.write("\n");
  process.stdout.write(bold(cyan(`  ╔${line}╗\n`)));
  process.stdout.write(bold(cyan(`  ║${pad(" " + bench.name + " v1.1.0", 50)}║\n`)));
  process.stdout.write(bold(cyan(`  ║${pad(" " + bench.description, 50)}║\n`)));
  process.stdout.write(bold(cyan(`  ╚${line}╝\n`)));
  process.stdout.write("\n");
}

// ---------------------------------------------------------------------------
// Main Entry Point
// ---------------------------------------------------------------------------

async function main(): Promise<void> {
  const benchId = process.argv[2] || "combined";
  const bench = getBenchmark(benchId);

  if (!bench) {
    process.stderr.write(`\n${red("[ERROR]")} Unknown benchmark: ${benchId}\n`);
    process.stderr.write(`Available benchmarks: ${BENCHMARKS.map((b) => b.id).join(", ")}\n`);
    process.exit(1);
  }

  renderBanner(bench);

  const summary = await runBenchmark(bench.dataset);

  process.stdout.write(renderTableHeader() + "\n");
  for (const result of summary.results) {
    process.stdout.write(renderResultRow(result) + "\n");
  }

  process.stdout.write(renderSummary(summary, bench));

  if (summary.weightedScorePercent < 50) {
    process.exit(1);
  }
}

main().catch((err: unknown) => {
  const message = err instanceof Error ? err.message : String(err);
  process.stderr.write(`\n${red("[FATAL]")} Benchmark run aborted: ${message}\n`);
  process.exit(2);
});
