import { BPHS_BENCH_DATASET } from "./bphs/dataset.js";
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
];

export function getBenchmark(id: string): BenchmarkDefinition | undefined {
  return BENCHMARKS.find((b) => b.id === id);
}
