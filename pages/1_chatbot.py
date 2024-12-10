"""Streamlit chatbot interface for Llama 2 model using Ollama backend."""

# Remove or comment out the unused import
# import json

import os

import requests
import streamlit as st

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# Configure page settings
st.set_page_config(page_title="Llama 2 Chatbot", page_icon="🦙")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# App title
st.title("🦙 Llama 2 Chatbot")

# Add sidebar controls
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []

# Add model parameters in sidebar
st.sidebar.title("Model Parameters")
temperature = st.sidebar.slider(
    "Temperature", min_value=0.1, max_value=2.0, value=0.7, step=0.1
)


# Function to generate response from Ollama
def generate_response(prompt, temperature):
    """Generate a response from the Ollama API.

    Args:
        prompt (str): The user's input prompt
        temperature (float): The temperature parameter for response generation

    Returns:
        str: The generated response from the model, or None if an error occurs
    """
    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False,
                "temperature": temperature,
            },
        )
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        st.error(f"Error connecting to Ollama: {str(e)}")
        return None


# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        # Generate response
        response = generate_response(prompt, temperature)

        if response:
            message_placeholder.markdown(response)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
