import os, streamlit as st, pandas as pd, plotly.graph_objects as go
from datetime import datetime as dt

# Cargamos el contenido del json en un Data Frame obteniendo la ruta q contiene el archivo y luego combinando
# Con con el nombre del json
db=pd.read_json(os.path.join(os.path.dirname(__file__), '..', 'base de datos.json'))
db=db.transpose() # Transponer el dataframe
db = db.drop('Info', axis=1)

#Titulo de la visualizacion
st.title("Comportamiento de los diferentes parametros a lo largo del tiempo")
categories = ["MW disponibles","Demanda del dia","MW indisponibles por averias","MW en mantenimiento","MW limitados en la generacion termica"]

if not st.session_state.get("visible_series"):
    st.session_state["visible_series"] = []

fig = go.Figure()

# Agregar un selector de fechas para elegir el rango de fechas a mostrar
try:
    start_date = st.date_input(label='Fecha de inicio', value=db.index.min(), min_value=db.index.min(), max_value=end_date)  # type: ignore
except:
    start_date = st.date_input(label='Fecha de inicio', value=db.index.min(), min_value=db.index.min(), max_value=db.index.max())
start_date = dt(start_date.year, start_date.month, start_date.day)
end_date = st.date_input(label='Fecha de fin', value=db.index.max(), min_value=start_date, max_value=db.index.max())
end_date = dt(end_date.year, end_date.month, end_date.day)

# Filtrar la bd con respecto a las fechas seleccionadas
filter_df = db[(db.index >= start_date) & (db.index <= end_date)]

# Crear el gráfico
for line in filter_df:
    if type(filter_df[line][0]) != int:
        continue
    fig.add_scatter(x=filter_df.index , y=filter_df[line], mode="lines", name=line, visible=True)
    st.session_state["visible_series"].append(line)
st.session_state.fig_state = fig.to_dict()
st.plotly_chart(fig)

# 0420: Aquí hace falta usar el update o como se llame, pero por hoy no doy más, si alguien más sabe como usarlo 
# q lo ponga, en cada if pongan su análisis como (si me dio tiempo) yo puse en los q me correspondían, solo falta
# hacer q muestre la información correspondiente solo cuando ese sea el q está activado
# Lo probé de todas las formas posibles y no doy pie con bola con esto, si alguien lo logra q me despierte porfa.
# La idea es, q para eliminar las check box feas esas me di cuenta q la leyenda del gráfico si le das un clic,
# Elimina dicho gráfico de la gráfica, ahora estaba buscando una manera de guardar ese valor de q está activo o
# No en una variable, gpt recomendó dejar de usar el plotly.exenoseqcosa y usar el q está ahora, al final, no vi
# Diferencia, pero parece q es por lo q ven abajo, visible es una opción q no estaba disponible antes (o eso quiero
# creer), se supone q sea de la siguiente forma: Cuando visible = False el gráfico no se está mostrando, yo ya
# lo eh intentado todo y me knsé, mañana lo seguiré intentando pero por ahora terminé 0656

for trace in st.session_state.fig_state['data']:
    if trace['visible']:
        st.session_state["visible_series"].append(trace['name'])
        st.session_state.fig_state = fig.to_dict()
    else:
        st.session_state["visible_series"].remove(trace['name'])
        st.session_state.fig_state = fig.to_dict()
i=0
for line in st.session_state["visible_series"]:
    if len(st.session_state["visible_series"]) == 1:
        if line == 'Maxima afectacion':
            st.write(f'La serie {line} está marcada en la leyenda')
        elif line == 'MW disponibles':
            st.write(f'La serie {line} está marcada en la leyenda')
        elif line == 'Demanda del dia':
            st.write(f'La serie {line} está marcada en la leyenda')
        elif line == 'MW indisponibles por averias':
            st.write(f'En este momento observamos el gráfico de {line} desde el {start_date.day}/{start_date.month}/{start_date.year} hata el {end_date.day}/{end_date.month}/{end_date.year}.')
            st.write(f'Teniendo en cuenta nuestros datos, les mostraré las medidas de tendencia sentral correspondientes, como por ejemplo, {filter_df[line].mean()} es el promedio de {line} que hubo en este período de tiempo. Además de esto, también tenemos una mediana de {filter_df[line].median()}')
        elif line == 'MW en mantenimiento':
            st.write(f'La serie {line} está marcada en la leyenda')
        elif line == 'MW limitados en la generacion termica':
            st.write(f'La serie {line} está marcada en la leyenda')
    else:
        if i == 0:
            st.write('''Aquí se muestran todos los parámetros analizados a lo largo del tiempo, puede mostrar u ocultar alguna variable solo haciendo clic en su respectivo nombre en la leyenda que se encuentra a la derecha del gráfico
            Seleccionando un solo gráfico tendrá acceso a su respectivo análisis''')
            i+=1

    