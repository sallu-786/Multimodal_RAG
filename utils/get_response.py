from langchain_ollama import ChatOllama
system_msg = ( """"
           You are a helpful Assistant named TB Chat.
           If some documents given to you, You always Answer the questions properly based on the provided document.
           If the information is not in the documents or you can't find it, 
           then give your own information based answer. Don't hallucinate """
        )
def response_ollama(user_message: str, input_documents, chat_history: list=[], my_model="llama3"):
    model = ChatOllama(model=my_model, temperature=0)
    my_message = [{"role": "system", "content": system_msg}]

    for chat in chat_history[-1:]:
        if isinstance(chat, dict) and "role" in chat and "content" in chat:
           my_message.append(chat)
                                                     #Append the latest question in message
    my_message.append({"role": "user", "content": user_message})

        # Add input documents
    for doc in input_documents:
        if isinstance(doc, dict) and "content" in doc:
            my_message.append({"role": "user", "content": f"Document snippet:\n{doc['content']}"})
    
    response = model.invoke(                          #define model&input for response 
        my_message
        )
    return response.content



