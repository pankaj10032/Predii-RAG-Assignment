import os
import json
import re
from pathlib import Path
import pdfplumber
from openai import OpenAI
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PDF_PATH = "sample-service-manual 1 (1).pdf"
CHUNKS_DIR = "chunks"
COLLECTION_NAME = "ford_f150_suspension"

client = OpenAI(api_key=OPENAI_API_KEY)

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=OPENAI_API_KEY,
    model_name="text-embedding-3-large"
)


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
    text = re.sub(r'\(cid:122\)', '', text)
    text = re.sub(r'\(cid:\d+\)', '', text)
    text = re.sub(r'file:///.*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def table_to_markdown(table):
    """
    Convert table to Markdown format

    Args:
        table: Table data

    Returns:
        Markdown formatted table
    """
    if not table or len(table) < 2:
        return ""
    md = []
    header = [str(col).strip() if col else "" for col in table[0]]
    md.append("| " + " | ".join(header) + " |")
    md.append("| " + "---|" * len(header))
    for row in table[1:]:
        cleaned_row = [str(cell).strip().replace("\n", " ") if cell else "" for cell in row]
        md.append("| " + " | ".join(cleaned_row) + " |")
    return "\n".join(md)


def extract_and_chunk_pdf():
    """
    Extract and chunk PDF

    Returns:
        List of chunks
    """
    chunks = []
    output_path = Path(CHUNKS_DIR)
    output_path.mkdir(exist_ok=True)

    with pdfplumber.open(PDF_PATH) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            print(f"Processing page {page_num}...")

            full_text = page.extract_text() or ""
            cleaned_full = clean_text(full_text)

            tables = page.extract_tables()
            for idx, table in enumerate(tables):
                if table and len(table) > 1:
                    md_table = table_to_markdown(table)
                    chunk = {
                        "chunk_id": len(chunks) + 1,
                        "page": page_num,
                        "type": "table",
                        "parent_section": "Suspension System Manual",
                        "section": f"Table Page {page_num}",
                        "content": f"Table on Page {page_num}\n\n{md_table}",
                        "metadata": {"doc_type": "ford_f150_manual", "topic": "suspension", "has_table": True}
                    }
                    chunks.append(chunk)

            if cleaned_full:
                pattern = r'(?=(Inspection and Verification|Visual Inspection Chart|Symptom Chart|Pinpoint Test|Ball Joint Inspection|Camber and Caster|Ride Height Measurement))'
                sections = re.split(pattern, full_text, flags=re.IGNORECASE)

                current_parent = "Suspension System"
                for section in sections:
                    cleaned = clean_text(section)
                    if len(cleaned) < 80:
                        continue
                    if re.search(pattern, section, re.IGNORECASE):
                        current_parent = clean_text(section.split('\n')[0])

                    chunk = {
                        "chunk_id": len(chunks) + 1,
                        "page": page_num,
                        "type": "text",
                        "parent_section": current_parent,
                        "section": current_parent,
                        "content": cleaned,
                        "metadata": {"doc_type": "ford_f150_manual", "topic": "suspension", "has_table": False}
                    }
                    chunks.append(chunk)

    json_path = output_path / "suspension_chunks_final.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

    print(f"Chunking done! Total chunks: {len(chunks)}")
    return chunks


def create_vector_db(chunks):
    """
    Create vector database with embeddings

    Args:
        chunks: List of chunks

    Returns:
        ChromaDB collection
    """
    print("Creating Chroma vector database with OpenAI embeddings...")

    chroma_client = chromadb.PersistentClient(path="chroma_db")

    collection = chroma_client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=openai_ef,
        metadata={"hnsw:space": "cosine"}
    )

    documents = []
    metadatas = []
    ids = []

    for chunk in chunks:
        embed_text = f"Section: {chunk['parent_section']}\n{chunk['content']}"

        documents.append(embed_text)
        metadatas.append({
            "page": chunk["page"],
            "type": chunk["type"],
            "parent_section": chunk["parent_section"],
            "has_table": chunk["metadata"].get("has_table", False)
        })
        ids.append(f"chunk_{chunk['chunk_id']}")

    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    print(f"Vector DB created successfully!")
    print(f"Collection '{COLLECTION_NAME}' contains {len(chunks)} documents")
    return collection


if __name__ == "__main__":
    chunks = extract_and_chunk_pdf()
    collection = create_vector_db(chunks)
    print("Pipeline Complete! Ready for RAG queries.")
