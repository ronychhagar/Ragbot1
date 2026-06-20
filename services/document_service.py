import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from storage.vector_store import get_vector_store
from config import DOCS_PATH, CHUNK_SIZE, CHUNK_OVERLAP

def index_documents():

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    docs = []

    for file in os.listdir(DOCS_PATH):
        loader = TextLoader(os.path.join(DOCS_PATH, file))
        docs.extend(loader.load())

    chunks = splitter.split_documents(docs)

    vectordb = get_vector_store()
    vectordb.add_documents(chunks)
    vectordb.persist()
