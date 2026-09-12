from pathlib import Path

from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


DOCUMENTS_DIR = Path("documents")
CHROMA_DIR = "chroma_db"


def load_documents():

    documents = []

    for pdf_path in DOCUMENTS_DIR.glob("*.pdf"):

        reader = PdfReader(pdf_path)

        for page_number, page in enumerate(reader.pages):

            text = page.extract_text()

            if text:
                documents.append({
                    "text": text,
                    "source": pdf_path.name,
                    "page": page_number + 1
                })

    for txt_path in DOCUMENTS_DIR.glob("*.txt"):

        text = txt_path.read_text(encoding="utf-8")

        if text.strip():
            documents.append({
                "text": text,
                "source": txt_path.name,
                "page": 1
            })

    return documents


print("Lecture des documents...")

documents = load_documents()

print(f"{len(documents)} pages trouvees.")


splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100
)


texts = []
metadatas = []

for document in documents:

    chunks = splitter.split_text(document["text"])

    for chunk in chunks:

        texts.append(chunk)

        metadatas.append({
            "source": document["source"],
            "page": document["page"]
        })


print(f"{len(texts)} morceaux crees.")


embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)


vectorstore = Chroma(
    collection_name="business_documents",
    embedding_function=embeddings,
    persist_directory=CHROMA_DIR
)


vectorstore.add_texts(
    texts=texts,
    metadatas=metadatas
)


print("Indexation terminee.")
print(f"Base ChromaDB : {CHROMA_DIR}")
