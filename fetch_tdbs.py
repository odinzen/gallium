#!/usr/bin/env python3
"""Pull this repo's TDBs out of the shared vault into their working locations.

The vault (assets/tdb-store/ in odinzen_assessment_workspace) is the single committed home for
every own-derived TDB. Working repos do NOT commit their own copy; they keep a gitignored local
copy that this script populates from the vault. Run it from a working repo's root:

    python fetch_tdbs.py <group>        # group = llzo | gainsn | recycling-titanium

It reads MANIFEST.tsv and copies each row whose `group` matches into `dest_rel_path` (relative to
the current directory). Locating the vault, in order: $ODINZEN_TDB_STORE, then the script's own
folder if it lives in the vault, then a sibling checkout `../odinzen_assessment_workspace/assets/
tdb-store`. Set $ODINZEN_TDB_STORE if your workspace clone lives elsewhere.

`--check` reports drift (missing / differing local copy) without writing; exit 1 if any drift.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import os
import shutil
import sys
from pathlib import Path


def find_vault() -> Path:
    env = os.environ.get("ODINZEN_TDB_STORE")
    if env:
        return Path(env).expanduser().resolve()
    here = Path(__file__).resolve().parent
    if here.name == "tdb-store" and (here / "MANIFEST.tsv").exists():
        return here
    for cand in (
        Path.cwd() / ".." / "odinzen_assessment_workspace" / "assets" / "tdb-store",
        here.parent.parent.parent / "odinzen_assessment_workspace" / "assets" / "tdb-store",
    ):
        cand = cand.resolve()
        if (cand / "MANIFEST.tsv").exists():
            return cand
    sys.exit(
        "could not find the TDB vault. Set ODINZEN_TDB_STORE to "
        "<odinzen_assessment_workspace>/assets/tdb-store, or clone it beside this repo."
    )


def _sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def rows_for(vault: Path, group: str) -> list[dict]:
    with (vault / "MANIFEST.tsv").open(encoding="utf-8", newline="") as fh:
        rows = [r for r in csv.DictReader(fh, delimiter="\t") if r["group"] == group]
    if not rows:
        groups = sorted({r["group"] for r in csv.DictReader((vault / "MANIFEST.tsv").open(encoding="utf-8"), delimiter="\t")})
        sys.exit(f"no manifest rows for group '{group}'. Known groups: {', '.join(groups)}")
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description="Populate this repo's TDBs from the shared vault.")
    ap.add_argument("group", help="vault group: llzo | gainsn | recycling-titanium")
    ap.add_argument("--check", action="store_true", help="report drift only, do not write")
    args = ap.parse_args()

    vault = find_vault()
    drift = False
    for r in rows_for(vault, args.group):
        src = vault / r["vault_path"]
        dst = Path(r["dest_rel_path"])
        if not src.exists():
            print(f"MISSING IN VAULT  {src}")
            drift = True
            continue
        if args.check:
            state = "ok" if dst.exists() and _sha256(dst) == _sha256(src) else "DRIFT"
            if state != "ok":
                drift = True
            print(f"{state:5}  {dst}")
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            print(f"fetched  {dst}")
    return 1 if (args.check and drift) else 0


if __name__ == "__main__":
    raise SystemExit(main())
