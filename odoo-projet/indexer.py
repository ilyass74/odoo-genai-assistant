import os
import chromadb

DOSSIER_DOCS = "documents"

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("documents_btel")


def charger_documents():
    chunks = []
    metadatas = []
    ids = []
    compteur = 0
    for nom_fichier in os.listdir(DOSSIER_DOCS):
        if not nom_fichier.endswith(".txt"):
            continue
        chemin = os.path.join(DOSSIER_DOCS, nom_fichier)
        with open(chemin, "r", encoding="utf-8") as f:
            contenu = f.read()
        paragraphes = [p.strip() for p in contenu.split("\n\n") if p.strip()]
        for p in paragraphes:
            chunks.append(p)
            metadatas.append({"source": nom_fichier})
            ids.append(f"chunk_{compteur}")
            compteur += 1
    return chunks, metadatas, ids


if __name__ == "__main__":
    chunks, metadatas, ids = charger_documents()
    print(f"{len(chunks)} morceaux de texte trouves.")
    collection.upsert(documents=chunks, metadatas=metadatas, ids=ids)
    print("Indexation terminee. Total dans la collection :", collection.count())
