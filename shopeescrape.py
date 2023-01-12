import json
import pandas as pd
import requests

headers = {"user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}

def get_url():
    urls=[]
    for i in range(0, 50):
        url = "https://shopee.co.id/api/v4/recommend/recommend?bundle=shop_page_category_tab_main&item_card=2&limit=30&offset={}&section=shop_page_category_tab_main_sec&shopid=14318452&sort_type=1&tab_name=popular".format(i*30)
        urls.append(url)
    return urls

def scrape(url):
    req = requests.get(url, headers=headers).json()
    data = []
    for i in range(len(req["data"]["sections"][0]["data"]["item"])):
        name        = req["data"]["sections"][0]["data"]["item"][i]["name"]
        brand       = req["data"]["sections"][0]["data"]["item"][i]["brand"]
        discount    = req["data"]["sections"][0]["data"]["item"][i]["discount"]
        price       = int(req["data"]["sections"][0]["data"]["item"][i]["price"])/100000
        pricebef    = int(req["data"]["sections"][0]["data"]["item"][i]["price_before_discount"])/100000
        price_min   = int(req["data"]["sections"][0]["data"]["item"][i]["price_min"])/100000
        pricebef_min= int(req["data"]["sections"][0]["data"]["item"][i]["price_min_before_discount"])/100000
        price_max   = int(req["data"]["sections"][0]["data"]["item"][i]["price_max"])/100000
        pricebef_max= int(req["data"]["sections"][0]["data"]["item"][i]["price_max_before_discount"])/100000
        gr_ongkir   = req["data"]["sections"][0]["data"]["item"][i]["show_free_shipping"]
        toko        = req["data"]["sections"][0]["data"]["item"][i]["shop_name"]
        lokasi      = req["data"]["sections"][0]["data"]["item"][i]["shop_location"]
        itemid      = req["data"]["sections"][0]["data"]["item"][i]["itemid"]
        shopid      = req["data"]["sections"][0]["data"]["item"][i]["shopid"]
        hyperlink   = '=HYPERLINK("'+"https://shopee.co.id/api/v4/item/get?itemid={}&shopid={}".format(itemid, shopid)+'", "'+name+'")'
        sold        = req["data"]["sections"][0]["data"]["item"][i]["sold"]
        stock       = req["data"]["sections"][0]["data"]["item"][i]["stock"]
        star        = req["data"]["sections"][0]["data"]["item"][i]["item_rating"]["rating_star"]
        rating_1    = req["data"]["sections"][0]["data"]["item"][i]["item_rating"]["rating_count"][1]
        rating_2    = req["data"]["sections"][0]["data"]["item"][i]["item_rating"]["rating_count"][2]
        rating_3    = req["data"]["sections"][0]["data"]["item"][i]["item_rating"]["rating_count"][3]
        rating_4    = req["data"]["sections"][0]["data"]["item"][i]["item_rating"]["rating_count"][4]
        rating_5    = req["data"]["sections"][0]["data"]["item"][i]["item_rating"]["rating_count"][5]

        data.append(
            (name, brand, discount, price, pricebef, price_min, pricebef_min, price_max, pricebef_max, gr_ongkir, toko, lokasi, itemid, shopid, hyperlink, sold, stock, star, rating_1, rating_2, rating_3, rating_4, rating_5)
        )
    return data

def data_frame(data):
    df = pd.DataFrame(data, columns=["Nama Barang", "Merk", "Diskon", "Harga", "Harga Sebelum Diskon", "Harga Min", "Harga Min Sebelum Diskon", "Harga Max", "Harga Max Sebelum Diskon", "Gratis Ongkir", "Toko", "Lokasi", "Item ID", "Toko ID", "Link", "Terjual", "Stock", "Rating", "Bintang 1", "Bintang 2", "Bintang 3", "Bintang 4", "Bintang 5"])
    return df

if __name__ == "__main__":
    urls = get_url()

    dt=[]
    for i in range(0, len(urls)):
        url = urls[i]
        scrapes = scrape(url)
        dt.extend(scrapes)

    dtfr = data_frame(dt)

dtfr.to_excel("unilever.xlsx", index=False)
print("selesai")
