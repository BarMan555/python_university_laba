from bs4 import BeautifulSoup
import requests
import logging
import os

COUNT = 10
PAGES = 3
CORNER_FOLDER = "Lab1"
MAIN_FOLDER = "dataset"
ROSES_FOLDER = "roses"
TULIPS_FOLDER = "tulips"
_headers = {
   "User-Agent":"Mozilla/5.0"
}
url_rose="https://www.bing.com/images/search?q=rose.jpg&redig=7D4B2E55AA5E4A4CA223FB76FBC6D258&first=1"
url_tulip="https://www.bing.com/images/search?q=tulip.jpg&qs=UT&form=QBIR&sp=1&lq=0&pq=tulip.jpg&sc=2-9&cvid=9577F520591A403C88168B8637C22677&first=1"

logging.basicConfig(level=logging.INFO, filename=os.path.join(CORNER_FOLDER, "py_log.log"), filemode="w")

def create_folder(folder: str)->str:

    try:
        if not os.path.exists(folder):
            os.makedirs(folder)
    except Exception as err: 
        logging.error(f"{err}", exc_info=True)


def download(list_images : list, folder : str):

    count = 0
    exec_count = 0
    for flower_url in list_images:
        if count > COUNT: break
        try:
            src=flower_url['src']
            response = requests.get(src)
            create_folder(folder)
            with open(os.path.join(folder, f"{count:04}.jpg").replace("\\", "/"), "wb") as file:
                file.write(response.content)
                count+=1
        except Exception as err:
            exec_count+=1
            logging.warning(f"Error flower_url{count+exec_count+1}. {err}")
    logging.info(f"Successful download - {count}")
    logging.info(f"Unsuccessful download - {exec_count}")

    

def make_list(url : str) -> list:

    list_img = []
    new_url = url[:-1]
    try:
        for page in range(1, PAGES):
            url = f"{new_url}{page}"
            html = requests.get(url, headers=_headers) 
            soup = BeautifulSoup(html.text, "lxml")
            list_img += soup.find_all("img", class_="mimg")
        return list_img
    except Exception as err:
        logging.error(f"{err}", exc_info=True)


if __name__ == "__main__":
    roses = make_list(url_rose)
    download(roses, os.path.join(CORNER_FOLDER, MAIN_FOLDER, ROSES_FOLDER).replace("\\", "/"))

    tulips = make_list(url_tulip)
    download(tulips, os.path.join(CORNER_FOLDER, MAIN_FOLDER, TULIPS_FOLDER).replace("\\", "/"))

