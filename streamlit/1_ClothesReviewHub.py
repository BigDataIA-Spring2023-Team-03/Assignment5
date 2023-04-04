import streamlit as st
from PIL import Image

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type="jpg")

if uploaded_file is not None:
    # Load image
    image = Image.open(uploaded_file)

    # Display image
    st.image(image, caption="Uploaded Image", use_column_width=True)

    
