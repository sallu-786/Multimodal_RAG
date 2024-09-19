import streamlit as st
from dotenv import load_dotenv
from utils.chat_log import save_chat_log, get_downloadable_excel
from utils.generate_embeddings import retriever,url_retriever,handle_file_upload
from utils.generate_image import image_to_base64, generate_img
from utils.file_format_handler import displayPDF
from utils.get_response import response_chatgpt_az
from st_copy_to_clipboard import st_copy_to_clipboard 
''' To adjust frame height of st_copy_to_clipboard please go to--> your_venv\Lib\site-packages\st_copy_to_clipboard\frontend\main.js 
and change value of Streamlit.setFrameHeight(35)'''


# Configuration
load_dotenv()
USER_NAME = "user"
ASSISTANT_NAME = "assistant"


def reset_conversation():
    if "messages" in st.session_state and len(st.session_state.messages) > 0:
        st.session_state.pop("messages", None)

def main():
    # Adding the fade-in effect CSS

    with open('css/styles.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    st.markdown(
        '''
        <div id="root">
            <h1 class="title">TB Chat</h1>
           
        </div>
        ''', 
        unsafe_allow_html=True
    )


    # File Upload Sidebar option
    with st.sidebar:
        
        
        st.session_state.mode = st.radio("Select Mode:", ("Chat", "Files","URL"))


        if st.session_state.mode == "Chat":

            st.session_state.file = st.file_uploader("Upload Image 🖼️ ", accept_multiple_files=False, type=["png", "jpg", "jpeg"])
        elif st.session_state.mode == "Files":


            st.session_state.file = st.file_uploader("Upload File 📂", accept_multiple_files=False, type=['pdf', 'docx', 'pptx', 'xlsx', 'csv', 'txt'])
        elif st.session_state.mode == "URL":

            st.session_state.target_url = st.text_input("URL",placeholder="https://tourism.gov.pk/")
        send_button = st.button("submit", key="send_button")

        if st.session_state.file and st.session_state.file.type == 'application/pdf':
            with st.expander("PDF Preview"):       
                displayPDF(st.session_state.file)
    
        if send_button and st.session_state.file:


            # try:
            if st.session_state.mode == "Chat":
                if st.session_state.file.type in ['image/jpeg', 'image/png']:
                    img_base64 = image_to_base64(st.session_state.file)
                    if "chat_log" not in st.session_state:
                        st.session_state.chat_log = []
                    st.session_state.chat_log.append({
                        "role": "user", 
                        "content": [{
                            "type": "image_url",
                            "image_url": {"url": f"data:{st.session_state.file.type};base64,{img_base64}"}
                        }]
                    })

                else:
                    st.error("Image Processing Failed")

            elif st.session_state.mode == "Files":  # Files mode                
                if st.session_state.file.type not in ['image/jpeg', 'image/png']:
                    text_chunks = handle_file_upload([st.session_state.file])
                    if text_chunks:
                        st.session_state.text_chunks = text_chunks
                        st.session_state.file_name = st.session_state.file.name
                else:
                    st.error("File Processing Failed")


    if "chat_log" not in st.session_state:
        st.session_state.chat_log = []

    with st.sidebar:
        col1, col2 = st.columns([1, 1])
        with col2:
            rst = st.button("Clear Chat🗑️", key="reset_button")
            if rst:
                st.session_state.chat_log = []

    # Display previous messages
    for message in st.session_state.chat_log:
        with st.chat_message(message["role"]):
            if isinstance(message["content"], list):
                for content in message["content"]:
                    if content["type"] == "text":
                        st.write(content["text"])
                        if message["role"]=="assistant":
                            st_copy_to_clipboard(content["text"]) 
                    elif content["type"] == "image_url":
                        st.image(content["image_url"]["url"])
            else:
                st.write(message["content"])

    message = st.chat_input("Enter your message here")

    if message:
        try:
            with st.chat_message(USER_NAME):
                st.write(message)
            
            with st.spinner("Processing..."):
                if st.session_state.mode == "Files" and "text_chunks" in st.session_state:
                    # Process text-based files
                    reranked_results = retriever(st.session_state.text_chunks, message)
                    doc_texts = [{"content": doc.page_content, "metadata": doc.metadata} for doc in reranked_results]
                    response = response_chatgpt_az(message, doc_texts, chat_history=st.session_state.chat_log)

                elif st.session_state.mode == "Chat":
                    response = response_chatgpt_az(message,[],chat_history=st.session_state.chat_log)

                elif st.session_state.mode == "URL":
                    reranked_results_url=url_retriever(st.session_state.target_url,message)
                    url_text = [{"content": doc.page_content, "metadata": doc.metadata} for doc in reranked_results_url]
                   
                    response = response_chatgpt_az(message, url_text, chat_history=st.session_state.chat_log)
                 
              

            with st.chat_message(ASSISTANT_NAME):
                        assistant_msg = response["answer"]
                        st.write(assistant_msg)
                        st_copy_to_clipboard(assistant_msg)
                        
            st.session_state.chat_log.append({"role": "user", "content": [{"type": "text", "text": message}]})
            st.session_state.chat_log.append({"role": "assistant", "content": [{"type": "text", "text": assistant_msg}]})
                        
            save_chat_log(message, assistant_msg)
                

            
        except Exception as e:
            st.error(f"Error: Please ensure to submit a valid File/URL first. Use Chat mode otherwise")

    downloadable_excel = get_downloadable_excel()
    if downloadable_excel:
        with st.sidebar:
            with col1:
                st.download_button(
                label="Chat Log ⬇️",
                data=downloadable_excel,
                file_name="chat_log.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )


st.session_state.choice= st.sidebar.selectbox("App Mode", ["QA", "Text2Image"])
if st.session_state.choice == "QA":
    main()

elif st.session_state.choice == "Text2Image":
    generate_img()
