from bs4 import BeautifulSoup

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract product data from the HTML table, ignoring boilerplate.

def parse_html_catalog(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    # ------------------------------------------
    
    docs = []
    
    # Tìm bảng có id main-catalog
    table = soup.find('table', id='main-catalog')
    if not table: return docs
        
    tbody = table.find('tbody')
    for row in tbody.find_all('tr'):
        cols = row.find_all('td')
        if len(cols) >= 5:
            product_id = cols[0].text.strip()
            name = cols[1].text.strip()
            category = cols[2].text.strip()
            price_str = cols[3].text.strip().lower()
            stock_str = cols[4].text.strip()
            
            # Xử lý giá 'N/A' hoặc 'Liên hệ'
            price = None
            if price_str not in ['n/a', 'liên hệ']:
                clean_price = price_str.replace('vnd', '').replace(',', '').strip()
                try: price = float(clean_price)
                except: pass
                
            try: stock = int(stock_str)
            except: stock = 0
            
            docs.append({
                "document_id": f"html-{product_id}",
                "content": f"Product: {name} in {category}",
                "source_type": "HTML",
                "author": "VinShop",
                "timestamp": None,
                "source_metadata": {
                    "product_name": name,
                    "price": price,
                    "stock": stock
                }
            })
            
    return docs
