import streamlit as st
import requests
import base64
import io
from PIL import Image
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="AI Logo Generator",
    page_icon="🎨",
    layout="wide",
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: 500;
        margin-bottom: 2rem;
    }
    .logo-card {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        background-color: #f9f9f9;
    }
    .stButton button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)


API_URL = os.getenv("API_URL", "https://utkarsh134-logogeneration.hf.space/generate-logo")


def display_logos(logos):
    """Display the generated logos with download buttons"""
    st.markdown("### Your Generated Logos")
    st.markdown("Select and download your favorite designs")
    

    cols = st.columns(len(logos))
    
    for i, logo in enumerate(logos):
        with cols[i]:
            with st.container():
                st.markdown(f"<div class='logo-card'>", unsafe_allow_html=True)
                

                base64_data = logo["base64_data"]
                

                if base64_data.startswith('data:'):

                    base64_data = base64_data.split(',')[1] if ',' in base64_data else base64_data
                

                try:
                    image_bytes = base64.b64decode(base64_data)
                    image = Image.open(io.BytesIO(image_bytes))
                    

                    st.image(image, caption=f"Logo {i+1}", use_container_width=True)
                    
                    btn = st.download_button(
                        label=f"Download Logo {i+1}",
                        data=image_bytes,
                        file_name=logo["name"],
                        mime=f"image/{logo['format']}"
                    )
                except Exception as e:
                    st.error(f"Could not display logo {i+1}: {str(e)}")
                
                st.markdown("</div>", unsafe_allow_html=True)


st.markdown("<div class='main-header'>AI Logo Generator</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Create beautiful, unique logos for your brand</div>", unsafe_allow_html=True)


with st.form("logo_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        brand_name = st.text_input("Brand Name", placeholder="Enter your brand name")
    
    with col2:
        domain = st.text_input("Industry/Domain", placeholder="e.g., Technology, Healthcare, Education")
    

    submitted = st.form_submit_button("Generate Logos")


if submitted:
    if not brand_name or not domain:
        st.error("Please provide both brand name and domain.")
    else:
        with st.spinner("Generating your logos... This might take a minute."):
            try:

                payload = {
                    "brand_name": brand_name,
                    "domain": domain
                }
                

                response = requests.post(API_URL, json=payload)
                

                if response.status_code == 200:

                    logos = response.json().get("logos", [])
                    if logos:
                        display_logos(logos)
                    else:
                        st.warning("No logos were generated. Please try again.")
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
