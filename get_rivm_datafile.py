import requests
from bs4 import BeautifulSoup
import pandas as pd
import io


site = "https://www.volksgezondheidenzorg.info/sites/default/files/map/detail_data/klik_corona08032020.csv"
site2 = "https://www.volksgezondheidenzorg.info/onderwerp/infectieziekten/regionaal-internationaal/coronavirus-covid-19#!node-coronavirus-covid-19-meldingen"

page = requests.get(site)
print(page)

#if page.status_code == 200:
#    pd.DataFrame(page.content)

#print(pd)


url="https://raw.githubusercontent.com/cs109/2014_data/master/countries.csv"
s=requests.get(site).content
c=pd.read_csv(io.StringIO(s.decode('utf-8')), delimiter=";")
print(c)