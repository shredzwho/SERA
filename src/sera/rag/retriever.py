import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DB_PATH = os.path.join(BASE_DIR, "data", "simple_db.json")

class ContextRetriever:
    def __init__(self, db_path=DB_PATH):
        """
        Initializes the sentence-transformer embedding model.
        """
        self.db_path = db_path
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.knowledge_base = self._load_db()

    def _load_db(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_chunks(self, chunks: list):
        """
        Embeds a list of strings and appends them to the JSON store.
        """
        # Ensure dir exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        embeddings = self.model.encode(chunks)
        
        for chunk, emb in zip(chunks, embeddings):
            self.knowledge_base.append({
                "text": chunk,
                "embedding": emb.tolist()
            })
            
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(self.knowledge_base, f)

    def retrieve(self, query: str, top_k: int = 1) -> str:
        """
        Finds the top_k most similar chunks using cosine similarity.
        """
        if not self.knowledge_base:
            return ""
            
        query_emb = self.model.encode(query)
        
        results = []
        for item in self.knowledge_base:
            doc_emb = np.array(item["embedding"])
            # Cosine similarity
            sim = np.dot(query_emb, doc_emb) / (np.linalg.norm(query_emb) * np.linalg.norm(doc_emb))
            results.append((sim, item["text"]))
            
        # Sort by similarity descending
        results.sort(key=lambda x: x[0], reverse=True)
        
        # Bypass Pyre2 slice inferencing bug
        limit = min(int(top_k), len(results))
        top_docs = [results[i] for i in range(limit)]
        
        # Only return matches that are reasonably relevant (similarity > 0.3)
        relevant_docs = [doc for sim, doc in top_docs if sim > 0.3]
        
        if not relevant_docs:
            return ""
            
        context_str = "RETRIEVED CONTEXT (Use this to answer the query if relevant):\n"
        context_str += "-" * 40 + "\n"
        for i, text in enumerate(relevant_docs):
            context_str += f"Document {i+1}:\n{text}\n"
            context_str += "-" * 40 + "\n"
            
        return context_str
