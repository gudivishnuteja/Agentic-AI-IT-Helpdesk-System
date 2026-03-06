from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import os

DB_DIR = "chroma_db"


def get_embedding_model():

    return HuggingFaceEmbeddings(
        model_name="BAAI/bge-m3",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )


def ingest_documents(data_dir="data"):

    documents = []

    for file in os.listdir(data_dir):

        if file.endswith(".pdf"):

            loader = PyPDFLoader(os.path.join(data_dir, file))
            docs = loader.load()

            documents.extend(docs)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=300
    )

    chunks = splitter.split_documents(documents)

    embeddings = get_embedding_model()

    vectordb = Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory=DB_DIR
    )

    vectordb.persist()

    print(f"Ingested {len(chunks)} chunks.")
    

def get_vector_db():

    embeddings = get_embedding_model()

    return Chroma(
        persist_directory=DB_DIR,
        embedding_function=embeddings
    )