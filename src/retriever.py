import streamlit as st
import chromadb
from sentence_transformers import SentenceTransformer

# Cache the heavy model loading so Streamlit doesn't reload it every interaction
@st.cache_resource
def load_models():
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    client = chromadb.PersistentClient(path="./data/chromadb")
    collection = client.get_collection("docpilot")
    return embedder, collection


def retrieve(query, n_results=3):
    """
    Find the most relevant chunks for a given question
    
    Example:
    query = "How do I load a dataset in HuggingFace?"
    → searches ChromaDB
    → returns top 3 most relevant chunks
    """
    
    embedder, collection = load_models()
    
    # Convert question to numbers (same way we converted docs)
    query_embedding = embedder.encode([query]).tolist()
    
    # Search ChromaDB for similar chunks
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )
    
    # Format results nicely
    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "url": results["metadatas"][0][i]["url"]
        })
    
    return chunks


if __name__ == "__main__":
    # Quick test
    test_query = "How do I load a dataset in HuggingFace?"
    results = retrieve(test_query)
    
    print(f"Query: {test_query}\n")
    for i, chunk in enumerate(results):
        print(f"Result {i+1}:")
        print(f"Source: {chunk['source']}")
        print(f"URL: {chunk['url']}")
        print(f"Text: {chunk['text'][:200]}...")
        print("---")