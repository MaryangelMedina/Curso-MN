import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Laboratorio Virtual: Decaimiento", layout="wide")

st.title("🧪 Laboratorio Virtual: Leyes de Decaimiento")
st.markdown(f"**Unidad 3:** Dr. Roberto Isoardi")

# --- SIDEBAR: Parámetros de Entrada ---
st.sidebar.header("⚙️ Configuración de la Fuente")
isótopo = st.sidebar.selectbox("Seleccionar Isótopo", ["F-18", "Tc-99m", "I-131", "C-11", "Personalizado"])

if isótopo == "F-18": t_half = 109.7 / 60  # horas
elif isótopo == "Tc-99m": t_half = 6.01
elif isótopo == "I-131": t_half = 192.48 # 8.02 días * 24
elif isótopo == "C-11": t_half = 20.3 / 60
else: t_half = st.sidebar.number_input("T 1/2 (horas)", value=1.0)

a0 = st.sidebar.number_input("Actividad Inicial (A0) en MBq", value=100.0)
tiempo_max = st.sidebar.slider("Tiempo de observación (horas)", 1, 48, 12)

# --- CÁLCULOS MATEMÁTICOS ---
lam = np.log(2) / t_half
tau = 1 / lam

# Generar datos para la curva
t = np.linspace(0, tiempo_max, 100)
at = a0 * np.exp(-lam * t)

# --- LAYOUT PRINCIPAL ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Resultados de la Fuente")
    st.write(f"**Constante de decaimiento (λ):** `{lam:.4f} h⁻¹`")
    st.write(f"**Vida Media (τ):** `{tau:.2f} horas`")
    st.write(f"**Actividad a las {tiempo_max}h:** `{a0 * np.exp(-lam * tiempo_max):.2f} MBq`")
    
    st.info("💡 **Método Gráfico:** Observa cómo en el gráfico semilogarítmico (pestaña 2), la curva se vuelve una línea recta.")

with col2:
    st.subheader("🔄 Conversor de Unidades")
    val_bq = st.number_input("Convertir MBq a Ci", value=100.0)
    st.write(f"{val_bq} MBq = **{val_bq * 0.027:.4f} mCi**")
    st.write(f"*(Equivalencia: 1 Ci = 37 GBq)*")

# --- GRÁFICOS ---
tab1, tab2 = st.tabs(["Curva de Decaimiento", "Gráfico Semilogarítmico"])

with tab1:
    fig, ax = plt.subplots()
    ax.plot(t, at, color='red', lw=2)
    ax.set_xlabel("Tiempo (horas)")
    ax.set_ylabel("Actividad (MBq)")
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)

with tab2:
    fig2, ax2 = plt.subplots()
    ax2.semilogy(t, at, color='blue', lw=2)
    ax2.set_xlabel("Tiempo (horas)")
    ax2.set_ylabel("Log Actividad (MBq)")
    ax2.grid(True, which="both", alpha=0.3)
    st.pyplot(fig2)

# --- EFICIENCIA DE MEDICIÓN ---
st.divider()
st.subheader("⏱️ Cálculo de Eficiencia ($\epsilon$)")
counts = st.number_input("Cuentas medidas (CPM)", value=5000)
st.write(f"Si la actividad real es de {a0} MBq, la eficiencia es mínima. Este módulo ayuda a calcular la relación entre cuentas detectadas y desintegraciones reales.")
