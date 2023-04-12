import csv
import requests
from bs4 import BeautifulSoup


def get_html(url):
    headers = {"User-Agent":"Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}
    response = requests.get(url, headers=headers)
    return response.text

def get_total_pages(html):
    soup = BeautifulSoup(html, "lxml")
    
    pages_url = soup.find("div", class_ ="pager-wrap").find("ul")
    last_page = pages_url.find_all("li")[-1]
    total_pages = last_page.find("a").get("href").split("=")[-1]
    return int(total_pages)

def write_to_csv(data):
    with open("kivano_smartphones.csv", "a") as csv_file:
        writer = csv.writer(csv_file, delimiter="/")
        writer.writerow((data["title"],
                         data["price"],
                         data["photo"]))

def get_page_data(html):
    soup = BeautifulSoup(html, "lxml")
    product_list = soup.find("div", class_ ="list-view")
    products = product_list.find_all("div", class_ = "item product_listbox oh")


    for product in products:
        try:
            photo = product.find("div", class_ = "listbox_img pull-left").find("a").find("img").get("src")
        except:
            photo = "Error"
        try:
            title = product.find("div", class_ = "listbox_title oh").find("a").text
        except: 
            title = ""
        try:
            price = product.find("div", class_ = "listbox_price text-center").find("strong").text
        except:
            price = "Нет в наличии"

        data = {"title": title, "price": price, "photo": photo}
        write_to_csv(data)

def main():
    smartphones_url = "https://www.kivano.kg/mobilnye-telefony"
    pages = "?page="

    total_pages = get_total_pages(get_html(smartphones_url))
    for page in range(1, total_pages):
        url_with_page = smartphones_url + pages + str(page)
        html = get_html(url_with_page)
        get_page_data(html)


main()
