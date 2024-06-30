import lxml.html as web
from urllib.request import urlopen
from  urllib.error import URLError

def getPriceDolar():
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