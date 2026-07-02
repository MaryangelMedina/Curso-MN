import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulador de Generador Mo-99/Tc-99m", layout="wide")

st.title("🧪 Laboratorio Virtual: Dinámica del Generador $^{99}\\text{Mo}/^{99\\text{m}}\\text{Tc}$")
st.markdown("**Unidad 2:** Producción de Radioisótopos y Radiofarmacia")

# --- PARÁMETROS ---
st.sidebar.header("⚙️ Configuración del Generador")
A_mo0 = st.sidebar.number_input("Actividad inicial de Mo-99 (GBq)", value=100.0)
tiempo_elucion = st.sidebar.slider("Momento de la elución / lavado (horas)", 12, 72, 24)

# Constantes físicas
t_half_mo = 66.0   # Mo-99 en horas
t_half_tc = 6.005  # Tc-99m en horas

lam_mo = np.log(2) / t_half_mo
lam_tc = np.log(2) / t_half_tc
F = 0.86  # Fracción de decaimiento de Mo-99 que va a Tc-99m

# --- CÁLCULO DE CURVAS ---
# Fase 1: Crecimiento hasta la elución
t1 = np.linspace(0, tiempo_elucion, 200)
A_mo1 = A_mo0 * np.exp(-lam_mo * t1)
# Ecuación de Bateman para el hijo
A_tc1 = (F * lam_tc * A_mo0 / (lam_tc - lam_mo)) * (np.exp(-lam_mo * t1) - np.exp(-lam_tc * t1))

# Fase 2: Después de la elución (elución al 100% de eficiencia para simplificar)
t2 = np.linspace(tiempo_elucion, 96, 200)
A_mo2 = A_mo0 * np.exp(-lam_mo * t2)

# El Mo-99 sigue igual, pero el Tc-99m cae a cero en t=tiempo_elucion y vuelve a crecer
A_mo_en_elucion = A_mo0 * np.exp(-lam_mo * tiempo_elucion)
A_tc2 = (F * lam_tc * A_mo_en_elucion / (lam_tc - lam_mo)) * (np.exp(-lam_mo * (t2 - tiempo_elucion)) - np.exp(-lam_tc * (t2 - tiempo_elucion)))

# Unir vectores para graficar
t_total = np.concatenate((t1, t2))
A_mo_total = np.concatenate((A_mo1, A_mo2))
A_tc_total = np.concatenate((A_tc1, A_tc2))

# --- INTERFAZ ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📊 Estado del Generador")
    st.metric(label="Actividad de Mo-99 al lavar", value=f"{A_mo_en_elucion:.2f} GBq")
    st.metric(label="Tc-99m extraído (Teórico)", value=f"{(F * lam_tc * A_mo0 / (lam_tc - lam_mo)) * (np.exp(-lam_mo * tiempo_elucion) - np.exp(-lam_tc * tiempo_elucion)):.2f} GBq")
    
    st.info("💡 **Análisis asincrónico:** Observá cómo tras la elución, el Tc-99m tarda aproximadamente 24 horas en alcanzar su máximo crecimiento (Equilibrio Transitorio) antes de empezar a decaer al ritmo del padre.")

with col2:
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(t_total, A_mo_total, label="$^{99}$Mo (Padre)", color="red", lw=2)
    ax.plot(t_total, A_tc_total, label="$^{99\\text{m}}$Tc (Hijo)", color="blue", lw=2)
    ax.axvline(x=tiempo_elucion, color="green", linestyle="--", label="Elución (Lavado)")
    
    ax.set_xlabel("Tiempo (horas)")
    ax.set_ylabel("Actividad (GBq)")
    ax.set_title("Curva de Crecimiento y Decaimiento en el Generador")
    ax.legend()
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
