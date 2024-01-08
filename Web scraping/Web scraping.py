import csv, requests, json
from datetime import date, datetime as dt
from bs4 import BeautifulSoup

# Abrir el archivo json
with open('./base de datos.json') as bdjson:
    json_data = json.load(bdjson)

    # Leer el archivo CSV
    with open('./Web scraping/links.csv', 'r') as file:
        reader = csv.reader(file)
        
        # Obtener los datos de cada una de las urls y parsear el html
        responses={}
        for row in reader:
            data = [int(i) for i in row[3].split(' ')]
            data = str(date(data[2], data[1], data[0]))
            if data in json_data:
                continue
            try:
                response = requests.get(row[1])
                soup = BeautifulSoup(response.text, 'html.parser')
            except:
                continue
            responses[data] = {
                'Maxima afectacion': None,
                'MW disponibles': None,
                'Demanda del dia': None,
                'MW indisponibles por averias': None,
                'MW en mantenimiento': None,
                'MW limitados en la generacion termica': None,
                'Termoelectricas fuera de servicio': [
                    '',
                    ''
                ],
                'Termoelectricas en mantenimiento': [
                    '',
                    ''
                ],
                'Info':soup.get_text()
            }

# Guardar el archivo JSON actualizado
json_data.update(responses)
json_data = dict(sorted(json_data.items(), key=lambda x: dt.strptime(x[0], '%Y-%m-%d'), reverse=True))
with open('./base de datos.json', 'w') as f:
    json.dump(json_data, f, indent=4)
