
from pprint import pprint
from time import sleep
from geopy.geocoders import Nominatim
import json
from pathlib import Path

path = Path("geocoded_results.json")

if not path.exists():
    text = """Auf dem Hügel, 53121 Bonn
    Endenicher Allee, 53115 Bonn
    Im Blumengarten, 53127 Bonn
    Am Überesch, 48268 Greven
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

    split_lines = [line.strip() for line in text.splitlines()]
    #split_text = [line.split(',') for line in split_lines]


    geolocator = Nominatim(user_agent="TestGeocoder")

    found = []
    for address in split_lines:
        sleep(5)   
        try:
            location = geolocator.geocode(address)
            if location:
                pprint(location)
                found.append((address, location.raw))
                pprint(found)
        except Exception as e:
            pprint(f"Error geocoding {address}: {e}")
            found.append((address, None))


    with open(path, "w", encoding="utf-8") as json_file:
        json.dump(found, json_file, ensure_ascii=False, indent=4)
else:
    with open(path, "r", encoding="utf-8") as json_file:   
        found = json.load(json_file)  

#pprint(found)       

def to_german_number(number):
    """Convert a number to a German number format."""
    return str(number).replace(".", ",")

display = [f"{i[0]};  {to_german_number(i[1]["lat"])}; {to_german_number(i[1]["lon"])}" for i in found]

pprint(display)



   

