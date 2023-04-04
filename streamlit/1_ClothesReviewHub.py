import streamlit as st
from PIL import Image
from google.cloud import vision
import io
import os
from google.oauth2 import service_account
from decouple import config
import boto3

# AWS KEYS
aws_access_key_id = config('aws_access_key_id')
aws_secret_access_key = config('aws_secret_access_key')
# log_aws_access_key_id = config('log_aws_access_key_id')
# log_aws_secret_access_key = config('log_aws_secret_access_key')
# Google Credentials
credentials = service_account.Credentials.from_service_account_file('damg7245-team3-assignment5-b0ba9f72c8a3.json')

# S3 Details:
s3_bucket_name = 'damg7245-assignment5'

# Create an S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)


def detect_labels(file):
    """Detects labels in the file."""
    client = vision.ImageAnnotatorClient(credentials=credentials)

    # with io.open(file, 'rb') as image_file:
    #     content = image_file.read()
    content = file.read()

    image = vision.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')

    label_list = []
    for label in labels:
        label_list.append(label.description)
        print(label.description)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    
    return label_list
    

#########################################################################
# Create a dropdown to select an existing file from the S3 bucket
s3_objects = s3_client.list_objects_v2(Bucket=s3_bucket_name, Prefix='Input/')
s3_files = [obj["Key"] for obj in s3_objects.get("Contents", []) if not obj['Key'] == 'Input/']
# Get Necessary file
s3_files = [file.split('/')[1] for file in s3_files if file[-1] != '/' and file.split('.')[1] in ('jpg')]

selected_file = st.selectbox("Select an existing file from S3", ["None"] + s3_files)

# IMAGE SELECTION
# Upload image
# TODO: max size is 4MB
uploaded_file = st.file_uploader("Choose an image (jpg):", type="jpg")

if uploaded_file is not None:
    # Upload to S3
    if uploaded_file.name.split('.')[1] not in ('jpg'):
        st.error(f'Incorrect File Format!')
        st.stop()
    # Get the file name and size
    filename = uploaded_file.name
    # if not filename == st.session_state.file_name:
    #     st.session_state.transcription_generated = False
    #     st.session_state.transcript = ''
    #     st.session_state.file_name = filename
    #     st.session_state.convert_to_transcript = False
    filesize = uploaded_file.size

    # Print the file name and size
    st.write("File name:", filename)
    st.write("File size:", filesize, "bytes")

    # Upload the file to the S3 bucket if it doesn't already exist
    if filename not in s3_files:
        s3_client.upload_fileobj(uploaded_file, s3_bucket_name, 'Input/' + filename)
        st.write("File uploaded successfully!")
    else:
        st.write("File already exists in S3 bucket.")
    
    # Load image
    image = Image.open(uploaded_file)
    # TESTING
    # print(uploaded_file)
    # print(type(uploaded_file))
    # print(type(image))

    # Display image
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Get Image file from S3
    response = s3_client.get_object(Bucket=s3_bucket_name, Key='Input/' + filename)
    image_data = response["Body"]

    # Google Vision API to detect labels
    label_list = detect_labels(image_data)

    st.write(f'Label List: {label_list}')

    # """Detects labels in the file."""
    # client = vision.ImageAnnotatorClient(credentials=credentials)

    # # TESTING 
    # path = 'Example_Images/patagonia_fleece.jpg'

    # with io.open(path, 'rb') as image_file:
    #     content = image_file.read()

    # image = vision.Image(content=content)

    # response = client.label_detection(image=image)
    # labels = response.label_annotations
    # print('Labels:')

    # for label in labels:
    #     print(label.description)

    # if response.error.message:
    #     raise Exception(
    #         '{}\nFor more info on error messages, check: '
    #         'https://cloud.google.com/apis/design/errors'.format(
    #             response.error.message))
