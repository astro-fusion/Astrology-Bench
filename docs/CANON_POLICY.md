# Canon policy

The canon is the set of classical passages that Level 2 gold is allowed to cite.
It lives in `canon/REGISTRY.yaml` (texts and editions) and `canon/<text>.yaml`
(entries). This page says what may enter it and how it is used.

## Why citations must be verifiable

Astro-Bench scores whether a model cites classical Vedic texts accurately and
whether it abstains when it cannot. A gold citation that someone typed from memory
would reward the same failure the benchmark exists to catch: a confident
chapter-and-verse that nobody checked. So every gold citation is a passage that a
named person (or agent) read at a public URL and copied. No chapter or verse number
enters the canon from memory.

## Edition pinning

Chapter and verse numbers differ between translations of the same text. The
registry therefore pins one edition per text (`edition_id`), and every entry and
every model citation is read against that edition.

- **BPHS is pinned to R. Santhanam (Ranjan Publications).** Santhanam and G. C.
  Sharma number chapters differently, so a model that cites "Chapter 36" from the
  Sharma edition can be correct about the text and wrong against this canon.
  Santhanam has 97 chapters, and verse headings such as `3-4. GAJA KESARI YOGA`
  give the verse range used here. Entries for other BPHS editions are accepted only
  by adding that edition to the registry with its own verified entries.
- Brihat Jataka is Iyer (Aiyar) 2nd edition, 1905, 28 chapters. Brihat Samhita is
  Iyer 1884 on wisdomlib, 106 chapters. Phaladeepika is Sastri 2nd edition, 1950,
  28 adhyayas. Saravali is Santhanam, 55 chapters in the archive.org scan.
- Jaimini Sutras is Suryanarain Rao. The archive.org scan holds Part 1 only
  (Adhyayas 1 and 2), so entries cite `chapter` = adhyaya and `verse` =
  `pada.sutra` (for example `1.29`, `4.1`). Adhyayas 3 and 4 are unverified.
- Quotes are taken from the text as scanned. Archive.org full text is OCR, so a
  quote can carry a scan typo (for example "old sign" for "odd sign" in BPHS
  6.5-6). Entries were chosen to avoid garbled passages, and a test should compare
  quotes after whitespace normalisation only.

## Verified statuses

| Status | Meaning | May be used for |
|---|---|---|
| `quoted` | The entry's author read the passage at `url` and the quote is a verbatim substring of it | Level 2 gold; accepted citation |
| `paraphrased` | Only a secondary source (commentary, article, note) was found | Never gold. Review queue and `also_in` leads only |
| `untraced` | No passage found after searching the registry texts | Recorded so the rule is generated as `source: modern`; never citation-graded |

`untraced` rules appear in an `untraced:` list in the text file that was searched.
A finding of "no classical verse exists" is valid: Kala Sarpa yoga does not occur in
the scanned BPHS, Brihat Jataka, Phaladeepika, Saravali or Jaimini text.

## Quote length and fair use

A quote is at most 40 words. It must be contiguous, may start or end mid-sentence,
and must not use ellipses to join separated text. The limit keeps the canon a pointer
to the source, not a copy of it; the translations of BPHS, Phaladeepika, Saravali and
Jaimini Sutras are in copyright or of unclear status, and short quotation for
verification and criticism is the only use made of them. Public-domain texts are
marked `public_domain: true` in the registry.

## Adding an entry

Open a pull request that adds one entry to `canon/<text>.yaml` with:

1. `chapter` and `verse` in the pinned edition, as strings (ranges such as `3-5` allowed);
2. `quote`, copied from the page at `url`, 40 words or fewer;
3. `url` where a reviewer can read the page, never a search result or a paywalled page;
4. `rule_key` from the generator list (or a new snake_case key explained in the PR);
5. `verified: quoted` only if you read the quote there, otherwise `paraphrased` or `untraced`;
6. `verified_by` and `verified_at`.

The reviewer opens the URL and checks the quote and the chapter heading. One entry may
carry several `rule_keys` when a single verse states several rules (for example
Sunapha, Anapha and Durudhara); `rule_key` is the first of them.

## Disputes between translations

Where two texts state the same rule, list the other as `also_in` (text, chapter,
verse). The scorer accepts any `also_in` locus as a correct citation. Where they
disagree on content, say how in a `dispute` note on the entry and keep both loci.
Disputes found while building this canon include:

- Gaja Kesari: BPHS (Santhanam 36.3-4) allows an angle from the ascendant or the
  Moon and excludes debilitation, combustion and inimical sign; the common
  definition (Jataka Parijata, called Kesari yoga in Phaladeepika 6.14 per
  Santhanam's note) is Jupiter in a kendra from the Moon alone.
- Kemadruma: the cancelling conditions differ between BPHS 37.11-13, Brihat Jataka
  13.3 and Saravali 13.2.
- Brihat Jataka 1.13: the stanza gives Mars at 28 degrees, Iyer's table note prints 29.
- Brihat Jataka counts 31 kinds each of Sunapha and Anapha; Saravali 13.3 counts 30.
- Phaladeepika (Sastri) 4.4-5 says retrograde planets are strong, even in depression.
  The popular rule that an exalted retrograde planet acts as debilitated was not
  found at the cited place; three legacy items are flagged for it.

## Fabrication penalty

A citation scores +1 when it matches a gold entry or an `also_in` locus (text and
chapter, verse when gold has one), 0 when `citations` is empty, and -1 when it names
a text not in the registry, a chapter beyond the registry's chapter count, or a real
locus that does not support the claim. The share of items with any -1 is reported as
the fabricated-citation rate.

Abstaining scores 0 and guessing risks -1, so a model that cannot cite should say so.
A confident wrong chapter is worse than a blank, because a reader who trusts it will
not check, and a blank at least tells the reader to look.
