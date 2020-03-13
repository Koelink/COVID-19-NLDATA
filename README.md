# COVID-19-NLDATA

Processing of the data as supplied by RIVM (National Institute for Public Health and the Environment) in the Netherlands.

## Data is used for:
[Map of municipalities and province](https://studentdeployswebsite.z28.web.core.windows.net/) van Reddit-user [Crappy_bara](https://www.reddit.com/user/crappy_bara)

[Cool visualization](https://i.imgur.com/4PNpuOj.gif) from Reddit-user [FeelsLikeBatMan](https://www.reddit.com/user/FeelsLikeBatMan/)

## Datasets:


### Municipality/provinces

https://www.cbs.nl/-/media/_excel/2020/03/gemeenten%20alfabetisch%202020.xlsx 

(Thanks to Reddit-user [mrmaxedtan](https://www.reddit.com/user/mrmaxedtank/))


### RIVM Covid-19 Site:

https://www.rivm.nl/coronavirus-kaart-van-nederland#node-coronavirus-covid-19-meldingen


### Direct link to csv:
Update 12-03-2020:

The method old method is not working anymore (https://www.volksgezondheidenzorg.info/sites/default/files/map/detail_data/klik_corona{dag}{maand}{jaar}.csv). I use the div id="csvData" in the html from the [RIVM site](https://www.rivm.nl/coronavirus-kaart-van-nederland).  

### johns Hopkins CSSE Github:

https://github.com/CSSEGISandData/COVID-19


## todo:
- Use the last version of "time_series_19-covid-Confirmed.csv" instead of generation the file every time
- Lists for healed patients and deceased patients (depending on how RIVM supplies these data)
- Automatic upload to Github and Google Drive
- Infections per 100k inhabitants
- Growth in the last 24 hours
