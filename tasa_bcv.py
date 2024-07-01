import lxml.html as web
from urllib.request import urlopen
from urllib.error import URLError
import datetime as dt
import json

def priceDolar():
    url = "https://www.bcv.org.ve/"
    max_attempts = 3
    attempts = 0
    while attempts < max_attempts:
        try:
            tree = web.parse(urlopen(url)).getroot()
        except URLError:
            attempts += 1
            print("Intentando obtener precio del dolar")
            print(f"Intento {attempts}/{max_attempts}: Error de conexión. Reintentando...")
        else:
            price_dolar = tree.xpath(".//div[@id='dolar']/div/div/div[@class='col-sm-6 col-xs-6 centrado']/strong/text()")
            price_dolar = price_dolar[0].replace(",", ".").strip()
            price_dolar = round(float(price_dolar), 2)
            return price_dolar
    else:
        print("No se pudo conectar al sitio web después de varios intentos. Verifica tu conexión a Internet.")
        return None

def getPriceDolar():
    path_dir = "datas_files/conf_date.json"

    actual_date = dt.date.today()
    save_date = {"Date": str(actual_date)}

    try:
        with open(path_dir, "r") as f:
            date_saved = json.load(f)

    except FileNotFoundError:
        print("No existe la base de datos donde se almacena el precio del dolar. \nSe ha creado la base de datos")
        date_saved = save_date

        with open(path_dir, "w") as f:
            json.dump(save_date, f, indent=4)

    except json.decoder.JSONDecodeError:
        print("No se encuentra el precio del dolar en la base de datos. Se añadirá al del día de hoy.")
        date_saved = save_date
        with open(path_dir, "w") as f:
            json.dump(save_date, f, indent=4)

    if date_saved["Date"] != str(actual_date) or "Value Dolar" not in date_saved:
        print("Buscando precio del dolar...")
        value_dolar = priceDolar()
        print("Terminado\n")
        save_date["Value Dolar"] = value_dolar

        with open(path_dir, "w") as f:
            json.dump(save_date, f, indent=4)
        return value_dolar

    else:
        with open(path_dir, "r") as f:
            value_dolar = json.load(f)
        return value_dolar["Value Dolar"]