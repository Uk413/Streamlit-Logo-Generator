import streamlit as st
import requests
from PIL import Image
import base64
import io

API_URL = "https://utkarsh134-logogeneration.hf.space"

st.set_page_config(
    page_title="Logo Generator",
    page_icon="🎨",
    layout="wide"
)

st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .logo-container {
        border: 1px solid #eee;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem;
        text-align: center;
        background-color: white;
    }
    .stButton button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

st.title("AI Logo Generator")
st.markdown("Generate professional logos for your brand using AI")

with st.form("logo_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        brand_name = st.text_input("Brand Name", placeholder="Enter your brand name")
    
    with col2:
        domain = st.text_input("Domain/Industry", placeholder="e.g., Technology, Healthcare, Food")
    
    submit_button = st.form_submit_button("Generate Logos")

def decode_base64_to_image(base64_data):

    if "base64," in base64_data:
        base64_data = base64_data.split("base64,")[1]
    
    image_bytes = base64.b64decode(base64_data)
    image = Image.open(io.BytesIO(image_bytes))
    return image


def clean_base64_data(base64_string):
    """
    Clean and validate base64 data, ensuring it's in the correct format
    Returns tuple of (is_valid, cleaned_data)
    """

    if not isinstance(base64_string, str):
        return False, None
    

    if base64_string.startswith('data:'):
        try:

            _, data = base64_string.split(';base64,', 1)
            return True, data
        except ValueError:

            return False, None
    

    try:

        decoded = base64.b64decode(base64_string)
        return True, base64_string
    except:
        return False, None

if submit_button and brand_name and domain:
    with st.spinner("Generating logos... This may take a minute"):
        try:

            response = requests.post(
                f"{API_URL}/generate-logo",
                json={"brand_name": brand_name, "domain": domain}
            )
            
            if response.status_code == 200:

                st.write("Response received:")
                response_data = response.json()
                
   
                if "logos" in response_data:
                    st.write(f"Found {len(response_data['logos'])} logos in response")
                    if len(response_data['logos']) > 0:
                        sample_logo = response_data['logos'][0]
                        st.write("Sample logo keys:", list(sample_logo.keys()))
                        if "base64_data" in sample_logo:
                            base64_preview = sample_logo["base64_data"][:50] + "..." if len(sample_logo["base64_data"]) > 50 else sample_logo["base64_data"]
                            st.write("Base64 data preview:", base64_preview)
                else:
                    st.write("Response format:", response_data.keys())
                
                logos_data = response_data.get("logos", [])
                
                if logos_data:
                    st.success(f"Generated {len(logos_data)} logos!")
                    

                    cols = st.columns(3)
                    
                    for i, logo in enumerate(logos_data):
                        col_idx = i % 3
                        
                        with cols[col_idx]:
                            st.markdown(f"<div class='logo-container'>", unsafe_allow_html=True)
                            
             
                            try:
                                base64_data = logo["base64_data"]
                                st.write(f"Image {i+1} data type:", type(base64_data))
                                

                                is_valid, cleaned_base64 = clean_base64_data(base64_data)
                                
                                if is_valid:

                                    img_format = logo.get("format", "png")
                                    image_data_uri = f"data:image/{img_format};base64,{cleaned_base64}"
                                    

                                    st.image(image_data_uri, caption=f"Logo {i+1}", use_container_width=True)
                                    
           
                                    download_filename = logo.get("name", f"logo_{i+1}.{img_format}")
                                    
                                    try:
                                        st.download_button(
                                            label=f"Download Logo {i+1}",
                                            data=base64.b64decode(cleaned_base64),
                                            file_name=download_filename,
                                            mime=f"image/{img_format}",
                                            key=f"download_btn_{i}"
                                        )
                                    except Exception as e:
                                        st.error(f"Error creating download button for logo {i+1}: {str(e)}")
                                else:
                                    st.error(f"Logo {i+1} has invalid base64 data")
                                    st.write("Data preview:", str(base64_data)[:100] + "..." if base64_data and len(str(base64_data)) > 100 else str(base64_data))
                            except Exception as e:
                                st.error(f"Error displaying logo {i+1}: {str(e)}")
                                st.write("Error details:", str(e))
                            
                            st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.warning("No logos were generated. Please try again.")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        
        except requests.exceptions.ConnectionError:
            st.error(f"Could not connect to the API at {API_URL}. Make sure the API server is running.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
elif submit_button:
    st.warning("Please enter both brand name and domain.")

