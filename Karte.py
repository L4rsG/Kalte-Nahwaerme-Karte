import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import branca
import os
import sys
# import geopandas as gpd
# from geopy.geocoders import Nominatim

def import_table(data):
  '''imports excel data'''
  table = pd.read_csv(data)
  return table

# def add_location(df):
#   '''adds longitude and latitude to df'''
#   longitude = []
#   latitude = []
#   geolocator = Nominatim(user_agent="app_name")
#   for city in df['Stadt']:
#     location = geolocator.geocode(city)
#     longitude.append(location.longitude)
#     latitude.append(location.latitude)
#   df['Longitude'] = longitude
#   df['Latitude'] = latitude
#   return df

def popup_html(row,df):
    i = row
    city=df['Stadt'].iloc[i]
    project_name=df['Projektname'].iloc[i]  
    operator=df['Betreiber'].iloc[i]
    year=df['Fertigstellung'].iloc[i]
    we=df['Anzahl der Wohneinheiten'].iloc[i]
    g=df['Anzahl der Gebäude'].iloc[i]
    link=df['Internet-Link'].iloc[i]

    # Wohneinheiteun und Gebäude wurden als float dargestellt deshalb:
    try:
        we=int(we)
    except:()

    try:
        g=int(g)
    except:()

    left_col_color = "#9da4dd"
    left_col_color2 = "#c2c9ff"
    right_col_color = "#ddd69d"
    right_col_color2 = "#fff8c2"
    
    html = """<!DOCTYPE html>
<html>
<head>
<h4 style="margin-bottom:10"; width="200px">{}</h4>""".format(city) + """
</head>
    <table style="height: 150px; width: 500px;">
<tbody>
<tr>
<td style="width: 100px;background-color: """+ left_col_color +""";"><span style="color: #000000;">Projektname</span></td>
<td style="background-color: """+ right_col_color +""";">{}</td>""".format(project_name) + """
</tr>
<tr>
<td style="width: 100px;background-color: """+ left_col_color2 +""";"><span style="color: #000000;">Betreiber</span></td>
<td style="background-color: """+ right_col_color2 +""";">{}</td>""".format(operator) + """
</tr>
<tr>
<td style="width: 100px;background-color: """+ left_col_color +""";"><span style="color: #000000;">Fertigstellung</span></td>
<td style="background-color: """+ right_col_color +""";">{}</td>""".format(year) + """
</tr>
<tr>
<td style="width: 100px;background-color: """+ left_col_color2 +""";"><span style="color: #000000;">Wohneinheiten</span></td>
<td style="background-color: """+ right_col_color2 +""";">{}</td>""".format(we) + """
</tr>
<tr>
<td style="width: 100px;background-color: """+ left_col_color +""";"><span style="color: #000000;">Gebäude</span></td>
<td style="background-color: """+ right_col_color +""";">{}</td>""".format(g) + """
</tr>
<tr>
<td style="width: 100px;background-color: """+ left_col_color2 +""";"><span style="color: #000000;">Quelle</span></td>
<td style="background-color: """+ right_col_color2 +""";">{}</td>""".format(link) + """
</tr>
</tbody>
</table>
</html>
"""

    return html
def add_marker(df,m):
    '''
    adds markers on the map m
    df: table/DataFrame
    m: map
    '''
    for i in range (0,len(df)):
        # Koordinaten zuordnen
        lng = df['Longitude'][i]
        lat = df['Latitude'][i]

        # Popup-Tabelle
        html = popup_html(i,df)
        iframe = branca.element.IFrame(html=html,width=510,height=280)
        popup = folium.Popup(folium.Html(html, script=True), max_width=500)
        
        #Marker erstellen
        folium.Marker(
        location=[lat, lng],
        popup=popup,
        ).add_to(m)

def display_map(df):

    map = folium.Map(location=[51.5,10.5], zoom_start=6)
    
    add_marker(df,map)

    st_map = st_folium(map, height=700, width=700)

app_title = 'Kalte Nahwärmenetze in Deutschland'
#icon = 'Icon_Fachhochschule_Münster.png'
#image = 'Logo_of_Fachhochschule_Münster.png'
data = os.path.join(sys.path[1], 'Tabelle_Karte.csv')

def main():
    st.set_page_config(page_title=app_title)
    #st.image(image)
    st.title(app_title)

    # Tabelle mit Wärmenetzen laden
    df = import_table(data)

    # Karte laden
    display_map(df)
    
    # Tabelle darstellen
    st.write(df)
if __name__ == '__main__':
    main()