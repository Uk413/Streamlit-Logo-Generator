import streamlit as st
import requests
import base64

API_URL = "https://utkarsh134-logogeneration.hf.space/generate-logo"  

st.set_page_config(page_title="Logo Generator", layout="centered")
st.title("Logo Generator ")

with st.form("logo_form"):
    brand_name = st.text_input("Brand Name", placeholder="e.g., EcoTech")
    domain = st.text_input("Domain / Industry", placeholder="e.g., Renewable Energy")
    submitted = st.form_submit_button("Generate Logos")

if submitted:
    if not brand_name or not domain:
        st.warning("Please fill both fields.")
    else:
        with st.spinner("Generating logos..."):
            response = requests.post(API_URL, json={"brand_name": brand_name, "domain": domain})
        
        if response.status_code == 200:
            data = response.json()
            logos = data.get("logos", [])
            
            if logos:
                st.success(f"Generated {len(logos)} logo(s):")
                for idx, logo in enumerate(logos, 1):
                    st.image(logo["base64_data"], caption=logo["name"],use_container_width=True)
                    

                    image_bytes = base64.b64decode(logo["base64_data"].split(",")[1])
                    st.download_button(
                        label="Download",
                        data=image_bytes,
                        file_name=logo["name"],
                        mime=f"image/{logo['format']}"
                    )
            else:
                st.info("No logos returned.")
        else:
            st.error(f"API error: {response.status_code} - {response.text}")
