# MultiModal-RAG
An open-source Multimodal RAG-UI for chatting with your documents and images. Key tools used for development are
- Streamlit for UI
- Azure OpenAI for LLM/Embeddings in _**main branch**_ \
      LLAVA (for Chat/Image mode), LLAMA3.1 (files&URL mode) and e5-large for embeddings in _**Local_rag branch**_ {Completely Open-Source}
- Langchain for RAG implementation (Vector based{Default} and Hybrid both available)
- Faiss for Vector Data Indexing

[TB chat.webm](https://github.com/user-attachments/assets/0fa89f57-8ad2-4f6f-b42e-f6720a4a6a4a)

# Key Features
- Generate Images using Dall-E (Text2Img App mode)
- Normal text based and image based chat in Chat Mode (QA App mode)
- Retrieval Augmented Generation in File mode with support for following formats (QA App mode)

   1.PDF (Preview file in sidebar)

   2.Word Document(.docx)

   3.Excel (.csv,xlsx)

   4.Power Point (.pptx)

   5.Text (.txt)

6.Chat about website content in URL mode (QA App mode)

7.Download Complete Chat History stored in local Csv file

# Installation

- Make sure you have python installed. Then go to directory where you want to download the file in command prompt

- Create new virtual environment and activate. To do so in windows cmd, use following commands


      python -m venv my_env
      my_env\Scripts\activate

- Download the Zip file and extract into desired folder or Clone the repository using following command 


      git clone https://github.com/sallu-786/Multimodal_RAG.git

- Install the required libraries

        pip install -r requirements.txt

- Go to .env file and set your AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY. Then enter the model name and API version. If you want to use some other model visit https://python.langchain.com/v0.2/docs/integrations/llms/
- Go to utils/generate_embeddings.py and enter the embedding model details as needed. 
- For image Generation Dall-E-3 is deployed via Azure OpenAI. Please make changes according to your requirement in utils/generate_image.py

  
  
