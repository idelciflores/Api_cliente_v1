import sqlite3
import pandas as pd

DB_NAME = "usuarios_api.db"

def conectar():
    return sqlite3.connect(DB_NAME)

def crear_tabla():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY,
            nombre TEXT,
            usuario TEXT,
            email TEXT,
            ciudad TEXT,
            telefono TEXT,
            sitio_web TEXT
        )
    """)
    conn.commit()
    conn.close()

def guardar_usuarios(usuarios):
    conn = conectar()
    cursor = conn.cursor()
    for u in usuarios:
        cursor.execute("""
            INSERT OR REPLACE INTO usuarios (id, nombre, usuario, email, ciudad, telefono, sitio_web)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            u['id'], u['name'], u['username'], u['email'], 
            u['address']['city'], u['phone'], u['website']
        ))
    conn.commit()
    conn.close()

def consultar_usuarios():
    conn = conectar()
    df = pd.read_sql_query("SELECT * FROM usuarios", conn)
    conn.close()
    return df

def eliminar_datos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios")
    conn.commit()
    conn.close()