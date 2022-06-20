from bs4 import BeautifulSoup as bs4
import json
import requests
import pandas as pd


def get_product_info(url):
    """
    get name, description, upc, image, price
    """
    res = requests.get(url)
    soup = bs4(res.content, 'html.parser')
    desc_div = soup.find('div', class_='product-description-name')
    name = desc_div.find('h1').text
    label_div = soup.find('div', class_='product-description-price-label')
    upc = label_div.find('h2').text
    description_span = soup.find('span', itemprop='description')
    description = description_span.text
    offerDetails = soup.find('span', itemprop='offerDetails')
    price_table = offerDetails.find('table')
    price = price_table.find_all('tr')[2].find_all('td')[2].text.strip()
    image_div = soup.find('div', class_='product-image-main')
    domain = "http://www.efooddepot.com"
    image_path = domain + image_div.find('img').get('src')
    return {
        "name": name,
        "upc": upc,
        "description": description,
        "price": price,
        "image": image_path,
    }


if __name__ == '__main__':
    with open('links.json', 'r', encoding='utf-8') as fn:
        data = json.load(fn)
    links = data['links']
    results = []
    for link in links:
        product = get_product_info(link)
        print(product)
        results.append(product)
    df = pd.DataFrame(results)
    df.to_csv('results.csv', index=False, sep=';')
    print('Done')
    exit(0)
