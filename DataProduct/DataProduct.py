import os, streamlit as st, pandas as pd,plotly.express as px, plotly.graph_objects as go
from datetime import datetime as dt

# Cargamos el contenido del json en un Data Frame obteniendo la ruta q contiene el archivo y luego combinando
# Con con el nombre del json
db=pd.read_json(os.path.join(os.path.dirname(__file__), '..', 'base de datos.json'))
db=db.transpose() # Transponer el dataframe
db = db.drop('Info', axis=1)

with st.container():
    st.title("El déficit de electricidad en Cuba")
    st.write("""
         En los últimos annos el país ha experimentado importantes afectaciones relacionadas con el Sistema Electroenergético Nacional, que unido a varias factores
         la disponibilidad del petróleo y otros han generado gran descontento en la población. Es por eso que mediante el siguiente estudio se pretende que la población
         adquiera un mayor conocimiento sobre el tema y de esta forma generar una mayor conciencia de por qué resulta importante el ahorro de electricidad.
         """)

with st.expander("Comportamiento de los parametros"):
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

db.index.name = 'Fecha'
db = db.reset_index()
if db['Fecha'].dtype != 'datetime64[ns]':
    db['Fecha'] = pd.to_datetime(db['Fecha'])
        
db['Mes'] = db['Fecha'].dt.month
db['Mes']=db['Mes'].astype (str)
db['Año'] = db['Fecha'].dt.year

with st.expander("Máxima afectación durante el horario pico"):
    st.write("---")
    st.title("Máxima afectación durante el horario pico:")
    st.write(f"""A la largo de los annos las cifras de las máximas afectaciones durante el horario pico han sido bastante elevadas, principalmente en el anno 2022, donde alcanzaron los valores más elevados.
             La maxima afectación del anno 2022 se reportó en el mes de octubre, cuyas afectaciones promedio en el mes fueron de  1138 MW aproximadamente. 
             Sin embargo en 2023, la maxima afectacion por mes fue de 473.5 MW en el mes de abril, esto nos demuestra la existencia de factores que, unido a las diferentes
             medidas tomadas por la empresa el'ectrica de conjunto con otros organismos, han posibilitado la disminución de la afectación.
             De igual forma, el comportamiento de la variable no es igual entre ambos annos. Las máximas afectaciones de 2022 corresponden a los meses desde agosto hasta noviembre,
             mientras que en 2023 las máximas afectaciones se corresponden a abril, septiembre, octubre y noviembre.
             El mes de menor afectación en el anno 2022 es marzo, mientras que el mes de menor afectación en el 2023 es julio.
             
             """)
 
    #Calcular la media por mes de la máxima afectación en el horario pico para cada año
    media_por_mes = db.groupby(['Año', 'Mes'])['Maxima afectacion'].mean().reset_index()
    fig = px.bar(media_por_mes, x='Mes', y='Maxima afectacion', barmode="group",color='Año' ,color_discrete_sequence=px.colors.qualitative.Plotly)

    # Mostrar el gráfico en Streamlit
    st.write("Media de máxima afectación en el horario pico por mes")
    st.plotly_chart(fig)
    
    #hacer un grafico de cajas:
    # Crear un selectbox para seleccionar el año
    ano = st.selectbox("Selecciona un año", db['Año'].unique())
    # Filtrar el dataframe basado en la selección del usuario
    db_filtrado = db[db['Año'] == ano]
    # Crear el boxplot
    boxplot = px.box(db_filtrado, x="Mes", y="Maxima afectacion",
                    title='Distribución de Máxima Afectación durante Horario Pico de Megawatts por Mes',
                    labels={'Max_Afectacion_Horario_Pico_MW': 'Máxima Afectación (MW)', 'x': 'Mes'},
                    color_discrete_sequence=['#2B83BA'])
    st.plotly_chart(boxplot)
    
with st.expander("Demanda vs Disponibilidad"):
    st.write("---")
    st.title("Disponibilidad vs Demanda")
    st.write("""
             La disponibilidad y la demanda del sistema electroenergetico nacional varia con el transcurso del día, por lo que, para el análisis de esta variable hemos
             analizado la disponibilidad y la demanda a las 6:00-7:00 am.
             Resulta imposible hablar de disponibilidad sin hablar de demanda y viceversa, lo cual se comprueba en el siguiente grafico que muestra la fuerte correlaci'on exitente entre las dos variables:
             """)
    #grafico de dispersion
    fig = px.scatter(db_filtrado, x='Demanda del dia', y='MW disponibles', text='Mes', title='Demanda vs. Disponibilidad')
    # Personalizar el diseño del gráfico
    fig.update_traces(marker=dict(size=12, line=dict(width=2, color='DarkSlateGrey')),
                    selector=dict(mode='markers+text'))
    # Visualizar el gráfico en Streamlit
    st.plotly_chart(fig)
    
    st.write("""
             De la misma forma, en dependencia de la disponibilidad y la demanda del día es posible conocer el déficit diario de electricidad, y de esta forma conocer los meses de mayor déficit.
             De esta forma los meses de mayor deficit de electricidad de 2022 corresponden con junio, septiembre y noviembre.
             En 2023 el mayor deficit estuvo dado en los meses de septiembre, octubre, noviembre y junio. 
             Por lo que coinciden los meses de junio, septiembre y noviembre como meses con mayor deficit de electricidad en el anno.
             """
    )
    
    deficit=db["Demanda del dia"]-db["MW disponibles"]
    deficit[deficit<0]=0
    db["Deficit"]=deficit
    year=st.selectbox("Seleccione el anno",db['Año'].unique())
    media_deficit = db.groupby(['Año', 'Mes'])['Deficit'].mean().reset_index()
    db_filtrado2 = db[db['Año'] == year]
    fig=px.bar(db_filtrado2, x='Mes', y='Deficit', title=f'Déficit por mes en {ano}')
    st.plotly_chart(fig)
    
with st.expander("MW limitados en la generación térmica"):
    st.write("---")
    st.title("MW limitados y generación térmica:")
    st.write("""
             
             """)