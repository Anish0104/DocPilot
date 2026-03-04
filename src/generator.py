import os
from groq import Groq
from src.utils import load_environment
from src.retriever import retrieve

# Load API key and initialize Groq client
load_environment()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_answer(query, chunks):
    """
    Send question + relevant chunks to Groq LLM
    and get a proper answer back
    """
    
    # Combine all chunks into one context block
    context = "\n\n".join([chunk["text"] for chunk in chunks])
    
    # This is the prompt we send to the LLM
    prompt = f"""You are DocPilot, an AI assistant that helps developers 
understand ML framework documentation.

Use ONLY the context below to answer the question.
If the answer is not in the context, say "I couldn't find that in the documentation."
Always be concise and include code examples if present in the context.

Context from documentation:
{context}

Question: {query}

Answer:"""

    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.1  # Low temperature = more factual, less creative
    )
    
    return response.choices[0].message.content


def ask(query):
    """
    Full RAG pipeline:
    1. Retrieve relevant chunks
    2. Generate answer from chunks
    3. Return answer + sources
    """
    
    # Step 1: Find relevant chunks
    chunks = retrieve(query, n_results=3)
    
    # Step 2: Generate answer
    answer = generate_answer(query, chunks)
    
    # Step 3: Get unique sources
    sources = list(set([chunk["url"] for chunk in chunks]))
    
    return {
        "answer": answer,
        "sources": sources
    }


if __name__ == "__main__":
    # Quick test
    test_query = "How do I load a dataset in HuggingFace?"
    result = ask(test_query)
    
    print(f"Question: {test_query}\n")
    print(f"Answer:\n{result['answer']}\n")
    print(f"Sources:")
    for source in result['sources']:
        print(f"  - {source}")