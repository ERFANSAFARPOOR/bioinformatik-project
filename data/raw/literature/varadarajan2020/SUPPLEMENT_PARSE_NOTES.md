# SUPPLEMENT_PARSE_NOTES — varadarajan2020

- **study_id:** varadarajan2020
- **citation:** **PENDING_VERIFY** — MPAO1 comparative-genomics + Tn-seq essentiality
  study (author "Varadarajan" inferred from filenames; **DOI/PMID not yet verified**).
  Do NOT cite until confirmed via CrossRef/NCBI. This is a NEW study, not in the
  original 6-paper corpus.
- **strain:** **MPAO1** (locus tags `MPAO1_xxxxx`; PAO1 `PAxxxx` provided as a
  best-blast-hit mapping inside the same supplement).
- **phenotype class(es):** **generally-essential** + **condition-specific-essential**
  (LB / minimal / sputum / human serum).

## Files inspected
- `Supplementary Dataset 1 (MPAO1).xlsx` (1,581,884 B) — sheet `MPAO1_CDS`: MPAO1 gene
  catalog + comparative genomics vs PAO1 (`PAO1_gene_name`, best-hit). **Mapping source.**
- `Supplementary Dataset 2 (MPAO1).xlsx` (31,549 B) — sheet `TableS3`: MPAO1-vs-PAO1-UW
  SNP/INDEL variant table. **NOT_RELEVANT** for essentiality labels.
- `Supplementary Dataset 3 (MPAO1).xlsx` (1,381,986 B) — sheets `Core_CDS_MPAO1_PAO1`,
  `Unique_MPAO1_CDS`, `Unique_PAO1_CDS`: CDS with `essential?` flag + PAO1 mapping.
- `Supplementary Dataset 4 (MPAO1).xlsx` (62,800 B) — sheet `essentialGenes_MPAO1`:
  **per-condition essentiality matrix**. **Primary label source.**
- 2 PDFs (Supplementary Information, Reporting Summary) — context only.

## Column layout
- **DS4 `essentialGenes_MPAO1`** (header on **row index 0**): `Locus` |
  `Essential in x/16 samples` | `LB-1_Rep1` | `LB-1_Rep2` | `LB-1_Rep3` | `LB-2_Rep1` |
  `LB-2_Rep2` | `Minimal-1` | `Minimal-2` | `Minimal-3` | `Sputum-1..4` | `HumanSerum`.
  Cell = `1` (essential in that sample) or blank.
- **DS1 `MPAO1_CDS` / DS3 `Core_CDS_MPAO1_PAO1`** (header on row index 1, group row 0):
  `locus_tag` (MPAO1) | start | end | … | `best_hit protein` | `PAO1_gene_name` |
  `essential?` (DS3) — provides the **MPAO1 → PAO1** join.

## Likely columns
- **gene ID / locus tag:** `Locus` / `locus_tag` = `MPAO1_xxxxx`.
- **PAO1 mapping:** `best_hit protein` / `PAO1_gene_name` (DS1, DS3) = PAO1 `PAxxxx`.
- **strain:** none (MPAO1 constant).
- **condition / media:** DS4 replicate columns grouped by `LB` / `Minimal` / `Sputum`
  / `HumanSerum`.
- **essentiality:** DS4 per-sample `1`; `Essential in x/16 samples` aggregate; DS3
  `essential?` boolean.
- **threshold / statistics:** essential-in-N-of-16-samples; per-condition essentiality
  = essential across that condition's replicates. Exact cutoff per paper methods.

## Direct PAO1 mapping status
**INDIRECT** — MPAO1 locus tags, mapped to PAO1 via the in-supplement best-hit columns
(DS1/DS3). More reliable than cross-strain orthology (MPAO1 is a PAO1 sublineage), but
still a mapping step: **retain one-to-many and missing mappings** (project rule 3).

## Source-locator strategy
`source_file` + `source_sheet` + `source_row` + `Locus` (MPAO1) + mapped `PAO1` tag.

## Uncertainty notes
- **Citation unverified** — must confirm DOI/PMID before any use.
- MPAO1→PAO1 mapping must be built + validated (one-to-many / missing handled).
- MPAO1 differs from PAO1-UW at some loci (DS2 SNP/INDEL table) — flag mapped genes
  that fall on divergent loci.

## Parse-readiness
**NEEDS_HUMAN_REVIEW** — structurally strong (clear gene + condition + essentiality
columns and an in-supplement PAO1 map), but blocked on (a) citation verification and
(b) validated MPAO1→PAO1 mapping. Becomes READY_FOR_L03_PARSE once both are resolved.

## Extraction plan (next script)
1. **First** verify the DOI/PMID/citation.
2. Build MPAO1→PAO1 map from DS1/DS3 `best_hit`/`PAO1_gene_name` (retain ambiguity/missing).
3. Parse DS4 per-condition essentiality (LB/Minimal/Sputum/HumanSerum kept separate).
4. Map MPAO1→PAO1; emit rows with both IDs, condition, phenotype class, source locator;
   mark unmapped/ambiguous as `NEEDS_REVIEW`. No binary collapse across conditions.
