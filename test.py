import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

site = " https://www.rivm.nl/coronavirus-kaart-van-nederland" 
page = requests.get(site)

soup = BeautifulSoup(page.content, 'html.parser')
data = soup.find_all(id="csvData")[0].get_text()



ned_maanden = ['januari', 'februari', 'maart', 'april', 'mei', 'juni', 'juli', 'augustus', 'september', 'november', 'december']
date = data.split("peildatum ")[1][:14].split(" ")
month = ned_maanden.index(date[1])  + 1
if month < 10 :
    month = "0" + str(month)
today = date[0] + month + str(datetime.now().year)


data  = data.split("\n")
df_list = []
for line in range(len(data)):
    line_list = data[line].split(";")
    if line == 1:
        headers = line_list
    if len(line_list) > 1 and line > 1:
            df_list.append(line_list[:3])

print(df_list)
print(headers)
df = pd.DataFrame(df_list, columns = headers)
df["id"] = df["Gemnr"].astype(int)
df = df[df["id"] >= 0]
#df.set_index("id", inplace = True)
df["Aantal"].fillna(0, inplace=True)
df["Aantal"] = df["Aantal"].astype(int)
print(df)
print(date)
print(today)
df.to_csv(f"input_data/klik_corona{today}.csv", index=False, sep=";")
print(ned_maanden.index(date[1]))