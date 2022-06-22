import re


def extract_price(value):
    results = re.findall('[0-9]+', value)
    return "".join(results)


def convert_to_float(value):
    new_value = value.replace('.','').replace(',','.')
    return float(new_value)
