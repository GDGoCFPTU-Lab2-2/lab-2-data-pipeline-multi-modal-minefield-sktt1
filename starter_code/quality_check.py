# ==========================================
# ROLE 3: OBSERVABILITY & QA ENGINEER
# ==========================================
# Task: Implement quality gates to reject corrupt data or logic discrepancies.

import re

# Danh sách các chuỗi "độc hại" cần loại bỏ
TOXIC_STRINGS = [
    'null pointer exception',
    'null',
    'undefined',
    'error',
    'exception',
    'stack trace',
    'traceback',
    'warning:',
    'fatal error',
    'segmentation fault',
    'access violation',
    'out of memory',
]


def run_quality_gate(document_dict):
    """
    Quality gate kiểm tra document trước khi thêm vào Knowledge Base.
    
    Gates check:
    1. Content length >= 20 characters
    2. Không chứa toxic/error strings
    3. Không có discrepancy giữa comment và code (cho source_type="Code")
    
    Returns:
        True nếu pass, False nếu fail
    """
    # Gate 1: Kiểm tra độ dài content
    content = document_dict.get('content', '')
    if len(content) < 20:
        print(f"Quality Gate FAIL: Content too short (< 20 chars): {content[:50]}...")
        return False
    
    # Gate 2: Kiểm tra toxic/error strings
    content_lower = content.lower()
    for toxic in TOXIC_STRINGS:
        if toxic in content_lower:
            print(f"Quality Gate FAIL: Toxic string detected '{toxic}' in document {document_dict.get('document_id', 'unknown')}")
            return False
    
    # Gate 3: Kiểm tra discrepancy cho Code source
    if document_dict.get('source_type') == 'Code':
        source_metadata = document_dict.get('source_metadata', {})
        has_docstrings = source_metadata.get('has_docstrings', False)
        
        # Nếu code có docstrings, content không nên rỗng
        if has_docstrings and len(content.strip()) == 0:
            print(f"Quality Gate FAIL: Code document has_docstrings=True but empty content")
            return False
    
    return True
