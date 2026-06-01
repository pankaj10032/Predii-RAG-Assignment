import json
import re
from pathlib import Path
import pdfplumber


def clean_text(text):
    """
    Clean extracted text
    
    Args:
        text: Raw text
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def table_to_markdown(table):
    """
    Convert extracted table to Markdown format
    
    Args:
        table: Extracted table data
        
    Returns:
        Markdown formatted table
    """
    if not table or len(table) == 0:
        return ""
    md = []
    header = [str(col).strip() if col else "" for col in table[0]]
    md.append("| " + " | ".join(header) + " |")
    md.append("| " + " | ".join("---" for _ in header) + " |")
    for row in table[1:]:
        cleaned = [str(cell).strip().replace("\n", " ") if cell else "" for cell in row]
        md.append("| " + " | ".join(cleaned) + " |")
    return "\n".join(md)


def extract_and_chunk_pdf(pdf_path, output_dir="chunks"):
    """
    Extract text and tables from PDF and create semantic chunks
    
    Args:
        pdf_path: Path to PDF file
        output_dir: Output directory for chunks
        
    Returns:
        List of chunks
    """
    chunks = []
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            print(f"Processing page {page_num}...")
            
            full_page_text = clean_text(page.extract_text() or "")
            
            tables = page.extract_tables()
            for idx, table in enumerate(tables):
                if table and len(table) > 1:
                    md_table = table_to_markdown(table)
                    chunk = {
                        "chunk_id": len(chunks) + 1,
                        "page": page_num,
                        "type": "table",
                        "parent_section": "Suspension System Manual",
                        "section": f"Table on Page {page_num}",
                        "content": f"**Table {idx+1} - Page {page_num}**\n\n{md_table}",
                        "metadata": {
                            "doc_type": "workshop_manual",
                            "topic": "suspension_diagnosis",
                            "has_table": True
                        }
                    }
                    chunks.append(chunk)
            
            text = page.extract_text() or ""
            if text.strip():
                section_pattern = r'(?=(Symptom Chart|Pinpoint Test|Ride Height Measurement|Inspection and Verification|Visual Inspection Chart|Ball Joint Inspection|Camber and Caster Adjustment|Component Tests))'
                sections = re.split(section_pattern, text, flags=re.IGNORECASE)
                
                current_parent = "General"
                for i, section in enumerate(sections):
                    if not section.strip():
                        continue
                    cleaned = clean_text(section)
                    if len(cleaned) < 50:
                        continue
                        
                    if re.match(section_pattern, section):
                        current_parent = section.strip()[:100]
                    
                    chunk = {
                        "chunk_id": len(chunks) + 1,
                        "page": page_num,
                        "type": "text",
                        "parent_section": current_parent,
                        "section": current_parent,
                        "content": cleaned,
                        "metadata": {
                            "doc_type": "workshop_manual",
                            "topic": "suspension_diagnosis",
                            "has_table": False
                        }
                    }
                    chunks.append(chunk)
    
    json_path = output_path / "suspension_chunks.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)
    
    for chunk in chunks:
        md_content = f"""# {chunk['section']}
**Page:** {chunk['page']} | **Type:** {chunk['type']} | **Parent:** {chunk['parent_section']}

{chunk['content']}

---
"""
        md_path = output_path / f"chunk_{chunk['chunk_id']:03d}_p{chunk['page']}_{chunk['type']}.md"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
    
    print(f"\n Advanced Chunking Complete!")
    print(f"Total Chunks: {len(chunks)}")
    print(f"Saved to: {output_path.resolve()}")
    print(f"JSON: suspension_chunks.json (with metadata)")
    
    return chunks
