"""CSV Question Analyzer module for processing questions from CSV files."""

import os

import pandas as pd
import requests
import streamlit as st

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# Configure page settings
st.set_page_config(page_title="CSV Insight Bot", page_icon="🤖", layout="wide")

# Add custom CSS
st.markdown(
    """
    <style>
    .main {
        padding: 2rem;
    }
    .stTitle {
        color: #2E4B7C;
        font-size: 3rem !important;
    }
    .stSubheader {
        color: #4A4A4A;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def analyze_with_llama(question, csv_context):
    """Analyze question using the Llama model with CSV context.

    Args:
        question (str): The question to analyze
        csv_context (str): The CSV data context

    Returns:
        str: The analysis result or error message
    """
    try:
        prompt = f"""Given the following CSV data:
{csv_context}

Please answer this question about the data:
{question}"""

        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False,
                "temperature": 0.7,
            },
        )
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        return f"Error connecting to Llama: {str(e)}"


# Initialize session state for storing results
if "results" not in st.session_state:
    st.session_state.results = []

# UI Elements
st.title("🤖 CSV Insight Bot")
st.markdown(
    """
    <div style="background-color: #f0f2f6; padding: 1rem; border-radius: 10px;
         margin-bottom: 2rem;">
    Welcome! I'm your CSV Analysis Assistant.
    I can help you understand your data by answering questions about it.
    Upload your CSV file, and I'll be ready to assist you!
    </div>
    """,
    unsafe_allow_html=True,
)

# Move sidebar content up
with st.sidebar:
    st.title("🔍 Guide")
    st.markdown(
        """
    ### How to Use
    1. 📤 Upload your CSV file below
    2. 📊 Preview your data
    3. 💬 Ask any questions about your data
    4. 🔄 Get AI-powered insights

    ### Tips
    - Ask specific questions
    - Reference column names
    - Try different perspectives
    """
    )

    if st.button("🗑️ Clear Chat History", type="secondary"):
        st.session_state.messages = []
        st.session_state.results = []

# File upload
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        # Read CSV file
        df = pd.read_csv(uploaded_file, header=1)

        if df.empty:
            st.error("📭 The uploaded CSV file appears to be empty.")
        else:
            # Display preview with better formatting
            st.markdown("### 📊 Data Preview")
            with st.expander("Show/Hide Data Preview", expanded=True):
                st.dataframe(df.head(10), use_container_width=True, height=300)

            csv_context = df.head(10).to_string()

            # Create a cleaner chat interface
            st.markdown("### 💬 Chat with your Data")

            # Display chat history with better formatting
            for message in st.session_state.get("messages", []):
                with st.chat_message(
                    message["role"],
                    avatar="🤖" if message["role"] == "assistant" else "👤",
                ):
                    st.markdown(message["content"])

            if prompt := st.chat_input("Ask me anything about your data..."):
                if "messages" not in st.session_state:
                    st.session_state.messages = []

                st.session_state.messages.append({"role": "user", "content": prompt})

                with st.chat_message("assistant", avatar="🤖"):
                    with st.spinner("🤔 Analyzing your question..."):
                        response = analyze_with_llama(prompt, csv_context)

                        if response:
                            st.markdown(response)
                            st.session_state.messages.append(
                                {"role": "assistant", "content": response}
                            )

    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")
