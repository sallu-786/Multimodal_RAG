from openai import AzureOpenAI
from PIL import Image
import base64
import io
import streamlit as st
import time

client_img = AzureOpenAI(
    api_version="",
    api_key="",
    azure_endpoint=""
)
def image_to_base64(image_file):
    image = Image.open(image_file)
    buffer = io.BytesIO()
    image.save(buffer, format=image.format)
    img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return img_str


# Function to generate AI based images using OpenAI Dall-E
def call_DallE(text):
    response = client_img.images.generate(
        model="Dalle3",
        prompt=text,
        n=1
    )
    image_url = response.data[0].url
    return image_url


def generate_img():
    with open('css/styles.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    st.markdown(
        '''
        <div id="root">
            <h1 class="title">TB ImGen</h1>
           
        </div>
        ''', 
        unsafe_allow_html=True
    )
    input_prompt = st.text_input("Enter your text prompt")
    if input_prompt is not None:
        if st.button("Generate Image"):
            # Create a placeholder for the progress bar
            progress_bar = st.progress(0)
            
            # Simulate progress while generating the image
            for i in range(100):
                # Update the progress bar
                progress_bar.progress(i + 1)
                time.sleep(0.5)  # Adjust this value to control the speed of the progress bar
            
            # Generate the image
            image_url = call_DallE(input_prompt)
            
            # Complete the progress bar
            progress_bar.progress(100)
            
            # Display the generated image
            st.image(image_url, caption="Image Generated using DALL-E")
