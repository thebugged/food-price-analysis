import json
import folium
import pandas as pd
import streamlit as st
from streamlit_folium import folium_static

st.set_page_config(
    layout='wide', 
    page_icon='🇳🇬', 
    page_title="Food Price Analysis")

# Load geojson data
geojson_file = "data/nigeria_geojson.geojson"
with open(geojson_file) as f:
    nigeria_geojson = json.load(f)

# Load price data
data_file = "data/avg_prices_2023.csv"
data = pd.read_csv(data_file)

# Create a dictionary for quick lookup
price_dict = data.set_index('state').to_dict(orient='index')

# Update GeoJson properties with price data
for feature in nigeria_geojson['features']:
    state_name = feature['properties']['state']
    if state_name in price_dict:
        feature['properties']['avgprice'] = price_dict[state_name]['avgprice']
        feature['properties']['avgusdprice'] = price_dict[state_name]['avgusdprice']
    else:
        feature['properties']['avgprice'] = None
        feature['properties']['avgusdprice'] = None

# Create folium map
m = folium.Map(
    location=[9.0820, 8.6753], 
    zoom_start=7, 
    scrollWheelZoom=False, 
    tiles='CartoDB positron', 
    name="Light Map")

# Add choropleth layer
choropleth = folium.Choropleth(
    geo_data=nigeria_geojson,
    name='choropleth',
    data=data,
    columns=['state', 'avgprice'],
    key_on='feature.properties.state',
    fill_color='YlGn',
    fill_opacity=0.8,
    line_opacity=0.2,
    legend_name='Average Price (NGN)',
    highlight=True,
    reset=True,
).add_to(m)

# Add GeoJson layer with updated properties
folium.GeoJson(
    nigeria_geojson,
    name="States",
    style_function=lambda x: {
        'fillColor': 'white', 
        'color': 'black',
        "weight": 2,
        # "dashArray": "4, 4"
        },

    highlight_function=lambda x: {
        'fillColor': 'white', 
        'fillOpacity': 0.7, 
        'weight': 0.5},
        
    tooltip=folium.GeoJsonTooltip(
        fields=['state', 'avgprice', 'avgusdprice'],
        aliases=['State','Average Price (NGN):', 'Average Price (USD):'],
        labels=True,
        sticky=True,
    ),
    popup=folium.GeoJsonPopup(
        fields=['state', 'avgprice', 'avgusdprice'],
        aliases=['State','Average Price (NGN):', 'Average Price (USD):'],
        labels=True,
        localize=True,
        
    )
).add_to(m)

folium.LayerControl().add_to(m)

st.markdown("## Food Price Analysis")
st.caption("Data Source: https://data.humdata.org/dataset/wfp-food-prices-for-nigeria")

st.divider()
st.markdown("Access the in-depth Notebook analysis [here](https://colab.research.google.com/drive/188_sV4N-kncjwFGqSMGCyqcrsr88IcQY?usp=sharing)")

# Display the map
folium_static(m, width=1400, height=900)

st.markdown("made by [thebugged](https://github.com/thebugged)")
