
from pprint import pprint
from time import sleep
from geopy.geocoders import Nominatim

text = """Auf dem Hügel, 53121 Bonn
Endenicher Allee, 53115 Bonn
Im Blumengarten, 53127 Bonn
48268 Greven, Am Überesch
Hinter der Ley, 57258 Freudenberg 
Im Mettelsiefen, 53639 Königswinter
Max Plank Straße 53, 33659 Bielefeld
Michael-Levailly-Straße 1, 53127 Bonn
Klemens-August-Straße 8, 53115 Bonn
Graf-Gallen-Straße 11, 53129 Bonn
Straße des 8.Mai 1, 15890 Eisenhüttenstadt
Gesch.-Scholl-Str. 11, 03222 Lübbenau
Rudolfstraße 8, 56838 Iserlohn
Karl-Lade-Staße 41, 10369 Berlin
"""

split_lines = text.splitlines()
#split_text = [line.split(',') for line in split_lines]


geolocator = Nominatim(user_agent="TestGeocoder")

found = []
for address in split_lines:
    sleep(5)   
    try:
        location = geolocator.geocode(address)
        if location:
            found.append((address,(location.latitude, location.longitude)))
        
      
    except Exception as e:
       pprint(e)
pprint(found)