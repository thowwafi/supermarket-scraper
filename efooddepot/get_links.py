from bs4 import BeautifulSoup as bs4
import json
import requests
import pandas as pd


def main(url):
    res = requests.get(url)
    soup = bs4(res.content, 'html.parser')
    boxes = soup.find_all('td', class_="fourth")
    links = []
    for box in boxes:
        href = box.find('a').get('href')
        links.append(href)
    return links


def get_product_info(url):
    """
    get gambar, upc, descripsi, harga
    """
    res = requests.get(url)
    soup = bs4(res.content, 'html.parser')
    # name = soup.find('h1', class_="product-name").text
    # price = soup.find('span', class_="price").text
    return {
        "name": "",
        "price": "",
        "image": "",
        "upc": "",
        "description": "",
    }


if __name__ == '__main__':
    all_links = []
    # There are 160 pages in Indonesian products pages
    for i in range(1, 161):
        url = f"http://www.efooddepot.com/products/grid/24/0/0/0/0/25/{i}/all.html"
        print('url', url)
        links = main(url)
        all_links.extend(links)
    data = {
        "links": all_links,
    }
    with open('links.json', 'w', encoding='utf-8') as fn:
        json.dump(data, fn, indent=4, ensure_ascii=False)
    # results = []
    # for link in all_links:
    #     product = get_product_info(link)
    #     print(product)
    #     results.append(product)
    # df = pd.DataFrame(results)
    # df.to_csv('results.csv')
    print('Done')
    exit(0)
