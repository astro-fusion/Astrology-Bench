/**
 * @file src/benchmarks/jaimini/dataset.ts
 * @description Test cases derived from Jaimini Sutras focusing on Chara Karakas and Rasi Drishti.
 */

import type { TestCase } from "../../types/index.js";

const JAI_01: TestCase = {
  id: "JAI-01",
  source: "Jaimini",
  tier: "HARD",
  topic: "Career Potential (Amatyakaraka)",
  prompt: "Using strictly Jaimini Sutras, rate my career potential from 1 to 5.",
  goldScore: 5,
  logic: "The 10th lord is debilitated (bad in BPHS), but the Amatyakaraka (career planet) is exalted in Navamsha and aspected by Atmakaraka via Rasi Drishti.",
  reference: { book: "Jaimini Sutras", chapter: "2", verse: "1" },
  tags: ["career", "chara_karaka", "rasi_drishti"],
  chartState: {
    ascendant: "Leo",
    "10th_lord": "Venus in Virgo (Debilitated)",
    atmakaraka: "Sun in Aries",
    amatyakaraka: "Jupiter in Cancer (Exalted in D9)",
    rasi_drishti: "Atmakaraka aspects Amatyakaraka",
  },
};

export const JAIMINI_BENCH_DATASET: ReadonlyArray<TestCase> = Object.freeze([
  JAI_01,
]);
