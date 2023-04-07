import streamlit as st
from PIL import Image
import os
import requests
from tempfile import NamedTemporaryFile
import tempfile


# Comparing Source and Target Images
def compare_score(image1_path, image2_path):
    '''
    Uses API from DeepAI to compare two images and returns a value that tells you how visually similar they are.
    The lower the score, the more contextually similar the two images are with a score of '0' being identical.
    '''
    url = "https://api.deepai.org/api/image-similarity"
    headers = {"api-key": "d7b43115-5b69-4fff-bc91-3bc404b3f23a"}

    files = {"image1": open(image1_path, 'rb'), "image2": open(image2_path, 'rb')}

    response = requests.post(url, headers=headers, files=files)

    response_json = response.json()
    return response_json['output']['distance']

st.title("Comparing and Finding the Best Match Clothing Item")

st.subheader("Upload Source Image")
# Using file uploader to upload the source image
source_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])


# Displaying the uploaded source image
if source_file is not None:
    image = Image.open(source_file)
    st.image(image, caption="Uploaded Image", width=300)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
        tmp_file.write(source_file.getbuffer())
        file_path = tmp_file.name

if source_file is not None:
    source_path = file_path
    st.write("Source File Path:", file_path)

# Upload single target file
st.subheader("Upload Target Images")
target_files = st.file_uploader("Choose images", type=["jpg", "jpeg", "png"])

# Displaying the uploaded target images
if target_files is not None:
    image = Image.open(target_files)
    # st.image(image, caption="Uploaded Image", width=200)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
        tmp_file.write(target_files.getbuffer())
        file_path = tmp_file.name

if target_files is not None:
    target_path = file_path
    st.write('Target File path:', file_path)

st.subheader("Comparison Score")
st.text("Apparel with the Lowest Score is the Best Match")
if source_path is not None and target_path is not None:
    score = compare_score(source_path, target_path)
    st.write('Camparison Score:', score)

if target_files is not None:
    image = Image.open(target_files)
    st.image(image, caption="Uploaded Image", width=200)


# ## Code for uploading multiple Images
# # Using file uploader to upload multiple target image
# target_files = st.file_uploader("Choose images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# # Error Handeling to just upload 3 target images
# if len(target_files) > 3:
#     st.error("You can upload a maximum of three images.")

# # Displaying the uploaded target images
# if target_files is not None  and len(target_files) <= 3:
#     # Create a row with multiple columns using st.columns()
#     col1, col2, col3 = st.columns(3)
#     columns = [col1, col2, col3]
#     # Iterate over each uploaded file and display the images horizontally
#     for i, uploaded_file in enumerate(target_files):
#         # Opening target file
#         image = Image.open(uploaded_file)
#         with columns[i % 3]:
#             st.image(image, caption="Uploaded Image", width=200)
            





        



