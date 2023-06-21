import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_option_menu import option_menu
import pandas as pd
import os
import sys
from PIL import Image

def import_table(data):
  '''imports excel data'''
  table = pd.read_csv(data)
  return table

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

    left_col_color = "#e2e0f5"
    left_col_color2 = "#d0cdef"
    right_col_color = "#f3f5e0"
    right_col_color2 = "#ecefcd"
    
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
#icon = 'Icon_Fachhochschule_Münster.png'<
data = os.path.join(sys.path[1], 'Tabelle_Karte.csv')

def main():
    st.set_page_config(page_title=app_title)
    
    # Bild darstellen
    image = Image.open(os.path.join(sys.path[1],'FH_Logo.png'))
    st.image(image)

    # Titel
    st.title(app_title)

    # Tabelle mit Wärmenetzen laden
    df = import_table(data)

    # with st.sidebar:
    #     select = option_menu(
    #         menu_title = None,
    #         options=['Karte','Tabelle','FH Seite "Wärmenetze 4.0"']
    #     )

    # Einleitungstext
    st.write('Im Rahmen der Förderung durch das Programm „Wärmenetze 4.0“ des Bundesamts für Wirtschaft und Ausfuhrkontrolle (BAFA) beantragten die Stadtwerke Warendorf in Kooperation mit der FH Münster, neben Planung und Bau außerdem, als einziges Projekt in Deutschland, die Förderung für das 4. Modul mit dem Forschungsziel des „Capacity Building“. Die Aufgabe der FH Münster liegt darin, die Technologie der kalten Nahwärmenetze weiter in den Fokus von Wärmeversorgern zu rücken und damit aktiv zur Reduzierung der in der Wärmeversorgung anfallenden CO2-Emissionen beizutragen.')

    # Kartenbeschreibung
    st.write('Folgende Karte gibt einen Überblick über bereits realisierte und geplante kalte Nahwärmenetze in Deutschland. Klicken Sie auf einen Marker um Informationen zu dem Netz zu erhalten. In der unten stehenden Tabelle sind für jedes Netz zusätzliche detailliertere Informationen aufgetragen.')

    # Email
    st.write('Falls Sie von einem kalten Nahwärmenetz wissen, welches in unserer Sammlung noch nicht vertreten ist, oder zusätzliche Informationen zu einem Nahwärmenetz haben, kontaktieren Sie uns gerne: lars.goray@fh-muenster.de')
    
    # Hinweis
    st.write('Hinweis: Die Koordinaten der abgebildeten Netze geben nicht den exakten Standort des Netzes an, sondern die Position der Stadt, in der sich das Netz befindet.')

    # Karte laden
    display_map(df)

    # Tabelle darstellen
    st.write(df)
if __name__ == '__main__':
    main()