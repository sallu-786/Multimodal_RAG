
#in This file we read the text from files and create embeddings plus obtain keywords using bm25 search
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from utils.file_format_handler import get_pdf_text,get_text,get_word_text,get_ppt_text,get_excel_text,get_csv_text
import os

from langchain_huggingface import HuggingFaceEmbeddings
from langchain.retrievers import EnsembleRetriever
from dotenv import load_dotenv
from langchain_community.retrievers import BM25Retriever
import time
import streamlit as st

load_dotenv()

model="intfloat/multilingual-e5-large" 


#Handle multiple files
def get_file(files):
    if isinstance(files, list):
        text_chunks = []
        for file in files:
            filename = file.name 
            if filename.endswith('.pdf'):
                text_chunks.extend(get_pdf_text(file))
            elif filename.endswith('.txt'):
                text_chunks.extend(get_text(file))
            elif filename.endswith(('.docx', '.doc')):
                text_chunks.extend(get_word_text(file))
            elif filename.endswith(('.pptx', '.ppt')):
                text_chunks.extend(get_ppt_text(file))
            elif filename.endswith(('.xlsx', '.xls')):
                text_chunks.extend(get_excel_text(file))
            elif filename.endswith('.csv'):
                text_chunks.extend(get_csv_text(file))
            else: 
                raise ValueError(f"Unsupported file type: {filename}")
        
        return text_chunks
    
    #single file
    else:
        filename = files.name 
        if filename.endswith('.pdf'):
            return get_pdf_text(files)
        elif filename.endswith('.txt'):
            return get_text(files)
        elif filename.endswith(('.docx', '.doc')):
            return get_word_text(files)
        elif filename.endswith(('.pptx', '.ppt')):
            return get_ppt_text(files)
        elif filename.endswith(('.xlsx', '.xls')):
            return get_excel_text(files)
        elif filename.endswith('.csv'):
            return get_csv_text(files)
        else: 
            raise ValueError(f"Unsupported file type: {filename}")


def get_text_chunks(pages):  # divide text of file into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=10, 
                                          length_function=len)
    chunks = []
    for text, page_number in pages:
        for chunk in text_splitter.split_text(text):
            chunks.append({"text": chunk, "page_number": page_number})
    return chunks



#Document Retriever-------------------------------------------------------------------------------------------- 

class DocumentChunk:                   #create a class to store text chunk with metadata (page number)
    def __init__(self, page_content, metadata):
        self.page_content = page_content
        self.metadata = metadata

def retriever(text_chunks, query):
  
    embeddings = HuggingFaceEmbeddings(model_name=model)  
    documents = [DocumentChunk(page_content=chunk['text'], metadata={'page': chunk['page_number']}) 
                 for chunk in text_chunks]
    vector_store = FAISS.from_documents(documents, embeddings)
    faiss_retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    ensemble_retriever = EnsembleRetriever(
        retrievers=[faiss_retriever],
        weights=[1.0]  # Weights sum to 1.0 for single vector based retriever
    )
    final_result = ensemble_retriever.invoke(query)
    return final_result


def hybrid_retriever(text_chunks, query,embed_model=model):
  
    docs = [DocumentChunk(page_content=chunk['text'], metadata={'page': chunk['page_number']})
                for chunk in text_chunks]
    bm25_retriever = BM25Retriever.from_documents(docs)

    embeddings = HuggingFaceEmbeddings(model_name=model)  
    documents = [DocumentChunk(page_content=chunk['text'], metadata={'page': chunk['page_number']}) 
                 for chunk in text_chunks]
    
    vector_store = FAISS.from_documents(documents, embeddings)
    faiss_retriever = vector_store.as_retriever()
    ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, faiss_retriever], weights=[0.5, 0.5])
    final_result = ensemble_retriever.invoke(query)
    final_result1 = final_result[:3]
    return final_result1


# when file is uploaded by user, create new vector data for that file
def create_new_vector_db(file):
    with st.spinner("Creating vector data"):
        text = get_file(file)
        text_chunks = get_text_chunks(text)
    return text_chunks

def handle_file_upload(file):
    if file:
        text_chunks = create_new_vector_db(file)
        alert=st.success("Vector data created successfully.")
        time.sleep(3)
        alert.empty()
        return text_chunks

    else:                             
        pass



#URL Retriever------------------------------------------------------------------------------------------------------------

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

def url_retriever(target_url,query):
   
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
