import streamlit as st
from PIL import Image
from google.cloud import vision
from google.oauth2 import service_account
from decouple import config
import boto3
import openai
import io
from amazonWebScraper import WalmartReviews
from ProductBuy import should_buy_product
from Logging.aws_logging import write_logs
import json

# AWS KEYS
aws_access_key_id = config('aws_access_key_id')
aws_secret_access_key = config('aws_secret_access_key')

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

##########################################################################
# Goog Cloud Vision APIs
# Detect Labels and Logos
def detect_labels_logos(file):
    """Detects labels in the file."""
    client = vision.ImageAnnotatorClient(credentials=credentials)

    content = file.read()
    image = vision.Image(content=content)

    # Labels
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

    # Logos
    response = client.logo_detection(image=image)
    logos = response.logo_annotations
    print('Logos:')

    logo_list = []
    for logo in logos:
        logo_list.append(logo.description)
        print(logo.description)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    
    return label_list, logo_list


#########################################################################
st.title('ClothesReviewHub')
st.subheader('Three Upload Options: Take a Picture, Select Existing from S3, Upload an Image')

# Take Picture Option
link = 'http://44.214.57.19:8501/Camera_Image'

st.markdown(f'To take a picture using your device, use this link: <a href={link}>Take Picture</a>', unsafe_allow_html=True)

# Create a dropdown to select an existing file from the S3 bucket
s3_objects = s3_client.list_objects_v2(Bucket=s3_bucket_name, Prefix='Input/')
s3_files = [obj["Key"] for obj in s3_objects.get("Contents", []) if not obj['Key'] == 'Input/']
# Get Necessary file
s3_files = [file.split('/')[1] for file in s3_files if file[-1] != '/' and file.split('.')[1] in ('jpg')]
selected_file = "None"
selected_image = None
if len(s3_files) == 0:
    st.write("No files found in S3 bucket.")
    selected_file = None
else:
    selected_file = st.selectbox("Select an existing file from S3", ["None"] + s3_files)
    if not selected_file == "None":
        try:
            obj = s3_client.get_object(Bucket=s3_bucket_name, Key="Input/" + selected_file)
            file_content = obj['Body'].read()
            selected_image = Image.open(io.BytesIO(file_content))
            st.image(selected_image, caption=selected_file, use_column_width=True)
        except:
            st.error("File not found")
    else:
        st.write("No File Selected")

uploaded_file = st.file_uploader("Choose an image (jpg):", type="jpg")

if uploaded_file and selected_file != "None":
    st.write("Error: please select only one option")

else:

    if selected_image is not None:
        response = s3_client.get_object(Bucket=s3_bucket_name, Key='Input/' + selected_file)
        image_data = response["Body"]
        label_list, logo_list = detect_labels_logos(image_data)

        st.write(f'Label List: {label_list}')

        label_query = ""
        for i in label_list:
            label_query += i
            label_query += " "

        st.write("")
        st.write(label_query)
        st.write(f'Logo List: {logo_list}')

        st.subheader('Select Marketplace to Search for Similar Products:')
        walmart = st.checkbox('Get Walmart Reviews')

        if walmart:
            products, reviews = WalmartReviews(label_query)
            log_results = {'Image_File': selected_file,
                           'Logo_List': logo_list,
                           'Label_List': label_list,
                           'Marketplace': 'Walmart',
                           'Products': products
                           }
            write_logs(str(log_results))
            for j,i in enumerate(products):
                st.image(i, width=300)

                st.write('Want to Learn More? Check below to generate a summary of product reviews:')
                learn_more = st.checkbox('Learn More?', key = j)
                if learn_more:
                    all_reviews = ""
                    st.title('Summary of Reviews')
                    for item in reviews:
                        st.text("")
                        summary_prompt = "Summarize the below reviews into 2-3 sentences and suggest whether a user should buy the product:"

                        completion = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=[{"role": "user", "content": summary_prompt + str(item)}],
                            temperature=0.7
                        )

                        chat_output = completion.choices[0].message.content.strip()
                        st.write(chat_output)

    if uploaded_file is not None:
        # Upload to S3
        if uploaded_file.name.split('.')[1] not in ('jpg'):
            st.error(f'Incorrect File Format!')
            st.stop()
        filename = uploaded_file.name
        filesize = uploaded_file.size

        st.write("File name:", filename)
        st.write("File size:", filesize, "bytes")

        if filename not in s3_files:
            s3_client.upload_fileobj(uploaded_file, s3_bucket_name, 'Input/' + filename)
            st.write("File uploaded successfully!")
        else:
            st.write("File already exists in S3 bucket.")

        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Get Image file from S3
        response = s3_client.get_object(Bucket=s3_bucket_name, Key='Input/' + filename)
        image_data = response["Body"]
        label_list, logo_list = detect_labels_logos(image_data)

        st.write(f'Label List: {label_list}')

        label_query = ""
        for i in label_list:
            label_query += i
            label_query += " "

        st.write("")
        st.write(label_query)
        st.write(f'Logo List: {logo_list}')

        st.subheader('Select Marketplace to Search for Similar Products:')
        walmart = st.checkbox('Get Walmart Reviews')

        if walmart:
            products, reviews = WalmartReviews(label_query)

            log_results = {'Image_File': filename,
                           'Logo_List': logo_list,
                           'Label_List': label_list,
                           'Marketplace': 'Walmart',
                           'Products': products
                           }
            write_logs(str(log_results))

            json_str = json.dumps(log_results)
            s3_client.put_object(Bucket=s3_bucket_name, Key='Results/' + filename.split('.')[0] + '.json',
                                 Body=json_str)

            st.write(f"{filename.split('.')[0]}.json uploaded to S3")

            for j,i in enumerate(products):
                st.image(i, width=300)
                st.write('Want to Learn More? Check below to generate a summary of product reviews:')
                learn_more = st.checkbox('Learn More?', key = j)
                # Generate Summary of Reviews
                if learn_more:
                    all_reviews = ""
                    st.title('Summary of Reviews')
                    for item in reviews:
                        st.text("")
                        summary_prompt = "Summarize the below reviews into 2-3 sentences and suggest whether a user should buy the product:"

                        completion = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=[{"role": "user", "content": summary_prompt + str(item)}],
                            temperature=0.7
                        )

                        chat_output = completion.choices[0].message.content.strip()
                        st.write(chat_output)
