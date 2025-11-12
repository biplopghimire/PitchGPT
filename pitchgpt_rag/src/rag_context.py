# pitchgpt_rag/src/rag_context.py
import os
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from collections import OrderedDict
from pitchgpt_rag.src.text_cleaner import normalize, truncate

INDEX_PATH = "pitchgpt_rag/.faiss_index"

def _embeddings():
    model_name = os.getenv("HF_EMBED_MODEL", "BAAI/bge-small-en-v1.5")
    return HuggingFaceEmbeddings(
        model_name=model_name,
        encode_kwargs={"normalize_embeddings": True}
    )

def build_retriever(index_path: str = INDEX_PATH):
    if not Path(index_path).exists():
        return None
    emb = _embeddings()
    vs = FAISS.load_local(index_path, emb, allow_dangerous_deserialization=True)
    return vs.as_retriever(search_type="similarity", search_kwargs={"k": 6})

def retrieve_context(query: str, k: int = 6) -> str:
    retriever = build_retriever()
    if retriever is None:
        return "_No retrieved context (index not found)._"
    docs = retriever.get_relevant_documents(query)

    # Group by (source, page), preserve order, clean and truncate snippets
    groups: "OrderedDict[tuple, list[str]]" = OrderedDict()
    for d in docs[:k]:
        src = d.metadata.get("source", "unknown")
        page = d.metadata.get("page")
        key = (src, page)
        groups.setdefault(key, [])
        cleaned = normalize(d.page_content)
        groups[key].append(truncate(cleaned, 240))

    # Render a compact Markdown bullet list
    lines: list[str] = []
    for (src, page), snippets in groups.items():
        page_label = f" (page {page})" if page is not None else ""
        lines.append(f"- Source: {src}{page_label}")
        for s in snippets[:2]:
            lines.append(f"  - {s}")
    return "\n".join(lines) if lines else "_No retrieved context._"