import csv
import os
from os import path
import datetime

from jinja2 import Environment, FileSystemLoader

from CONTS import BASE_FOLDER_TEMPLATE, BASE_FOLDER_IMG, NAME_TEMPLATE_HTML, BASE_FOLDER_ROOT, NAME_HTML_SAVE


def generate_pdf():
    os.system(f" wkhtmltopdf {os.path.join(BASE_FOLDER_ROOT, NAME_HTML_SAVE)} --enable-local-file-access "
              f"{os.path.join(BASE_FOLDER_ROOT, 'catalogo.pdf')}    ")


def save_html(path_html, content):
    with open(f"{path_html}", "w+") as file_html:
        file_html.write(content)
        print(f"Saved at: ", path_html)


def read_db():
    path_db = os.path.join(BASE_FOLDER_ROOT, "list.csv")
    with open(path_db, "r", encoding="utf-8") as db:
        file_csv = csv.DictReader(db)
        return list(file_csv)


def read_imagens(path_folder) -> list:
    return os.listdir(path_folder) if path.exists(path_folder) else []


def generate_template_html(items):
    env = Environment(loader=FileSystemLoader(BASE_FOLDER_TEMPLATE))
    template = env.get_or_select_template(NAME_TEMPLATE_HTML)

    path_imgs = path.abspath(BASE_FOLDER_IMG)

    data = {}
    details = []

    for item in items:
        imgs = []

        for link in read_imagens(path.join(path_imgs, item['hash'])):
            src = f"{path.join('img', item['hash'], link)}"
            imgs.append((item['hash'], src))

        details.append({
            "description": item['text'],
            "count": int(item['count']) if item['count'] else 0,
            "price": item['amount'],
            "imgs": imgs,
            "hash": item['hash']
        })

        data = {"header_description": "Descripción del producto",
                "header_count": "Cantidad",
                "header_price": "Precio",
                "data": details,
                "date": datetime.datetime.now()
                }

    html = template.render(data)
    save_html(os.path.join(BASE_FOLDER_ROOT, NAME_HTML_SAVE), html)


def main():
    path_template = "/home/xizuth/Projects/generate_catalog/src/catalogo/"
    env = Environment(loader=FileSystemLoader(path_template))
    template = env.get_or_select_template("template.jinja-html")

    text = "MiniTaladro Inalámbrico USB, pluma de pulido de grabado inalámbrico,taladro eléctrico para joyería, herramientas Dremel de Metal, tallado deperforación de polvo"
    links = [
        "file:///home/xizuth/Projects/generate_catalog/src/catalogo/img/1cc7277ac38665553f1f4b428c25a4b6/a1cc7277ac38665553f1f4b428c25a4b6_1.jpg",
        "file:///home/xizuth/Projects/generate_catalog/src/catalogo/img/1cc7277ac38665553f1f4b428c25a4b6/a1cc7277ac38665553f1f4b428c25a4b6_2.jpg",
        "file:///home/xizuth/Projects/generate_catalog/src/catalogo/img/1cc7277ac38665553f1f4b428c25a4b6/a1cc7277ac38665553f1f4b428c25a4b6_3.jpg"]
    imgs = []
    amount = 23.82
    count = 10
    hash_code = "9201272a5ed11cb4d7c91ecdf13d1688"

    for link in links:
        imgs.append((hash_code, link))

    data = {
        "header_description": "Descripcion del producto",
        "header_count": "Cantidad",
        "header_price": "Precio",
        "data": [{
            "description": text,
            "count": count,
            "price": amount,
            "imgs": imgs
        },
            {
                "description": text,
                "count": 2,
                "price": 2.2,
                "imgs": imgs
            },
        ]

    }

    html = template.render(data)

    # print(html)

    # config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
    # name_pdf = "./catalogo.pdf"
    #
    # pdfkit.from_file("catalogo.html",name_pdf, configuration=config, options={"--enable-local-file-access": ""})


if __name__ == "__main__":
    # main()
    i = read_db()
    generate_template_html(i)
    generate_pdf()
