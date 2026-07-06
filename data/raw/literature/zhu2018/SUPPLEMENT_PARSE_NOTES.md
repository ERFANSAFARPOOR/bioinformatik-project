# SUPPLEMENT_PARSE_NOTES — zhu2018

- **study_id:** zhu2018
- **citation:** **PENDING_VERIFY** — GigaScience manuscript `GIGA-D-17-00272` /
  `giy021`; genome-scale metabolic **reconstruction** of *P. aeruginosa* PAO1
  (model **iPAO1**), with lipid A / LPS / polymyxin focus. Likely DOI
  10.1093/gigascience/giy021, PMCID PMC6333913 — **verify before citing.**
- **strain:** PAO1 (as an *in silico* model, iPAO1).
- **phenotype class(es):** **N/A** — this is a modeling paper, not an experimental
  essentiality/fitness screen.

## Files inspected
- Manuscript PDFs: `GIGA-D-17-00272_Original_Submission.pdf`, `…_Revision_1.pdf`;
  4 review/response PDFs; `giy021_supp/additionalFile1.docx`.
- `giy021_supp/additionalFile2–27.xlsx` = Datasets EV1–EV26: reconstruction artifacts
  (draft/final metabolites, reactions, genes of iPAO1; biomass formula; lipid A / LPS
  randomised-stoichiometry and flux analyses; polymyxin-response fluxes; turnover rates).
- `additionalFile17.xlsx` (EV16) = "Genes in model iPAO1".
- `additionalFile19.xlsx` (EV18) = "Comparison of predicted gene essentiality with
  transposon insertion mutant libraries" — a **model-derived** comparison, NOT an
  independent experimental label set.

## Classification & relevance
**Background / competing PAO1 reconstruction — out of scope for L-03 experimental
label extraction.** iPAO1 is *another metabolic model*, not an experimental
essentiality dataset. `additionalFile19`'s "experimental" side is itself drawn from
the same Tn-seq libraries we ingest directly (Lee/Turner), so using it would double-count.

## Direct PAO1 mapping status
Model gene IDs are PAO1 `PAxxxx` (iPAO1), but this is a *model*, so mapping is moot for
experimental validation.

## Uncertainty notes
- DOI/PMCID `PENDING_VERIFY`.
- Do not treat any zhu2018 sheet as an experimental essentiality label source.

## Parse-readiness
**NOT_RELEVANT_FOR_L03.** Files retained, provenance logged, no extraction planned.

## Extraction plan (next script)
None for L-03. **Optional future task (separate, model-vs-model):** compare iMO1056
predicted essentiality against iPAO1 (`additionalFile17` genes, `additionalFile16`
reactions) as a reconstruction cross-check — this is NOT experimental validation and
must never be reported as precision/recall against experiment.
