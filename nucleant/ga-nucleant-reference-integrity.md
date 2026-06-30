# Ga-nucleant manuscript — reference integrity report

Manuscript: **"Stability-filtered lattice matching for supercooling nucleants in gallium and its
low-melting alloys"** (ACS reformat).
Source file audited: **`artifacts/manuscripts/Stability-filtered lattice matching … (ACS-v2).docx`**
— the newest (2026-06-26 11:40) and most complete sibling: 20 references in ACS style, adds the
Materials Project / ICSD / NIST-JANAF / Vonnegut / Kelton-Greer / Einstein supporting citations and
a third author (Kristina Lilova). Five siblings exist:

| file | mtime | refs | note |
|---|---|---|---|
| (draft) | 06-15 20:36 | — | earliest |
| (refs-corrected) | 06-25 18:58 | 13 | bracket `[N]` style, terse data-availability line |
| (submission-ready) | 06-26 09:32 | 13 | **identical reference content to refs-corrected** (only the data-availability sentence differs); already incorporates the corrected refs |
| (ACS-v1) | 06-26 09:47 | ~20 | first ACS reformat |
| **(ACS-v2)** | **06-26 11:40** | **20** | **verified here** — newest, most complete, ACS numbering |

The "(submission-ready)" file the directive names is **older** than ACS-v2 and carries the
13-reference subset; ACS-v2 is the live target and the one verified. The 13 refs in
submission-ready are a strict subset of ACS-v2's 20 (same metadata), so this report covers both.

Verification method follows CLAUDE.md rule 6 / the reference-integrity checklist: every academic
reference's claimed authors / title / year / volume / first page diffed against the canonical
Crossref record by printed DOI. Tooling reused the assessment workspace's `verify_dois.py`
(`norm`, `clean_title`, full-author-list conflation `author_list_diff`), extended with volume and
first-page diffs — same script shape as `_work/verify_cooling_refs.py`. Gray literature (a
thermochemical-tables monograph, a textbook) has no journal-article Crossref record and is judged
editorially, not gated.

Run artifacts: `_work/verify_ganucleant_refs.py`, `_work/ganucleant_ref_verify_result.json`.

## Headline

- **The academic reference metadata is clean.** All 18 journal references resolve by their printed
  DOI to a real paper whose authors, title, year, volume, and first page match the canonical
  Crossref record. **No conflated author lists, no wrong initials, no dropped co-authors, no
  paraphrased titles** — the first-paper incident's failure modes are absent here. Every DOI is
  printed in the manuscript and every one resolves to the right paper.
- **One automated flag is a confirmed false positive** ([3] Majzlan): title ratio 0.68 only because
  Crossref's title embeds the formula parentheticals "(β-TeO₂), (α-TeO₂)" that the manuscript
  abbreviates. Authors (all six), year, volume, and first page match exactly. Not a defect.
- **The real problem is the body↔list linkage, not the metadata.** ACS-v2's prose carries
  essentially no in-text citation numbers: only **7 superscript numerals exist in the whole
  document, all inside Table 3** (refs 1, 4, 11, 12). The running text cites by author name
  ("Zhang and co-workers", "Chakravarty et al.") or by data-source name, with the ACS superscript
  callouts never inserted. As a result most references cannot be tied to a specific sentence, and
  two ([2] Niu, [3] Majzlan) have no in-text anchor of any kind — number, author name, or clear
  topical hook. This must be fixed before submission (details below). Same defect, milder, in the
  bracket-style siblings: submission-ready has explicit `[N]` callouts for only 4 of its 13 refs.
- Per rule 6, do **not** hand-edit the bibliography or type citation text. Use the verified
  **DOI add-list** (`ga-nucleant-reference-DOIs.tsv`) to add each item to Zotero by identifier,
  insert the in-text citations through the Zotero plugin, and regenerate the bibliography via CSL.

## Must-fix before submission

### 1. Insert the missing in-text citations (the body has almost none)
ACS journals use superscript numeric citations. In ACS-v2 those numbers appear **only in Table 3**;
the entire Introduction, Methods, and Results prose has none. Every claim that rests on a reference
needs its superscript callout inserted via the Zotero plugin so the list and text stay in sync.
The mapping below records where each reference belongs (verified by topical content):

| ref | belongs at (claim in text) | currently anchored? |
|---|---|---|
| 1 Zhang | measured 67.8 K supercooling; the five-nucleant ranking; 0.5 wt% loading | name + Table 3 (¹) |
| 2 Niu | **no in-text hook found** — homogeneous nucleation / ab-initio Ga value | **ORPHAN — cite or drop** |
| 3 Majzlan | TeO₂ thermodynamics behind the reduction energetics | **ORPHAN — cite or drop** |
| 4 Koh | Ga-In-Sn twin endotherm, liquidus 284 K | name + Table 3 (⁴) |
| 5 Turnbull | Turnbull driving force; bounded disregistry relation | name |
| 6 Bramfitt | carbide/nitride heterogeneous nucleation of iron | name |
| 7 Telkes | nucleation of supersaturated salt solutions | name |
| 8 Zinkevich | Ga-O assessment, the −665 kJ/mol O₂ gate line | topical ("665", "Ga2O3, minus") — no callout |
| 9 Gossé | Te-O phase relations, TeO₂→Ga₂O₃ reduction | topical ("reduces TeO₂") — no callout |
| 10 Joshipura | native-oxide / passivation supercooling | topical ("oxide skin", "passiv") — no callout |
| 11 Chakravarty | (010) nucleation plane, cubic carbide/nitride data | name + Table 3 (¹¹) |
| 12 Ki | porous Ga PCM, ZrN/HfC supercooling cut | name + Table 3 (¹²) |
| 13 Cao | silica-nanoparticle supercooling suppression | name |
| 14 Otis (pycalphad) | CALPHAD database solved with pycalphad | name |
| 15 Jain (Materials Project) | broad Materials Project query | name |
| 16 Bergerhoff (ICSD) | lattice parameters from ICSD | name |
| 17 Chase (NIST-JANAF) | formation energies from NIST-JANAF | name (gray lit) |
| 18 Vonnegut | bounded Turnbull-Vonnegut potency relation | name |
| 19 Kelton-Greer | classical nucleation theory background | topical — no callout (gray lit) |
| 20 Einstein | Einstein viscosity relation, +2.5–7.5% | name |

### 2. Resolve the two orphan references [2] and [3]
- **[2] Niu et al., "Ab initio phase diagram and nucleation of gallium," Nat. Commun. 11 (2020)
  2654** — verified real and correct, but no sentence in the body cites it (no author name, no
  number, no topical hook found). It is the natural citation for the homogeneous-nucleation /
  ab-initio context. Add an in-text citation at that claim, or drop it from the list.
- **[3] Majzlan et al., "Thermodynamic properties of tellurite, paratellurite, TeO₂ glass and
  Te(IV) phases," Geochemistry 82 (2022) 125915** — verified real and correct; it underpins the
  TeO₂ reduction energetics but is never explicitly invoked. Cite it where the −1184 kJ TeO₂→Ga₂O₃
  reaction energetics are stated, or drop it.

Decide per item in Zotero (insert the citation, then refresh) so the numbering stays consistent —
do not renumber by hand.

## Advisory

- **[13] Cao initials differ between siblings.** ACS-v2 prints "Cao, L.; Park, H.; … Ono, K.";
  the bracket siblings printed "Y. Cao, J. Park, … T. Ono". Crossref gives first names —
  **Liya Cao, Hyunjin Park, … Kazuki Ono** — i.e. the ACS-v2 initials (L., H., K.) are the correct
  ones and the older "Y. Cao / J. Park / T. Ono" were wrong. ACS-v2 already fixed this; just
  confirm when adding by DOI that Zotero pulls the Crossref initials.
- **[3] Majzlan title.** Keep the manuscript's short form or expand to Crossref's
  "…tellurite (β-TeO₂), paratellurite (α-TeO₂), TeO₂ glass, and Te(IV) phases" — either renders
  fine; the abbreviation is faithful, not a paraphrase. Protect the formula subscripts/Greek with
  `<sub>`/nocase spans in the CSL output.
- **Title-case / formula protection.** Several titles carry chemical subscripts and Greek
  (TeO₂, β-/α-, Ga₂O₃, Molekuldimensionen→Moleküldimensionen umlaut in [20]). When the bibliography
  is generated, verify the CSL output preserves subscripts and the umlaut.
- **[9] Gossé accent.** Crossref's author family is "Gossé"; ensure Zotero keeps the acute accent
  (the manuscript already has it).

## Per-reference verdict (academic items)

All 18 resolved by printed DOI and metadata-clean. The lone automated flag ([3]) is a
title-tokenization false positive (formula parentheticals in the Crossref title), hand-confirmed
correct on authors / year / volume / page.

| Ref | Verdict | Printed DOI (resolves, canonical) |
|---|---|---|
| 1 | OK | 10.1016/j.ijheatmasstransfer.2019.119055 |
| 2 | OK metadata — **ORPHAN in text** | 10.1038/s41467-020-16372-9 |
| 3 | OK (title flag = false positive) — **ORPHAN in text** | 10.1016/j.chemer.2022.125915 |
| 4 | OK | 10.1016/j.mtla.2019.100512 |
| 5 | OK | 10.1063/1.1699435 |
| 6 | OK | 10.1007/bf02642799 |
| 7 | OK | 10.1021/ie50510a036 |
| 8 | OK | 10.1111/j.1551-2916.2004.00683.x |
| 9 | OK | 10.1007/s11669-025-01175-6 |
| 10 | OK | 10.1016/j.isci.2023.106493 |
| 11 | OK | 10.1063/5.0060207 |
| 12 | OK | 10.1002/advs.202310185 |
| 13 | OK (ACS-v2 initials correct; see Advisory) | 10.1063/1.3645596 |
| 14 | OK | 10.5334/jors.140 |
| 15 | OK | 10.1063/1.4812323 |
| 16 | OK | 10.1021/ci00038a003 |
| 18 | OK | 10.1063/1.1697813 |
| 20 | OK | 10.1002/andp.19063240204 |

## Gray literature (not gated — judged editorially)

| Ref | Item | Verdict |
|---|---|---|
| 17 | Chase, NIST-JANAF Thermochemical Tables, 4th ed.; J. Phys. Chem. Ref. Data Monograph 9; AIP, 1998 | Standard data monograph; no per-volume article DOI. Acceptable; enter in Zotero by hand (book/monograph) with full fields. |
| 19 | Kelton & Greer, *Nucleation in Condensed Matter*; Pergamon Materials Series Vol. 15, 2010; ISBN 978-0-08-042147-6 | Textbook; no Crossref article record. Acceptable. **Currently has no in-text callout** — cite it at the classical-nucleation-theory background or drop. |

## Citation-placement / list bugs found by inspection (metadata diff can't see these)

- **No truncation.** No in-text citation number exceeds the list length in either version (max
  callout 12 ≤ 20 in ACS-v2; 13 ≤ 13 in submission-ready). Nothing cited points past the list.
- **Orphans:** [2] Niu and [3] Majzlan are in the list but never cited in the body by number,
  name, or clear topical hook (see Must-fix §2). [19] Kelton-Greer is cited only by topic, no
  explicit callout.
- **Systemic under-citation (the main bug):** the ACS-v2 body is missing its superscript citation
  numbers almost entirely — only 4 distinct refs (1, 4, 11, 12) are numerically anchored, all in
  Table 3. This is a reformatting gap from the bracket→ACS conversion, not a metadata error, but it
  blocks a clean list↔text reconciliation and must be completed in Zotero before submission.

## Remaining "finish it" gaps (not references)

- Confirm ACS-v2 is the intended submission target over submission-ready (different author list —
  ACS-v2 adds Kristina Lilova — and different section structure: ACS-v2 merges Methods into
  Results). The reference work here applies to whichever is chosen.
- After inserting the in-text citations, re-run `verify_dois.py --zotero-api` over the group library
  once these 18 DOIs are added, to confirm the CSL-rendered fields still match Crossref.
