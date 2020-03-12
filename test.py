import requests
from bs4 import BeautifulSoup
import pandas as pd

today ="12032020"
site = " https://www.rivm.nl/coronavirus-kaart-van-nederland" 
page = requests.get(site)

soup = BeautifulSoup(page.content, 'html.parser')
data = soup.find_all(id="csvData")[0].get_text()
#print(data)

df_list = []
date = data.split("peildatum ")[1][:14]
data  = data.split("\n")
for line in range(len(data)):
    line_list = data[line].split(";")
    if line == 1:
        headers = line_list
    if len(line_list) > 1 and line > 1:
            df_list.append(line_list)

print(df_list)
print(headers)
#date = df_list[]
df = pd.DataFrame(df_list, columns = headers)
df["id"] = df["Gemnr"].astype(int)
df = df[df["id"] >= 0]
#df.set_index("id", inplace = True)
df["Aantal"].fillna(0, inplace=True)
df["Aantal"] = df["Aantal"].astype(int)
print(df)
print(date)
df.to_csv(f"input_data/klik_corona{today}.csv", index=False, sep=";")