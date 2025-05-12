import streamlit as st
import requests

API_URL = "https://utkarsh134-logogeneration.hf.space/generate-logo"  

st.set_page_config(page_title="Logo Generator", layout="wide")
st.title("🧠 Logo Generator")

st.markdown("""
    <style>
    .stButton button {
        width: 100%;
    }
    .logo-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
    }
    .logo-container {
        border: 1px solid #ddd;
        padding: 1rem;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    with st.form("logo_form"):
        brand_name = st.text_input("Brand Name", placeholder="e.g., EcoTech")
        domain = st.text_input("Domain / Industry", placeholder="e.g., Renewable Energy")
        submitted = st.form_submit_button("Generate Logos")

if submitted:
    if not brand_name or not domain:
        st.warning("Please fill both fields.")
    else:
        with st.spinner("🎨 Generating creative logos..."):
            try:
                response = requests.post(API_URL, json={"brand_name": brand_name, "domain": domain})
                response.raise_for_status()
                
                data = response.json()
                logos = data.get("logos", [])
                
                if logos:
                    st.success(f"✨ Successfully generated {len(logos)} unique logos!")
                    
                    cols = st.columns(3)
                    
                    for idx, logo in enumerate(logos):
                        with cols[idx % 3]:
                            st.markdown(f"### Logo {idx + 1}")
                            st.image(logo["url"], use_container_width=True)
                            
                            col_dl1, col_dl2 = st.columns(2)
                            with col_dl1:
                                st.markdown(f'<a href="{logo["url"]}" target="_blank" download="{logo["name"]}"><button style="width:100%">💾 Download</button></a>', unsafe_allow_html=True)
                            with col_dl2:
                                st.markdown(f"Format: {logo['format'].upper()}")
                else:
                    st.info("No logos were generated. Please try again.")
                    
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Error communicating with the API: {str(e)}")
            except Exception as e:
                st.error(f"❌ An unexpected error occurred: {str(e)}")
