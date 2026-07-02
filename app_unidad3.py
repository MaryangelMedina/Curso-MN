import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(page_title="Lab Virtual: Leyes de Decaimiento", layout="wide")

st.title("🧪 Laboratorio Virtual: Leyes de Decaimiento Radiactivo")
st.markdown("**Unidad Nº 3:** Disertante: Dr. Roberto Isoardi")
st.write("Simulación interactiva de la velocidad de desintegración y cálculo de la actividad en función del tiempo.")

# Datos de radionucleidos médicos reales (T1/2 en minutos)
isoto_datos = {
    "Flúor-18 (18F)": {"t12": 109.7, "uso": "Marcación de FDG para PET/CT metabólico."},
    "Tecnecio-99m (99mTc)": {"t12": 360.0, "uso": "Centellogramas óseos, cardíacos y SPECT general."},
    "Carbono-11 (11C)": {"t12": 20.3, "uso": "Estudios neurológicos específicos y oncología rápida."},
    "Yodo-131 (131I)": {"t12": 11520.0, "uso": "Tratamiento de cáncer de tiroides e hipertiroidismo."}
}

col_izq, col_der = st.columns([1, 2])

with col_izq:
    st.subheader("⚙️ Configuración de la Fuente")
    seleccion = st.selectbox("Seleccione el Radionucleido:", list(isoto_datos.keys()))
    
    t12 = isoto_datos[seleccion]["t12"]
    st.info(f"**Período de semidesintegración ($T_{{1/2}}$):** {t12} min. | **Uso:** {isoto_datos[seleccion]['uso']}")

    actividad_inicial = st.number_input("Actividad Inicial ($A_0$) en mCi:", min_value=0.1, value=10.0, step=0.5)
    tiempo_transcurrido = st.slider("Tiempo transcurrido / Retraso ($t$ en minutos):", min_value=0, max_value=int(t12 * 3), value=int(t12 / 2))

# Cálculos físicos fundamentales
lambda_rad = np.log(2) / t12
vida_media = 1 / lambda_rad
actividad_final = actividad_inicial * np.exp(-lambda_rad * tiempo_transcurrido)
porcentaje_remanente = (actividad_final / actividad_inicial) * 100

with col_der:
    st.subheader("📊 Parámetros Matemáticos Calculados")
    
    # Métricas principales
    m1, m2, m3 = st.columns(3)
    m1.metric("Constante de decaimiento ($\lambda$)", f"{lambda_rad:.5f} min⁻¹")
    m2.metric("Vida Media ($\\tau$)", f"{vida_media:.1f} min")
    m3.metric("Actividad Final $A(t)$", f"{actividad_final:.2f} mCi")

    # Conversión de unidades solicitada por el programa
    st.write("---")
    st.markdown("**🔄 Equivalencia de Unidades en el Sistema Internacional:**")
    act_bq = actividad_final * 37  # 1 mCi = 37 MBq
    st.write(f"La actividad remanente de **{actividad_final:.2f} mCi** equivale a **{act_bq:.2f} MBq** (Becquerel).")

    # Gráfico de decaimiento exponencial
    t_eje = np.linspace(0, int(t12 * 3), 500)
    a_eje = actividad_inicial * np.exp(-lambda_rad * t_eje)

    fig1, ax1 = plt.subplots(figsize=(8, 3.8))
    ax1.plot(t_eje, a_eje, color="#ff4b4b", linewidth=2, label="Curva Exponencial $A(t) = A_0 \\cdot e^{-\\lambda t}$")
    ax1.scatter(tiempo_transcurrido, actividad_final, color="#1f77b4", s=120, zorder=5, label="Punto de Medición")
    ax1.axhline(actividad_final, color="gray", linestyle="--", alpha=0.5)
    ax1.axvline(tiempo_transcurrido, color="gray", linestyle="--", alpha=0.5)
    ax1.set_xlabel("Tiempo (minutos)")
    ax1.set_ylabel("Actividad (mCi)")
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    st.pyplot(fig1)
