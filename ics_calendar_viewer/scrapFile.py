import requests
from ics import Calendar
import os

# Masquage
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# URL du calendrier (jusqu'au 1 septembre 2025)
url = "https://ade-usmb-ro.grenet.fr/jsp/custom/modules/plannings/direct_cal.jsp?data=b5cfb898a9c27be94975c12c6eb30e9233bdfae22c1b52e2cd88eb944acf5364c69e3e5921f4a6ebe36e93ea9658a08f,1&resources=4884&projectId=2&calType=ical&lastDate=2042-08-14&nocache"

# Télécharger le fichier .ics
response = requests.get(url)
if response.status_code == 200:
    
    path = os.path.join(os.path.dirname(__file__), "templates/emploi_du_temps.ics")
    with open("emploi_du_temps.ics", "wb") as file:
        file.write(response.content)
    print("ics file succesfully downloaded")
else:
    print("Error :", response.status_code)
    exit()

with open("emploi_du_temps.ics", "r", encoding="utf-8") as file:
    calendrier = Calendar(file.read())

# Aficher les événements
print("\n Emploi du temps :\n" + "=" * 30)
for event in calendrier.events:
    print(f" {event.name}") 
    print(f" Début : {event.begin.to('local')}") 
    print(f" Fin : {event.end.to('local')}")
    print(f" Lieu : {event.location if event.location else 'Non spécifié'}")
    print("-" * 30)

