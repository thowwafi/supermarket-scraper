from bs4 import BeautifulSoup as bs4
import json
import mimetypes
import requests
import pandas as pd
import re


def extract_price(value):
    results = re.findall('[0-9]+', value)
    return "".join(results)


def convert_to_float(value):
    new_value = value.replace('.','').replace(',','.')
    return float(new_value)


def save_image(image_url, name):
    response = requests.get(image_url)
    content_type = response.headers['content-type']
    extension = mimetypes.guess_extension(content_type)
    img_data = response.content
    with open(f"{name}{extension}", 'wb') as handler:
        handler.write(img_data)


def save_excel(data, path):
    df = pd.DataFrame(data)
    df.to_excel(path, index=False)


def get_product_info(url):
    """
    get name, description, upc, image, price
    """
    res = requests.get(url)
    soup = bs4(res.content, 'html.parser')
    table = soup.find('table', class_='table table-striped')
    rows = table.find_all('tr')
    upc = rows[0].find('td').text
    price = extract_price(rows[2].find('td').text)
    lebar = convert_to_float(rows[4].find('td').text)
    berat = convert_to_float(rows[5].find('td').text)
    panjang = convert_to_float(rows[7].find('td').text)
    tinggi = convert_to_float(rows[8].find('td').text)
    image_url = soup.find('product-zoomer').get('regular')
    if desc_head := soup.find('div', {'id': 'product_description'}):
        description = desc_head.next_sibling.next_sibling.text.strip()
    else:
        description = ""
    kategori = soup.find('ul', class_='breadcrumb').text.strip().replace('\n\n', '/').replace('\n', ' ')
    
    save_image(image_url, f"./bormadago/images/{upc}")
    return {
        "name": soup.find('h1').text,
        "deskripsi": description,
        "kategori": kategori,
        "upc": upc,
        "jenis_produk": rows[1].find('td').text,
        "harga": price,
        "ketersediaan": rows[3].find('td').text,
        "lebar": lebar,
        "berat": berat,
        "manufacturer": rows[6].find('td').text,
        "panjang": panjang,
        "tinggi": tinggi,
        "image": image_url,
        "link": url
    }


if __name__ == '__main__':
    # read links from json file
    with open('./bormadago/links.json', 'r', encoding='utf-8') as fn:
        data = json.load(fn)
    links = data['links']

    # get product info
    results = []
    for link in links:
        print(link)
        product = get_product_info(link)
        results.append(product)

    # write results to csv
    save_excel(results, "./bormadago/bormadago.xlsx")
    print('Done')
    exit(0)
