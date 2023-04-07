import openai
import io
import os
from dotenv import load_dotenv
import boto3
import io
import os
import requests
from dotenv import load_dotenv
from typing import Tuple
import boto3
from botocore.client import Config
import json

load_dotenv()
openai_key = os.getenv("open_ai_key")

openai.api_key = openai_key

def should_buy_product(review):
    prompt = "Based on the following review, determine if the review is positive or negative? \n\nReview: {}\nOutput:".format(review)
    print(prompt)
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=1,
        n=1,
        stop=None,
    )
    output = response['choices'][0]['text']
    print("\n Response",response)
    return output