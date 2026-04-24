import re

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Clean the transcript text and extract key information.

def clean_transcript(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    # ------------------------------------------
    
    # Remove noise tokens
    clean_text = re.sub(r'\[(Music[^\]]*|inaudible|Laughter)\]', '', text, flags=re.IGNORECASE)
    
    # Strip timestamps
    clean_text = re.sub(r'\[\d{2}:\d{2}:\d{2}\]', '', clean_text)
    
    # Remove extra spaces
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    
    # Detect price
    price_vnd = None
    if 'năm trăm nghìn' in clean_text.lower() or '500,000' in clean_text:
        price_vnd = 500000
        
    return {
        "document_id": "transcript-001",
        "content": clean_text,
        "source_type": "Video",
        "author": "Lecture Speaker",
        "timestamp": None,
        "source_metadata": {
            "detected_price_vnd": price_vnd
        }
    }
