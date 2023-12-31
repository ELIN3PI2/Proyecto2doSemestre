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

if 'end_date' not in st.session_state:
    st.session_state.end_date = dt(db.index.max().year, db.index.max().month, db.index.max().day)
if 'start_date' not in st.session_state:
    st.session_state.start_date = dt(db.index.min().year, db.index.min().month, db.index.min().day)

fig = go.Figure()

# Agregar un selector de fechas para elegir el rango de fechas a mostrar
start_date = st.date_input(label='Fecha de inicio', value=db.index.min(), min_value=db.index.min(), max_value=st.session_state.end_date)
st.session_state.start_date = dt(start_date.year, start_date.month, start_date.day)
end_date = st.date_input(label='Fecha de fin', value=db.index.max(), min_value=st.session_state.start_date, max_value=db.index.max())
st.session_state.end_date = dt(end_date.year, end_date.month, end_date.day)

# Filtrar la bd con respecto a las fechas seleccionadas
filter_df = db[(db.index >= st.session_state.start_date) & (db.index <= st.session_state.end_date)]
filter_df = filter_df.drop(['Termoelectricas fuera de servicio', 'Termoelectricas en mantenimiento'], axis = 1)

maxafectcheck = st.checkbox("Maxima afectacion", True)
mwdispctcheck = st.checkbox("MW disponibles", True)
demdiactcheck = st.checkbox("Demanda del dia", True)
mwinavctcheck = st.checkbox("MW indisponibles por averias", True)
mwmantctcheck = st.checkbox("MW en mantenimiento", True)
mwligtctcheck = st.checkbox("MW limitados en la generacion termica", True)

# Crear el gráfico
for line in filter_df:
    if (line == 'Maxima afectacion' and maxafectcheck) or (line == 'MW disponibles' and mwdispctcheck) or (line == 'Demanda del dia' and demdiactcheck) or (line == 'MW indisponibles por averias' and mwinavctcheck) or (line == 'MW en mantenimiento' and mwmantctcheck) or (line == 'MW limitados en la generacion termica' and mwligtctcheck):
        visibility = True
    else:
        visibility = 'legendonly'
    fig.add_scatter(x=filter_df.index , y=filter_df[line], mode="lines", name=line, visible=visibility)

st.plotly_chart(fig)

if maxafectcheck and not mwdispctcheck and not demdiactcheck and not mwinavctcheck and not mwligtctcheck and not mwligtctcheck:
    st.write(f'La serie 1 está marcada en la leyenda')
elif mwdispctcheck and not maxafectcheck and not demdiactcheck and not mwinavctcheck and not mwligtctcheck and not mwligtctcheck:
    st.write(f'La serie 2 está marcada en la leyenda')
elif demdiactcheck and not mwdispctcheck and not demdiactcheck and not mwinavctcheck and not mwligtctcheck and not mwligtctcheck:
    st.write(f'La serie 3 está marcada en la leyenda')
elif mwinavctcheck and not mwdispctcheck and not demdiactcheck and not maxafectcheck and not mwligtctcheck and not mwligtctcheck:
    column = 'MW indisponibles por averias'
    st.write(f'En este momento observamos el gráfico de {column} desde el {start_date.day}/{start_date.month}/{start_date.year} hata el {end_date.day}/{end_date.month}/{end_date.year}.')
    st.write(f'Teniendo en cuenta nuestros datos, les mostraré las medidas de tendencia central correspondientes, como por ejemplo, {round(filter_df[column].mean(), 2)} es, aprocimadamente, el promedio de {column} que hubo en el período de tiempo seleccionado. Además de esto, también tenemos una mediana de {filter_df[line].median()}.')
    if len(filter_df[column].mode()) == 1:
        st.write(f'En el caso de la moda, no necesariamente es un solo valor pero, en el rango q usted eligió en este caso, si es un solo valor y este es {filter_df[column].mode()[0]}')
    else:
        liste = [str(i) for i in filter_df[column].mode()]
        st.write(f'En el caso de la moda, no necesariamente es un solo valor, de echo, en el rango q usted eligió son {len(filter_df[column].mode())} valores y estos son {", ".join(liste)}')
    st.write(f'Ahora toca mostrar el valor máximo, que en este conjunto de datos es de {filter_df[column].max()} y el valor mínimo que es de {filter_df[column].min()}')
    st.write(f'Gracias a la desviación estándar podemos observar cuanto se aleja de su media, en este caso su valor es de aproximadamente {round(filter_df[column].std(), 2)}, a continuación muestro un gráfico comparando la desviación estándar y el gráfico de arriba:')
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=filter_df.index, y=filter_df[column], mode='lines', name=column))
    fig2.add_trace(go.Scatter(x=[filter_df.index[-1], filter_df.index[0]], y=[filter_df[column].std(), filter_df[column].std()], mode='lines', name='Desviación Estándar'))
    fig.update_layout(title=column, xaxis_title='Fecha', yaxis_title='MW')
    st.plotly_chart(fig2)
    st.write(f'')
    st.write(f'')
elif mwmantctcheck and not mwdispctcheck and not demdiactcheck and not mwinavctcheck and not maxafectcheck and not mwligtctcheck:
    st.write(f'La serie 4 está marcada en la leyenda')
elif mwligtctcheck and not mwdispctcheck and not demdiactcheck and not mwinavctcheck and not mwmantctcheck and not maxafectcheck:
    st.write(f'La serie 5 está marcada en la leyenda')
else:
    st.write('Aquí se muestran todos los parámetros analizados a lo largo del tiempo, puede mostrar u ocultar alguna gráfico solo marcando o desmarcando su respectiva check box que se encuentra arriba del gráfico.\nSeleccionando un solo gráfico tendrá acceso a su respectivo análisis')
