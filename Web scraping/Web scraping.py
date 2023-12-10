import csv
import requests
from bs4 import BeautifulSoup
import re

# Leer el archivo CSV
with open('./links.csv', 'r') as file:
      reader = csv.reader(file)
      # Obtener las URL que aparecen dentro del fichero en la columna correspondiente
      urls = [row[1] for row in reader]

#obtener los datos de cada una de las urls y parsear el html
responses=[]
for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    responses.append(soup)

#crear una lista vacia que almacene el contenido visible de cada uno de los reportes
text=[]
#obtener el texto visible de cada uno de los urls
for content in responses:
    visible_text= content.get_text()
    text.append(visible_text)
print(text)
#almacenar la información de los reportes en un archivo txt
with open("reportes.txt","w") as report:
    for info in text:
        report.write(info+"./n")

