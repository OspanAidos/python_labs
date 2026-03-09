import re
import json

with open("raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

price_pattern = r'\d[\d ]*,\d{2}'
prices = re.findall(price_pattern, text)

def price_to_float(p):
    return float(p.replace(" ", "").replace(",", "."))

prices_float = [price_to_float(p) for p in prices]

product_pattern = r'\d+\.\n(.+)'
products = re.findall(product_pattern, text)

total = sum(prices_float)

datetime_pattern = r'Время:\s*(\d{2}\.\d{2}\.\d{4})\s*(\d{2}:\d{2}:\d{2})'
datetime_match = re.search(datetime_pattern, text)

date = datetime_match.group(1) if datetime_match else None
time = datetime_match.group(2) if datetime_match else None

payment_pattern = r'(Банковская карта|Наличные)'
payment_match = re.search(payment_pattern, text)

payment_method = payment_match.group(1) if payment_match else None

result = {
    "products": products,
    "prices": prices_float,
    "calculated_total": total,
    "date": date,
    "time": time,
    "payment_method": payment_method
}

print(json.dumps(result, indent=4, ensure_ascii=False))