# MultiModal-RAG
An open-source Multimodal RAG-UI for chatting with your documents and images. Key tools used for development are
- Streamlit for UI
- Azure OpenAI for LLM/Embeddings
- Langchain for RAG implementation (Vector based{Default} and Hybrid both available)
- Faiss for Vector Data Indexing

[TB chat.webm](https://github.com/user-attachments/assets/f0ca0b53-9360-4adb-8bbf-b039c0499abb)


# Key Features
- Generate Images using Dall-E (Text2Img App mode)
- Normal text based and image based chat in Chat Mode (QA App mode)
- Retrieval Augmented Generation in File mode with support for following formats (QA App mode)
    -PDF (Preview file in sidebar)
    -Word Document(.docx)
    -Excel (.csv,xlsx)
    -Power Point (.pptx)
    -Text (.txt)
- Chat about website content in URL mode (QA App mode)
- Download Complete Chat History stored in local Csv file

# Installation

-Make sure you have python installed. Then go to directory where you want to download the file in command prompt

- Create new virtual environment and activate. To do so in windows cmd, use following commands
      ```python -m venv my_env
      my_env\Scripts\activate```

-Download the Zip file and extract into desired folder or Clone the repository using following command 
      ```git clone https://github.com/sallu-786/MultiModal-RAG.git```

- Install the required libraries
      ```pip install -r requirements.txt```

- Go to .env file and set your AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY. Then enter the model name and API version. If you want to use some other model visit https://python.langchain.com/v0.2/docs/integrations/llms/
- Go to utils/generate_embeddings.py and enter the embedding model name as deployed. If you want to use Open Source embedding model use the code that has been commented inside the file
- For image Generation Dall-E-3 is deployed via Azure OpenAI. Please make changes according to your requirement in utils/generate_image.py

  
  
