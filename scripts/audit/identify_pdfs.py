"""Identify PDFs by extracting embedded metadata/text using only stdlib.

Read-only. Decompresses FlateDecode streams and scans for title/DOI/author.
"""
import re
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PDF_DIR = ROOT / "conditian"

def printable_runs(data: bytes, minlen=6):
    return re.findall(rb"[\x20-\x7e]{%d,}" % minlen, data)

def extract(path: Path):
    raw = path.read_bytes()
    info = {"file": path.name, "size": len(raw)}

    # XMP / Info dictionary text (uncompressed)
    text_blobs = [raw]
    # Decompress all FlateDecode streams
    for m in re.finditer(rb"stream\r?\n", raw):
        start = m.end()
        end = raw.find(b"endstream", start)
        if end == -1:
            continue
        chunk = raw[start:end]
        try:
            text_blobs.append(zlib.decompress(chunk))
        except Exception:
            pass

    big = b"\n".join(text_blobs)

    # DOI
    dois = sorted(set(re.findall(rb"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+", big)))
    # clean trailing junk
    dois = [d.decode(errors="ignore").rstrip(").;,") for d in dois]
    info["dois"] = dois[:8]

    # XMP dc:title
    titles = re.findall(rb"<dc:title>.*?</dc:title>", big, re.S)
    info["xmp_title"] = [t.decode(errors="ignore") for t in titles][:2]

    # PDF Info /Title and /Author
    for key in (b"Title", b"Author", b"Subject"):
        mm = re.search(rb"/%s\s*\(((?:[^()\\]|\\.)*)\)" % key, raw)
        if mm:
            info[key.decode().lower()] = mm.group(1).decode("latin-1", errors="ignore")
        # UTF-16 hex form
        mh = re.search(rb"/%s\s*<([0-9A-Fa-f]+)>" % key, raw)
        if mh and key.decode().lower() not in info:
            try:
                info[key.decode().lower()] = bytes.fromhex(mh.group(1).decode()).decode("utf-16-be", errors="ignore")
            except Exception:
                pass

    # First readable text run mentioning Pseudomonas / aeruginosa / essential
    runs = printable_runs(big, 12)
    hits = [r.decode(errors="ignore") for r in runs
            if re.search(rb"aeruginosa|essential|Pseudomonas|cystic|sputum|growth arrest|fitness", r, re.I)]
    info["context_hits"] = hits[:6]
    return info

for p in sorted(PDF_DIR.glob("*.pdf")):
    info = extract(p)
    print("=" * 70)
    print("FILE:", info["file"], f"({info['size']} bytes)")
    print("TITLE(info):", info.get("title"))
    print("AUTHOR(info):", info.get("author"))
    print("SUBJECT:", info.get("subject"))
    print("XMP TITLE:", info.get("xmp_title"))
    print("DOIs:", info.get("dois"))
    print("CONTEXT:")
    for h in info["context_hits"]:
        print("   -", h[:160])
