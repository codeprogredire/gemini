from PIL import Image
import google.generativeai as genai
import os  # for environment variables
import streamlit as st
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro vision
model = genai.GenerativeModel('gemini-pro-vision')


def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text


def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                'mime_type': uploaded_file.type,
                'data': bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("File not found")

# streamlit app


st.set_page_config(page_title="Multi Language Invoice Extractor")
st.header("Multi Language Invoice Extractor")
st.subheader("Extract information from invoice in multiple languages")

input = st.text_input("Input Prompt: ", key="input")

uploaded_file = st.file_uploader(
    "Upload Invoice", type=["png", "jpg", "jpeg"], key="image")

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)


submit = st.button("Tell me about the invoice")

input_prompt = """
    You are an expert in invoice extraction. we will show you an invoice and you will tell us what information you want to extract from it. 
"""

if submit:
    if input == "":
        st.write("Please enter a prompt")
    elif uploaded_file is None:
        st.write("Please upload an invoice")
    else:
        image_parts = input_image_setup(uploaded_file)
        response = get_gemini_response(input_prompt, image_parts, input)
        st.subheader("The response is:")
        st.write(response)