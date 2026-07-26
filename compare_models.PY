#!/usr/bin/env python3
"""
compare_models.py

مقایسه‌ی دو فایل مدل متابولیک SBML (.xml) بدون نیاز به نصب کتابخونه‌ی cobra.
این اسکریپت مستقیم XML رو می‌خونه و موارد زیر رو مقایسه می‌کنه:
  - تعداد reactions
  - تعداد species (متابولیت‌ها)
  - تعداد genes (از gene products یا notes)
  - لیست ID هایی که فقط در یکی از دو فایل هستن (نه هر دو)

استفاده:
    python compare_models.py "models\\paeruginosa_MODEL1507180020.xml" "models\\raw\\paeruginosa_MODEL1507180020.xml"
"""

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def strip_ns(tag: str) -> str:
    """حذف namespace از تگ XML، مثلا {http://...}reaction -> reaction"""
    return tag.split("}")[-1] if "}" in tag else tag


def parse_model(path: Path):
    """
    پارس یک فایل SBML و استخراج شناسه‌های reactions, species, و genes.
    برمی‌گردونه: dict با کلیدهای 'reactions', 'species', 'genes' -> هرکدوم یک set از id ها
    """
    reactions = set()
    species = set()
    genes = set()

    try:
        tree = ET.parse(path)
    except ET.ParseError as e:
        print(f"[✗] خطا در پارس {path}: {e}", file=sys.stderr)
        return None

    root = tree.getroot()

    for elem in root.iter():
        tag = strip_ns(elem.tag)
        elem_id = elem.get("id")

        if tag == "reaction" and elem_id:
            reactions.add(elem_id)
        elif tag == "species" and elem_id:
            species.add(elem_id)
        elif tag == "geneProduct" and elem_id:
            # فرمت SBML-FBC v2: geneProduct های جدا
            genes.add(elem_id)

    # اگر مدل قدیمی‌تره و geneProduct نداره، از notes/تگ GENE_ASSOCIATION استخراج کن
    if not genes:
        text_dump = ET.tostring(root, encoding="unicode")
        gene_matches = re.findall(r"GENE_ASSOCIATION:\s*([^<\n]+)", text_dump)
        gene_ids = set()
        for match in gene_matches:
            # جدا کردن اسامی ژن از عبارات boolean مثل "(geneA and geneB) or geneC"
            found = re.findall(r"[A-Za-z0-9_.\-]+", match)
            gene_ids.update(g for g in found if g.lower() not in ("and", "or"))
        genes = gene_ids

    return {"reactions": reactions, "species": species, "genes": genes}


def compare(name_a: str, data_a: dict, name_b: str, data_b: dict):
    print("\n" + "=" * 70)
    print("نتیجه‌ی مقایسه")
    print("=" * 70)

    for category in ["reactions", "species", "genes"]:
        set_a = data_a[category]
        set_b = data_b[category]

        only_a = set_a - set_b
        only_b = set_b - set_a
        common = set_a & set_b

        print(f"\n--- {category} ---")
        print(f"  {name_a}: {len(set_a)} مورد")
        print(f"  {name_b}: {len(set_b)} مورد")
        print(f"  مشترک: {len(common)} مورد")

        if only_a:
            sample = sorted(only_a)[:10]
            print(f"  ⚠️  فقط در {name_a} هست ({len(only_a)} مورد), نمونه: {sample}")
        if only_b:
            sample = sorted(only_b)[:10]
            print(f"  ⚠️  فقط در {name_b} هست ({len(only_b)} مورد), نمونه: {sample}")
        if not only_a and not only_b:
            print(f"  ✅ کاملاً یکسان")


def main():
    parser = argparse.ArgumentParser(description="مقایسه‌ی دو فایل مدل SBML")
    parser.add_argument("file_a", help="مسیر فایل مدل اول")
    parser.add_argument("file_b", help="مسیر فایل مدل دوم")
    args = parser.parse_args()

    path_a = Path(args.file_a)
    path_b = Path(args.file_b)

    for p in (path_a, path_b):
        if not p.exists():
            print(f"[✗] فایل پیدا نشد: {p}", file=sys.stderr)
            sys.exit(1)

    print(f"[i] در حال پارس کردن: {path_a}")
    data_a = parse_model(path_a)
    print(f"[i] در حال پارس کردن: {path_b}")
    data_b = parse_model(path_b)

    if data_a is None or data_b is None:
        sys.exit(1)

    compare(str(path_a), data_a, str(path_b), data_b)

    print("\n" + "=" * 70)
    print("جمع‌بندی")
    print("=" * 70)
    diffs = []
    for category in ["reactions", "species", "genes"]:
        if data_a[category] != data_b[category]:
            diffs.append(category)

    if diffs:
        print(f"⚠️  این دو فایل در موارد زیر فرق دارن: {', '.join(diffs)}")
        print("    توصیه: مشخص کنید کدوم نسخه در کد (src/load_model.py, src/config.py) استفاده می‌شه،")
        print("    و اون رو به عنوان نسخه‌ی رسمی (source of truth) نگه دارید.")
    else:
        print("✅ از نظر محتوای reactions/species/genes یکسان هستن؛ تفاوت حجم فایل احتمالاً")
        print("   به خاطر فرمت‌بندی (whitespace, ترتیب تگ‌ها، متادیتا) هست، نه محتوای علمی مدل.")


if __name__ == "__main__":
    main()