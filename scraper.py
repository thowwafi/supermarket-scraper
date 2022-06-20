import os
import requests
from bs4 import BeautifulSoup as bs4


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
    # return name, price


if __name__ == '__main__':
    links = main()
    for link in links:
        name, price = get_product_info(link)
        print(name, price)
    print('Done')
    exit(0)
