import pandas as pd
from datetime import datetime, timedelta

# Datasets:
# Gemeente/provincies = https://www.cbs.nl/-/media/_excel/2020/03/gemeenten%20alfabetisch%202020.xlsx
# Verspreiding per dag = https://www.volksgezondheidenzorg.info/onderwerp/infectieziekten/regionaal-internationaal/coronavirus-covid-19#node-coronavirus-covid-19-meldingen
# data beschikbaar vanaf:
dag = "03"
maand = "03"
jaar = "2020"
datafile = f"https://www.volksgezondheidenzorg.info/sites/default/files/map/detail_data/klik_corona{dag}{maand}{jaar}_0.csv"


def reddit_confirmed_table(df, sort):
    reddit_df = df
    cols = df.columns.tolist()
    temp_dict = {"": ":-"}
    for i in range(len(cols)):
        temp_dict[cols[i]] = ":-"
    reddit_df = pd.DataFrame([temp_dict])
    reddit_df.set_index("", inplace=True)
    reddit_df = pd.concat([reddit_df, df])

    cols = reddit_df.columns.tolist()
    cols = [f"**{col}**" for col in cols]
    reddit_df.set_axis(cols, axis=1, inplace=True)
    if sort == "gemeente":
        reddit_df["**Gemeentenaam**"] = reddit_df["**Gemeentenaam**"].apply(lambda x: f"**{x}**")
        reddit_df.iloc[[0]] = ":-"
        reddit_df.set_index("**Gemeentenaam**", inplace=True)
        reddit_df.drop("**Provincienaam**", axis=1, inplace=True)
        reddit_df.to_csv("reddit_table/reddit_time_series_19-covid-Confirmed_city.csv", sep="|")
        
    elif sort == "provincie":
        reddit_df = reddit_df.T
        cols = reddit_df.columns.tolist()
        cols = [f"**{col}**" for col in cols if col != ":-"]
        cols = [":-"] + cols
        reddit_df.set_axis(cols, axis=1, inplace=True)
        reddit_df = reddit_df.T
        reddit_df.index.name = "**Provincie**"
        index_cols = reddit_df.index.tolist()
        for index, row in reddit_df.iterrows():
            index_nr = index_cols.index(index)
            for c, x in enumerate(row):
                if isinstance(x, float):
                    reddit_df.iloc[index_nr,c] = int(x)
        reddit_df.to_csv("reddit_table/reddit_time_series_19-covid-Confirmed_provinice.csv", sep="|")


def province_confirmed_table(df):
    province_df = df.groupby("Provincienaam").sum()
    province_df.to_csv(f"rivm_covid_19_data/rivm_covid_19_time_series/time_series_19-covid-Confirmed_province.csv")
    province_df.to_excel(f"rivm_covid_19_data/rivm_covid_19_time_series/time_series_19-covid-Confirmed_province.xlsx")
    
    amount_of_days = 5
    reddit_confirmed_table(province_df[province_df.columns[-amount_of_days:]], "provincie")
    province_df.plot()
    print(province_df)


def update_data():
    first_day = datetime.strptime('27022020', "%d%m%Y").date()
    today = datetime.now().date()

    dates = [first_day + timedelta(days=x) for x in range(0, (today-first_day).days + 1)]

    df = pd.DataFrame()

    for i in dates:
        try:
            file = f"input_data/klik_corona{datetime.strftime(i,'%d%m%Y')}.csv"
            temp_df = pd.read_csv(file, delimiter=";", decimal=",")
            temp_df["Gemeentecode"] = temp_df["id"].apply(lambda x: str(int(x)))
            temp_df.set_index("id", inplace=True)
            temp_df[datetime.strftime(i,'%d-%m-%Y')] = temp_df["Aantal"]
            temp_df = temp_df[[datetime.strftime(i,'%d-%m-%Y')]]

            df = pd.concat([df, temp_df], sort=True, axis=1)

        except Exception as e:
            print(e)

    df.dropna(how='all', inplace=True)
    df.fillna(value=0, inplace=True)        

    provincie_df = pd.read_excel("input_data/Gemeenten alfabetisch 2020.xlsx")
    provincie_df.set_index("Gemeentecode", inplace = True)
    provincie_df = provincie_df[["Provincienaam", "Gemeentenaam"]]
    df = df.merge(provincie_df, left_index=True, right_index=True)

    cols = df.columns.tolist()
    cols = cols[-2:] + cols[:-2]
    df = df[cols]

    df.sort_values(['Gemeentenaam'], ascending=1, inplace = True)
    df.index.name = "gemeente_id"

    df.to_csv(f"rivm_covid_19_data/rivm_covid_19_time_series/time_series_19-covid-Confirmed_city.csv")
    df.to_excel(f"rivm_covid_19_data/rivm_covid_19_time_series/time_series_19-covid-Confirmed_city.xlsx")

    
    print(df)

    reddit_confirmed_table(df, "gemeente")
    province_confirmed_table(df)
    

if __name__ == "__main__":
    update_data()
