import streamlit as st
import sqlite3
from datetime import datetime

# 1. CONFIGURACIÓN DE LA PÁGINA Y ESTILOS VISUALES (CSS)
st.set_page_config(
    page_title="¿Mi bibol comió bien?", 
    page_icon="❤️", 
    layout="centered"
)

# Estilo personalizado para cambiar el fondo, botones y textos a tonos románticos
st.markdown("""
    <style>
    /* Fondo de la aplicación */
    .stApp {
        background-color: #FFF5F5;
    }
    
    /* Estilo del título principal */
    h1 {
        color: #D53F8C !important;
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
    }
    
    /* Subtítulos */
    h3 {
        color: #4A5568 !important;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Personalización de los botones de Streamlit */
    div.stButton > button {
        background-color: #FFFFFF;
        color: #D53F8C;
        border: 2px solid #FED7E2;
        border-radius: 20px;
        padding: 10px 20px;
        font-weight: bold;
        font-size: 16px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    div.stButton > button:hover {
        background-color: #E11D48 !important;
        color: white !important;
        border-color: #E11D48 !important;
        transform: translateY(-2px);
        box-shadow: 0px 6px 8px rgba(225, 29, 72, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# 2. CONEXIÓN A BASE DE DATOS LOCAL
conn = sqlite3.connect('registro_comida.db', check_same_thread=False)
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS registro (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        fecha TEXT, 
        opcion TEXT, 
        estrellas REAL
    )
''')
conn.commit()

# 3. FUNCIONES DE LÓGICA
def guardar_registro(opcion, estrellas):
    # Guardamos la fecha en un formato más amigable (Día/Mes/Año Hora)
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
    c.execute("INSERT INTO registro (fecha, opcion, estrellas) VALUES (?, ?, ?)", (fecha_actual, opcion, estrellas))
    conn.commit()

def obtener_total_estrellas():
    c.execute("SELECT SUM(estrellas) FROM registro")
    res = c.fetchone()[0]
    return res if res is not None else 0.0

def obtener_historial():
    c.execute("SELECT fecha, opcion, estrellas FROM registro ORDER BY id DESC")
    return c.fetchall()

# 4. INTERFAZ DE USUARIO
st.write("<h1 style='margin-bottom: 0px;'>¿Mi bibol comió bien? ❤️</h1>", unsafe_allow_html=True)
st.write("<p style='text-align: center; color: #718096; font-size: 1.1em;'>Registra cómo te fue con tu comida hoy, mi niña</p>", unsafe_allow_html=True)
st.write("---")

total_actual = obtener_total_estrellas()

# Control de mensajes en la sesión
if 'mensaje' not in st.session_state:
    st.session_state.mensaje = None
    st.session_state.tipo_mensaje = None

# Distribución de los 3 botones en columnas
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Sí 🌟", use_container_width=True):
        guardar_registro("Sí", 1.0)
        st.session_state.mensaje = "Muy bieeen mi niña, felicidades 🎉"
        st.session_state.tipo_mensaje = "success"
        st.rerun()

with col2:
    if st.button("Más o menos ⛅", use_container_width=True):
        guardar_registro("Más o menos", 0.5)
        st.session_state.mensaje = "Estoy orgulloso de tu esfuerzo, tú puedes 💪"
        st.session_state.tipo_mensaje = "info"
        st.rerun()

with col3:
    if st.button("No 🌧️", use_container_width=True):
        guardar_registro("No", 0.0)
        st.session_state.mensaje = "Fue un día duro mi bebé, pero tú puedes lograrlo. Creo en ti 🧸"
        st.session_state.tipo_mensaje = "error"
        st.rerun()

# Espacio para mostrar los mensajes con diseños nativos bonitos
if st.session_state.mensaje:
    st.write("")
    if st.session_state.tipo_mensaje == "success": 
        st.success(st.session_state.mensaje)
    elif st.session_state.tipo_mensaje == "info": 
        st.info(st.session_state.mensaje)
    elif st.session_state.tipo_mensaje == "error": 
        st.warning(st.session_state.mensaje)

st.write("---")

# 5. CONTADOR Y META HACIA LA BOLSA
st.markdown("### 🎯 Tu progreso hacia la bolsa 👜")
progreso_porcentaje = min(total_actual / 60.0, 1.0)

# Barra de progreso rosa por defecto en el ecosistema
st.progress(progreso_porcentaje)
st.metric(label="Estrellas acumuladas", value=f"{total_actual} / 60 ⭐")

# Celebración si llega a la meta
if total_actual >= 60:
    st.balloons()
    st.success("¡Felicidades mi vida! 👑 ¡Te has ganado tu bolsa! 👜❤️ ¡Te amo!")

st.write("---")

# 6. TABLA DE HISTORIAL VISUAL
st.markdown("### 📋 Historial de tus estrellitas")
historial = obtener_historial()

if historial:
    tabla_datos = []
    for fila in historial:
        fecha, opcion, est = fila
        if est == 1.0:
            est_str = "⭐ Excelente"
        elif est == 0.5:
            est_str = "½ ⭐ Buen esfuerzo"
        else:
            est_str = "❌ Mañana será mejor"
            
        tabla_datos.append({
            "Fecha y Hora": fecha, 
            "¿Comió bien?": opcion, 
            "Premio": est_str
        })
    # Mostramos la tabla estilizada
    st.dataframe(tabla_datos, use_container_width=True, hide_index=True)
else:
    st.info("Aún no hay registros. ¡Tu primera estrellita te espera hoy! ✨")