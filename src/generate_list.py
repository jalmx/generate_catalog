#! /usr/bin/env python3

import csv
import hashlib
import json
import os
from datetime import datetime

from bs4 import BeautifulSoup

from download_images import get_image
from CONTS import BASE_FOLDER_ROOT


def clear_title(text: str):
    """
    Clear the text title from html
    """
    return text.replace("\n", " ").replace("  ", "").strip()


# def get_list_from_file(path):
#     items = []
#     with open(path) as file_html:
#         html = BeautifulSoup(file_html, "html.parser")
#         content_main = html.find_all("div", "order-detail-item")[0]

#         for div_item in content_main.find_all("div", class_="order-detail-item-content-wrap"):
#             text = clear_title(div_item.find("div", class_="item-title").find("a").text)
#             link = div_item.find("div", class_="item-title").find("a")["href"]
#             amount, count = div_item.find("div", class_="item-price").text[4:].split("x")
#             hash = hashlib.md5(text.encode()).hexdigest()

#             items.append({"text": text, "link": link, "amount": float(amount), "count": int(count), "hash": hash})
#     return items


def get_price(amount: str):
    value = 0.0
    if amount.find("MX") != -1:
        value = amount.replace("MX$", "")
    else:
        print("No is MX")
    return value


def generate_hash(text: str):
    return hashlib.md5(text.encode()).hexdigest()


def get_list_from_sublist_file(path):
    try:
        items = []
        with open(path) as file_html:
            html = BeautifulSoup(file_html, "html.parser")
            content_main = html.find_all("div", "order-detail-item")[0]

            for div_item in content_main.find_all(
                "div", class_="order-detail-item-content-wrap"
            ):
                try:
                    text = clear_title(
                        div_item.find("div", class_="item-title").find("a").text
                    )
                    link = div_item.find("div", class_="item-title").find("a")["href"]
                    price_raw, count = div_item.find(
                        "div", class_="item-price"
                    ).text.split("x")
                    items.append(
                        {
                            "text": text,
                            "link": link,
                            "amount": get_price(price_raw),
                            "count": int(count),
                            "hash": generate_hash(text),
                        }
                    )
                except Exception as e:
                    print("error:", e)
                    print(div_item)
                    print("=" * 50)

        return items

    except Exception as e:
        return None


def get_list_from_file(path):
    try:
        items = []
        with open(path) as file_html:
            html = BeautifulSoup(file_html, "html.parser")
            content_main = html.find_all("div", "comet-checkbox-group")[0]

            for div_item in content_main.find_all("div", class_="order-item"):
                try:
                    text = clear_title(
                        div_item.find("div", class_="order-item-content-info-name")
                        .find("a")
                        .text
                    )
                    link = div_item.find(
                        "div", class_="order-item-content-info-name"
                    ).find("a")["href"]
                    price_raw, count = div_item.find(
                        "div", class_="order-item-content-info-number"
                    ).text.split("x")

                    items.append(
                        {
                            "text": text,
                            "link": link,
                            "amount": get_price(price_raw),
                            "count": int(count),
                            "hash": generate_hash(text),
                        }
                    )
                except Exception as e:
                    print("error:", e)
                    print(div_item)
                    print("=" * 50)
            return items
    except Exception as e:
        return None


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
        items = (
            get_list_from_file(file_html) or get_list_from_sublist_file(file_html) or []
        )

        content += items

    if len(content):
        if json_name:
            save_json(content, name_file=json_name)
        elif csv_name:
            save_csv(content, name_file=csv_name)
    else:
        print("No saved file content")

    return content


def main():
    # list_files = ["./assets/raw_list/pedido_0.html", "./assets/raw_list/pedido_1.html",
    #               "./assets/raw_list/pedido_2.html",
    #               "./assets/raw_list/pedido_3.html", "./assets/raw_list/pedido_4.html",
    #               "./assets/raw_list/pedido_5.html"
    #               ]

    list_files = ["src/assets/raw_list/pedido_lcd.html"]  # for debug

    os.makedirs(BASE_FOLDER_ROOT, exist_ok=True)

    db = generate_list(list_files, csv_name=f"{BASE_FOLDER_ROOT}/list{datetime.now()}.csv")

    # download imagen
    for item in db:
        get_image(url_site=item["link"], name_folder=item["hash"])

    # item = db[2]
    # get_image(url_site=item["link"], name_folder=item["hash"])


if __name__ == "__main__":
    main()
