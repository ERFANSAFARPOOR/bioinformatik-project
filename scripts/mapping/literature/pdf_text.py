"""Read-only stdlib PDF text extraction + keyword-context search.

No third-party deps (reccobra39 has no pdf library). Decompresses FlateDecode
streams and reconstructs approximate text from Tj/TJ operators. Approximate:
good enough to locate Methods threshold/definition statements; NOT a faithful
layout reproduction. Never modifies any file.

Usage:
    python scripts/literature/pdf_text.py <pdf_path>                # dump text
    python scripts/literature/pdf_text.py <pdf_path> <regex> [...]  # contexts
"""
import re
import sys
import zlib
from pathlib import Path


def pdf_text(path: Path) -> str:
    raw = Path(path).read_bytes()
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
    parens = re.findall(rb"\(((?:[^()\\]|\\.)*)\)", big)

    def dec(p: bytes) -> str:
        s = p.decode("latin-1", errors="ignore")
        return s.replace("\\(", "(").replace("\\)", ")").replace("\\\\", "\\")

    text = " ".join(dec(p) for p in parens)
    return re.sub(r"\s+", " ", text)


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python pdf_text.py <pdf_path>")
        print("  python pdf_text.py <pdf_path> <regex> [regex2 ...]")
        sys.exit(1)

    p = Path(sys.argv[1])

    if not p.exists():
        print(f"PDF not found: {p}")
        sys.exit(1)

    terms = sys.argv[2:]

    text = pdf_text(p)

    sys.stderr.write(f"[{p.name}: {len(text)} chars extracted]\n")

    if not terms:
        print(text)
    else:
        for term in terms:
            print("=" * 72)
            print(f"TERM: {term}")

            hits = list(re.finditer(term, text, re.I))

            if not hits:
                print("  (no match)")
                continue

            for m in hits:
                a = max(0, m.start() - 260)
                b = min(len(text), m.end() + 360)

                print(f"...{text[a:b]}...")
                print("-" * 40)