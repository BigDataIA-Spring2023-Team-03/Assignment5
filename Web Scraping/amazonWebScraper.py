from serpapi import GoogleSearch

query = "Black Tshirt Men"
params = {
  "engine": "walmart",
  "query": query,
  "api_key": "<Serp api key>",
  "sort": "best_seller"
}

search = GoogleSearch(params)
results = search.get_dict()
organic_results = results["organic_results"]

top3 = organic_results[:3]

top3_dict = {}

index = 0
for i in top3:
  top3_dict[index]= {}
  top3_dict[index]['us_item_id'] = i['us_item_id']
  top3_dict[index]['title'] = i['title']
  top3_dict[index]['thumbnail'] = i['thumbnail']
  index = index + 1

for i in top3_dict.values():
  params = {
    "engine": "walmart_product_reviews",
    "product_id": i['us_item_id'],
    "api_key": "9661f96f63bd4ca12a877d9ea0d9597fb800a41f432d1d77895032f340352939",
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



