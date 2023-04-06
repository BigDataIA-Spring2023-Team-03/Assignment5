import streamlit as st
import boto3
from datetime import datetime
from decouple import config
import ClothesReviewHub

# AWS KEYS
aws_access_key_id = config('aws_access_key_id')
aws_secret_access_key = config('aws_secret_access_key')
# log_aws_access_key_id = config('log_aws_access_key_id')
# log_aws_secret_access_key = config('log_aws_secret_access_key')

# S3 Details:
s3_bucket_name = 'damg7245-assignment5'

# Create an S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)

#######################################################
st.title('Image from Camera')

image_title = st.text_input('Image Title', '')
picture = st.camera_input("Take a picture:")

if picture and image_title != '':
    st.image(picture)
    filename = image_title + '_' + datetime.now().strftime("%d_%m_%y") + '.jpg'

    # Upload the file to the S3 bucket if it doesn't already exist
    if filename not in ClothesReviewHub.s3_files:
        # with open (filename,'wb') as file:
        #     file.write(picture.getbuffer())
        s3_client.upload_fileobj(picture, s3_bucket_name, 'Input/' + filename)
        st.write("File uploaded successfully!")
    else:
        st.write("File already exists in S3 bucket.")
    
    st.write(f'{filename} uploaded to S3! Go to ClothesReviewHub and select file from S3 dropdown.')
    # TODO: Auto selected in select an existing file from S3 on the ClothesReviewHub page
    