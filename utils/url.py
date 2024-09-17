from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os 
from dotenv import load_dotenv
from langchain.retrievers import EnsembleRetriever
load_dotenv()

model="intfloat/multilingual-e5-large" 

def url_chunks(target_url):
    loader = WebBaseLoader(target_url)
    raw_document = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=10,
        length_function=len
    )
    splited_document = text_splitter.split_documents(raw_document)
    return splited_document

def rag_with_url(target_url,query):
   
    loader = WebBaseLoader(target_url)
    raw_document = loader.load()
    embeddings = HuggingFaceEmbeddings(model_name=model)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=10,
        length_function=len
    )
    splited_document = text_splitter.split_documents(raw_document)
    vector_store = FAISS.from_documents(splited_document, embeddings)
    faiss_retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    ensemble_retriever = EnsembleRetriever(
        retrievers=[faiss_retriever],
        weights=[1.0]  # Weights sum to 1.0 for single retriever
    )
    final_result = ensemble_retriever.invoke(query)

    return final_result
