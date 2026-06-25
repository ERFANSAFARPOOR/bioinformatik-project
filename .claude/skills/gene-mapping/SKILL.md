---
name: gene-mapping
description: Build/maintain the reproducible mapping between model (PAO1) gene IDs, PAO1 and PA14 locus tags, gene names, ortholog groups, and UniProt. Trigger when asked to map genes, reconcile strains, or join experimental gene lists to model IDs.
---

# Gene mapping (PAO1 model <-> PA14 experiments)

## Trigger
Asked to map/translate gene identifiers, reconcile PAO1 vs PA14, build ortholog
tables, or join experimental gene lists to model gene IDs.

## Inputs
- Model genes (1054 PAO1 `PAxxxx` locus tags) → `data/processed/gene_mapping.csv`
- Authoritative ortholog source (e.g. pseudomonas.com ortholog table, or
  study-provided PAO1-homolog columns), downloaded with provenance
- Experimental gene lists from `literature_evidence.csv`

## Ordered workflow
1. Start from the identity layer: model_gene_id == PAO1 locus_tag (confidence high).
2. Obtain a sourced PAO1↔PA14 ortholog mapping; record source + version + date.
3. Join PA14 locus tags, gene names, ortholog groups, UniProt — each with
   `mapping_source` and `mapping_confidence`.
4. Retain and explicitly flag one-to-many, many-to-one, and missing mappings;
   never silently drop or collapse them.
5. Produce a coverage report: mapped, unmapped, ambiguous, and
   present-in-model-but-no-GPR genes.

## Validation requirements
- Every mapped row cites its source and a confidence level.
- Round-trip spot checks (PAO1→PA14→PAO1) for a sample agree with the source.
- Counts of ambiguous/missing are reported, not hidden.

## Prohibited behavior
- Assuming PAO1 and PA14 IDs are interchangeable.
- Inventing orthologs or filling gaps with guesses.
- Editing raw ortholog downloads in place.

## Expected outputs
Updated `data/processed/gene_mapping.csv` (PA14/name/ortholog/UniProt populated),
a coverage/ambiguity report, provenance entries, blockers updated (B-MAP-01).
