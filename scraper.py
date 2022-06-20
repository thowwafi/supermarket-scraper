from bs4 import BeautifulSoup as bs4
import requests
import pandas as pd


url = "http://www.efooddepot.com/ethnics/indonesian.html"


def main():
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
    links = main()
    results = []
    for link in links:
        product = get_product_info(link)
        print(product)
        results.append(product)
    df = pd.DataFrame(results)
    df.to_csv('results.csv')
    print('Done')
    exit(0)
