# Energy submission package — assembly checklist

Manuscript: "Materials Design for Compute Thermal Management: From Dielectric Fluids to Gallium Based
Cooling Systems." Target: Energy (Elsevier). Base file: `Downloads/BUF6EC_1.DOC`.

This folder holds the drafted package items. Front/back matter (CRediT, competing-interest
declaration, data-availability, AI-use statement) already lives inline in the manuscript; split out
into separate files only if the Energy submission system requires it (the V11 versions under
`../V11-RSER-submission/` are ready templates).

## Contents
- `Cover_Letter_Energy.md` — drafted; fill [DATE], confirm article type and editor salutation.
- `Suggested_Reviewers_Energy.md` — six suggestions, materials + heat-reuse balanced.
- `Highlights_Energy.md` — the five manuscript highlights, character counts checked.
- `Title_Page_Energy.md` — adapted for Energy; metrics noted.
- `figures/` — all 10 figures, renumbered for the Energy text (Fig1–10). Fig9 is the author's
  validated computed liquidus (addendum Fig C4).

## Still to do before submission
1. Apply the four reference fixes (see `manuscripts/cooling-reference-integrity.md`): replace [20],
   add Olson, fix Dublin [12]→[15], resolve uncited [16]/[17]/[32].
2. Fold in the cross-version content you want (see `manuscripts/cooling-energy-integration-plan.md`)
   and the consistency fixes (1.5 vs 1.7 MW; R1234ze GWP; the 519 mL primary source).
3. Build the bibliography in Zotero by add-by-DOI from `manuscripts/cooling-reference-DOIs.tsv`, then
   generate it via CSL. Run the Crossref/Zotero gate over the full list (including any V11 additions).
4. Produce the Graphical Abstract (slot is blank).
5. Add a Supplementary parameter table for the §9 CALPHAD computation (addendum Tables 1–9).
6. Convert these .md drafts into the .docx forms the Energy system expects (use the V11 .docx as
   templates to avoid reformatting).
