import pandas as pd

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Process sales records, handling type traps and duplicates.

def process_sales_csv(file_path):
    # --- FILE READING (Handled for students) ---
    df = pd.read_csv(file_path)
    # ------------------------------------------
    
    # 1. Remove duplicate rows based on 'id'
    df = df.drop_duplicates(subset=['id'], keep='first')
    
    # 2. Clean 'price' column v1
    def clean_price(val):
        if pd.isna(val) or val in ['N/A', 'NULL', 'Liên hệ']:
            return None
        val_str = str(val).lower().replace('$', '').replace(',', '').strip()
        if 'five dollars' in val_str:
            return 5.0
        try:
            return float(val_str)
        except ValueError:
            return None
            
    df['price'] = df['price'].apply(clean_price)
    
    # Bỏ qua dòng có price âm
    df = df[df['price'] >= 0]
    
    # 3. Normalize 'date_of_sale'
    def parse_date(date_str):
        if pd.isna(date_str): return None
        # Remove ordinals like 16th, 2nd
        date_str = str(date_str).replace('th', '').replace('nd', '').replace('st', '').replace('rd', '')
        try:
            return pd.to_datetime(date_str, format='mixed', dayfirst=True).strftime('%Y-%m-%d')
        except:
            return None
            
    df['date_of_sale'] = df['date_of_sale'].apply(parse_date)
    
    docs = []
    for _, row in df.iterrows():
        # Định nghĩa UnifiedDocument dict
        timestamp = f"{row['date_of_sale']}T00:00:00Z" if row['date_of_sale'] else None
        docs.append({
            "document_id": f"csv-{row['id']}",
            "content": f"Sản phẩm: {row['product_name']}, Danh mục: {row['category']}",
            "source_type": "CSV",
            "author": str(row['seller_id']) if pd.notna(row['seller_id']) else "Unknown",
            "timestamp": timestamp,
            "source_metadata": {
                "price": row['price'],
                "currency": row['currency'],
                "stock_quantity": row['stock_quantity'] if pd.notna(row['stock_quantity']) else 0
            }
        })
        
    return docs
