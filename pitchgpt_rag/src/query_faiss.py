from langchain_community.vectorstores import FAISS
from embeddings_factory import get_embeddings

if __name__ == "__main__":
    emb = get_embeddings()
    vs = FAISS.load_local("pitchgpt_rag/.faiss_index", emb, allow_dangerous_deserialization=True)

    query = "CAGR of Data Management Market"
    docs = vs.similarity_search(query, k=4)

    for i, d in enumerate(docs, 1):
        print(f"\n{i}) source={d.metadata.get('source')}")
        print(d.page_content[:300], "...")