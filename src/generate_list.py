# Leer la lista de archivos html
# generar todas las lista de los articulos en un JSON Array
# generar con esta db un archivo csv
# generar un markdown para una tabla

from bs4 import BeautifulSoup


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
            items.append({"text": text, "link": link})

    return items

def save_json(items):
    

def main():
    list_files = ["./assets/pedido_1.html", "./assets/pedido_2.html", "./assets/pedido_3.html", "./assets/pedido_4.html", "./assets/pedido_5.html"]
    content = []
    for file_html in list_files:
        content += get_list_from_file(file_html)

    save_json(content)



if __name__ == "__main__":
    main()
