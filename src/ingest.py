import requests
from bs4 import BeautifulSoup
import chromadb
from sentence_transformers import SentenceTransformer
from src.utils import chunk_text, clean_text

# Documentation URLs we want to scrape
DOCS_URLS = {
    "huggingface": [
        "https://huggingface.co/docs/transformers/quicktour",
        "https://huggingface.co/docs/datasets/loading",
        "https://huggingface.co/docs/transformers/training",
        "https://huggingface.co/docs/transformers/pipeline_tutorial",
        "https://huggingface.co/docs/transformers/model_sharing",
        "https://huggingface.co/docs/transformers/tokenizer_summary",
        "https://huggingface.co/docs/transformers/fine_tuning",
    ],
    "pytorch": [
        "https://pytorch.org/docs/stable/tensor_tutorial.html",
        "https://pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html",
        "https://pytorch.org/tutorials/beginner/basics/optimization_tutorial.html",
        "https://pytorch.org/tutorials/beginner/basics/data_tutorial.html",
        "https://pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html",
        "https://pytorch.org/tutorials/beginner/basics/saveloadrun_tutorial.html",
    ],
    "scikit-learn": [
        "https://scikit-learn.org/stable/getting_started.html",
        "https://scikit-learn.org/stable/supervised_learning.html",
    ],
}

def scrape_page(url):
    """Download and extract text from a documentation page"""
    try:
        print(f"Scraping: {url}")
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Remove navigation, footer, scripts (we only want main content)
        for tag in soup(["nav", "footer", "script", "style", "header"]):
            tag.decompose()
        
        text = soup.get_text()
        text = clean_text(text)
        return text
    
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return None


def load_documents():
    """Scrape all documentation pages and return as list"""
    documents = []
    
    for source, urls in DOCS_URLS.items():
        for url in urls:
            text = scrape_page(url)
            if text:
                documents.append({
                    "text": text,
                    "source": source,
                    "url": url
                })
    
    print(f"Loaded {len(documents)} documents")
    return documents


def store_in_chromadb(documents):
    """Convert documents to embeddings and store in ChromaDB"""
    
    # Initialize ChromaDB (saves locally in ./data folder)
    client = chromadb.PersistentClient(path="./data/chromadb")
    
    # Delete existing collection if it exists (fresh start)
    try:
        client.delete_collection("docpilot")
    except:
        pass
    
    collection = client.create_collection("docpilot")
    
    # Load embedding model (converts text to numbers)
    print("Loading embedding model...")
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    
    all_chunks = []
    all_embeddings = []
    all_ids = []
    all_metadata = []
    
    chunk_id = 0
    
    for doc in documents:
        # Split document into chunks
        chunks = chunk_text(doc["text"], chunk_size=500, overlap=50)
        
        for chunk in chunks:
            if len(chunk.strip()) < 50:  # Skip very short chunks
                continue
                
            all_chunks.append(chunk)
            all_metadata.append({
                "source": doc["source"],
                "url": doc["url"]
            })
            all_ids.append(f"chunk_{chunk_id}")
            chunk_id += 1
    
    print(f"Embedding {len(all_chunks)} chunks... (this takes 1-2 minutes)")
    all_embeddings = embedder.encode(all_chunks).tolist()
    
    # Store everything in ChromaDB
    collection.add(
        documents=all_chunks,
        embeddings=all_embeddings,
        metadatas=all_metadata,
        ids=all_ids
    )
    
    print(f"Successfully stored {len(all_chunks)} chunks in ChromaDB!")
    return collection


def run_ingestion():
    """Main function to run the full ingestion pipeline"""
    print("Starting DocPilot ingestion pipeline...")
    documents = load_documents()
    store_in_chromadb(documents)
    print("Ingestion complete!")


if __name__ == "__main__":
    run_ingestion()