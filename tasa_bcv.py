import lxml.html as web
from urllib.request import urlopen

url = "https://www.bcv.org.ve/"

tree = web.parse(urlopen(url)).getroot()

price_dolar = tree.xpath(".//div[@id='dolar']/div/div/div[@class='col-sm-6 col-xs-6 centrado']/strong/text()")
price_dolar = price_dolar[0].replace(",", ".").strip()
price_dolar = round(float(price_dolar), 2)