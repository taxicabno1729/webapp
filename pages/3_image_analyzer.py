import streamlit as st
import pytesseract
from PIL import Image
import requests
import io
import numpy as np

# Configure page settings
st.set_page_config(
    page_title="Image Text Analyzer",
    page_icon="📷"
)

# Initialize image variable
image = None

def perform_ocr(image):
    try:
        # Extract text from image using Tesseract
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        return f"Error performing OCR: {str(e)}"

def analyze_with_llama(content):
    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': 'llama3.2',
                'prompt': f"Please analyze and summarize the following text extracted from an image:\n\n{content}",
                'stream': False,
                'temperature': 0.7
            }
        )
        response.raise_for_status()
        return response.json()['response']
    except Exception as e:
        return f"Error connecting to Llama: {str(e)}"

# UI Elements
st.title("📷 Image Text Analyzer")
st.write("Upload an image or provide a URL to extract and analyze text")

# Add upload method selection
upload_method = st.radio("Choose upload method:", ["Upload File", "Image URL"])

if upload_method == "Upload File":
    uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        ocr_text = perform_ocr(image)
        st.write("Extracted Text:")
        st.text(ocr_text[:1000] + "..." if len(ocr_text) > 1000 else ocr_text)
        llama_analysis = analyze_with_llama(ocr_text)
        st.write("Llama Analysis:")
        st.text(llama_analysis[:1000] + "..." if len(llama_analysis) > 1000 else llama_analysis)
else:
    url = st.text_input("Enter image URL:")
    if url:
        try:
            response = requests.get(url)
            image = Image.open(io.BytesIO(response.content))
        except Exception as e:
            st.error(f"Error loading image from URL: {str(e)}")

# Rest of the code remains the same... 