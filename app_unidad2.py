import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# Configuración de la página
st.set_page_config(page_title="Simulador Animado de Generador", layout="wide")

st.title("🧪 Laboratorio Virtual: Ordeñe Animado del Generador $^{99}\\text{Mo}/^{99\\text{m}}\\text{Tc}$")
st.markdown("**Unidad Nº 2:** Producción de Radioisótopos y Radiofarmacia")
st.write("Simulación visual del proceso de elución en la columna de alúmina y el principio del equilibrio transitorio.")

# --- PARÁMETROS EN LA BARRA LATERAL ---
st.sidebar.header("⚙️ Configuración del Generador")
A_mo0 = st.sidebar.number_input("Actividad inicial de Mo-99 cargada (GBq):", min_value=10.0, value=100.0, step=10.0)
tiempo_acumulado = st.sidebar.slider("Tiempo de crecimiento antes del ordeñe (horas):", 4, 72, 24)

# Constantes físicas reales
t_half_mo = 66.0   # Mo-99 en horas
t_half_tc = 6.005  # Tc-99m en horas
lam_mo = np.log(2) / t_half_mo
lam_tc = np.log(2) / t_half_tc
F = 0.86  # Fracción de decaimiento útil

# --- CÁLCULO DE ACTIVIDADES ---
# Actividad justo antes de eluir (Ecuación de Bateman)
act_mo_antes = A_mo0 * np.exp(-lam_mo * tiempo_acumulado)
act_tc_antes = (F * lam_tc * A_mo0 / (lam_tc - lam_mo)) * (np.exp(-lam_mo * tiempo_acumulado) - np.exp(-lam_tc * tiempo_acumulado))

# --- INTERFAZ VISUAL: EL GENERADOR EN EL LABORATORIO ---
col_visual, col_grafico = st.columns([1, 1.2])

with col_visual:
    st.subheader("🏢 Animación de la Columna del Generador")
    st.write(f"Estado de la columna tras **{tiempo_acumulado} horas** de acumulación:")
    
    # Simulación visual de la carga de la columna
    st.write("🔴 **Actividad de Mo-99 (Padre retenido en la alúmina):**")
    porcentaje_mo = min(100, int((act_mo_antes / A_mo0) * 100))
    st.progress(porcentaje_mo / 100, text=f"{act_mo_antes:.2f} GBq restantes")
    
    st.write("🔵 **Actividad de Tc-99m (Hijo acumulado listo para extraer):**")
    # El máximo teórico alcanzable es cercano al Mo, usamos eso como escala de la barra
    porcentaje_tc = min(100, int((act_tc_antes / act_mo_antes) * 100))
    st.progress(porcentaje_tc / 100, text=f"{act_tc_antes:.2f} GBq disponibles")
    
    st.write("---")
    st.markdown("### 🤖 Operación de Radiofarmacia")
    st.write("Presioná el botón para pasar la solución salina por la columna y extraer el Tc-99m hacia el vial vacío.")
    
    # BOTÓN ANIMADO CON SPINNER Y CELEBRACIÓN
    if st.button("🧼 REALIZAR ELUCCIÓN (ORDEÑAR GENERADOR)"):
        with st.spinner("⏳ Pasando solución salina por la columna de alúmina... arrastrando el Pertecnetato..."):
            time.sleep(2.5) # Pausa dramática para simular el goteo real
        
        st.balloons() # Animación gráfica de festejo en pantalla
        st.success(f"¡Elución completada con éxito!")
        
        # El Vial Blindado de salida
        st.markdown("### 📦 Vial de Recogida Obtenido:")
        st.info(f"🧪 **Contenido del Vial:** Pertecnetato de Sodio ($^{99\\text{m}}\\text{Tc}O_4^-$)\n\n"
                f"🔥 **Actividad Extraída:** **{act_tc_antes:.2f} GBq**\n\n"
                f"⏱️ **Hora del proceso:** {tiempo_acumulado} hs desde la carga.")
        
        st.metric(label="✨ Eficiencia de extracción teórica", value="95% - 100%")

with col_grafico:
    st.subheader("📈 Gráfico de Equilibrio Transitorio")
    st.write("Observá cómo se intersectan las curvas en el punto máximo de crecimiento:")
    
    # Generar vectores para la gráfica antes del lavado
    t = np.linspace(0, 96, 500)
    A_mo_graf = A_mo0 * np.exp(-lam_mo * t)
    A_tc_graf = (F * lam_tc * A_mo0 / (lam_tc - lam_mo)) * (np.exp(-lam_mo * t) - np.exp(-lam_tc * t))
    
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(t, A_mo_graf, label="$^{99}$Mo (Padre retenido)", color="red", lw=2.5)
    ax.plot(t, A_tc_graf, label="$^{99\\text{m}}$Tc (Hijo libre)", color="blue", lw=2.5, linestyle="--")
    
    # Línea que marca dónde decidió eluir el alumno
    ax.axvline(x=tiempo_acumulado, color="green", linestyle=":", lw=2, label=f"Tu elución ({tiempo_acumulado} hs)")
    ax.scatter(tiempo_acumulado, act_tc_antes, color="green", s=100, zorder=5)
    
    ax.set_xlabel("Tiempo acumulado (horas)")
    ax.set_ylabel("Actividad (GBq)")
    ax.legend(loc="upper right")
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    
    st.info("💡 **Guía de análisis:** Si movés el control de la izquierda a las **23-24 horas**, vas a ver que el hijo llega a su punto máximo (Equilibrio Transitorio). Lavar antes de ese tiempo implica sacar menos actividad; esperar mucho más significa perder decaimiento del padre de forma innecesaria.")
