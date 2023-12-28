import streamlit as st, pandas as pd
import json
import os
import plotly.express as px
import matplotlib.pyplot as plt

#Obtiene la ruta del directorio que contiene archivo.py
current_dir = os.path.dirname(__file__)
# Combinamos la ruta del directorio con el nombre del archivo JSON
json_file_path = os.path.join(current_dir, '..', 'base de datos.json')

# Abre el archivo JSON y lo carga
with open(json_file_path, 'r') as file:
    data = json.load(file)
 
#carga el contenido del json en un dataframe 
db=pd.DataFrame(data)
#transponer el dataframe
df=db.transpose()
#almacena todas las fechas en la variable dates
dates= df.index
#Titulo de la visualizacion
st.title("Comportamiento de los diferentes parametros a lo largo del tiempo")

fig = px.line()
categories = ["Maxima afectacion", "MW disponibles","Demanda del dia","MW indisponibles por averias","MW en mantenimiento","MW limitados en la generacion termica"]
selected_lines = []
for category in categories:
   if st.checkbox(category):
       selected_lines.append(category)
default_line = "Maxima afectacion"
show_maxima_afectacion = st.checkbox(default_line, value=True, key=default_line)
#Una vez que el checkbox se define, agregar la línea al gráfico si está seleccionada
if show_maxima_afectacion:
    fig.add_scatter(x=dates, y=df[default_line], mode="lines", name=default_line)
# Crear el gráfico combinado con las líneas seleccionadas
for line in selected_lines:
    fig.add_scatter(x=dates , y=df[line], mode="lines", name=line)
#el gráfico combinado
st.plotly_chart(fig)