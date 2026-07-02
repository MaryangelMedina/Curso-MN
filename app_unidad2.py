import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# Configuración de la página
st.set_page_config(page_title="Simulador Multi-Ordeñe de Generador", layout="wide")

st.title("🧪 Laboratorio Virtual: Dinámica del Generador y Multi-Ordeñe ($^{99}\mathrm{Mo}/^{99\mathrm{m}}\mathrm{Tc}$)")
st.markdown("**Unidad Nº 2:** Producción de Radioisótopos y Radiofarmacia")
st.write("Simulá el comportamiento del generador a lo largo de una semana completa realizando múltiples eluciones consecutivas.")

# --- INICIALIZAR EL HISTORIAL DE ORDEÑES EN LA SESIÓN ---
if 'historial_eluciones' not in st.session_state:
    st.session_state.historial_eluciones = []

# --- PARÁMETROS EN LA BARRA LATERAL ---
st.sidebar.header("⚙️ Configuración del Generador")
A_mo0 = st.sidebar.number_input("Actividad inicial de Mo-99 (GBq):", min_value=10.0, value=100.0, step=10.0)

st.sidebar.write("---")
st.sidebar.subheader("🧼 Control de Eluciones")
hora_lavado = st.sidebar.slider("Seleccionar hora para el próximo ordeñe:", min_value=1, max_value=168, value=24, step=1)

col_btn1, col_btn2 = st.sidebar.columns(2)
with col_btn1:
    if st.sidebar.button("🧼 Ordeñar"):
        if hora_lavado not in st.session_state.historial_eluciones:
            st.session_state.historial_eluciones.append(hora_lavado)
            st.session_state.historial_eluciones.sort()
            st.toast(f"¡Generador eluido a las {hora_lavado} hs!", icon="🧼")
with col_btn2:
    if st.sidebar.button("🔄 Reiniciar"):
        st.session_state.historial_eluciones = []
        st.rerun()

# Constantes físicas reales (en horas)
t_half_mo = 66.0   
t_half_tc = 6.005  
lam_mo = np.log(2) / t_half_mo
lam_tc = np.log(2) / t_half_tc
F = 0.86  

# --- CÁLCULO VECTORIAL PARA 1 SEMANA (168 HORAS) ---
horas = np.linspace(0, 168, 1500)
act_mo = A_mo0 * np.exp(-lam_mo * horas)
act_tc = np.zeros_like(horas)

# Ecuación de Bateman tramo por tramo según el historial de eluciones
for i, h in enumerate(horas):
    eluciones_previas = [e for e in st.session_state.historial_eluciones if e <= h]
    
    if not eluciones_previas:
        t_tramo = h
        mo_inicio_tramo = A_mo0
        tc_inicio_tramo = 0
    else:
        ultima_elucion = max(eluciones_previas)
        t_tramo = h - ultima_elucion
        mo_inicio_tramo = A_mo0 * np.exp(-lam_mo * ultima_elucion)
        tc_inicio_tramo = 0 # Asumimos eficiencia del 100% (cae a cero en el lavado)

    # Componente de producción exponencial
    termino_bateman = (F * lam_tc * mo_inicio_tramo / (lam_tc - lam_mo))
    crecimiento = termino_bateman * (np.exp(-lam_mo * t_tramo) - np.exp(-lam_tc * t_tramo))
    decaimiento_remanente = tc_inicio_tramo * np.exp(-lam_tc * t_tramo)
    
    act_tc[i] = crecimiento + decaimiento_remanente

# --- INTERFAZ GRÁFICA ---
col_izq, col_der = st.columns([1, 2.5])

with col_izq:
    st.subheader("📋 Estado Actual")
    if st.session_state.historial_eluciones:
        st.write("**Ordeñes realizados (horas del ciclo):**")
        st.info(", ".join([f"{e}h" for e in st.session_state.historial_eluciones]))
        
        # Calcular los GBq del último ordeñe realizado
        ultima = max(st.session_state.historial_eluciones)
        eluciones_antes = [e for e in st.session_state.historial_eluciones if e < ultima]
        if not eluciones_antes:
            t_acum = ultima
            mo_ini = A_mo0
        else:
            t_acum = ultima - max(eluciones_antes)
            mo_ini = A_mo0 * np.exp(-lam_mo * max(eluciones_antes))
        
        gbq_extraidos = (F * lam_tc * mo_ini / (lam_tc - lam_mo)) * (np.exp(-lam_mo * t_acum) - np.exp(-lam_tc * t_acum))
        st.metric(label="🔥 Actividad extraída en último ordeñe", value=f"{gbq_extraidos:.2f} GBq")
    else:
        st.warning("Aún no realizaste ningún ordeñe. El Tecnecio seguirá acumulándose hasta entrar en equilibrio transitorio con el Molibdeno.")
    
    st.write("---")
    st.markdown("""
    💡 **Consigna Práctica Asincrónica:**
    1. Simulá una rutina típica de servicio: Realizá un ordeñe cada 24 horas (horas 24, 48, 72, 96...).
    2. Analizá el gráfico de la derecha: Observá cómo los picos de azul ($^{99\mathrm{m}}\mathrm{Tc}$) son cada vez más chicos. Esto demuestra visualmente el impacto del decaimiento del padre ($^{99}\mathrm{Mo}$) en la productividad semanal del radionucleido.
    """)

with col_der:
    st.subheader("📈 Curva de Eluciones Múltiples (Ciclo de 7 días)")
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(horas, act_mo, label="$^{99}$Mo (Padre en columna)", color="red", lw=2.5)
    ax.plot(horas, act_tc, label="$^{99\mathrm{m}}$Tc (Hijo eluido/creciendo)", color="blue", lw=2)
    
    # Dibujar líneas discontinuas verticales por cada lavado realizado
    for e in st.session_state.historial_eluciones:
        ax.axvline(e, color="green", linestyle=":", alpha=0.7, lw=2)
        
    ax.set_xlabel("Tiempo acumulado de la semana (horas)")
    ax.set_ylabel("Actividad en la columna (GBq)")
    ax.set_xlim(0, 168)
    ax.legend(loc="upper right")
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
