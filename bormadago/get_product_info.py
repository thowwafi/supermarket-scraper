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
    th_upc = table.find('th', text=re.compile('upc', re.I))
    upc = th_upc.find_next('td').text

    th_jenis_produk = table.find('th', text=re.compile('jenis produk', re.I))
    jenis_produk = th_jenis_produk.find_next('td').text

    th_price = table.find('th', text=re.compile('harga', re.I))
    price = th_price.find_next('td').text
    price = extract_price(price)

    th_ketersediaan = table.find('th', text=re.compile('ketersediaan', re.I))
    ketersediaan = th_ketersediaan.find_next('td').text

    th_lebar = table.find('th', text=re.compile('lebar', re.I))
    lebar = th_lebar.find_next('td').text
    lebar = convert_to_float(lebar)

    th_berat = table.find('th', text=re.compile('berat', re.I))
    berat = th_berat.find_next('td').text
    berat = convert_to_float(berat)

    th_manufacturer = table.find('th', text=re.compile('manufacturer', re.I))
    manufacturer = th_manufacturer.find_next('td').text

    th_panjang = table.find('th', text=re.compile('panjang', re.I))
    panjang = th_panjang.find_next('td').text
    panjang = convert_to_float(panjang)

    th_tinggi = table.find('th', text=re.compile('tinggi', re.I))
    tinggi = th_tinggi.find_next('td').text
    tinggi = convert_to_float(tinggi)
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
        "jenis_produk": jenis_produk,
        "harga": price,
        "ketersediaan": ketersediaan,
        "lebar": lebar,
        "berat": berat,
        "manufacturer": manufacturer,
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
