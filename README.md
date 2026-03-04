# DocPilot

DocPilot is an AI Documentation Assistant that provides precise, source-cited answers to questions about the HuggingFace, PyTorch, and Scikit-learn documentation. 

It uses a Retrieval-Augmented Generation (RAG) architecture powered by ChromaDB for local vector search and Groq's LLaMA 3.1 model for fast, accurate generation.

## Features

- **Multi-Library Knowledge Base**: Covers HuggingFace (Transformers, Datasets, Pipelines), PyTorch (Tensors, Autograd, Model Building), and Scikit-learn (Classical ML).
- **Source Citations**: Every answer includes direct links to the official documentation sources.
- **Modern UI**: A premium, glassmorphic Streamlit interface. 
- **100% Free Stack**: Built entirely with free and open-source tools (Streamlit, ChromaDB locally, Groq free tier).

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/Anish0104/DocPilot.git
   cd DocPilot
   ```

2. **Create a virtual environment (Optional but Recommended)**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   # source venv/bin/activate    # On macOS/Linux
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your API Key**
   Create a `.env` file in the root directory and add your Groq API key:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

5. **Run the Application**
   ```bash
   streamlit run app.py
   ```

## Architecture

- **Frontend**: Streamlit
- **Vector Database**: ChromaDB (Local)
- **LLM**: LLaMA 3.1 via Groq API
- **Embeddings**: HuggingFace sentence transformers

## License
MIT License
