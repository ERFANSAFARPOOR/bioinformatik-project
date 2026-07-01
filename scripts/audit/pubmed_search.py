"""Read-only PubMed search via NCBI E-utilities for PAO1-focused literature.

Prints, per query: total count and the top hits (PMID, year, journal, title,
DOI, PMCID-if-open-access) so inclusion decisions are evidence-based. No writes.
"""
import json
import sys
import time
import urllib.parse
import urllib.request

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

QUERIES = [
    'Pseudomonas aeruginosa PAO1 essential genes Tn-seq',
    'Pseudomonas aeruginosa MPAO1 essential genes',
    'Pseudomonas aeruginosa PAO1 transposon sequencing fitness',
    'Pseudomonas aeruginosa PAO1 condition-specific essential genes',
    'Pseudomonas aeruginosa PAO1 genome-scale metabolic model',
    'Pseudomonas aeruginosa iMO1056',
    'Pseudomonas aeruginosa PAO1 FBA gene essentiality',
    'Pseudomonas aeruginosa PAO1 deletion library metabolic genes',
    'Pseudomonas aeruginosa PAO1 CRISPRi essential',
    'Pseudomonas aeruginosa PAO1 TraDIS',
]


def get(url):
    with urllib.request.urlopen(url, timeout=30) as r:
        return r.read().decode("utf-8", "ignore")


def esearch(term, retmax=6):
    q = urllib.parse.quote(term)
    url = f"{EUTILS}/esearch.fcgi?db=pubmed&term={q}&retmax={retmax}&sort=relevance&retmode=json"
    d = json.loads(get(url))["esearchresult"]
    return int(d.get("count", 0)), d.get("idlist", [])


def esummary(pmids):
    if not pmids:
        return {}
    url = f"{EUTILS}/esummary.fcgi?db=pubmed&id={','.join(pmids)}&retmode=json"
    return json.loads(get(url)).get("result", {})


def main():
    for term in QUERIES:
        try:
            count, ids = esearch(term)
        except Exception as e:
            print(f"### QUERY: {term}\n  ERROR: {e}")
            continue
        print(f"### QUERY: {term}  (total={count})")
        res = esummary(ids)
        for pid in ids:
            it = res.get(pid, {})
            if not it:
                continue
            year = (it.get("pubdate", "") or "")[:4]
            jour = it.get("fulljournalname", it.get("source", ""))
            title = it.get("title", "").replace("\n", " ")
            doi = ""
            for aid in it.get("articleids", []):
                if aid.get("idtype") == "doi":
                    doi = aid.get("value", "")
            pmc = ""
            for aid in it.get("articleids", []):
                if aid.get("idtype") == "pmc":
                    pmc = aid.get("value", "")
            print(f"  - PMID {pid} | {year} | {jour} | {doi} | {pmc}")
            print(f"    {title}")
        print()
        time.sleep(0.4)


if __name__ == "__main__":
    main()
