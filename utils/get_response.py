import os
import streamlit as st




#For Azure Open Ai---------------------------------------------------------
from openai import AzureOpenAI
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
client = AzureOpenAI(api_version="")
model = ""

system_msg = (
            """"
           You are a helpful Assistant named TB Chat.
           If some documents given to you, You always Answer the questions properly based on the provided document.
           If the information is not in the documents or you can't find it, 
           then give your own information based answer. Don't hallucinate """
        )





# Function to get response from LLM model (Chat-GPT-Azure)---------------------------------------------------


def response_chatgpt_az(message: str, input_documents, chat_history: list = []):

    messages = [{"role": "system", "content": system_msg}]

    # Add chat history
    for chat in chat_history[-2:]:
        if isinstance(chat, dict) and "role" in chat and "content" in chat:
            messages.append(chat)

    # Add user message
    messages.append({"role": "user", "content": message})

    # Add input documents
    for doc in input_documents:
        if isinstance(doc, dict) and "content" in doc:
            messages.append({"role": "user", "content": f"Document snippet:\n{doc['content']}"})

    try:
        response = client.chat.completions.create(model=model, messages=messages, temperature=0)
        return {
            "answer": response.choices[0].message.content,
            "sources": input_documents,
            
        }
    except Exception as e:
        st.error(f"Could not find LLM model: {str(e)}")
        return None



