"""Meme Generator module for creating custom memes via the Imgflip API."""

import os
from io import BytesIO

import requests
import streamlit as st
from PIL import Image

# Configure page settings
st.set_page_config(page_title="Meme Generator", page_icon="🎭")


def get_meme_templates():
    """Fetch available meme templates from imgflip API."""
    try:
        response = requests.get("https://api.imgflip.com/get_memes")
        if response.status_code == 200:
            return response.json()["data"]["memes"]
        return []
    except Exception as e:
        st.error(f"Error fetching meme templates: {str(e)}")
        return []


def generate_meme(template_id, text0, text1, username, password):
    """Generate a meme using the imgflip API."""
    url = "https://api.imgflip.com/caption_image"
    params = {
        "template_id": template_id,
        "username": username,
        "password": password,
        "text0": text0,
        "text1": text1,
    }

    try:
        response = requests.post(url, data=params)
        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                return data["data"]["url"]
            else:
                st.error(f"API Error: {data['error_message']}")
                return None
    except Exception as e:
        st.error(f"Error generating meme: {str(e)}")
        return None


# UI Elements
st.title("🎭 Meme Generator")
st.write("Create custom memes using popular templates!")

# Imgflip credentials
# You should store these securely in environment variables
IMGFLIP_USERNAME = os.getenv("IMGFLIP_USERNAME", "TheCrazyKid2007")
IMGFLIP_PASSWORD = os.getenv("IMGFLIP_PASSWORD", "TheCreativeKid2007")

# Get meme templates
templates = get_meme_templates()

if templates:
    # Create a selection box with meme templates
    selected_template = st.selectbox(
        "Choose a meme template:", options=templates, format_func=lambda x: x["name"]
    )

    # Display selected template preview
    if selected_template:
        col1, col2 = st.columns([1, 1])

        with col1:
            st.image(
                selected_template["url"], caption=selected_template["name"], width=300
            )

        with col2:
            # Input fields for meme text
            top_text = st.text_input("Top Text:", key="top_text")
            bottom_text = st.text_input("Bottom Text:", key="bottom_text")

            if st.button("Generate Meme"):
                if not (IMGFLIP_USERNAME and IMGFLIP_PASSWORD):
                    st.error(
                        "Please set your Imgflip credentials in environment variables!"
                    )
                else:
                    with st.spinner("Generating meme..."):
                        meme_url = generate_meme(
                            selected_template["id"],
                            top_text,
                            bottom_text,
                            IMGFLIP_USERNAME,
                            IMGFLIP_PASSWORD,
                        )

                        if meme_url:
                            st.success("Meme generated successfully!")
                            st.image(meme_url, caption="Generated Meme")

                            # Download button
                            response = requests.get(meme_url)
                            image = Image.open(BytesIO(response.content))
                            buf = BytesIO()
                            image.save(buf, format="PNG")
                            st.download_button(
                                label="Download Meme",
                                data=buf.getvalue(),
                                file_name="generated_meme.png",
                                mime="image/png",
                            )
else:
    st.error("Unable to fetch meme templates. Please try again later.")

# Add instructions in sidebar
with st.sidebar:
    st.markdown(
        """
    ### How to Use
    1. Select a meme template
    2. Enter your top and bottom text
    3. Click 'Generate Meme'
    4. Download your created meme

    Note: This tool uses the Imgflip API to generate memes.
    """
    )
