import streamlit as st
import pandas as pd

# Base de récords del mundo en 2000m (en segundos)
# Podés agregar todos los botes que necesites
wbt_2000m = {
    'M1x': 390.7, 'M2-': 368.5, 'M2x': 359.7, 'M4x': 332.0, 'M4-': 337.8, 'M8+': 317.7,
    'LM1x': 399.5, 'LM2x': 365.3, 'LM2-': 382.9, 'LM4x': 342.7, 'LM4-': 343.1,
    'BM1x': 402.0, 'BM2x': 367.5, 'BM2-': 379.7, 'BM4x': 339.5, 'BM4-': 344.3,
    'JM1x': 405.4, 'JM2x': 378.1, 'JM2-': 387.9, 'JM4x': 346.4, 'JM4-': 347.7, 'JM8+': 333.4,
    'MenM1x': 411.4, 'MenM2x': 384.1, 'MenM4x': 352.4, 'NovM1x': 411.4, 'NovM2x': 384.1,
    'W1x': 427.7, 'W2-': 407.4, 'W2x': 397.3, 'W4x': 365.1, 'W4-': 369.8, 'W8+': 351.8,
    'LW1x': 443.3, 'LW2x': 400.4, 'LW2-': 437.0, 'LW4x': 375.9, 'LW4-': 396.4,
    'BW1x': 433.6, 'BW2x': 406.8, 'BW2-': 418.4, 'BW4x': 375.9, 'BW4-': 382.2,
    'JW1x': 451.5, 'JW2x': 417.4, 'JW2-': 435.5, 'JW4x': 383.8, 'JW4-': 392.7, 'JW8+': 372.1,
    'MenW1x': 457.5, 'MenW2x': 423.4, 'MenW4x': 389.8, 'NovW1x': 457.5, 'NovW2x': 423.4, 'Mix8+': 334.4
}

st.set_page_config(page_title="Pronósticos de Remo", layout="centered")
st.title("⏱️ T.B.C. Pronósticos")

# Inicializar la tabla temporal en la memoria de la app
if 'entrenamiento' not in st.session_state:
    st.session_state.entrenamiento = pd.DataFrame(columns=['Categoría', 'Tripulación', 'Tiempo', 'Pronóstico (%)'])

# --- PANEL DE INGRESO ---
st.subheader("Cargar Bote")
col_fecha, col_dist = st.columns(2)
fecha = col_fecha.date_input("Fecha")
distancia = col_dist.number_input("Distancia del trabajo (m)", min_value=250, value=2000, step=250)

col1, col2 = st.columns(2)
categoria = col1.selectbox("Categoría", options=list(wbt_2000m.keys()))
tripulacion = col2.text_input("Tripulación")

col_min, col_sec = st.columns(2)
minutos = col_min.number_input("Minutos", min_value=0, value=12, step=1)
segundos = col_sec.number_input("Segundos", min_value=0.0, max_value=59.9, value=0.0, step=0.1)

if st.button("➕ Agregar a la lista"):
    # Cálculos
    tiempo_real_sec = (minutos * 60) + segundos
    tiempo_ideal = wbt_2000m[categoria] * (distancia / 2000.0)
    pronostico = (tiempo_ideal / tiempo_real_sec) * 100
    
    tiempo_formateado = f"{int(minutos):02d}:{segundos:04.1f}"
    
    # Crear el registro del nuevo bote
    nuevo_bote = pd.DataFrame([{
        'Categoría': categoria,
        'Tripulación': tripulacion,
        'Tiempo': tiempo_formateado,
        'Pronóstico (%)': pronostico
    }])
    
    # Sumarlo a la tabla temporal
    st.session_state.entrenamiento = pd.concat([st.session_state.entrenamiento, nuevo_bote], ignore_index=True)

## --- PANEL DE RESULTADOS ---
st.divider()
st.subheader(f"Resultados de la fecha: {fecha.strftime('%d/%m/%Y')}")

if not st.session_state.entrenamiento.empty:
    # ORDENAR de mayor a menor pronóstico y resetear el índice (0 será el 1°, 1 el 2°, etc.)
    df_ordenado = st.session_state.entrenamiento.sort_values(by='Pronóstico (%)', ascending=False).reset_index(drop=True)
    df_ordenado.index = df_ordenado.index + 1

    # Lógica de colores para el podio
    def resaltar_podio(row):
        if row.name == 1:
            return ['background-color: #FFD700; color: black; font-weight: bold'] * len(row) # Oro
        elif row.name == 2:
            return ['background-color: #C0C0C0; color: black; font-weight: bold'] * len(row) # Plata
        elif row.name == 3:
            return ['background-color: #CD7F32; color: black; font-weight: bold'] * len(row) # Bronce
        return [''] * len(row) # Resto sin color
    
    # Formateo visual
    df_vista = df_ordenado.copy()
    df_vista['Pronóstico (%)'] = df_vista['Pronóstico (%)'].apply(lambda x: f"{x:.2f}%")
    
    # Mostrar la tabla aplicando el estilo
    st.dataframe(df_vista.style.apply(resaltar_podio, axis=1), use_container_width=True)
    
    if st.button("🗑️ Limpiar tabla (Nuevo entrenamiento)"):
        st.session_state.entrenamiento = pd.DataFrame(columns=['Categoría', 'Tripulación', 'Tiempo', 'Pronóstico (%)'])
        st.rerun()
else:
    st.info("No hay botes cargados en este entrenamiento todavía.")
