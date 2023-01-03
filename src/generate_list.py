#! /usr/bin/env python3

import csv
import hashlib
import json
import os

from bs4 import BeautifulSoup

from download_images import get_image
from CONTS import BASE_FOLDER_ROOT

def clear_title(text: str):
    """
    Clear the text title from html
    """
    return text.replace("\n", " ").replace("  ", "").strip()


def get_list_from_file(path):
    items = []
    with open(path) as file_html:
        html = BeautifulSoup(file_html, "html.parser")
        content_main = html.find_all("div", "order-detail-item")[0]

        for div_item in content_main.find_all("div", class_="order-detail-item-content-wrap"):
            text = clear_title(div_item.find("div", class_="item-title").find("a").text)
            link = div_item.find("div", class_="item-title").find("a")["href"]
            amount, count = div_item.find("div", class_="item-price").text[4:].split("x")
            hash = hashlib.md5(text.encode()).hexdigest()

            items.append({"text": text, "link": link, "amount": float(amount), "count": int(count), "hash": hash})
    return items


def save_json(items, name_file):
    content = "["
    for item in items:
        o = json.dumps(item, ensure_ascii=False)
        content += str(o) + ","

    content = content[:-1]
    content += "]"

    with open(name_file, "+w", encoding="utf-8") as file_json:
        file_json.write(content)

    print(f"JSON saved in: {name_file}")


def save_csv(items, name_file):
    with open(name_file, "+w", encoding="utf-8") as file_csv:
        csv_writer = csv.DictWriter(file_csv, fieldnames=[key for key in items[0]])
        csv_writer.writeheader()
        csv_writer.writerows(items)
    print(f"CSV saved in: {name_file}")


def generate_list(files_path, csv_name, json_name="") -> list:
    content = []
    for file_html in files_path:
        content += get_list_from_file(file_html)

    if json_name:
        save_json(content, name_file=json_name)
    if csv_name:
        save_csv(content, name_file=csv_name)

    return content


def main():
    list_files = ["./assets/raw_list/pedido_0.html", "./assets/raw_list/pedido_1.html",
                  "./assets/raw_list/pedido_2.html",
                  "./assets/raw_list/pedido_3.html", "./assets/raw_list/pedido_4.html",
                  "./assets/raw_list/pedido_5.html"
                  ]

    # list_files = ["./assets/pedido_1.html"] # for debug

    os.makedirs(BASE_FOLDER_ROOT, exist_ok=True)

    db = generate_list(list_files, csv_name=f"{BASE_FOLDER_ROOT}/list.csv")

    # print(db)
    for item in db:
        get_image(url_site=item["link"], name_folder=item["hash"])

    # item = db[2]
    # get_image(url_site=item["link"], name_folder=item["hash"])


if __name__ == "__main__":
    main()
