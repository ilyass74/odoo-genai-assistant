import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("documents_btel")


def chercher_documents(question, n=2):
    resultats = collection.query(query_texts=[question], n_results=n)
    morceaux = resultats["documents"][0]
    return "\n---\n".join(morceaux)
