import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json
import time
import random

ua = UserAgent()
headers = {'User-Agent': ua.random}

def get_page(sex, size):
    if sex == "чоловічі кросівки":
        sex_transliteration = "choloviki"
    elif sex == "жіночі кросівки":
        sex_transliteration = "zhinki"
    url = f'https://www.adidas.ua/{sex_transliteration}/vzuttya/{str(size)}?page=1'
    print(url)
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')

    snickers_array = []
    pages_count = soup.find("p", class_="common-text pagination__select--total").text

    for page in range(1, int(pages_count) + 1):
        url = f'https://www.adidas.ua/{sex_transliteration}/vzuttya/{str(size)}?page={page}'
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'lxml')
        data = soup.find_all("div", class_="product__content")
        print(page, '/', pages_count)

        for index, snickers in enumerate(data):

            if snickers.find("div", class_="product__woblers--item"):
                snickers_array.append({
                    "product name": snickers.find("div", class_="product__title").text,
                    "category":  snickers.find("div", class_="product__category").text,
                    "price first":  snickers.find("div", class_="price__first").text,
                    "sale price": snickers.find("div", class_="price__sale").text if snickers.find("div", class_="price__sale") else "",
                    "sale %": snickers.find("div", class_="product__woblers--item").text if snickers.find("div", class_="product__woblers--item") else "",
                    'colors': snickers.find(class_="product__colors-count").text if snickers.find(class_="product__colors-count") else "",
                    "link": "https://www.adidas.ua"+ snickers.find("a", class_ = "product__info").get("href")
                })
            else:
                continue

        filename = 'adidas_snickers.json'
        with open(filename, "w") as file:
            json.dump(snickers_array, file, indent=2)
        # time.sleep(random.uniform(2, 5))
def main():
    get_page("women", 5)

if __name__ == '__main__':
    main()
