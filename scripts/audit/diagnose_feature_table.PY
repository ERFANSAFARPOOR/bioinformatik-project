#!/usr/bin/env python3
"""
diagnose_feature_table.py

پیدا کردن دقیق خطی که باعث IndexError در parse_feature_table می‌شه.
این اسکریپت فایل feature table رو خط به خط چک می‌کنه و هر خطی که
تعداد ستون‌هاش با هدر مچ نشه رو گزارش می‌ده.

استفاده:
    python diagnose_feature_table.py data\\raw\\ortholog\\pao1_feature_table
    python diagnose_feature_table.py data\\raw\\ortholog\\pa14_feature_table
"""

import gzip
import io
import sys
from pathlib import Path


def open_table(stem: Path):
    txt = stem.with_suffix(".txt")
    if txt.exists():
        return open(txt, encoding="utf-8")
    gz = Path(str(stem) + ".txt.gz")
    return io.TextIOWrapper(gzip.open(gz, "rb"), encoding="utf-8")


def main():
    if len(sys.argv) < 2:
        print("استفاده: python diagnose_feature_table.py <مسیر بدون پسوند، مثل data/raw/ortholog/pao1_feature_table>")
        sys.exit(1)

    stem = Path(sys.argv[1])

    with open_table(stem) as f:
        header_line = f.readline()
        header = header_line.lstrip("#").rstrip("\r\n").split("\t")
        idx = {h: i for i, h in enumerate(header)}

        print(f"[i] تعداد ستون‌های هدر: {len(header)}")
        print(f"[i] ستون‌ها: {header}")

        if "attributes" not in idx:
            print("\n⚠️  ستون 'attributes' اصلاً توی هدر نیست! این ریشه‌ی اصلی مشکله.")
        else:
            print(f"[i] index ستون 'attributes' = {idx['attributes']}")

        bad_lines = []
        total_gene_lines = 0

        for line_num, line in enumerate(f, start=2):  # از خط ۲ چون خط ۱ هدر بود
            p = line.rstrip("\r\n").split("\t")
            if not p or p[0] != "gene":
                continue

            total_gene_lines += 1

            if "attributes" in idx and idx["attributes"] >= len(p):
                bad_lines.append((line_num, len(p), p))

        print(f"\n[i] تعداد کل خطوطی که ستون اول‌شون 'gene' بود: {total_gene_lines}")
        print(f"[i] تعداد خطوط مشکل‌دار (کمتر از تعداد ستون لازم): {len(bad_lines)}")

        if bad_lines:
            print("\n--- نمونه‌ی خطوط مشکل‌دار (حداکثر ۵ تا) ---")
            for line_num, n_cols, content in bad_lines[:5]:
                print(f"\n  خط {line_num}: تعداد ستون = {n_cols} (باید حداقل {idx.get('attributes', '?') + 1} باشه)")
                print(f"  محتوا: {content}")


if __name__ == "__main__":
    main()