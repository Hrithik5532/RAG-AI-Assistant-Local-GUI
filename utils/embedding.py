from langchain_fireworks import FireworksEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader, CSVLoader
import os
def vector_embedding(path):
    embeddings = FireworksEmbeddings(model="nomic-ai/nomic-embed-text-v1.5")
    
    if os.path.isdir(path):
        loader = PyPDFLoader(path)
        docs = loader.load()
    else:
        ext = os.path.splitext(path)[-1].lower()
        if ext == '.txt':
            loader = TextLoader(path)
        elif ext == '.pdf':
            loader = PyPDFLoader(path)
        elif ext == '.csv':
            loader = CSVLoader(path)
            
        else:
            raise ValueError(f"Unsupported file type: {ext}")
        docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    final_documents = text_splitter.split_documents(docs)
    vectors = FAISS.from_documents(final_documents, embeddings)
    return vectors
