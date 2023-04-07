import os
import streamlit as st
import boto3
from botocore.errorfactory import ClientError
import requests
import time
import json
import pandas as pd
from datetime import datetime, timedelta
from decouple import config

# DEV or PROD
environment = 'PROD'
if environment == 'DEV':
    webserver = 'localhost:8080'
elif environment == 'PROD':
    webserver = 'airflow-airflow-webserver-1:8080'


# AWS KEYS
aws_access_key_id = config('aws_access_key_id')
aws_secret_access_key = config('aws_secret_access_key')
# AWS LOG KEYS
log_aws_access_key_id = config('log_aws_access_key_id')
log_aws_secret_access_key = config('log_aws_secret_access_key')

# Create an S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)


# create a client for logs
clientlogs = boto3.client('logs',
                        region_name='us-east-1',
                        aws_access_key_id=log_aws_access_key_id,
                        aws_secret_access_key=log_aws_secret_access_key)

# S3 Details:
s3_bucket_name = 'damg7245-assignment5'
s3_folder = 'Results'
# Cloudwatch details:
log_group = 'assignment5-log-group'


# Set the title of the app
st.title("Admin Dashboard")
st.write('This dashboard shows history of app.')

# Enter Password to Access Batch Functionality
password = st.text_input("Enter Password:")

if password != '':
    if password == 'damgadmin': 
        #############################################################################
        # # CUSTOM QUESTION HISTORY FROM CLOUD WATCH
        # query = """
        # fields @timestamp, @message | filter @message like /Custom_Question/ | sort @timestamp desc | limit 25
        # """

        # start_query_response = clientlogs.start_query(
        #     logGroupName=log_group,
        #     startTime=int((datetime.today() - timedelta(days=5)).timestamp()),
        #     endTime=int(datetime.now().timestamp()),
        #     queryString=query,
        # )
        # # start_query_response

        # query_id = start_query_response['queryId']

        # response = None

        # while response == None or response['status'] == 'Running':
        #     print('Waiting for query to complete ...')
        #     time.sleep(1)
        #     response = clientlogs.get_query_results(
        #         queryId=query_id
        #     )

        # data = response['results']

        # message_records = []
        # for record in data:
        #     # convert dictionary string to dictionary
        #     # st.write(type(eval(record[1]['value'])))
        #     record_dict = eval(record[1]['value'])
        #     message_records.append(record_dict)

        # # message_records
        # log_df = pd.DataFrame(message_records)
        # st.header('CloudWatch Records of Image History (25 Most Recent):')
        # st.write(log_df.head(25))


        # ######################################################################################################
        # Download Results for a specific file
        # Create a dropdown to select an existing file from the S3 bucket
        s3_objects = s3_client.list_objects_v2(Bucket=s3_bucket_name, Prefix='Input/')
        s3_files = [obj["Key"] for obj in s3_objects.get("Contents", []) if not obj['Key'] == 'Input/']
        # Get Necessary file
        s3_files = [file.split('/')[1] for file in s3_files if file[-1] != '/' and file.split('.')[1] in ('jpg')]

        selected_file = st.selectbox("Get Image and Results from Previous run:", ["None"] + s3_files)
        # st.write(selected_file) 
        selected_file = 'jared_sweater_06_04_23.jpg'

        if selected_file:
            # Check if file has been run through the app
            result_file = selected_file.split('.')[0] + '.json'

            try:
                s3_client.head_object(Bucket=s3_bucket_name, Key=f'{s3_folder}/{result_file}')
                st.write(f"{selected_file} has a results file!")

                # download file
                # s3_client.download_file(s3_bucket_name, f'{s3_folder}/{result_file}', result_file)

                # Download the file from S3
                response = s3_client.get_object(Bucket=s3_bucket_name, Key=f'{s3_folder}/{result_file}')

                # Get the file content
                file_content = response['Body'].read()

                st.download_button('Download Results', file_content, result_file)

            except ClientError as e:
                if e.response['Error']['Code'] == "404":
                    # The key does not exist.
                    st.write(f"Image, {selected_file} doesn't have a results file!")
                elif e.response['Error']['Code'] == 403:
                    # Unauthorized, including invalid bucket
                    st.write('Unauthorized, including invalid bucket')
        
    else:
        st.error("You don't have permission to access this functionality")
