import lxml.html as web
from urllib.request import urlopen
from urllib.error import URLError
import datetime as dt
import json

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
            print(f"Attempt  {attempts}/{max_attempts}: Connection error. Retrying...")
        else:
            price_dolar = tree.xpath(".//div[@id='dolar']/div/div/div[@class='col-sm-6 col-xs-6 centrado']/strong/text()")
            price_dolar = price_dolar[0].replace(",", ".").strip()
            price_dolar = round(float(price_dolar), 2)
            return price_dolar
    else:
        print("\nCould not connect to the website after several attempts. Check your Internet connection.\n")
        return False

def importPriceDolar():
    path_dir = "datas_files/conf_date.json"
    actual_date = dt.date.today()
    save_date = {"Date": str(actual_date)}

    try:
        with open(path_dir, "r") as f:
            date_saved = json.load(f)

    except FileNotFoundError:
        print("The database where the dollar price is stored does not exist. \nBut now \
              the database has been created")
        date_saved = save_date

        with open(path_dir, "w") as f:
            json.dump(save_date, f, indent=4)

    except json.decoder.JSONDecodeError:
        print("The price of the dollar is not found in the database. It will be added to today's price.")
        date_saved = save_date

        with open(path_dir, "w") as f:
            json.dump(save_date, f, indent=4)

    if date_saved["Date"] != str(actual_date) or "Value Dolar" not in date_saved or date_saved["Value Dolar"] == False:
        print("Looking for dollar price....")
        value_dolar = getPriceDolar()

        if value_dolar:
            print("Completed\n")
            save_date["Value Dolar"] = value_dolar

            with open(path_dir, "w") as f:
                json.dump(save_date, f, indent=4)
            return value_dolar

    else:
        with open(path_dir, "r") as f:
            value_dolar = json.load(f)
        return value_dolar["Value Dolar"]