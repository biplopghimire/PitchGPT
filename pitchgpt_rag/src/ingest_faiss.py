# pitchgpt_rag/src/ingest_faiss.py
import glob
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

load_dotenv()

def load_docs(pattern="pitchgpt_rag/data/**/*"):
    docs = []
    for p in glob.glob(pattern, recursive=True):
        path = Path(p)
        if path.is_dir():
            continue
        if path.suffix.lower() == ".pdf":
            docs += PyPDFLoader(str(path)).load()
        elif path.suffix.lower() in {".txt", ".md"}:
            docs += TextLoader(str(path), encoding="utf-8").load()
    return docs

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1200,
    chunk_overlap=150,
    separators=["\n\n", "\n", ". ", ".", " "]
)

if __name__ == "__main__":
    docs = load_docs()
    if not docs:
        print("No documents found in ./pitchgpt_rag/data")
        raise SystemExit(1)

    chunks = splitter.split_documents(docs)
    print(f"Loaded {len(docs)} docs, created {len(chunks)} chunks")

    model_name = os.getenv("HF_EMBED_MODEL", "BAAI/bge-small-en-v1.5")
    emb = HuggingFaceEmbeddings(
        model_name=model_name,
        encode_kwargs={"normalize_embeddings": True}
    )

    vs = FAISS.from_documents(chunks, emb)
    vs.save_local("pitchgpt_rag/.faiss_index")
    print("Ingestion complete. Index saved to pitchgpt_rag/.faiss_index")