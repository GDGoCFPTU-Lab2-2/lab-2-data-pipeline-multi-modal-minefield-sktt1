import json
import time
import os
import sys

# Robust path handling
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DATA_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "raw_data")

# Fix Unicode output on Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


# Import role-specific modules
from schema import UnifiedDocument
from process_pdf import extract_pdf_data
from process_transcript import clean_transcript
from process_html import parse_html_catalog
from process_csv import process_sales_csv
from process_legacy_code import extract_logic_from_code
from quality_check import run_quality_gate

# ==========================================
# ROLE 4: DEVOPS & INTEGRATION SPECIALIST
# ==========================================
# Task: Orchestrate the ingestion pipeline and handle errors/SLA.

def main():
    start_time = time.time()
    final_kb = []
    failed_docs = []
    
    # --- FILE PATH SETUP (Handled for students) ---
    pdf_path = os.path.join(RAW_DATA_DIR, "lecture_notes.pdf")
    trans_path = os.path.join(RAW_DATA_DIR, "demo_transcript.txt")
    html_path = os.path.join(RAW_DATA_DIR, "product_catalog.html")
    csv_path = os.path.join(RAW_DATA_DIR, "sales_records.csv")
    code_path = os.path.join(RAW_DATA_DIR, "legacy_pipeline.py")
    
    output_path = os.path.join(os.path.dirname(SCRIPT_DIR), "processed_knowledge_base.json")
    # ----------------------------------------------

    print("=" * 50)
    print("Starting Data Pipeline...")
    print("=" * 50)

    # --- Process PDF ---
    print("\n[1/5] Processing PDF...")
    try:
        doc = extract_pdf_data(pdf_path)
        if doc and run_quality_gate(doc):
            final_kb.append(doc)
            print(f"   [OK] PDF added: {doc['document_id']}")
        else:
            failed_docs.append({"id": "pdf-lecture-notes", "reason": "Failed quality gate"})
            print(f"   [FAIL] PDF failed quality gate")
    except Exception as e:
        print(f"   [ERROR] PDF error: {e}")
        failed_docs.append({"id": "pdf-lecture-notes", "reason": str(e)})

    # --- Process Transcript ---
    print("\n[2/5] Processing Transcript...")
    try:
        doc = clean_transcript(trans_path)
        if doc and run_quality_gate(doc):
            final_kb.append(doc)
            print(f"   [OK] Transcript added: {doc['document_id']}")
        else:
            failed_docs.append({"id": "transcript-001", "reason": "Failed quality gate"})
            print(f"   [FAIL] Transcript failed quality gate")
    except Exception as e:
        print(f"   [ERROR] Transcript error: {e}")
        failed_docs.append({"id": "transcript-001", "reason": str(e)})

    # --- Process HTML ---
    print("\n[3/5] Processing HTML Catalog...")
    try:
        docs = parse_html_catalog(html_path)
        for doc in docs:
            if run_quality_gate(doc):
                final_kb.append(doc)
                print(f"   [OK] HTML product added: {doc['document_id']}")
            else:
                failed_docs.append({"id": doc['document_id'], "reason": "Failed quality gate"})
        print(f"   [OK] HTML: {len(docs)} products processed")
    except Exception as e:
        print(f"   [ERROR] HTML error: {e}")

    # --- Process CSV ---
    print("\n[4/5] Processing Sales CSV...")
    try:
        docs = process_sales_csv(csv_path)
        for doc in docs:
            if run_quality_gate(doc):
                final_kb.append(doc)
                print(f"   [OK] CSV record added: {doc['document_id']}")
            else:
                failed_docs.append({"id": doc['document_id'], "reason": "Failed quality gate"})
        print(f"   [OK] CSV: {len(docs)} records processed")
    except Exception as e:
        print(f"   [ERROR] CSV error: {e}")

    # --- Process Legacy Code ---
    print("\n[5/5] Processing Legacy Code...")
    try:
        doc = extract_logic_from_code(code_path)
        if doc and run_quality_gate(doc):
            final_kb.append(doc)
            print(f"   [OK] Code added: {doc['document_id']}")
        else:
            failed_docs.append({"id": "code-legacy-pipeline", "reason": "Failed quality gate"})
            print(f"   [FAIL] Code failed quality gate")
    except Exception as e:
        print(f"   [ERROR] Code error: {e}")
        failed_docs.append({"id": "code-legacy-pipeline", "reason": str(e)})

    # --- Save to JSON ---
    print("\n" + "=" * 50)
    print("Saving Knowledge Base...")
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(final_kb, f, ensure_ascii=False, indent=2)
        print(f"[OK] Saved to: {output_path}")
    except Exception as e:
        print(f"[ERROR] Failed to save: {e}")

    # --- Summary ---
    end_time = time.time()
    print("\n" + "=" * 50)
    print("PIPELINE SUMMARY")
    print("=" * 50)
    print(f"Total processing time: {end_time - start_time:.2f} seconds")
    print(f"Total valid documents: {len(final_kb)}")
    print(f"Failed documents: {len(failed_docs)}")
    if failed_docs:
        print("\nFailed document IDs:")
        for d in failed_docs:
            print(f"  - {d['id']}: {d['reason']}")


if __name__ == "__main__":
    main()
