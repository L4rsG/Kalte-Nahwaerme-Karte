import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_option_menu import option_menu
import pandas as pd
from PIL import Image
from folium.plugins import MarkerCluster

app_title = 'Kalte Nahwärmenetze in Deutschland'            # Titel der App
icon = Image.open('FH_icon.png')  # Pfad zum FH Icon (FH Münster Logo als Icon im Browsertab)

st.set_page_config(
        page_title=app_title,
        page_icon = icon,
        layout="wide",
        initial_sidebar_state="expanded"
        )
#@st.cache_data
def import_table(data):
  '''imports excel data'''
  table = pd.read_csv(data)
  return table

#@st.cache_data
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

def find_multi_values(df):
     '''searches column for multiple entries and returns a list with the entries'''
     value_counts = df['Stadt'].value_counts()
     multiples = value_counts[value_counts>1].index.tolist()
     return multiples

#@st.cache_data
def add_marker(df,m):
    '''
    adds markers on the map m
    df: table/DataFrame
    m: map
    '''
    
    multiples = find_multi_values(df) # mehrfach vorkommende Städte
    clusters = {}
    for i in range (0,len(df)):
        
        # Koordinaten zuordnen
        lng = df['Longitude'][i]
        lat = df['Latitude'][i]

        # Popup-Tabelle
        html = popup_html(i,df)
        popup = folium.Popup(folium.Html(html, script=True), max_width=500)
        
        # Prüfen ob der Ort mehrmals vorkommt
        stadt = df['Stadt'][i]
        if stadt in multiples:
            # Überprüfen, ob der Cluster bereits existiert
            if stadt not in clusters:
                cluster_name = 'cluster_' + str(stadt)
                clusters[stadt] = MarkerCluster(name=cluster_name).add_to(m)
            cluster = clusters[stadt]
            # Marker erstellen und zum Cluster hinzufügen
            folium.Marker(location=[lat, lng], popup=popup).add_to(cluster)
        else:
            # Marker erstellen
            folium.Marker(location=[lat, lng], popup=popup).add_to(m)

#@st.cache_data
def display_map(df):

    map = folium.Map(location=[51.5,10.5], zoom_start=6)
    add_marker(df,map)
    st_map = st_folium(map, height=700, width=800)

def main():
    data = ('Tabelle_Karte.csv')       # Pfad zur Tabelle
    df = import_table(data)            # Tabelle mit Wärmenetzen laden
    # Titel und Logo
    Titel, Logo = st.columns([4, 1])
    with Titel:
            # Titel
            st.title(app_title)
    with Logo:
            # Logo darstellen
            image = Image.open('FH_Logo.png')
            st.image(image)

    # Mit Sidebarmenu in Kategorien unterteilen
    with st.sidebar:
        select = option_menu(
            menu_title = None,
            options=['Karte','Tabelle','FH-Seite "Wärmenetze 4.0"'],
            icons=['map','table','house']
        )

    if select == 'Karte':
        # Einleitungstext
        st.write('Im Rahmen der Förderung durch das Programm „Wärmenetze 4.0“ des Bundesamts für Wirtschaft und Ausfuhrkontrolle (BAFA) beantragten die Stadtwerke Warendorf in Kooperation mit der FH Münster, neben Planung und Bau außerdem, als einziges Projekt in Deutschland, die Förderung für das 4. Modul mit dem Forschungsziel des „Capacity Building“. Die Aufgabe der FH Münster liegt darin, die Technologie der kalten Nahwärmenetze weiter in den Fokus von Wärmeversorgern zu rücken und damit aktiv zur Reduzierung der in der Wärmeversorgung anfallenden CO2-Emissionen beizutragen.')
        st.subheader('Karte mit kalten Nahwärmenetzen in Deutschland')

        # Kartenbeschreibung
        st.write('Folgende Karte gibt einen Überblick über bereits realisierte und geplante kalte Nahwärmenetze in Deutschland. Klicken Sie auf einen Marker um Informationen zu dem Netz zu erhalten. Unter dem Reiter "Tabelle" sind für jedes Netz zusätzliche detailliertere Informationen angegeben.')
        
        '---'

        col1, col2 = st.columns([5,2])
        with col1:
            # Karte laden
            display_map(df)

        with col2:
            # Hinweis
            st.write('Hinweis: Die Koordinaten der abgebildeten Netze geben nicht den exakten Standort des Netzes an, sondern die Position der Stadt, in der sich das Netz befindet.')
            
            # Email Kontakt
            st.write('Falls Sie von einem kalten Nahwärmenetz wissen, welches in unserer Sammlung noch nicht vertreten ist, oder zusätzliche Informationen zu einem Nahwärmenetz haben, schreiben Sie uns gerne an: lars.goray@fh-muenster.de')

    if select == 'Tabelle':
        st.subheader('Tabelle mit kalten Nahwärmenetzen in Deutschland')
        st.write('In dieser Tabelle sind zusätzliche detailliertere Informationen zu den kalten Nahwärmenetzen enthalten. Mit dem Pfeil-Symbol in der oberen rechten Ecke der Tabelle lässt sich die Tabelle vergrößern.')

        '---'

        col1, col2 = st.columns([5,2])
        with col1:
            st.write(df)    # Tabelle darstellen

        with col2:
            # Hinweis
            st.write('Hinweis: Die Koordinaten der abgebildeten Netze geben nicht den exakten Standort des Netzes an, sondern die Position der Stadt, in der sich das Netz befindet.')
            
            # Email Kontakt
            st.write('Falls Sie von einem kalten Nahwärmenetz wissen, welches in unserer Sammlung noch nicht vertreten ist, oder zusätzliche Informationen zu einem Nahwärmenetz haben, schreiben Sie uns gerne an: lars.goray@fh-muenster.de')
    
    if select == 'FH-Seite "Wärmenetze 4.0"':
        # Link zur FH Seite
        st.write('Hier geht es zur Hauptseite "Wärmenetze 4.0 - In de Brinke" der FH Münster: https://de.fh-muenster.de/iep/waermenetze-4.0.php')

    #Förderung
    st.divider()
    bafa, text = st.columns([1,3])
    with bafa:
        image_bafa = Image.open('bafa.png')
        st.image(image_bafa)
    with text:
        st.write('Das Projekt "Wärmenetze 4.0 - In de Brinke" wird gefördert durch das Bundesamt für Wirtschaft und Ausfuhrkontrolle.')
if __name__ == '__main__':
    main()
