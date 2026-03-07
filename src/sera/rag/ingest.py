import os
import argparse
from sera.rag.retriever import ContextRetriever

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list:
    """
    Splits a large text into smaller chunks for embedding, with some overlap to preserve context.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[slice(int(start), int(end))])
        start += (chunk_size - overlap)
    return chunks

def ingest_file(filepath: str):
    """
    Reads a text file, chunks it, and stores the embeddings in the simple JSON DB.
    """
    if not os.path.exists(filepath):
        print(f"Error: File {filepath} not found.")
        return
        
    print(f"Reading file: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    print(f"Chunking text (length: {len(content)} chars)...")
    chunks = chunk_text(content)
    
    print(f"Initializing Retriever Model...")
    retriever = ContextRetriever()
    
    print(f"Adding {len(chunks)} chunks to simple vector database...")
    retriever.save_chunks(chunks)
    print("Ingestion complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest a text file into Sera's knowledge base.")
    parser.add_argument("filepath", help="Path to the text file to ingest")
    args = parser.parse_args()
    
    ingest_file(args.filepath)
