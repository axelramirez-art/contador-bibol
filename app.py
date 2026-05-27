import streamlit as st
import sqlite3
from datetime import datetime
import requests
import base64

# 1. CONFIGURACIÓN DE LA PÁGINA Y ESTILOS VISUALES
st.set_page_config(
    page_title="¿Mi bibol comió bien?", 
    page_icon="❤️", 
    layout="centered"
)

# RECUERDA: Cambia 'tu_usuario_github' por tu nombre de usuario real de GitHub
USER_GITHUB = "tu_usuario_github" 
URL_LOGO = f"https://raw.githubusercontent.com/{USER_GITHUB}/contador-bibol/master/icono_app.png"

# Función mágica para incrustar la imagen directo en el navegador
def cargar_icono_base64(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return base64.b64encode(response.content).decode()
    except:
        pass
    return ""

logo_base64 = cargar_icono_base64(URL_LOGO)

# Si se logró convertir la imagen, se la clavamos al iPhone directamente en las raíces de la página
if logo_base64:
    data_uri = f"data:image/png;base64,{logo_base64}"
    st.markdown(f"""
        <span style="display:none;">
            <script>
                // Modificar todos los lugares donde Apple busca iconos
                var links = ['apple-touch-icon', 'apple-touch-icon-precomposed', 'icon', 'shortcut icon'];
                links.forEach(function(rel) {{
                    var link = document.querySelector("link[rel*='" + rel + "']") || document.createElement('link');
                    link.type = 'image/png';
                    link.rel = rel;
                    link.href = '{data_uri}';
                    document.getElementsByTagName('head')[0].appendChild(link);
                }});
            </script>
        </span>
    """, unsafe_allow_html=True)

# Estilo personalizado (CSS) para colores y visibilidad
st.markdown("""
    <style>
    /* Fondo de la aplicación */
    .stApp {
        background-color: #FFF5F5;
    }
    
    /* Contenedor del logo redondo */
    .logo-container {
        text-align: center;
        margin-top: 10px;
    }
    .logo-img {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid #D53F8C;
        box-shadow: 0px 4px 10px rgba(213, 63, 140, 0.3);
    }
    
    /* Título principal */
    h1 {
        color: #D53F8C !important;
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        margin-top: 10px !important;
    }
    
    /* Subtítulos */
    h3 {
        color: #4A5568 !important;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Forzar que las métricas tengan letra oscura */
    [data-testid="stMetricValue"] {
        color: #2D3748 !important;
        font-weight: bold !important;
    }
    [data-testid="stMetricLabel"] {
        color: #4A5568 !important;
    }
    
    /* Forzar que el texto dentro del expander sea oscuro */
    .stExpander div, .stExpander p, .stExpander label, .stExpander span {
        color: #2D3748 !important;
    }
    
    /* Botones de registro */
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
    }
    
    /* Cuadros de mensajes personalizados */
    .mensaje-exito {
        background-color: #DEF7EC;
        color: #03543F;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #31C48D;
        font-weight: 500;
        margin: 10px 0px;
    }
    .mensaje-info {
        background-color: #E1EFFE;
        color: #1E429F;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #3F83F8;
        font-weight: 500;
        margin: 10px 0px;
    }
    .mensaje-error {
        background-color: #FDE8E8;
        color: #9B1C1C;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #F05252;
        font-weight: 500;
        margin: 10px 0px;
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
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
    c.execute("INSERT INTO registro (fecha, opcion, estrellas) VALUES (?, ?, ?)", (fecha_actual, opcion, estrellas))
    conn.commit()

def obtener_total_estrellas():
    c.execute("SELECT SUM(estrellas) FROM registro")
    res = c.fetchone()[0]
    return res if res is not None else 0.0

def obtener_historial():
    c.execute("SELECT id, fecha, opcion, estrellas FROM registro ORDER BY id DESC")
    return c.fetchall()

def eliminar_ultimo_registro():
    c.execute("SELECT id FROM registro ORDER BY id DESC LIMIT 1")
    ultimo = c.fetchone()
    if ultimo:
        c.execute("DELETE FROM registro WHERE id = ?", (ultimo[0],))
        conn.commit()
        return True
    return False

def reiniciar_todo():
    c.execute("DELETE FROM registro")
    conn.commit()

# 4. INTERFAZ DE USUARIO
if logo_base64:
    st.markdown(f'<div class="logo-container"><img class="logo-img" src="data:image/png;base64,{logo_base64}"></div>', unsafe_allow_html=True)

st.write("<h1 style='margin-bottom: 0px;'>¿Mi bibol comió bien? ❤️</h1>", unsafe_allow_html=True)
st.write("<p style='text-align: center; color: #718096; font-size: 1.1em;'>Registra cómo te fue con tu comida hoy, mi niña</p>", unsafe_allow_html=True)
st.write("---")

total_actual = obtener_total_estrellas()

if 'mensaje' not in st.session_state:
    st.session_state.mensaje = None
    st.session_state.tipo_mensaje = None

# Botones de registro
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

# Mostrar mensajes
if st.session_state.mensaje:
    st.write("")
    if st.session_state.tipo_mensaje == "success": 
        st.markdown(f'<div class="mensaje-exito">{st.session_state.mensaje}</div>', unsafe_allow_html=True)
    elif st.session_state.tipo_mensaje == "info": 
        st.markdown(f'<div class="mensaje-info">{st.session_state.mensaje}</div>', unsafe_allow_html=True)
    elif st.session_state.tipo_mensaje == "error": 
        st.markdown(f'<div class="mensaje-error">{st.session_state.mensaje}</div>', unsafe_allow_html=True)

st.write("---")

# 5. CONTADOR Y META
st.markdown("### 🎯 Tu progreso hacia la bolsa 👜")
progreso_porcentaje = min(total_actual / 60.0, 1.0)
st.progress(progreso_porcentaje)

st.metric(label="Estrellas acumuladas", value=f"{total_actual} / 60 ⭐")

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
        _, fecha, opcion, est = fila
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
    st.dataframe(tabla_datos, use_container_width=True, hide_index=True)
    
    # Menú de herramientas
    st.write("")
    with st.expander("¿Presionaste mal? Presiona aquí ⚙️"):
        st.write("Usa estas opciones si hubo un error al registrar o si quieres limpiar las pruebas.")
        if st.button("⚠️ Borrar última estrellita (Btw te guardé el azul y tú me guardaste el rojo)", use_container_width=True):
            if eliminar_ultimo_registro():
                st.toast("¡Último registro eliminado!")
                st.session_state.mensaje = None
                st.rerun()
        if st.button("🚨 Reiniciar toda la tabla a cero", use_container_width=True):
            reiniciar_todo()
            st.toast("¡La tabla ha vuelto a cero!")
            st.session_state.mensaje = None
            st.rerun()
else:
    st.info("Aún no hay registros. ¡Tu primera estrellita te espera hoy! ✨")