from bs4 import BeautifulSoup as bs4
import json
import requests
import pandas as pd


def main(url):
    res = requests.get(url)
    soup = bs4(res.content, 'html.parser')
    ol_tag = soup.find('ol', class_='row')
    boxes = ol_tag.find_all('li')
    links = []
    for box in boxes:
        href = box.find('a').get('href')
        product_url = f"https://www.bormadago.com{href}"
        links.append(product_url)
    return links

if __name__ == '__main__':
    all_links = []
    # There are 500 pages of products
    for i in range(1, 501):
        url = f"https://www.bormadago.com/catalogue/?page={i}"
        print('url', url)
        links = main(url)
        all_links.extend(links)

    unique_links = list(set(all_links))
    # write results to json file
    data = {
        "links": unique_links,
    }
    with open('./bormadago/links.json', 'w', encoding='utf-8') as fn:
        json.dump(data, fn, indent=4, ensure_ascii=False)
    print('Done')
    exit(0)
