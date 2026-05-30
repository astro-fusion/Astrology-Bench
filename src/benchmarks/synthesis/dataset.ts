/**
 * @file src/benchmarks/synthesis/dataset.ts
 * @description Test cases for Cross-paradigm synthesis (BPHS vs Jaimini).
 */

import type { TestCase } from "../../types/index.js";

const SYN_01: TestCase = {
  id: "SYN-01",
  source: "Synthesis",
  tier: "VERY_HARD",
  topic: "Relationship Potential (BPHS vs Jaimini)",
  prompt: "Analyze my relationship potential. Rate it on a scale of 1 to 5. You must synthesize both Parashari structural rules and Jaimini Chara Karaka principles.",
  goldScore: 3,
  logic: "BPHS View: 7th lord in 8th, Venus combust (Score 1). Jaimini View: Darakaraka exalted conjunct Upapada Lagna in Kendra (Score 5). Synthesis: Conflicting systems yield a mixed/unconventional result (Score 3).",
  reference: { book: "Synthesis", chapter: "Mixed", verse: "N/A" },
  tags: ["marriage", "synthesis", "dialectical_contradiction"],
  chartState: {
    ascendant: "Aries",
    "7th_lord": "Venus in Scorpio (8th house, Combust)",
    darakaraka: "Jupiter in Cancer (Exalted)",
    upapada_lagna: "Cancer (4th house)",
    conjunctions: "Darakaraka conjunct Upapada Lagna",
  },
};

export const SYNTHESIS_BENCH_DATASET: ReadonlyArray<TestCase> = Object.freeze([
  SYN_01,
]);
