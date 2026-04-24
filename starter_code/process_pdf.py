import google.generativeai as genai
import os
import json
import time
from dotenv import load_dotenv

# Load biến môi trường từ .env
load_dotenv()

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Use Gemini API to extract structured data from lecture_notes.pdf

def extract_pdf_data(file_path):
    # --- FILE CHECK (Handled for students) ---
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return None
    # ------------------------------------------

    # Lấy API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Lỗi: GEMINI_API_KEY chưa được set trong file .env")
        return None

    # Khởi tạo Gemini
    genai.configure(api_key=api_key)
    
    try:
        # Upload file
        pdf_file = genai.upload_file(path=file_path)
        
        # Sử dụng model gemini-1.5-flash
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = """
        Extract the Title, Author, and a 3-sentence summary from this document.
        Return the result strictly as a valid JSON object with keys "Title", "Author", and "Summary".
        Do not add Markdown formatting like ```json.
        """
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = model.generate_content([pdf_file, prompt])
                
                # Parse JSON
                text = response.text.strip()
                if text.startswith("```json"): text = text[7:]
                if text.endswith("```"): text = text[:-3]
                text = text.strip()
                
                data = json.loads(text)
                title = data.get("Title", "Unknown Title")
                author = data.get("Author", "Unknown Author")
                summary = data.get("Summary", "")
                
                # Xóa file sau khi query để tránh lưu tạm trên Google server
                genai.delete_file(pdf_file.name)
                
                # Trả về format UnifiedDocument
                return {
                    "document_id": "pdf-lecture-notes",
                    "content": f"Title: {title}\nSummary: {summary}",
                    "source_type": "PDF",
                    "author": author,
                    "timestamp": None,
                    "source_metadata": {"title": title}
                }
                
            except Exception as e:
                # Xử lý Retry nếu gặp 429 Too Many Requests
                if '429' in str(e):
                    print(f"Rate limited. Retrying {attempt + 1}/{max_retries}...")
                    time.sleep(2 ** attempt)
                else:
                    raise e
                    
    except Exception as e:
        print(f"Lỗi extract PDF: {e}")
        
    return None
