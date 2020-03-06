# COVID-19-NLDATA

Verwerking van de data zoals die in Nederland door het RIVM wordt aangeleverd.

### Datasets:


### Gemeente/provincies

https://www.cbs.nl/-/media/_excel/2020/03/gemeenten%20alfabetisch%202020.xlsx 

(met dank aan https://www.reddit.com/user/mrmaxedtank/)


### Verspreiding per dag :

https://www.volksgezondheidenzorg.info/onderwerp/infectieziekten/regionaal-internationaal/coronavirus-covid-19#node-coronavirus-covid-19-meldingen


### directe link tot de csv per dag:

https://www.volksgezondheidenzorg.info/sites/default/files/map/detail_data/klik_corona{dag}{maand}{jaar}_0.csv

Deze link werkt op moment van schrijven (5-3-2020) vanaf 3 maart. 

### Github van Johns Hopkins CSSE:

https://github.com/CSSEGISandData/COVID-19


## todo:
- standaard laatste versie "time_series_19-covid-Confirmed.csv" ophalen en slechts laatste column toevoegen ipv elke keer opnieuw hele df maken
- afhankelijk van de manier waarop RIVM gaat aanleveren df's maken voor mogelijke overlijdenen en mensen die genezen zijn
- df op gemeenteniveau maken
- automatisch ophalen nieuwe data RIVM
- uploaden naar google drive? 
