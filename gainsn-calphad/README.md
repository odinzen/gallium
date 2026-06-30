# GaInSn-CALPHAD

Reproducibility package for:

**A CALPHAD assessment of the Ga-In-Sn liquidus for designable low-melting liquid-metal coolants**
Michael E. Bustamante, Kristina Lilova

*Submitted to CALPHAD, 2026*

---

## Contents

| Path | Description |
|------|-------------|
| `databases/GaInSn_fitted.tdb` | Fitted Ga-In-Sn database (ternary L = -8000 J/mol) |
| `databases/GaInSn.tdb` | Muggianu extrapolation, no ternary term |
| `databases/InSn_David2004.tdb` | In-Sn binary (David et al. 2004) |
| `databases/GaInSn_CALPHAD_parameters.txt` | Assessed parameters in plain text |
| `scripts/fit_gasn.py` | Nonlinear least-squares fit of Ga-Sn Redlich-Kister parameters |
| `scripts/fit_ternary.py` | Ternary parameter fit to Evans and Prince eutectic temperature |
| `scripts/tern_fitted.py` | Ternary liquidus surface (fitted, 1275-point mesh) |
| `scripts/tern_full.py` | Ternary liquidus surface (Muggianu extrapolation) |
| `scripts/make_paper_figs.py` | Binary phase diagrams and isopleths (Figs. 1-3, 8) |
| `scripts/run_pbsn2.py` | Pb-Sn control calculation |
| `scripts/refine_tern.py` | High-resolution eutectic finder |
| `scripts/sensitivity_check.py` | Sensitivity table (Table 3 of main text) |
| `figures/` | Manuscript figures (Fig1-Fig8) |

## Requirements

Python 3.10+, pycalphad >= 0.10, numpy, scipy, matplotlib. All available via conda-forge:

```
conda create -n gainSn -c conda-forge pycalphad numpy scipy matplotlib
conda activate gainSn
```

Run each script from the repo root (the directory containing `databases/` and `scripts/`):

```
python scripts/make_paper_figs.py
```

## Data availability

Pre-computed composition meshes (`tern_fitted_grid.npy`, `tern_full_grid.npy`) are deposited on Zenodo (DOI assigned on acceptance). Regenerate locally by running `tern_fitted.py` and `tern_full.py`.

## License

Code and databases: MIT License. Figures: CC BY 4.0.
