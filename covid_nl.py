import pandas as pd
from datetime import datetime, timedelta

# Datasets:
# Gemeente/provincies = https://www.cbs.nl/-/media/cbs/onze%20diensten/methoden/classificaties/overig/gemeenten%20alfabetisch%202019.xls
# Verspreiding per dag = https://www.volksgezondheidenzorg.info/onderwerp/infectieziekten/regionaal-internationaal/coronavirus-covid-19#node-coronavirus-covid-19-meldingen
# data beschikbaar vanaf:
dag = "03"
maand = "03"
jaar = "2020"
datafile = f"https://www.volksgezondheidenzorg.info/sites/default/files/map/detail_data/klik_corona{dag}{maand}{jaar}.csv"

first_day = datetime.strptime('03032020', "%d%m%Y").date()
today = datetime.now().date()

dates = [first_day + timedelta(days=x) for x in range(0, (today-first_day).days + 1)]

df = pd.DataFrame()

for i in dates:
    try:
        file = f"data/klik_corona{datetime.strftime(i,'%d%m%Y')}.csv"
        temp_df = pd.read_csv(file, delimiter=";")
        temp_df.set_index("Gemeente", inplace=True)
        temp_df[datetime.strftime(i,'%d-%m-%Y')] = temp_df["Aantal"]
        temp_df = temp_df[[datetime.strftime(i,'%d-%m-%Y')]]
        
        df = pd.concat([df, temp_df], sort=True, axis=1)
        
    except Exception as e:
        print(e)
        
        
df.dropna(how='all', inplace=True)
df.fillna(value=0, inplace=True)

provincie_df = pd.read_excel("data/Gemeenten alfabetisch 2019.xls")
provincie_df.set_index("Gemeentenaam", inplace = True)
provincie_df = provincie_df[["Provincienaam"]]
df = df.merge(provincie_df, left_index=True, right_index=True)
df.fillna(value="onbekend", inplace=True)

cols = df.columns.tolist()
cols = cols[-1:] + cols[:-1]
df = df[cols]


df.to_excel(f"gemeente tm {datetime.strftime(i,'%Y%m%d')}.xlsx")
df.to_csv(f"gemeente tm {datetime.strftime(i,'%Y%m%d')}.csv")
