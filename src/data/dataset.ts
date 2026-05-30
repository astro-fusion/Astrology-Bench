/**
 * @file src/data/dataset.ts
 * @description The 10 immutable gold-standard BPHS-Bench test cases.
 *
 * These cases span four difficulty tiers (EASY → VERY_HARD) and cover
 * canonical Vedic astrological interpretation rules from Brihat Parashara
 * Hora Shastra. Each gold score is derived from strict BPHS text analysis
 * and must never be modified without peer review and rule citation.
 *
 * Tier breakdown:
 *  - EASY      (TC-EASY-01, TC-EASY-02):   Direct lordship, single-dimension
 *  - MEDIUM    (TC-MED-03  → TC-MED-05):   Parivartana, Varga traps, combustion
 *  - HARD      (TC-HARD-06 → TC-HARD-08):  Vipareeta Yoga, Varga subversion
 *  - VERY_HARD (TC-VHARD-09, TC-VHARD-10): Dialectical contradictions, timing windows
 */

import type { TestCase } from "../types/index.js";

// ---------------------------------------------------------------------------
// EASY TIER — Direct, single-dimension BPHS interpretation
// ---------------------------------------------------------------------------

/**
 * TC-EASY-01 | Career Growth Baseline
 *
 * BPHS Rule Chain:
 *  - 10th lord Mars in own sign (Aries) in the 10th house → pinnacle of Karma Bhava strength.
 *  - Jupiter aspects the 10th house from the 2nd → adds Dhana + wisdom to career.
 *  - Active Mars Mahadasha → 10th lord period in force.
 *  - 34 bindus in 10th house → well above the 25-bindu strength threshold.
 * Verdict: Unambiguously excellent. Gold Score = 5.
 */
const TC_EASY_01: TestCase = {
  id: "TC-EASY-01",
  tier: "EASY",
  topic: "Career Growth Baseline",
  prompt:
    "On a scale of 1 to 5, how steady will my career growth be over the next few years? Reply with only a number.",
  goldScore: 5,
  chartState: {
    ascendant: "Cancer",
    "10th_house_sign": "Aries",
    "10th_lord": "Mars in Aries (Own Sign, 10th house)",
    "10th_house_aspects": "Jupiter aspect from 2nd house (Leo)",
    current_dasha: "Mars Mahadasha",
    ashtakavarga_10th_house_bindus: 34,
  },
};

/**
 * TC-EASY-02 | Marriage Promise Baseline
 *
 * BPHS Rule Chain:
 *  - 7th lord Venus debilitated in Virgo (11th house) → Vivaha Bhava lord fallen.
 *  - Saturn + Rahu in 7th house → Kalatra Bhava severely afflicted (Rahu causes chaos,
 *    Saturn delays/denies).
 *  - 19 bindus → critically below the 25-bindu minimum; 7th house is starved of strength.
 * Verdict: Highly inauspicious for marriage. Gold Score = 1.
 */
const TC_EASY_02: TestCase = {
  id: "TC-EASY-02",
  tier: "EASY",
  topic: "Marriage Promise Baseline",
  prompt:
    "Rate my chances of a harmonious, long-lasting marriage on a scale of 1 to 5. Reply with only a number.",
  goldScore: 1,
  chartState: {
    ascendant: "Scorpio",
    "7th_house_sign": "Taurus",
    "7th_lord": "Venus in Virgo (Debilitated, 11th house)",
    "7th_house_planets": ["Saturn", "Rahu"],
    ashtakavarga_7th_house_bindus: 19,
  },
};

// ---------------------------------------------------------------------------
// MEDIUM TIER — Multi-factor, Parivartana & Varga analysis required
// ---------------------------------------------------------------------------

/**
 * TC-MED-03 | Wealth Stability vs. Bindu Capacity
 *
 * BPHS Rule Chain:
 *  - Parivartana Yoga between 2nd lord Mercury (debilitated in Pisces/11th) and
 *    11th lord Jupiter (in Gemini/2nd) → exchange partially cancels debilitation
 *    via Neecha Bhanga but weakens both bhava lords simultaneously.
 *  - 21 bindus in 2nd house + 22 bindus in 11th house → both below 25; structural
 *    capacity for wealth is limited despite the exchange.
 *  - Jupiter Mahadasha → general expansion but Mercury's debility leaks into gains.
 * Verdict: Mixed — exchange yoga brings moderate opportunity, bindu shortfall
 *          limits sustained accumulation. Gold Score = 3.
 */
const TC_MED_03: TestCase = {
  id: "TC-MED-03",
  tier: "MEDIUM",
  topic: "Wealth Stability vs. Bindu Capacity",
  prompt:
    "How likely am I to build and keep long-term wealth? Rate 1 to 5. Reply with only a number.",
  goldScore: 3,
  chartState: {
    ascendant: "Taurus",
    "2nd_house_sign": "Gemini",
    "11th_house_sign": "Pisces",
    "2nd_lord": "Mercury in Pisces (11th house, Debilitated)",
    "11th_lord": "Jupiter in Gemini (2nd house)",
    parivartana_yoga: "2nd and 11th lords exchange houses",
    ashtakavarga_2nd_house_bindus: 21,
    ashtakavarga_11th_house_bindus: 22,
    current_dasha: "Jupiter Mahadasha",
  },
};

/**
 * TC-MED-04 | Children & Legacy Varga Trap
 *
 * BPHS Rule Chain:
 *  - D1: 5th lord Venus exalted in Cancer (10th house), Jupiter karaka exalted
 *    in Cancer (2nd house) → looks very auspicious on the surface.
 *  - D5 (Panchamsha – the divisional chart of children and dharma):
 *    Venus debilitated in Virgo and Jupiter placed in 8th house of D5 → the
 *    Varga chart overrides surface-level promise; children signification is damaged.
 *  - Venus Mahadasha → Mahadasha lord is debilitated in the children-specific varga.
 * Verdict: The Varga trap downgrades an apparent 5 to a 2. Gold Score = 2.
 */
const TC_MED_04: TestCase = {
  id: "TC-MED-04",
  tier: "MEDIUM",
  topic: "Children & Legacy Varga Trap",
  prompt:
    "Rate how smoothly I can expect my journey to parenthood to go, 1 to 5. Reply with only a number.",
  goldScore: 2,
  chartState: {
    ascendant: "Gemini",
    "5th_house_sign": "Libra",
    D1_5th_lord: "Venus in Pisces (Exalted, 10th house)",
    D1_jupiter_karaka: "Exalted in Cancer (2nd house)",
    D5_panchamsha_5th_lord: "Venus in Virgo (Debilitated in D5)",
    D5_jupiter_karaka: "Placed in the 8th house of D5",
    current_dasha: "Venus Mahadasha",
  },
};

/**
 * TC-MED-05 | Public Recognition Combustion Filter
 *
 * BPHS Rule Chain:
 *  - 10th lord Mercury in Leo (9th house) conjunct 9th lord Sun within 0.5° →
 *    Mercury is combust (within combustion orb of the Sun).
 *  - Combustion (Moudyami) strips Mercury of its independent Kendra-Kona signification.
 *  - Active Mercury Mahadasha → the combust Mahadasha lord cannot deliver fame.
 *  - 9th house placement suggests bhagya (fortune) but combustion neutralises it.
 * Verdict: Surface promise blocked by combustion. Gold Score = 2.
 */
const TC_MED_05: TestCase = {
  id: "TC-MED-05",
  tier: "MEDIUM",
  topic: "Public Recognition Combustion Filter",
  prompt:
    "How likely am I to gain public recognition or fame in my field? 1 to 5. Reply with only a number.",
  goldScore: 2,
  chartState: {
    ascendant: "Sagittarius",
    "10th_house_sign": "Virgo",
    "10th_lord": "Mercury in Leo (9th house)",
    "9th_lord": "Sun in Leo (9th house)",
    planetary_conjunction: "Mercury is within 0.5 degrees of the Sun",
    current_dasha: "Mercury Mahadasha",
  },
};

// ---------------------------------------------------------------------------
// HARD TIER — Vipareeta Yoga, Varga subversion, multi-factor contradictions
// ---------------------------------------------------------------------------

/**
 * TC-HARD-06 | Relationship Longevity Varga Subversion
 *
 * BPHS Rule Chain:
 *  - D1: 7th lord Venus exalted in Pisces (12th house) → exalted but in 12th
 *    (Vyaya Bhava); marriage partner connected to loss/foreign/dissolution themes.
 *  - D9 (Navamsha – the varga for marriage quality):
 *    Venus debilitated in Virgo in D9 → the marriage chart reveals the inner
 *    reality: the relationship quality is compromised despite D1 exaltation.
 *  - 17 bindus in 7th house → dangerously below strength minimum.
 *  - Venus Mahadasha → Mahadasha lord reveals D9 weakness.
 * Verdict: D9 subversion + bindu starvation. Gold Score = 2.
 */
const TC_HARD_06: TestCase = {
  id: "TC-HARD-06",
  tier: "HARD",
  topic: "Relationship Longevity Varga Subversion",
  prompt:
    "Rate my marriage prospects for stability and happiness, 1 to 5. Reply with only a number.",
  goldScore: 2,
  chartState: {
    ascendant: "Aries",
    "7th_house_sign": "Libra",
    D1_7th_lord: "Venus in Pisces (Exalted, 12th house)",
    D9_navamsha_7th_lord: "Venus in Virgo (Debilitated in D9)",
    ashtakavarga_7th_house_bindus: 17,
    current_dasha: "Venus Mahadasha",
  },
};

/**
 * TC-HARD-07 | Business Success Vipareeta Evaluation
 *
 * BPHS Rule Chain:
 *  - Saturn (6th lord) debilitated in Aries in 8th house → Harsha Yoga component:
 *    6th lord in 8th house is a Vipareeta Raja Yoga (adversity becomes strength).
 *  - Mars (8th lord) in Aquarius in 6th house → Sarala Yoga component:
 *    8th lord in 6th house is another Vipareeta configuration.
 *  - Together they form Harsha + Sarala combination → protects from adversity,
 *    gives resilience, but Shadbala of Mars = 0.85 (below 1.0 minimum) →
 *    Yoga is partially functional.
 *  - Mars Mahadasha → activates the Vipareeta yogas but weakly (Shadbala deficit).
 * Verdict: Moderate — Vipareeta provides resilience but Shadbala deficit limits
 *          explosive success. Gold Score = 3.
 */
const TC_HARD_07: TestCase = {
  id: "TC-HARD-07",
  tier: "HARD",
  topic: "Business Success Vipareeta Evaluation",
  prompt:
    "Rate my potential for successful, self-sustaining business wealth, 1 to 5. Reply with only a number.",
  goldScore: 3,
  chartState: {
    ascendant: "Virgo",
    "6th_lord": "Saturn in Aries (8th house, Debilitated)",
    "8th_lord": "Mars in Aquarius (6th house)",
    mutual_exchange: "6th and 8th lords exchange houses (Harsha/Sarala Yoga)",
    shadbala_mars: 0.85,
    current_dasha: "Mars Mahadasha",
  },
};

/**
 * TC-HARD-08 | Physical Vitality & Resilience
 *
 * BPHS Rule Chain:
 *  - 1st lord Moon in Gemini (12th house) → Lagna lord in Vyaya Bhava; vitality
 *    leaks away, body is in a chronically weakened state.
 *  - 8th lord Saturn in Sagittarius (6th house) → Saturn's full 7th aspect
 *    falls directly onto the 12th house Moon → the longevity indicator (8th lord)
 *    afflicts the vitality indicator (1st lord).
 *  - Moon is in Weak New Moon (Krishna Paksha, near Amavasya) → Paksha Bala
 *    is at its lowest; Moon loses additional functional strength.
 *  - Saturn Mahadasha → the health-afflicting planet is in full period.
 * Verdict: Seriously challenged vitality on three simultaneous axes. Gold Score = 2.
 */
const TC_HARD_08: TestCase = {
  id: "TC-HARD-08",
  tier: "HARD",
  topic: "Physical Vitality & Resilience",
  prompt:
    "Rate my overall physical resilience and health stability, 1 to 5. Reply with only a number.",
  goldScore: 2,
  chartState: {
    ascendant: "Cancer",
    "1st_lord": "Moon in Gemini (12th house)",
    "8th_lord": "Saturn in Sagittarius (6th house, aspects 12th house Moon)",
    moon_paksha_bala: "Weak New Moon phase",
    current_dasha: "Saturn Mahadasha",
  },
};

// ---------------------------------------------------------------------------
// VERY HARD TIER — Dialectical contradictions, nested timing windows
// ---------------------------------------------------------------------------

/**
 * TC-VHARD-09 | Financial Windfall Blocked Timing Window
 *
 * BPHS Rule Chain:
 *  - 9th lord (Bhagya/fortune) Mars debilitated in Cancer (12th house, Leo lagna) →
 *    fortune is eroded and cast into the house of loss.
 *  - Neecha Bhanga is technically active (dispositor Moon is in Kendra from Lagna)
 *    → cancellation partially applies, but does NOT fully restore fortune timing.
 *  - Pratyantar Dasha lord Mercury retrograde and debilitated in Pisces (8th house) →
 *    the operating sub-sub period lord is both retrograde and fallen in a Dusthana;
 *    timing window is blocked.
 *  - Saturn transiting exactly over natal Moon degree → gochara Saturn pressing on
 *    the emotional core and dispositor of the Neecha Bhanga; outcome is frozen.
 *  - 20 bindus in 2nd house → wealth house below strength threshold.
 * Verdict: Neecha Bhanga exists on paper but timing is blocked on four levels.
 *          Gold Score = 1.
 */
const TC_VHARD_09: TestCase = {
  id: "TC-VHARD-09",
  tier: "VERY_HARD",
  topic: "Financial Windfall Blocked Timing Window",
  prompt:
    "Rate my chances of a major financial windfall or inheritance in the next 18 months, 1 to 5. Reply with only a number.",
  goldScore: 1,
  chartState: {
    ascendant: "Leo",
    "9th_lord": "Mars in Cancer (12th house, Debilitated)",
    dispositor_state: "Moon is in Scorpio (Kendra from Lagna)",
    neecha_bhanga: "Active via dispositor placement",
    current_pratyantar_dasha_lord: "Mercury retrograde in Pisces (8th house, Debilitated)",
    transit_state: "Saturn transiting exactly over natal Moon degree",
    ashtakavarga_2nd_house_bindus: 20,
  },
};

/**
 * TC-VHARD-10 | Relationship Peace Dialectical Contradiction
 *
 * BPHS Rule Chain:
 *  - D1: 7th lord Sun debilitated in Libra (9th house) → Vivaha lord is fallen.
 *  - D9: Sun exalted in Aries in the Navamsha → inner marriage reality is
 *    surprisingly strong; contradicts D1 surface weakness.
 *  - Upapada Lagna in Scorpio with Rahu + Mars → Upapada (external marriage
 *    quality indicator) is turbulent and Mars/Rahu inflict intensity/conflict.
 *  - Rahu Mahadasha → amplifies the contradictions; Rahu expands both the
 *    D9 exaltation promise AND the Upapada affliction unpredictably.
 * Verdict: Dialectical contradiction — one varga supports, another afflicts;
 *          Rahu amplifies uncertainty. Neither strongly good nor bad. Gold Score = 3.
 */
const TC_VHARD_10: TestCase = {
  id: "TC-VHARD-10",
  tier: "VERY_HARD",
  topic: "Relationship Peace Dialectical Contradiction",
  prompt:
    "Rate the long-term emotional peace and compatibility in my primary relationship, 1 to 5. Reply with only a number.",
  goldScore: 3,
  chartState: {
    ascendant: "Aquarius",
    "7th_lord": "Sun in Libra (9th house, Debilitated)",
    upapada_lagna_sign: "Scorpio",
    upapada_lagna_planets: ["Rahu", "Mars"],
    D9_navamsha_7th_lord: "Sun in Aries (Exalted in D9)",
    current_dasha: "Rahu Mahadasha",
  },
};

// ---------------------------------------------------------------------------
// Exported Dataset
// ---------------------------------------------------------------------------

/**
 * The complete BPHS-Bench golden dataset.
 *
 * Order is preserved: EASY → MEDIUM → HARD → VERY_HARD.
 * This array is the single source of truth for all benchmark runs.
 * Do NOT mutate at runtime.
 */
export const BPHS_BENCH_DATASET: ReadonlyArray<TestCase> = Object.freeze([
  TC_EASY_01,
  TC_EASY_02,
  TC_MED_03,
  TC_MED_04,
  TC_MED_05,
  TC_HARD_06,
  TC_HARD_07,
  TC_HARD_08,
  TC_VHARD_09,
  TC_VHARD_10,
]);
