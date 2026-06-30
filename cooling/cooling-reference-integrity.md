# Cooling manuscript — reference integrity report

Manuscript: **"Materials Design for Compute Thermal Management: From Dielectric Fluids to
Gallium Based Cooling Systems"**, Energy (Elsevier) reframe.
Source file audited: `Downloads/BUF6EC_1.DOC` (the Energy version, ~7.2k words, 46 references,
internal date 2026-06-09). Downloaded with three siblings: `BUSTAM_2 (2).DOC` (RSER preprint v3),
`RSER_R_1.DOC` (resubmission strategy note), `COMPUT_1.DOC` (CALPHAD methods addendum).

Verification method follows CLAUDE.md rule 6 / the reference-integrity checklist: every academic
reference's claimed authors / title / year / volume / first page diffed against the canonical
Crossref record (by printed DOI where given, else by bibliographic search). Tooling reused the
assessment workspace's `verify_dois.py` (full author-list conflation diff + DataCite fallback),
extended here with volume and first-page diffs. Gray literature (datasheets, news, market reports,
government notices) has no Crossref record and is judged editorially, not by this gate.

Run artifacts: `_work/verify_cooling_refs.py`, `_work/ref_verify_result.json`.

## Headline

- The **academic reference metadata is clean**: every journal/conference reference resolves to a
  real paper whose authors, title, year, volume, and first page match the canonical record. No
  conflated author lists, no wrong initials, no paraphrased titles (the failure modes from the
  first-paper incident are absent here).
- **One academic reference must be replaced** ([20], no authors, does not resolve) — a verified
  real substitute is identified below.
- **Three citation-placement / list bugs** the metadata check cannot see, found by inspection:
  a missing Olson reference, a misplaced Dublin-AWS citation, and three uncited references.
- Per rule 6, do **not** hand-edit the bibliography. Use the verified **DOI add-list**
  (`cooling-reference-DOIs.tsv`) to add each item to Zotero by identifier, then regenerate the
  bibliography via CSL. The fixes below are specified so they can be made in Zotero + the document,
  not pasted as LLM-authored citation text.

## Must-fix before submission

### 1. Reference [20] does not resolve — replace it
Printed as: *"Optimization of Ga-based liquid metal thermal interface materials," Int. J. Heat
Mass Transfer, 2024.* No authors, no volume/page. Crossref has no paper matching this title in
IJHMT 2024; the closest hit is an unrelated 2021 SMTA conference paper (title ratio 0.75). This is
the one reference that reads as the directive's risk pattern (a plausible-sounding journal article
with no verifiable record).

**Verified replacement** (matches the in-text claim that LM-TIM conductivity is ~29.6–38.5 W/m·K,
IJHMT 2024):
> Y. Yan, Y. Zhuang, H. Ouyang, J. Hao, X. Han, "Experimental investigation on optimization of the
> performance of gallium-based liquid metal with high thermal conductivity as thermal interface
> material for efficient electronic cooling," International Journal of Heat and Mass Transfer,
> vol. 226 (2024) 125455. doi:10.1016/j.ijheatmasstransfer.2024.125455

Confirm the 29.6–38.5 W/m·K figures against this paper when you have the PDF; if they came from a
different source, cite that source instead.

### 2. Missing Olson reference (citation [37] is mislabeled)
The text attributes the process–structure–property–performance paradigm to **"Olson [37]"**
(Introduction, and again in the Conclusion), but reference **[37] is Rajagopal et al.** (the
materials-to-device heat-exchanger-tube paper), which is correctly cited for the separate
"materials-to-device" point at the end of the same Introduction paragraph. Olson's paper is not in
the list at all.

**Fix:** add Olson and point the paradigm sentences at it; keep [37] = Rajagopal for the
materials-to-device sentence.
> G. B. Olson, "Computational Design of Hierarchically Structured Materials," Science, vol. 277,
> no. 5330 (1997) 1237–1242. doi:10.1126/science.277.5330.1237

### 3. Dublin-AWS sentence cites the wrong reference
Introduction: *"In Dublin, students … heated by waste heat from an Amazon Web Services data
center [12]."* Reference **[12] is the ECHA PFAS/REACH restriction** (correctly used later for the
PFAS sentence). The Dublin deployment is reference **[15]** ("AWS data center heats Dublin
university campus," CNBC, 2026, with the TU Dublin 704 tCO2 measurement). Change this `[12]` to
`[15]`.

### 4. Uncited references — cite or drop
- **[16]** EnergiRaven / Viegand Maagoe (waste-heat potential) — never cited.
- **[17]** U.S. EPA NSPS combustion standard — never cited.
- **[32]** PRC Ministry of Commerce export-control announcement — never cited, and it duplicates
  the topic of the export-control sentence that currently cites **[27]** (USGS Gallium). Either cite
  [32] at "In July 2023, China … imposed export controls" or drop it and keep [27].

Decide per item: give it an in-text citation, or remove it. Do the renumbering in Zotero so the
in-text fields and the list stay in sync (rule 6) — do not renumber by hand.

## Advisory

- **Canonical DOIs for [43] and [45].** Both are correct in the manuscript (pycalphad, JORS 5
  (2017) 1; ESPEI, MRS Communications 9 (2019) 618). When adding to Zotero, use the canonical
  journal DOIs — `10.5334/jors.140` and `10.1557/mrc.2019.59` — not the 2024 book-chapter reprints
  that a title search surfaces first.
- **Reference [37] author list.** Crossref lists 11 authors ending at Miljkovic; the manuscript adds
  Sinha as a 12th. Sinha is plausibly a real co-author the Crossref record omits; confirm against
  the paper and keep or drop to match.
- **Gray-literature references have no DOI** and cannot go through Zotero add-by-identifier:
  [1]–[18] (minus the academic [19]... none in that block), [21], [25], [27], [32]. These are
  market reports, datasheets, news items, and agency documents. They are acceptable for the claims
  they support, but two are weak trade sources worth strengthening if a peer-reviewed equivalent
  exists: **[21]** (Patsnap/Eureka technical review) and **[25]** (360iResearch market report).
  Enter these in Zotero by hand with full, accurate fields (publisher, date, URL, access date).
- **Energy (Elsevier) wants DOIs on all references.** The TSV gives a verified DOI for every
  academic item; add them so the CSL output carries them.

## Per-reference verdict (academic items)

All resolved and metadata-clean unless noted. Apparent author-list flags from the automated run
([22], [23], [28], [30], [33], [36], [40]) were false positives from surname tokenization
("Bar-Cohen"→"cohen", "El Aissaoui"→"aissaoui", "Pilawa-Podgurski"→"podgurski") or from "et al."
abbreviation; each was checked by hand and is correct.

| Ref | Verdict | Canonical DOI |
|---|---|---|
| 19 | OK (ITHERM 2019 conf.) | 10.1109/itherm.2019.8757253 |
| 20 | **REPLACE** (no record) | 10.1016/j.ijheatmasstransfer.2024.125455 (Yan et al.) |
| 22 | OK | 10.1016/j.ijheatmasstransfer.2016.05.040 |
| 23 | OK | 10.1016/j.ijheatmasstransfer.2017.09.039 |
| 24 | OK | 10.1016/j.physleta.2006.09.041 |
| 26 | OK | 10.1016/j.mineng.2003.08.003 |
| 28 | OK | 10.1109/tcpmt.2021.3111114 |
| 29 | OK | 10.1007/s00339-009-5098-1 |
| 30 | OK | 10.1016/j.ijheatmasstransfer.2019.119055 |
| 31 | OK | 10.1016/j.scitotenv.2025.179046 |
| 33 | OK | 10.1016/j.ijheatmasstransfer.2019.118918 |
| 34 | OK | 10.1063/1.5013623 |
| 35 | OK | 10.1109/tcpmt.2019.2930089 |
| 36 | OK | 10.1038/s41928-022-00748-4 |
| 37 | OK (Rajagopal; see §2) | 10.1016/j.ijheatmasstransfer.2019.118497 |
| 38 | OK | 10.1016/0364-5916(90)90013-p |
| 39 | OK | 10.1023/a:1026373602352 |
| 40 | OK | 10.1016/j.tca.2003.10.020 |
| 41 | OK | 10.1179/030634578790434025 |
| 42 | OK | 10.1016/0364-5916(91)90030-n |
| 43 | OK (use canonical DOI) | 10.5334/jors.140 |
| 44 | OK | 10.1021/je400882q |
| 45 | OK (use canonical DOI) | 10.1557/mrc.2019.59 |
| 46 | OK | 10.1007/s11837-017-2318-6 |
| (new) Olson | ADD (see §2) | 10.1126/science.277.5330.1237 |

## Remaining "finish it" gaps (not references)

These are outstanding for a submission-ready Energy package; flagged here, not yet done:
- **Figures 7–10 are referenced in the text but absent from `figures-final/`** (which holds only
  Fig1–6). Missing: Fig 7 (gallium supercooling), Fig 8 (three-generation materials comparison),
  Fig 9 (computed Ga–In–Sn liquidus — this is the COMPUT addendum's result), Fig 10 (convergence
  timeline). The Graphical Abstract slot is also blank.
- **Version reconciliation.** This Energy version (7.2k words) is a condensation of the repo's
  RSER V11 (17k words). Confirm which is the live submission target before building the package.
- **Elsevier submission package** (cover letter, highlights doc, title page, CRediT, declarations,
  suggested reviewers) exists for the RSER V11 path under `V11-RSER-submission/`; an Energy package
  has not been assembled.
