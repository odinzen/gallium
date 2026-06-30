# Cooling paper — Energy (Elsevier) integration plan

Goal: finalize the **Energy version** (`BUF6EC_1.DOC`, ~7.2k words) as the single submission, and
make sure it carries every valuable piece of content, data, argument, and reference from the longer
versions (RSER **V11**, 17k words; preprint **v3**; the **CALPHAD addendum**; the **strategy note**)
so nothing good is lost in the condensation. This plan is the section-by-section spec for that merge.
Pair it with `cooling-reference-integrity.md` (the verified reference fixes) and
`cooling-reference-DOIs.tsv` (the Zotero add-list).

Source analysis: `_work/content_gap_map.md` (full cross-version diff). The Energy skeleton is
essentially the RSER v3 preprint plus the explicit §9 computed-liquidus section; almost everything
worth recovering lives in **V11**.

## How to run the merge (rule 6 discipline)
- Fold the content below into the Energy `.docx` in Word, section by section, in the author's voice.
- Every **new citation** goes into Zotero by identifier first (DOIs in `cooling-reference-DOIs.tsv`),
  then the bibliography is regenerated via CSL. Do not hand-type or paste LLM-authored reference text.
- Before submission, run `make verify-zotero` (or the manual Crossref checklist) over the full,
  expanded reference set — V11 carries ~96 references the Energy list lacks, and those have **not**
  been through the gate yet. The 24 academic refs already in the Energy list are verified (see the
  integrity report); the V11 additions you choose to pull in must be verified the same way.
- Keep Energy's journal fit in mind: Energy takes original research and focused reviews. Pull in the
  high-value substance below; do **not** re-inflate this back into the 17k-word RSER review. The
  strategy note moved the paper deliberately toward the gallium/CALPHAD spine — preserve that.

## Figure set (assembled, ready)
`Energy-submission/figures/` now holds all ten, renumbered for the Energy text:

| Energy Fig | File | Origin |
|---|---|---|
| 1 Compute heat landscape | Fig1_Compute_Heat_Landscape.jpg | existing |
| 2 Temperature gradient | Fig2_Temperature_Gradient.jpg | existing |
| 3 Water footprint | Fig3_Water_Footprint.jpg | existing |
| 4 Deployment table | Fig4_Deployment_Table.jpg | existing |
| 5 PCM transient (A/B) | Fig5_PCM_Transient.jpg | **new** (from [22],[23]) |
| 6 Gallium corrosion | Fig6_Gallium_Corrosion.jpg | **new** (from [29]) |
| 7 Gallium supercooling | Fig7_Gallium_Supercooling.jpg | **new** (from [4],[19],[30]) |
| 8 Materials design space | Fig8_Materials_Design_Space.jpg | existing (was "Fig5") |
| 9 Computed Ga–In–Sn liquidus (fitted) | Fig9_Computed_GaInSn_Liquidus_fitted.png | **CALPHAD addendum Fig C4** (author-validated) |
| 10 Convergence timeline | Fig10_Convergence_Timeline.jpg | existing (was "Fig6") |

The three new figures are reproducible from `_work/build_energy_figs.py`. Fig 9 is the author's own
computed result (eutectic 10.4 °C at Ga68-In20-Sn12 vs Evans & Prince 10.7 ± 0.3 °C), lifted from
the addendum rather than re-derived. Graphical Abstract slot is still blank — see "Open items".

## Reference fixes to apply first (from the integrity report)
1. Replace **[20]** (does not resolve) with Yan et al. 2024, IJHMT 226 125455
   (`10.1016/j.ijheatmasstransfer.2024.125455`).
2. Add **Olson 1997**, Science 277 1237 (`10.1126/science.277.5330.1237`) and point the
   paradigm sentences at it; keep [37]=Rajagopal for the materials-to-device sentence.
3. Dublin-AWS citation `[12]` → `[15]`.
4. Cite or drop the uncited **[16], [17], [32]**.

## Content to fold in, by section

Quantitative items are quoted from V11/v3/the addendum; verify against the underlying source when
you place each one. Priority A = strongest additions, do these; B = include if room.

### §1 Introduction — policy + demand-response context (B)
- EU Energy Efficiency Directive (recast) 2023/1791 and the German EnEfG waste-heat-reuse mandates
  (10/15/20% by 2026/27/28); MIIT PUE < 1.3 target. Frames heat reuse as regulation-driven, not
  optional. (V11 §1, refs already partly in Energy as [13].)
- Demand-response data point (V11 supplement): ERCOT interconnection queue ~226 GW of large flexible
  load; Riot curtailed ~700 MW in Aug 2023 and earned $31.7M in credits. One sentence makes the
  energy-systems case concrete. (Needs its source verified before use.)

### §2 Thermodynamic framework — exergy backbone (A)
The Energy version conserves-energy/destroys-exergy point is qualitative. V11 makes it quantitative;
add the exergy ladder (T₀ = 283 K / 10 °C reference):

| Output temperature | Exergy fraction of input |
|---|---|
| 35 °C (air) | ~8% |
| 60 °C | ~15% |
| 65 °C (immersion) | ~16% |
| 75 °C | ~19% |
| 80 °C (gallium target) | ~20% |
| 95 °C | ~23% |

Key framing: air→immersion roughly **doubles** recoverable exergy (8→16%); immersion→gallium adds
only ~4 points (16→20%) — "five-sixths of the input exergy is already destroyed at the rack." This
sharpens the paper's central thesis and should anchor §2.
- **Correct the heat-pump COP** to **4–6** (V11), not the Energy draft's 3–4; the compute-vs-heat-pump
  deficit is ~5×. (One-line fix.)

### §3 First-generation / cold-plate architecture (A)
The Energy version covers immersion but omits **direct-to-chip cold plates**, the dominant 2025
hyperscale AI architecture. Add a short subsection: cold plates capture at 50–65 °C (a notch below
immersion, usually needing a small heat-pump lift), but scale to ~1 MW/rack (GB200 NVL72) and are
what most new AI build-outs actually use. Without it the "materials generations" story has a visible
gap on the deployed state of the art. (V11 §3.2/3.2.1.)

### §4 Lifecycle CO₂ — rigor + more deployments (A)
- **Correct the headline CO₂ range.** The Energy draft's 2,000–3,800 tCO₂/container/yr assumes 100%
  thermal utilization. V11's corrected base case is **1,400–3,200 tCO₂/yr** at realistic utilization.
  Use the corrected figure and state the utilization assumption.
- **Breakeven condition** (V11 Table 6): compute-heat is net-CO₂-positive only where displaced grid
  intensity is below ~0.13–0.24 tCO₂/MWh — essentially Nordic hydro + French nuclear. Say this
  explicitly; it is the honest boundary of the claim.
- **Cold-plate AI case** (V11 Table 7): ~+900–1,500 tCO₂/yr net benefit in Finland vs ~−4,000
  (net harm) on the German grid — the geography dependence in one number.
- **Fluid embodied emissions**: 13–43 t per facility fill; not negligible against the displacement.
- **Deployments 6 → add the strongest few**: Yandex Mäntsälä (covers ~75% of town heat, ~40% gas-CO₂
  cut), Telehouse Frankfurt "FRANKY" (~400 tCO₂/yr), Microsoft–Fortum Espoo (350 MW, ~400,000 tCO₂/yr
  projected — the largest by far). Keep the table to the best-documented; note verification status.

### §5 Gallium — TRL honesty + defensible bounds (A)
- **TRL split**: gallium TIMs are TRL 8–9 (PS5, GalliTHERM in production); a facility-scale gallium
  cooling loop is TRL 3–4. State this so the second-generation claim is not over-read.
- **Reviewer-defensibility caveats** to add inline: the 60–68% transient reduction is a steady-state
  *upper bound* under specific pulse conditions; the CNT 2.3× conductivity enhancement is *not* scaled;
  the upper-end conductivity values need optimized geometry/oxide conditions.
- **Cite the author's calorimetry paper** as the experimental anchor for the Ga-In-Sn data:
  Bustamante, Lilova, Navrotsky, Harvey, Oishi, JTAC 149 (2024) 4817 (`10.1007/s10973-024-13035-5`).

### §6 Gallium engineering — toxicity + regulatory (A, currently absent from Energy)
- **Indium/Galinstan toxicity**: Galinstan is ~21.5% indium; ACGIH TLV 0.1 mg/m³, and Japan's ITO
  occupational target is 0.0003 mg/m³ (≈330× tighter). A facility handling tonnes of Galinstan has a
  real industrial-hygiene profile worth one paragraph in §6.
- **Gallium regulatory exposure**: critical-raw-material designations + the PRC export-control regime
  (ties to the existing §7 supply-chain text; cite [32] here).

### §7 Supply chain / circularity (B)
- **Circularity numbers**: dielectric fluid reclaim 70–85%; PFAS two-phase fluids need >1,100 °C
  thermal destruction; sourced ASIC e-waste figure is **30,700 t (2020)** — use this in place of the
  Energy draft's loose "15,000–30,000 t" in the Conclusion.

### §9 Computed phase equilibria — add the validation chain (A)
Energy §9 reports only the fitted endpoint. The addendum documents the full, traceable validation the
strategy note says is the novelty; fold in two or three sentences:
- Pipeline control on **Pb–Sn** (NIMS DB) reproduces the eutectic to **1.1 K**.
- Each binary reproduces its own eutectic from sourced parameters: Ga–In 16.4 °C (Rugg & Chart),
  Ga–Sn 22.4 °C (fitted to Zivkovic calorimetry, RMS 41 J/mol, enthalpic-only), In–Sn 120.9 °C with
  the β/γ intermediate phases (David et al.).
- The **unfitted** Muggianu ternary already lands at a physical **16.9 °C**; a single symmetric ternary
  term **L(Ga,In,Sn) = −4800 J/mol** fitted to the Evans & Prince invariant closes the last ~6 °C to
  **10.4 °C** (vs 10.7 ± 0.3 °C), binaries untouched.
- This is "one parameter fitted to one measured invariant," not a full ternary optimization — say so.
- The coefficient tables (addendum Tables 1–9) belong in a short **Supplementary** parameter table so
  the computation is reproducible. Extracted values are in `_work/comput_tables.txt`.
- **Use 10.7 ± 0.3 °C consistently** for the Evans & Prince eutectic (the addendum mixes 10.5 and 10.7).

## Consistency / fact nits to fix while merging
- **Power Mining thermal output**: the Introduction says **1.5 MW**; §4 says **1.7 MW**. Pick one
  (V11 and the lifecycle model use 1.7 MW) and make it consistent everywhere, including the abstract.
- **R1234ze GWP**: Energy says "GWP < 1" in §3.1/§8.1; V11 corrects this to **≈6**. Confirm against a
  primary refrigerant-GWP source and use one value.
- **519 mL water/100-word prompt [8]**: attributed in Energy to "Ren et al., MIT News 2025." The
  primary source is the Li/Yang/Islam/Ren "Making AI Less Thirsty" paper (arXiv 2023). Cite the
  primary, not the news write-up.
- **Article numbers are already correct in the Energy version** — Zhang [30] = 119055 and Guan
  [31] = 179046 were confirmed against Crossref. V11 carries typos (119052 / 178956); do **not** copy
  V11's numbers back in. (Rigor note: the resolved record is ground truth, not the other manuscript.)

## Open items (need author input or a separate pass)
- **Graphical Abstract** — still blank. Candidate: a single-row "three generations" strip
  (dielectric 65–75 °C → gallium >80 °C → embedded two-phase 1 kW/cm²) with the exergy/temperature
  ladder. Can be generated to match the figure style on request.
- **Energy submission package** — cover letter, highlights doc, suggested reviewers drafted under
  `Energy-submission/` (see that folder). Title page / CRediT / declarations already live inline in
  the manuscript and can be split out as Elsevier requires.
- **Full reference verification of V11 additions** — the ~96 extra refs you choose to pull in must go
  through add-by-DOI + the Crossref gate before submission. Only the 24 already in the Energy list are
  verified so far.
