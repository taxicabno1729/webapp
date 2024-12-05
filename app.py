import streamlit as st

# Configure page settings
st.set_page_config(
    page_title="Llama 2 AI Assistant",
    page_icon="🦙",
    layout="wide"
)

# App title and description
st.title("🦙 Llama 2 AI Assistant")
st.write("Welcome! Choose your desired AI assistant functionality from the sidebar.")

# Main page content
st.markdown("""
## Available Features:

### 🤖 Chatbot
Access our interactive Llama 2 chatbot for general conversations and queries.

### 🔍 Website Analyzer
Input any website URL to get an AI-powered analysis of its content.

---
**Instructions:**
1. Use the sidebar to navigate between features
2. Each tool has its own settings and parameters
3. You can return to this home page anytime using the navigation
""")

# Add footer
st.markdown("---")
st.markdown("Powered by Llama 2 | Built with Streamlit")