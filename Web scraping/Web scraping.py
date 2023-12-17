import csv
import requests
from bs4 import BeautifulSoup
import json

# Abrir el archivo json
with open('base de datos.json') as bdjson:
    json_data = json.load(bdjson)

    # Leer el archivo CSV
    with open('./Web scraping/links.csv', 'r') as file:
        reader = csv.reader(file)

        #obtener los datos de cada una de las urls y parsear el html
        responses={}
        for row in reader:
            if row[3] in json_data:
                continue
            try:
                response = requests.get(row[1])
                soup = BeautifulSoup(response.text, 'html.parser')
            except:
                continue
            responses[row[3]] = [
                {
                    'Maxima afectacion': 0,
                    'MW disponibles': 0,
                    'Demanda del dia': 0,
                    'MW indisponibles por averias': 0,
                    'MW en mantenimiento': 0,
                    'MW limitados en la generacion termica': 0,
                    'Termoelectricas fuera de servicio': [],
                    'Termoelectricas en funcionamiento': [],
                    'Info':soup.get_text()
                }
            ]

# Guardar el archivo JSON actualizado
with open('base de datos.json', 'w') as f:
    json.dump(responses, f, indent=4)
