import { BPHS_BENCH_DATASET } from "./bphs/dataset.js";
import { SARAVALI_BENCH_DATASET } from "./saravali/dataset.js";
import { PHALADEEPIKA_BENCH_DATASET } from "./phaladeepika/dataset.js";
import { JAIMINI_BENCH_DATASET } from "./jaimini/dataset.js";
import { SYNTHESIS_BENCH_DATASET } from "./synthesis/dataset.js";
import type { TestCase } from "../types/index.js";

export interface BenchmarkDefinition {
  id: string;
  name: string;
  description: string;
  dataset: ReadonlyArray<TestCase>;
}

export const BENCHMARKS: BenchmarkDefinition[] = [
  {
    id: "bphs",
    name: "BPHS-Bench",
    description: "Brihat Parashara Hora Shastra Evaluation Suite",
    dataset: BPHS_BENCH_DATASET,
  },
  {
    id: "phaladeepika",
    name: "Phaladeepika-Bench",
    description: "Mantreswara's Phaladeepika Evaluation Suite",
    dataset: PHALADEEPIKA_BENCH_DATASET,
  },
  {
    id: "saravali",
    name: "Saravali-Bench",
    description: "Kalyana Varma's Saravali Evaluation Suite",
    dataset: SARAVALI_BENCH_DATASET,
  },
  {
    id: "jaimini",
    name: "Jaimini-Bench",
    description: "Jaimini Sutras Evaluation Suite",
    dataset: JAIMINI_BENCH_DATASET,
  },
  {
    id: "synthesis",
    name: "Synthesis-Bench",
    description: "Cross-paradigm Synthesis Evaluation (BPHS vs Jaimini)",
    dataset: SYNTHESIS_BENCH_DATASET,
  },
  {
    id: "combined",
    name: "Astro-Bench Suite",
    description: "Unified evaluation across all classical modules",
    dataset: [
      ...BPHS_BENCH_DATASET,
      ...PHALADEEPIKA_BENCH_DATASET,
      ...SARAVALI_BENCH_DATASET,
      ...JAIMINI_BENCH_DATASET,
      ...SYNTHESIS_BENCH_DATASET,
    ],
  },
];

export function getBenchmark(id: string): BenchmarkDefinition | undefined {
  return BENCHMARKS.find((b) => b.id === id);
}
