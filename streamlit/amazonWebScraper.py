from serpapi import GoogleSearch
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
serp_key = os.getenv("serp_key")

def WalmartReviews(query):
  params = {
    "engine": "walmart",
    "query": query,
    "api_key": serp_key,
    "sort": "best_seller"
  }

  search = GoogleSearch(params)
  results = search.get_dict()
  organic_results = results["organic_results"]

  top3 = organic_results[:3]

  top3_dict = {}

  index = 0
  products = []
  for i in top3:
    top3_dict[index]= {}
    top3_dict[index]['us_item_id'] = i['us_item_id']
    top3_dict[index]['title'] = i['title']
    top3_dict[index]['thumbnail'] = i['thumbnail']

    products.append(top3_dict[index]['thumbnail'])

    index = index + 1
    

  for i in top3_dict.values():
    params = {
      "engine": "walmart_product_reviews",
      "product_id": i['us_item_id'],
      "api_key": serp_key,
      "sort": "relevancy"
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    print(results['overall_rating'])
    reviews = []
    for i in results['reviews']:
      text = {}
      if 'title' in i:
        text['title'] = i['title']
      text['review'] = i['text']
      reviews.append(text)

    print(reviews)
    return products,reviews



