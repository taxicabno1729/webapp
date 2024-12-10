"""Website content analyzer using Llama 2 model for intelligent analysis."""

import os
import re

import requests
import streamlit as st
from bs4 import BeautifulSoup

# Configure page settings
st.set_page_config(page_title="Website Content Analyzer", page_icon="🔍")


def clean_text(text):
    """Clean and normalize text by removing special characters and extra whitespace.

    Args:
        text (str): The input text to clean

    Returns:
        str: The cleaned text
    """
    # Remove extra whitespace and newlines
    text = re.sub(r"\s+", " ", text)
    # Remove special characters
    text = re.sub(r"[^\w\s.,!?-]", "", text)
    return text.strip()


def get_website_content(url):
    """Fetch and extract text content from a given URL.

    Args:
        url (str): The website URL to analyze

    Returns:
        str: The extracted text content or error message
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Get text content
        text = soup.get_text()
        return clean_text(text)
    except Exception as e:
        return f"Error fetching website content: {str(e)}"


def analyze_with_llama(content):
    """Analyze website content using the Llama 2 model.

    Args:
        content (str): The website content to analyze

    Returns:
        str: The analysis result or error message
    """
    try:
        response = requests.post(
            f"{os.getenv('OLLAMA_HOST', 'http://localhost:11434')}/api/generate",
            json={
                "model": "llama3.2",
                "prompt": (
                    "Please analyze and summarize the following website content "
                    f"in a clear and concise way:\n\n{content}"
                ),
                "stream": False,
                "temperature": 0.7,
            },
        )
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        return f"Error connecting to Llama: {str(e)}"


# UI Elements
st.title("🔍 Website Content Analyzer")
st.write("Enter a URL to analyze its content using Llama")

url = st.text_input("Enter website URL:", "https://example.com")

if st.button("Analyze"):
    with st.spinner("Fetching website content..."):
        content = get_website_content(url)

        if content.startswith("Error"):
            st.error(content)
        else:
            st.subheader("Website Content:")
            with st.expander("Show raw content"):
                st.text(content[:1000] + "..." if len(content) > 1000 else content)

            with st.spinner("Analyzing with Llama..."):
                analysis = analyze_with_llama(
                    content[:4000]
                )  # Limit content length to avoid token limits

                st.subheader("Llama Analysis:")
                st.text(analysis[:1000] + "..." if len(analysis) > 1000 else analysis)
