import ast
import re

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract docstrings and comments from legacy Python code.

def extract_logic_from_code(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        source_code = f.read()
    # ------------------------------------------
    
    docs = []
    
    try:
        tree = ast.parse(source_code)
    except:
        return {}
        
    docstrings = []
    
    # Module docstring
    module_doc = ast.get_docstring(tree)
    if module_doc: docstrings.append(f"Module: {module_doc}")
        
    # Function docstrings
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_doc = ast.get_docstring(node)
            if func_doc: docstrings.append(f"Function {node.name}: {func_doc}")
            
    content = "\n\n".join(docstrings)
    
    # Find business rules in comments
    business_rules = re.findall(r'#.*Business Logic Rule.*', source_code, re.IGNORECASE)
    if business_rules:
        content += "\nRules:\n" + "\n".join(business_rules)
        
    return {
        "document_id": "code-legacy-pipeline",
        "content": content,
        "source_type": "Code",
        "author": "Senior Dev",
        "timestamp": None,
        "source_metadata": {
            "has_docstrings": len(docstrings) > 0
        }
    }
