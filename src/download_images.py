from random import randint
from urllib.request import Request, urlopen, urlretrieve

from bs4 import BeautifulSoup


def download_image(url: str, name="unnamed", count=0):
    # todo: tomar el nombre del producto y colocarlo aqui
    name_file = f"{name}_{count}.{url.split('.')[-1]}"
    urlretrieve(url, name_file)
    print(f"Image saved: {name_file}")


def get_urls_image(html) -> list[str]:
    """
    Clear all string to retrieve the list of url for download picture
    """
    line = html.split("imagePathList")[1][2:].split(',"name":"ImageModule"')
    return line[0].replace("[", "").replace("]", "").replace('"', "").split(",")


def get_image(url_site):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
    }

    request = Request(url_site, headers=headers)
    with urlopen(request) as response:
        html = response.read().decode("utf-8")
        html = BeautifulSoup(html, "html.parser")
        for script in html.find_all("script"):
            if 0 < str(script).find('"imagePathList":'):
                count = 1
                for url_imgs in get_urls_image(script.text):
                    download_image(url_imgs)
                break


def main():
    """
    For testing in development
    """
    urls = ["https://www.aliexpress.com/item/1005004265387289.html",
            "https://www.aliexpress.com/item/1005004652465892.html", "https://www.aliexpress.com/item/33001319493.html","https://www.aliexpress.com/item/1005003767035620.html",]

    for url in urls:
        get_image(url)


if __name__ == "__main__":
    main()
