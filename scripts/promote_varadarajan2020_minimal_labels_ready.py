"""Promote Varadarajan2020 Minimal (MOPS-pyruvate) candidate labels to READY (D-21).

Human decision 2026-08-01: APPROVED_FOR_PRIMARY_BINARY_VALIDATION.

- Preserves the CANDIDATE CSV unchanged (audit trail).
- Writes READY gene-level evidence + frozen primary binary universe.
- Recomputes source counts from DS1/DS4 independently; aborts on mismatch.
- Does NOT compute confusion-matrix metrics (TP/TN/FP/FN, MCC, F1, etc.).
- Does NOT modify D-20 Lee2015 original READY positives.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.stdout.reconfigure(encoding="utf-8")

DS1 = ROOT / "data/raw/literature/varadarajan2020/Supplementary Dataset 1 (MPAO1).xlsx"
DS4 = ROOT / "data/raw/literature/varadarajan2020/Supplementary Dataset 4 (MPAO1).xlsx"
CANDIDATE = (
    ROOT
    / "data/processed/literature/gene_level"
    / "varadarajan2020_lee2015_minimal_gene_labels_CANDIDATE.csv"
)
LEE_READY = (
    ROOT
    / "data/processed/literature/gene_level"
    / "literature_evidence_gene_level_READY_mops_pyruvate_lee2015.csv"
)
OUT_READY = (
    ROOT
    / "data/processed/literature/gene_level"
    / "varadarajan2020_lee2015_minimal_gene_labels_READY.csv"
)
OUT_BINARY = (
    ROOT
    / "data/processed/literature/gene_level"
    / "varadarajan2020_lee2015_minimal_PRIMARY_BINARY_UNIVERSE.csv"
)
OUT_AUDIT = ROOT / "project_management/audit/negative_universe_lee2015"
PRED_CSV = ROOT / "results/essentiality/gene_essentiality_mops_pyruvate_lee2015.csv"
MODEL_PATH = ROOT / "models/paeruginosa_MODEL1507180020.xml"

PA_STD = re.compile(r"^PA\d{4}$")

# Expected counts from human-reviewed candidate audit (gates, not hard-coded labels)
EXPECTED = {
    "master_cds_count_ds1": 5799,
    "ds4_essential_union_count": 1117,
    "valid_pao1_unique_std_mappings": 5474,
    "minimal_1": 410,
    "minimal_2": 351,
    "minimal_3": 427,
    "minimal_sum_0": 5312,
    "minimal_sum_1": 72,
    "minimal_sum_2": 129,
    "minimal_sum_3": 286,
    "positive_genome": 415,
    "negative_genome": 5312,
    "ambiguous_genome": 72,
    "model_overlap_n": 1043,
    "model_overlap_positive": 214,
    "model_overlap_negative": 811,
    "model_overlap_ambiguous": 18,
    "primary_binary_total": 1025,
}

LABEL_MAP = {
    "POSITIVE": "POSITIVE_CONSENSUS_ESSENTIAL",
    "NEGATIVE": "NEGATIVE_0_OF_3_NOT_CALLED_ESSENTIAL",
    "AMBIGUOUS": "AMBIGUOUS_1_OF_3",
}

PROMO_NOTE = (
    "D-21 APPROVED_FOR_PRIMARY_BINARY_VALIDATION 2026-08-01 (human review): "
    "Varadarajan2020 remapping of Lee2015 Tn-seq SRP052838; Minimal-1/2/3 = "
    "MOPS-pyruvate; POSITIVE=minimal_sum>=2; NEGATIVE=minimal_sum==0 "
    "(0_of_3_not_called_essential); AMBIGUOUS=minimal_sum==1 excluded from "
    "primary binary. Not independent replication of Lee. Do not mix with D-20 "
    "Lee-original positives in one primary matrix."
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_pa_hits(val) -> list[str]:
    if pd.isna(val):
        return []
    s = str(val).strip()
    if not s or s.lower() == "nan":
        return []
    return [p.strip() for p in s.split(";") if p.strip()]


def load_model_genes() -> set[str]:
    genes: set[str] = set()
    try:
        import cobra

        model = cobra.io.read_sbml_model(str(MODEL_PATH))
        for g in model.genes:
            m = re.search(r"(PA\d{4})", g.id)
            if m:
                genes.add(m.group(1))
            elif PA_STD.match(g.id):
                genes.add(g.id)
    except Exception:
        if PRED_CSV.exists():
            p = pd.read_csv(PRED_CSV)
            col = "gene_id" if "gene_id" in p.columns else p.columns[0]
            for gid in p[col].astype(str):
                m = re.search(r"(PA\d{4})", gid)
                if m:
                    genes.add(m.group(1))
    return genes


def load_pred_genes() -> tuple[set[str], dict[str, str]]:
    pred_genes: set[str] = set()
    raw: dict[str, str] = {}
    if not PRED_CSV.exists():
        return pred_genes, raw
    p = pd.read_csv(PRED_CSV)
    col = "gene_id" if "gene_id" in p.columns else p.columns[0]
    for gid in p[col].astype(str):
        m = re.search(r"(PA\d{4})", gid)
        if m:
            pa = m.group(1)
            pred_genes.add(pa)
            raw[pa] = gid
    return pred_genes, raw


def recompute_from_sources() -> tuple[pd.DataFrame, dict]:
    """Rebuild gene-level labels from DS1+DS4 (same rules as candidate builder)."""
    df1 = pd.read_excel(DS1, sheet_name="MPAO1_CDS", header=1)
    df4 = pd.read_excel(DS4, sheet_name="essentialGenes_MPAO1", header=0)
    ds4_idx = df4.set_index("Locus", drop=False)
    model_genes = load_model_genes()
    pred_genes, pred_raw = load_pred_genes()

    rows = []
    for _, r in df1.iterrows():
        locus = r["locus_tag"]
        hits = parse_pa_hits(r["best_hit protein"])
        std_hits = [h for h in hits if PA_STD.match(h)]
        nonstd_hits = [h for h in hits if h and not PA_STD.match(h)]
        unique_flag = (r["unique?"] == 1) if not pd.isna(r.get("unique?")) else False

        if locus in ds4_idx.index:
            d4 = ds4_idx.loc[locus]
            if isinstance(d4, pd.DataFrame):
                d4 = d4.iloc[0]
            # DS4: 1 = called essential; blank/absent = not called essential (0)
            m1 = 1 if d4["Minimal-1"] == 1 else 0
            m2 = 1 if d4["Minimal-2"] == 1 else 0
            m3 = 1 if d4["Minimal-3"] == 1 else 0
            in_ds4 = True
            ess_n = d4["Essential in x/16 samples"]
        else:
            m1 = m2 = m3 = 0
            in_ds4 = False
            ess_n = 0

        msum = int(m1 + m2 + m3)
        if msum >= 2:
            short = "POSITIVE"
        elif msum == 1:
            short = "AMBIGUOUS"
        else:
            short = "NEGATIVE"

        if len(std_hits) == 1 and not nonstd_hits:
            map_status = "unique_std_PAO1"
            pao1 = std_hits[0]
        elif len(std_hits) > 1 and not nonstd_hits:
            map_status = "one_to_many_std_PAO1"
            pao1 = ";".join(std_hits)
        elif len(std_hits) >= 1 and nonstd_hits:
            map_status = "mixed_std_nonstd"
            pao1 = ";".join(hits)
        elif nonstd_hits and not std_hits:
            map_status = "nonstandard_only"
            pao1 = ";".join(nonstd_hits)
        elif unique_flag or pd.isna(r["best_hit protein"]):
            map_status = "no_PAO1_homolog"
            pao1 = ""
        else:
            map_status = "unmapped"
            pao1 = ""

        in_model = int(map_status == "unique_std_PAO1" and pao1 in model_genes)
        evaluable = int(
            map_status == "unique_std_PAO1" and pao1 in (pred_genes or model_genes)
        )
        if map_status != "unique_std_PAO1":
            excl = "mapping_not_unique_std" if map_status != "no_PAO1_homolog" else "no_pao1"
            if map_status == "no_PAO1_homolog":
                excl = "no_PAO1_homolog"
            elif map_status == "one_to_many_std_PAO1":
                excl = "one_to_many_std_PAO1"
            elif map_status == "nonstandard_only":
                excl = "nonstandard_only"
            elif map_status == "mixed_std_nonstd":
                excl = "mixed_std_nonstd"
            else:
                excl = "unmapped"
            model_gene_id = ""
        elif not in_model:
            excl = "absent_from_imo1056"
            model_gene_id = ""
        elif not evaluable:
            excl = "in_model_but_not_in_knockout_results"
            model_gene_id = pred_raw.get(pao1, pao1)
        else:
            excl = ""
            model_gene_id = pred_raw.get(pao1, pao1)

        rows.append(
            {
                "mpao1_locus": locus,
                "pao1_locus": pao1,
                "minimal_1": m1,
                "minimal_2": m2,
                "minimal_3": m3,
                "minimal_sum": msum,
                "short_label": short,
                "mapping_status": map_status,
                "in_imo1056": in_model,
                "model_evaluable": evaluable,
                "model_gene_id": model_gene_id,
                "in_ds4_essential_union": int(in_ds4),
                "essential_in_n_of_16_samples": ess_n if not pd.isna(ess_n) else 0,
                "mpao1_unique": int(unique_flag),
                "best_hit_protein_raw": (
                    "" if pd.isna(r["best_hit protein"]) else str(r["best_hit protein"])
                ),
                "base_exclusion_reason": excl,
            }
        )

    rebuilt = pd.DataFrame(rows)
    counts = {
        "master_cds_count_ds1": int(len(df1)),
        "ds4_essential_union_count": int(len(df4)),
        "valid_pao1_unique_std_mappings": int(
            (rebuilt["mapping_status"] == "unique_std_PAO1").sum()
        ),
        "minimal_1": int((df4["Minimal-1"] == 1).sum()),
        "minimal_2": int((df4["Minimal-2"] == 1).sum()),
        "minimal_3": int((df4["Minimal-3"] == 1).sum()),
        "minimal_sum_0": int((rebuilt["minimal_sum"] == 0).sum()),
        "minimal_sum_1": int((rebuilt["minimal_sum"] == 1).sum()),
        "minimal_sum_2": int((rebuilt["minimal_sum"] == 2).sum()),
        "minimal_sum_3": int((rebuilt["minimal_sum"] == 3).sum()),
        "positive_genome": int((rebuilt["short_label"] == "POSITIVE").sum()),
        "negative_genome": int((rebuilt["short_label"] == "NEGATIVE").sum()),
        "ambiguous_genome": int((rebuilt["short_label"] == "AMBIGUOUS").sum()),
        "imo1056_model_genes_std_PA": int(len(model_genes)),
        "prediction_evaluable_genes": int(len(pred_genes) if pred_genes else len(model_genes)),
    }
    return rebuilt, counts


def apply_d21_policy(rebuilt: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """Attach READY fields, freeze primary binary universe, collect exclusion stats."""
    ready = rebuilt.copy()
    ready["experimental_label"] = ready["short_label"].map(LABEL_MAP)
    ready["evidence_source"] = "Varadarajan2020_Lee2015_Tnseq_remap"
    ready["source_dataset"] = "DS1_MPAO1_CDS+DS4_essentialGenes_MPAO1"
    ready["condition"] = "MOPS-pyruvate_Minimal_1_2_3"
    ready["decision_id"] = "D-21"
    ready["human_review_decision"] = "APPROVED_FOR_PRIMARY_BINARY_VALIDATION"
    ready["review_status"] = "READY"
    ready["not_independent_replication_of_lee2015"] = 1
    ready["notes"] = (
        "minimal blank/absent=not_called_essential_per_Lee_script_remap; "
        "not independent screen | " + PROMO_NOTE
    )

    # Primary binary eligibility (iMO1056 evaluable = membership in model.genes /
    # knockout results; no extra GPR-only filter — see src/gene_essentiality.py)
    primary_mask = (
        (ready["mapping_status"] == "unique_std_PAO1")
        & (ready["in_imo1056"] == 1)
        & (ready["model_evaluable"] == 1)
        & (ready["short_label"].isin(["POSITIVE", "NEGATIVE"]))
        & (ready["minimal_sum"] != 1)
    )

    # Ambiguous in model: explicit exclusion
    amb_model = (
        (ready["mapping_status"] == "unique_std_PAO1")
        & (ready["in_imo1056"] == 1)
        & (ready["short_label"] == "AMBIGUOUS")
    )

    inclusion = []
    excl_out = []
    for i, row in ready.iterrows():
        if primary_mask.loc[i]:
            inclusion.append(1)
            excl_out.append("")
        elif amb_model.loc[i]:
            inclusion.append(0)
            excl_out.append("EXCLUDED_PRIMARY_BINARY_DISCORDANT_1_OF_3")
        else:
            inclusion.append(0)
            reason = str(row["base_exclusion_reason"] or "")
            if row["short_label"] == "AMBIGUOUS":
                if (
                    row["in_imo1056"] == 1
                    and row["mapping_status"] == "unique_std_PAO1"
                ):
                    reason = "EXCLUDED_PRIMARY_BINARY_DISCORDANT_1_OF_3"
                elif reason:
                    reason = f"{reason};AMBIGUOUS_1_OF_3"
                else:
                    reason = "EXCLUDED_PRIMARY_BINARY_DISCORDANT_1_OF_3"
            excl_out.append(reason if reason else "excluded_from_primary_binary")

    ready["binary_primary_inclusion"] = inclusion
    ready["exclusion_reason"] = excl_out

    # Many-MPAO1→one-PAO1 among unique_std ∩ model
    val = ready[
        (ready["mapping_status"] == "unique_std_PAO1") & (ready["in_imo1056"] == 1)
    ]
    pa_vc = val["pao1_locus"].value_counts()
    multi_pa = set(pa_vc[pa_vc > 1].index)
    if multi_pa:
        ready.loc[
            ready["pao1_locus"].isin(multi_pa), "exclusion_reason"
        ] = "many_MPAO1_to_one_PAO1"
        ready.loc[ready["pao1_locus"].isin(multi_pa), "binary_primary_inclusion"] = 0

    binary = ready[ready["binary_primary_inclusion"] == 1].copy()
    # one row per PAO1 (should already be unique)
    assert binary["pao1_locus"].is_unique, "duplicate PAO1 in primary binary universe"

    overlap = ready[
        (ready["mapping_status"] == "unique_std_PAO1") & (ready["in_imo1056"] == 1)
    ]
    stats = {
        "model_overlap_n": int(len(overlap)),
        "model_overlap_positive": int((overlap["short_label"] == "POSITIVE").sum()),
        "model_overlap_negative": int((overlap["short_label"] == "NEGATIVE").sum()),
        "model_overlap_ambiguous": int((overlap["short_label"] == "AMBIGUOUS").sum()),
        "primary_binary_positive": int(
            (binary["short_label"] == "POSITIVE").sum()
        ),
        "primary_binary_negative": int(
            (binary["short_label"] == "NEGATIVE").sum()
        ),
        "primary_binary_total": int(len(binary)),
        "ambiguous_excluded_from_binary": int(
            (ready["exclusion_reason"] == "EXCLUDED_PRIMARY_BINARY_DISCORDANT_1_OF_3").sum()
        ),
        "many_mpao1_to_one_pao1_unique_ids": int(len(multi_pa)),
        "exclusion_reason_counts": ready["exclusion_reason"]
        .replace("", "IN_PRIMARY_BINARY")
        .value_counts()
        .to_dict(),
        "mapping_status_counts": ready["mapping_status"].value_counts().to_dict(),
        "label_counts_ready": ready["experimental_label"].value_counts().to_dict(),
        "review_status_counts": ready["review_status"].value_counts().to_dict(),
    }
    return ready, binary, stats


def verify_against_candidate(rebuilt: pd.DataFrame) -> list[str]:
    """Ensure rebuild matches existing CANDIDATE core fields."""
    issues: list[str] = []
    if not CANDIDATE.exists():
        issues.append(f"missing candidate file: {CANDIDATE}")
        return issues
    cand = pd.read_csv(CANDIDATE)
    if len(cand) != len(rebuilt):
        issues.append(f"row count candidate={len(cand)} rebuilt={len(rebuilt)}")
        return issues
    merged = cand.merge(
        rebuilt[
            [
                "mpao1_locus",
                "short_label",
                "minimal_sum",
                "minimal_1",
                "minimal_2",
                "minimal_3",
                "mapping_status",
                "pao1_locus",
                "in_imo1056",
            ]
        ],
        on="mpao1_locus",
        how="outer",
        indicator=True,
    )
    if (merged["_merge"] != "both").any():
        issues.append("mpao1_locus set differs between candidate and rebuild")
    mism = merged[
        (merged["candidate_label"] != merged["short_label"])
        | (merged["minimal_sum_x"] != merged["minimal_sum_y"])
        | (merged["mapping_status_x"] != merged["mapping_status_y"])
        | (merged["pao1_locus_x"].fillna("") != merged["pao1_locus_y"].fillna(""))
        | (merged["in_imo1056_x"] != merged["in_imo1056_y"])
    ]
    if len(mism):
        issues.append(f"label/mapping mismatches vs candidate: {len(mism)} rows")
    return issues


def check_expected(counts: dict, stats: dict) -> list[str]:
    issues = []
    for k, exp in EXPECTED.items():
        if k in counts:
            got = counts[k]
        elif k in stats:
            got = stats[k]
        elif k == "primary_binary_total":
            got = stats["primary_binary_total"]
        else:
            continue
        if got != exp:
            issues.append(f"COUNT_MISMATCH {k}: expected={exp} got={got}")
    # cross-check binary components
    if stats["primary_binary_positive"] != EXPECTED["model_overlap_positive"]:
        issues.append(
            "COUNT_MISMATCH primary_binary_positive vs model_overlap_positive"
        )
    if stats["primary_binary_negative"] != EXPECTED["model_overlap_negative"]:
        issues.append(
            "COUNT_MISMATCH primary_binary_negative vs model_overlap_negative"
        )
    return issues


def verify_lee_ready_unchanged(lee_sha_before: str) -> list[str]:
    issues = []
    if not LEE_READY.exists():
        issues.append("D-20 Lee READY file missing")
        return issues
    sha = _sha256(LEE_READY)
    if sha != lee_sha_before:
        issues.append("D-20 Lee READY file was modified during promotion")
    lee = pd.read_csv(LEE_READY)
    if len(lee) != 437:
        issues.append(f"D-20 Lee READY row count changed: {len(lee)}")
    if "review_status" in lee.columns and not (lee["review_status"] == "READY").all():
        issues.append("D-20 Lee READY review_status altered")
    return issues


def integrity_checks(ready: pd.DataFrame, binary: pd.DataFrame) -> dict[str, str]:
    """Return check_name -> PASS/FAIL."""
    checks: dict[str, str] = {}

    def ok(name: str, cond: bool) -> None:
        checks[name] = "PASS" if cond else "FAIL"

    ok("no_duplicate_primary_pao1", binary["pao1_locus"].is_unique)
    ok(
        "primary_pao1_id_policy",
        binary["pao1_locus"].astype(str).str.match(r"^PA\d{4}$").all(),
    )
    ok("primary_all_in_imo1056", (binary["in_imo1056"] == 1).all())
    ok("primary_all_model_evaluable", (binary["model_evaluable"] == 1).all())
    ok(
        "no_ambiguous_in_primary",
        (binary["short_label"] != "AMBIGUOUS").all()
        and (binary["experimental_label"] != "AMBIGUOUS_1_OF_3").all(),
    )
    ok("no_minimal_sum_1_in_primary", (binary["minimal_sum"] != 1).all())
    ok(
        "negatives_are_sum_0",
        (
            binary.loc[
                binary["experimental_label"] == "NEGATIVE_0_OF_3_NOT_CALLED_ESSENTIAL",
                "minimal_sum",
            ]
            == 0
        ).all(),
    )
    ok(
        "positives_are_sum_ge_2",
        (
            binary.loc[
                binary["experimental_label"] == "POSITIVE_CONSENSUS_ESSENTIAL",
                "minimal_sum",
            ]
            >= 2
        ).all(),
    )
    ok(
        "both_labels_from_varadarajan",
        (binary["evidence_source"] == "Varadarajan2020_Lee2015_Tnseq_remap").all(),
    )
    ok(
        "every_ready_row_has_provenance",
        ready["evidence_source"].notna().all()
        and ready["source_dataset"].notna().all()
        and (ready["decision_id"] == "D-21").all(),
    )
    ok(
        "primary_counts_214_811",
        int((binary["short_label"] == "POSITIVE").sum()) == 214
        and int((binary["short_label"] == "NEGATIVE").sum()) == 811
        and len(binary) == 1025,
    )
    ok("candidate_file_preserved", CANDIDATE.exists())
    # No metrics columns accidentally written
    metricish = {
        "tp",
        "tn",
        "fp",
        "fn",
        "mcc",
        "f1",
        "precision",
        "recall",
        "specificity",
        "accuracy",
    }
    cols = {c.lower() for c in list(ready.columns) + list(binary.columns)}
    ok("no_metrics_columns", not bool(cols & metricish))

    # Blank→0 encoding is only for DS4 library calls / DS4-absent loci (documented),
    # never from Lee Dataset-S1 absence. Guard: no Lee S1 path in evidence_source.
    ok(
        "no_lee_s1_absence_as_negative",
        ready["evidence_source"].str.contains("Varadarajan").all()
        and (~ready["source_dataset"].astype(str).str.contains("lee2015.*sd01", case=False)).all(),
    )
    return checks


def main() -> int:
    lee_sha_before = _sha256(LEE_READY) if LEE_READY.exists() else ""

    rebuilt, source_counts = recompute_from_sources()
    cand_issues = verify_against_candidate(rebuilt)
    if cand_issues:
        print("STOP: candidate vs rebuild discrepancy:")
        for i in cand_issues:
            print(" -", i)
        return 2

    ready, binary, stats = apply_d21_policy(rebuilt)
    count_issues = check_expected(source_counts, stats)
    if count_issues:
        print("STOP: recomputed counts differ from human-review expectations:")
        for i in count_issues:
            print(" -", i)
        print("source_counts:", json.dumps(source_counts, indent=2))
        print("stats:", json.dumps({k: v for k, v in stats.items() if k != "exclusion_reason_counts"}, indent=2))
        return 3

    lee_issues = verify_lee_ready_unchanged(lee_sha_before)
    if lee_issues:
        print("STOP: D-20 Lee READY integrity failed:")
        for i in lee_issues:
            print(" -", i)
        return 4

    checks = integrity_checks(ready, binary)
    failed = [k for k, v in checks.items() if v != "PASS"]
    if failed:
        print("STOP: integrity checks failed:", failed)
        print(json.dumps(checks, indent=2))
        return 5

    # Write READY (full evidence; ambiguous retained with exclusion)
    keep_ready = [
        "mpao1_locus",
        "pao1_locus",
        "minimal_1",
        "minimal_2",
        "minimal_3",
        "minimal_sum",
        "experimental_label",
        "short_label",
        "mapping_status",
        "in_imo1056",
        "model_evaluable",
        "model_gene_id",
        "binary_primary_inclusion",
        "exclusion_reason",
        "evidence_source",
        "source_dataset",
        "condition",
        "decision_id",
        "human_review_decision",
        "review_status",
        "not_independent_replication_of_lee2015",
        "in_ds4_essential_union",
        "essential_in_n_of_16_samples",
        "mpao1_unique",
        "best_hit_protein_raw",
        "notes",
    ]
    OUT_READY.parent.mkdir(parents=True, exist_ok=True)
    ready[keep_ready].to_csv(OUT_READY, index=False)

    keep_binary = [
        "pao1_locus",
        "mpao1_locus",
        "model_gene_id",
        "minimal_1",
        "minimal_2",
        "minimal_3",
        "minimal_sum",
        "experimental_label",
        "short_label",
        "mapping_status",
        "in_imo1056",
        "model_evaluable",
        "binary_primary_inclusion",
        "evidence_source",
        "source_dataset",
        "condition",
        "decision_id",
        "human_review_decision",
        "review_status",
        "not_independent_replication_of_lee2015",
        "notes",
    ]
    binary_out = binary[keep_binary].sort_values("pao1_locus").reset_index(drop=True)
    binary_out.to_csv(OUT_BINARY, index=False)

    # Confirm candidate untouched
    assert CANDIDATE.exists()

    report = {
        "decision_id": "D-21",
        "status": "APPROVED_FOR_PRIMARY_BINARY_VALIDATION",
        "source_counts": source_counts,
        "universe_stats": {
            k: v
            for k, v in stats.items()
            if k
            not in {
                "exclusion_reason_counts",
                "mapping_status_counts",
                "label_counts_ready",
                "review_status_counts",
            }
        },
        "exclusion_reason_counts": stats["exclusion_reason_counts"],
        "mapping_status_counts": stats["mapping_status_counts"],
        "label_counts_ready": stats["label_counts_ready"],
        "review_status_counts": stats["review_status_counts"],
        "integrity_checks": checks,
        "artifacts": {
            "candidate_preserved": str(CANDIDATE.relative_to(ROOT)),
            "candidate_sha256": _sha256(CANDIDATE),
            "ready": str(OUT_READY.relative_to(ROOT)),
            "ready_sha256": _sha256(OUT_READY),
            "primary_binary_universe": str(OUT_BINARY.relative_to(ROOT)),
            "primary_binary_sha256": _sha256(OUT_BINARY),
            "lee_d20_ready_sha256": _sha256(LEE_READY),
            "lee_d20_rows": 437,
        },
        "metrics_computed": False,
        "gate": "READY_FOR_V01_BINARY_METRICS",
    }
    OUT_AUDIT.mkdir(parents=True, exist_ok=True)
    report_path = OUT_AUDIT / "D21_PROMOTION_INTEGRITY_REPORT.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    # Update counts JSON status fields (derived audit)
    counts_path = OUT_AUDIT / "NEGATIVE_UNIVERSE_COUNTS.json"
    if counts_path.exists():
        prev = json.loads(counts_path.read_text(encoding="utf-8"))
        prev["review_status"] = "READY"
        prev["outcome_proposal"] = "D21_APPROVED_FOR_PRIMARY_BINARY_VALIDATION"
        prev["primary_binary_positive"] = stats["primary_binary_positive"]
        prev["primary_binary_negative"] = stats["primary_binary_negative"]
        prev["primary_binary_total"] = stats["primary_binary_total"]
        prev["ready_artifact"] = str(OUT_READY.relative_to(ROOT))
        prev["binary_universe_artifact"] = str(OUT_BINARY.relative_to(ROOT))
        counts_path.write_text(json.dumps(prev, indent=2), encoding="utf-8")

    print("Wrote", OUT_READY, "rows", len(ready))
    print("Wrote", OUT_BINARY, "rows", len(binary_out))
    print("Wrote", report_path)
    print("labels:", ready["experimental_label"].value_counts().to_dict())
    print(
        "binary:",
        binary_out["experimental_label"].value_counts().to_dict(),
        "total",
        len(binary_out),
    )
    print("integrity:", checks)
    print("gate: READY_FOR_V01_BINARY_METRICS")
    print("metrics_computed: False")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
