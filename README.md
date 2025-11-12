# PitchGPT 🚀

AI-powered pitch deck analyzer that evaluates startup companies by highlighting specific investment opportunities and risks using RAG (Retrieval-Augmented Generation) with industry data sources.

**Powered by Scottie Ventures**

---

## Features

- 🤖 **AI Analysis**: Gemini-powered pitch deck evaluation
- 📚 **RAG Integration**: Retrieves relevant context from SV developed industry reports and other popular industry reports and data
- 🎨 **Modern Web UI**: Clean, responsive interface with Scottie Ventures branding
- 📄 **Source Citations**: View and download referenced source documents

---

## Prerequisites

- Python 3.12+
- Virtual environment (`.venv`)
- Gemini API key (Google AI)

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/biplopghimire/PitchGPT.git
cd PitchGPT
```

### 2. Create and Activate Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the project root:
```bash
GEMINI_API_KEY=your_gemini_api_key_here
HF_EMBED_MODEL=BAAI/bge-small-en-v1.5
```

Get your Gemini API key from: https://ai.google.dev/

---

## Building the FAISS Index

The FAISS index enables semantic search across your industry data sources.

### 1. Add Your Data Sources
Place PDF files or text documents in the data directory:
```bash
pitchgpt_rag/data/
```

### 2. Build the Index
Run the ingestion script to create the FAISS vector database:
```bash
python pitchgpt_rag/src/ingest_faiss.py
```

This will:
- Load all PDFs from `pitchgpt_rag/data/`
- Split documents into chunks
- Generate embeddings using HuggingFace sentence-transformers
- Save the FAISS index to `pitchgpt_rag/.faiss_index/`

### 3. Verify the Index
Check that the index was created successfully:
```bash
ls pitchgpt_rag/.faiss_index/
# Should show: index.faiss, index.pkl
```

### Rebuilding the Index
Whenever you add new sources to `pitchgpt_rag/data/`, rebuild the index:
```bash
python pitchgpt_rag/src/ingest_faiss.py
```

---

## Running the Web Application

### Start the Server
```bash
python -m uvicorn api:app --reload --port 8000
```

### Access the Application
Open your browser and navigate to:
- **http://localhost:8000**
- **http://127.0.0.1:8000**

### API Documentation
Interactive API docs available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Using the Web Interface

1. **Enter Pitch**: Paste your startup pitch deck text into the textarea
2. **Load Example**: Click "Load Example" to see a sample pitch
3. **Analyze**: Click "Analyze Pitch" to get AI-powered insights
4. **View Sources**: Click "View Sources Referenced" to see the industry data used in the analysis
5. **Download PDFs**: Click on source filenames to download the original documents

---

## Project Structure

```
PitchGPT/
├── api.py                      # FastAPI server
├── pitchgpt.py                 # Main PitchGPT class
├── gemini_api.py               # Gemini API wrapper
├── prompts.json                # Prompt templates
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create this)
├── static/                     # Frontend files
│   ├── index.html             # Web UI
│   ├── styles.css             # Styling
│   └── scottie_ventures.logo.png
├── pitchgpt_rag/              # RAG system
│   ├── data/                  # Source documents (PDFs)
│   ├── .faiss_index/          # Vector database
│   └── src/
│       ├── ingest_faiss.py    # Index builder
│       ├── query_faiss.py     # Query interface
│       ├── rag_context.py     # Context retrieval
│       └── text_cleaner.py    # Text preprocessing
```

---

## Development

### Running Tests
```bash
python -m pytest tests/
```

## Technologies Used

- **FastAPI**: Modern web framework
- **LangChain**: LLM orchestration and RAG
- **FAISS**: Vector similarity search
- **Gemini AI**: Language model
- **Sentence Transformers**: Text embeddings
- **PyPDF**: PDF processing

---

## Contributors

- **Biplop Ghimire**
- **Ethan**

**Powered by Scottie Ventures**
