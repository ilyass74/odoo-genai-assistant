import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("documents_btel")

question = input("Pose ta question : ")

resultats = collection.query(query_texts=[question], n_results=2)

print("\nReponse(s) trouvee(s) :\n")
for doc, meta in zip(resultats["documents"][0], resultats["metadatas"][0]):
    print(f"[{meta['source']}]")
    print(doc)
    print("---")
