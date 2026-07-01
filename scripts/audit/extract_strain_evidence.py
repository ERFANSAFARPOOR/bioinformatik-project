"""Read-only strain/method evidence extractor for the literature PDFs.

Decompresses FlateDecode streams (stdlib only), reconstructs approximate text,
and reports context windows around strain / method / medium keywords so the
paper strain classification is evidence-based, not assumed.
"""
import re
import sys
import zlib
from pathlib import Path

PDF_DIR = Path("conditian")

# Keyword groups we care about for the PAO1-focus re-audit
KEYS = [
    r"PAO1", r"MPAO1", r"PA14", r"UCBPP-?PA14", r"PA103", r"PAK",
    r"transposon", r"Tn-?seq", r"TnSeq", r"TraDIS", r"mutant librar",
    r"sputum", r"SCFM", r"cystic fibrosis", r"LB\b", r"minimal medium",
    r"essential", r"fitness", r"insertion sequencing", r"CRISPRi",
    r"two-allele", r"Manoil", r"strain",
]
KEY_RE = re.compile("|".join(KEYS), re.I)


def pdf_text(path: Path) -> str:
    raw = path.read_bytes()
    blobs = []
    for m in re.finditer(rb"stream\r?\n", raw):
        start = m.end()
        end = raw.find(b"endstream", start)
        if end == -1:
            continue
        try:
            blobs.append(zlib.decompress(raw[start:end]))
        except Exception:
            pass
    big = b"\n".join(blobs)
    # Pull text shown by Tj / TJ operators: (...) Tj  and  [(..)..] TJ
    parens = re.findall(rb"\(((?:[^()\\]|\\.)*)\)", big)
    text = " ".join(p.decode("latin-1", errors="ignore") for p in parens)
    # collapse whitespace
    text = re.sub(r"\s+", " ", text)
    return text


def report(path: Path):
    text = pdf_text(path)
    print("=" * 78)
    print(f"FILE: {path.name}  (chars extracted: {len(text)})")
    # count keyword hits
    counts = {}
    for k in ["PAO1", "MPAO1", "PA14", "UCBPP", "sputum", "SCFM", "transposon",
              "Tn-seq", "TnSeq", "TraDIS", "CRISPRi", "two-allele", "Manoil",
              "essential", "fitness"]:
        counts[k] = len(re.findall(re.escape(k), text, re.I))
    print("COUNTS:", {k: v for k, v in counts.items() if v})
    # context windows around first strain mentions
    for term in ["PAO1", "MPAO1", "UCBPP", "PA14", "strain "]:
        m = re.search(re.escape(term), text, re.I)
        if m:
            a = max(0, m.start() - 90)
            b = min(len(text), m.end() + 120)
            print(f"  [{term}] ...{text[a:b]}...")


if __name__ == "__main__":
    targets = sys.argv[1:]
    files = ([PDF_DIR / t for t in targets] if targets
             else sorted(PDF_DIR.glob("*.pdf")))
    for p in files:
        if p.exists():
            report(p)
        else:
            print("MISSING:", p)
