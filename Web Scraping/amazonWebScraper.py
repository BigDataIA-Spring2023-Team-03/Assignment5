import requests
from bs4 import BeautifulSoup

search_term = 'nike sports shoes'
search_terms = search_term.split(" ")
search_string = "+".join(search_terms)
print(search_string)

url = f'https://www.amazon.com/s?k={search_string}'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

response = requests.get(url, headers=headers)
html_content = response.content

soup = BeautifulSoup(html_content, 'lxml')

products = soup.find_all('div', {'data-component-type': 's-search-result'})
print("products: ",products)
for product in products:
    # Get the product title
    title = product.find('h2').text.strip()

    # Get the product link
    link = product.find('a', {'class': 'a-link-normal'})['href']

    # Get the product image
    image = product.find('img')['src']

    # Print the product information
    print(title)
    print(link)
    print(image)
