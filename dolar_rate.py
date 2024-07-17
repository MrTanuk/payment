import lxml.html as web
from urllib.request import urlopen
from urllib.error import URLError
import datetime as dt
import json
import os
import conf_files

def loadCache(path_dir):
    if os.path.exists(path_dir):
        try:
            with open(path_dir, 'r') as archivo:
                return json.load(archivo)

        except FileNotFoundError:
            print("The database where the dollar value will be stored does not exist, check if it exists in the data_file folder.")
            return False

        except json.decoder.JSONDecodeError:
            option= input("There is no data in the database. Would you like to continue? y/n: ")

            if option.lower() == "y":
                conf_files.cleanScreen()
                return None

            elif option.lower() == "n":
                conf_files.cleanScreen()
                return False
    return None

def saveCache(path_dir, price_dolar, date_submitted):
    datos = {"Value Dolar": price_dolar, "Date": date_submitted}
    with open(path_dir, 'w') as archivo:
        json.dump(datos, archivo)

def getPriceDolar():
    url = "https://www.bcv.org.ve/"
    max_attempts = 3
    attempts = 0
    while attempts < max_attempts:
        try:
            tree = web.parse(urlopen(url)).getroot()
        except URLError:
            attempts += 1
            print("Trying to obtain dollar price...\n")
            print(f"Attempt {attempts}/{max_attempts}: Connection error. Retrying...")
        else:
            try:
                price_dolar = tree.xpath(".//div[@id='dolar']/div/div/div[@class='col-sm-6 col-xs-6 centrado']/strong/text()")
                price_dolar = price_dolar[0].replace(",", ".").strip()
                price_dolar = round(float(price_dolar), 2)

                date_submitted = tree.xpath("//*[@id='block-views-47bbee0af9473fcf0d6df64198f4df6b']/div/div[2]/div/div[8]/span/@content")
                date_submitted = "".join(date_submitted)
                return price_dolar, date_submitted
            
            except (IndexError, ValueError) as e:
                print(f"Error parsing data: {e}")
                return False, None
    else:
        print("\nCould not connect to the website after several attempts. Check your Internet connection.\n")
        return False, None

def importPriceDolar():
    path_dir_conf_date = conf_files.completedPath()
    path_dir_conf_date = path_dir_conf_date
    path_dir_conf_date += "datas_files/conf_date.json"

    datas_cache = loadCache(path_dir_conf_date)

    if datas_cache:
        date_cache = dt.datetime.strptime(datas_cache["Date"], "%Y-%m-%dT%H:%M:%S%z")
        price_dolar, date_submitted = getPriceDolar()
        if price_dolar and date_submitted:
            date_submitted_dt = dt.datetime.strptime(date_submitted, "%Y-%m-%dT%H:%M:%S%z")
            if date_submitted_dt <= date_cache:
                return datas_cache["Value Dolar"]
            else:
                print("Newer data available on the website")
                saveCache(path_dir_conf_date, price_dolar, date_submitted)
                return price_dolar
        else:
            print("Using cached data due to error in fetching new data")
            return datas_cache["Value Dolar"]

    elif datas_cache == None:
        print("Obtaining data from the website")
        price_dolar, date_submitted = getPriceDolar()
        if price_dolar and date_submitted:
            saveCache(path_dir_conf_date, price_dolar, date_submitted)
        return price_dolar

    if datas_cache == False:
        return False