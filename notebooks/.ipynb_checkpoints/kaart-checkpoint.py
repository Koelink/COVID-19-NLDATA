import geopandas as gpd
import pandas as pd
import numpy as np
import folium, branca
import requests, json
import branca.colormap as cm

from datetime import datetime, timedelta
from folium import FeatureGroup
from folium.features import GeoJson, GeoJsonTooltip

datum = datetime.now().strftime('%d-%m-%Y')

def createGemeenteGDF():
    dfGemeente = pd.read_csv("../rivm_covid_19_data/rivm_covid_19_time_series/time_series_19-covid-Confirmed_city.csv",
                             usecols=['gemeente_id', 'Gemeentenaam', datum])
    
    geojson = '../geo_data/gemeentes.geojson'
    gdf = gpd.read_file(geojson)
    gdf['code'] = gdf['code'].astype(int)
    gdfMerged  = gdf.merge(dfGemeente, how='left', left_on='code', right_on='gemeente_id')
    
    return(gdfMerged)

def createMap():
    m = folium.Map(
        location=[52, 5],
        zoom_start=7,
        tiles='cartodbpositron',
        min_zoom=7,
        max_zoom=10,)
    
    return m

def createColormap():
    df    = createGemeenteGDF()
    colormap = cm.linear.OrRd_09.scale(
            df[datum].min(),
            df[datum].max(),)
    
    colormap.caption = ('Aantal besmettingen op: ' + datum)
    
    return colormap

def createTooltip():
    tooltip = GeoJsonTooltip(
                    fields=["gemeentenaam", datum],
                    aliases=["Gemeente:", "Besmettingen:"],
                    localize=True,
                    sticky=False,
                    labels=True,
                    style="""
                        background-color: #F0EFEF;
                        border: 2px solid black;
                        border-radius: 1px;
                        box-shadow: 3px;
                    """,
                )
    return tooltip

def addGeoJson():
    colormap = createColormap()
    tooltip  = createTooltip()
    gdf       = createGemeenteGDF()
    
    g = folium.GeoJson(
                gdf,
                name="Gemeentes",
                style_function=lambda x: {
                    "fillColor": colormap(x["properties"][datum])
                    if x["properties"][datum] is not None
                    else "#E7E4E3",
                    "color": "black",
                    "weight": 1,
                    "fillOpacity": 0.75,
                },
                tooltip=tooltip
            )
    
    return g

def addGeoJsonProv():
    colormap = createColormap()
    tooltip  = createTooltip()
    gdf       = createGemeenteGDF()
    
    g = folium.GeoJson(
                gdf,
                name="Gemeentes",
                style_function=lambda x: {
                    "fillColor": colormap(x["properties"][datum])
                    if x["properties"][datum] is not None
                    else "#E7E4E3",
                    "color": "black",
                    "weight": 1,
                    "fillOpacity": 0.75,
                },
                tooltip=tooltip
            )
    
    return g

def createLegend():
    legend = folium.LayerControl(collapsed=False)
    
    return legend

def makeMap():
    m = createMap()
    colormap     = createColormap()
    geoJson      = addGeoJson()
    legend       = createLegend()
    
    feature_group = FeatureGroup(name='Gemeentes')
    
    geoJson.add_to(feature_group)
    feature_group.add_to(m)
    m.add_child(colormap)
    m.add_child(legend)

    return m

m = makeMap()
m.save("kaart_" + datum + ".html") 