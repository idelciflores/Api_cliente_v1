import streamlit as st
import pandas as pd
from api_client import obtener_usuarios_api
from database import crear_tabla, guardar_usuarios, consultar_usuarios, eliminar_datos
st.set_page_config(page_title="API-SQLITE", page_icon="📊", layout="wide")

crear_tabla()
st.title("Proyecto Cloud: API + SQLite + Streamlit")
st.write("Aplicación que consume una API pública, guarda los datos en SQLite y los muestra en una tabla.")

menu = st.sidebar.selectbox (
    "Seleccione una opción",
    [
        "Inicio",
        "Consumir API",
        "Ver la base de datos",
        "Buscar los usuarios",
        "Eliminar los datos"
    ]
)

if menu == "Inicio":
    st.header("Bienvenido a la aplicación")
    st.info("Seleccione una opción en el menú lateral para comenzar.")

elif menu == "Consumir API":
    st.header("Consumir API pública")
    if st.button("Obtener usuarios de la API"):
        usuarios = obtener_usuarios_api()
        if usuarios:
            guardar_usuarios(usuarios)
            st.success("¡Datos guardados! Ya puedes verlos en la tabla.")
            st.json(usuarios[0]) # Muestra el primer usuario como prueba
        else:
            st.error("Error al conectar con la API.")

elif menu == "Ver la base de datos":
    st.header("Tabla almacenada en SQLite")
    df = consultar_usuarios()
    if df.empty:
        st.warning("La base de datos está vacía. Ve a 'Consumir API' primero.")
    else:
        st.dataframe(df, use_container_width=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("Total usuarios", len(df))
        c2.metric("Ciudades", df["ciudad"].nunique())
        c3.metric("Correos", df["email"].nunique())

elif menu == "Buscar los usuarios":
    st.header("Buscar usuario")
    df = consultar_usuarios()
    if not df.empty:
        nombre = st.text_input("Nombre a buscar:")
        if nombre:
            res = df[df["nombre"].str.contains(nombre, case=False, na=False)]
            st.dataframe(res)

elif menu == "Eliminar los datos":
    st.header("Eliminar registros")
    if st.button("Confirmar: Eliminar todo"):
        eliminar_datos()
        st.success("Datos borrados correctamente.")