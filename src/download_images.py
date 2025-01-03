import os
import time
from random import randint, choice
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

from CONTS import BASE_FOLDER_IMG


def verify_exit(name="unnamed"):
    """
    Verify if exist the folder to save, otherwise return False
    """
    return True if os.path.exists(name) else False


def download_image(url: str, name="unnamed", count=0):
    """
    Download picture from url
    """
    ext_file = url.split(".")[-1]

    name_file = name
    if name.split(os.path.sep):
        name_file = name.split(os.path.sep)[-1]

    name_file = f"{name_file}_{count}.{ext_file}"

    print("download_img", name_file)

    folder_name = os.path.join(BASE_FOLDER_IMG, name)
    path_full_folder = os.path.abspath(folder_name)
    path_full_file = os.path.join(path_full_folder, name_file)

    if not os.path.exists(path_full_folder):
        os.makedirs(folder_name, exist_ok=True)
    if os.path.exists(path_full_file):
        return

    header = choice(get_headers())
    request = Request(url, headers=header)
    try:
        with open(path_full_file, "wb+") as picture:
            with urlopen(request) as response:
                picture.write(response.read())
                print(f"Image saved: {path_full_file}")
    except Exception as e:
        print(f"Fail to download: {request}")


def get_urls_image(html) -> list[str]:
    """
    Clear all string to retrieve the list of url for download picture
    """
    line = html.split("imagePathList")[1][2:].split(',"name":"ImageModule"')
    return line[0].replace("[", "").replace("]", "").replace('"', "").split(",")


def get_headers():
    """
    Get a list of headers
    https://www.useragents.me/
    """
    headers = [  # 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0',
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/105.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; SM-S906N Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 Build/OPD1.170811.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 7.1.1; G8231 Build/41.2.A.0.219; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1",
        "Mozilla/5.0 (iPhone12,1; U; CPU iPhone OS 13_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/15E148 Safari/602.1",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 YaBrowser/22.11.5.715 Yowser/2.5 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
    ]

    user_agents = []

    for header in headers:
        user_agents.append({"User-Agent": header})

    return user_agents


def sleeping():
    time_sleep = choice([1, 2, 3, 4, 5])
    print(f"sleeping {time_sleep}")
    time.sleep(time_sleep)


def get_image(url_site, name_folder="unnamed"):
    """
    Function main to export
    """

    name_folder = os.path.join(BASE_FOLDER_IMG, name_folder)
    path_folder_abs = os.path.abspath(name_folder)

    if verify_exit(name=path_folder_abs):
        print(f"Exist the folder with hash: {path_folder_abs}. Skipping")
        return
    else:
        os.makedirs(BASE_FOLDER_IMG, exist_ok=True)

    header = choice(get_headers())

    request = Request(url_site, headers=header)
    with urlopen(request) as response:
        if not response.status == 200:
            print(f"Fail to connect to: {url_site}")
            return
        html = response.read().decode("utf-8")
        html = BeautifulSoup(html, "html.parser")
        for script in html.find_all("script"):
            if 0 < str(script).find('"imagePathList":'):
                count = 1
                for url_imgs in get_urls_image(script.text):
                    download_image(url_imgs, name=path_folder_abs, count=count)
                    count += 1
                    sleeping()
                break
        sleeping()


def main():
    """
    For testing in development
    """

    urls = ["https://www.aliexpress.com/item/1005004265387289.html"]
    # ,
    # "https://www.aliexpress.com/item/1005004652465892.html",
    # "https://www.aliexpress.com/item/33001319493.html",
    # "https://www.aliexpress.com/item/1005003767035620.html", ]

    for url in urls:
        get_image(url, str(randint(0, 1000)))


if __name__ == "__main__":
    main()
