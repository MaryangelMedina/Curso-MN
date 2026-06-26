import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(page_title="Lab Virtual: Radioactividad Clínica", layout="wide")

st.title("🧪 Laboratorio Virtual: Radiactividad y Logística de Radiofármacos")
st.write("Herramienta interactiva para la gestión de dosis y simulación de generadores en Medicina Nuclear.")

# Creamos las dos pestañas basadas en tus ideas favoritas
tab1, tab2 = st.tabs(["📋 Idea 1: Turnero Clínico (Decaimiento)", "🐐 Idea 2: Ordeño del Generador (99Mo/99mTc)"])

# ==========================================
# PESTAÑA 1: EL TURNERO CLÍNICO
# ==========================================
with tab1:
    st.header("📋 Gestión de Dosis y Decaimiento en la Sala de Espera")
    st.write("Simulá el impacto del retraso de un paciente en la actividad real del radiofármaco antes de la inyección.")

    # Datos de radionucleidos médicos reales (T1/2 en minutos)
    isoto_datos = {
        "Flúor-18 (18F) - [PET]": {"t12": 109.7, "uso": "Marcación de FDG para PET/CT metabólico."},
        "Tecnecio-99m (99mTc) - [SPECT]": {"t12": 360.0, "uso": "Centellogramas óseos, cardíacos y SPECT general."},
        "Carbono-11 (11C) - [PET]": {"t12": 20.3, "uso": "Estudios neurológicos específicos y oncología rápida."},
        "Yodo-131 (131I) - [Terapia]": {"t12": 11520.0, "uso": "Tratamiento de cáncer de tiroides e hipertiroidismo."}
    }

    col_izq, col_der = st.columns([1, 2])

    with col_izq:
        st.subheader("⚙️ Configuración de la Dosis")
        seleccion = st.selectbox("Seleccione el Radionucleido:", list(isoto_datos.keys()))
        
        t12 = isoto_datos[seleccion]["t12"]
        st.info(f"**T_1/2:** {t12} min. | **Uso:** {isoto_datos[seleccion]['uso']}")

        actividad_inicial = st.number_input("Actividad Calibrada Inicial (mCi):", min_value=0.1, value=10.0, step=0.5, key="act_init")
        tiempo_transcurrido = st.slider("Tiempo de retraso del paciente (minutos):", min_value=0, max_value=int(t12 * 3), value=int(t12 / 2), key="time_slider")

    # Cálculos físicos usando las fórmulas del PDF de Alejandro Condori
    lambda_rad = np.log(2) / t12
    actividad_final = actividad_inicial * np.exp(-lambda_rad * tiempo_transcurrido)
    porcentaje_remanente = (actividad_final / actividad_inicial) * 100

    with col_der:
        # Métricas hospitalarias
        m1, m2, m3 = st.columns(3)
        m1.metric("Actividad Inicial", f"{actividad_inicial:.2f} mCi")
        m2.metric("Retraso", f"{tiempo_transcurrido} min")
        m3.metric("Actividad al Inyectar", f"{actividad_final:.2f} mCi", delta=f"-{(actividad_inicial - actividad_final):.2f} mCi", delta_color="inverse")

        # Gráfico de decaimiento
        t_eje = np.linspace(0, int(t12 * 3), 500)
        a_eje = actividad_inicial * np.exp(-lambda_rad * t_eje)

        fig1, ax1 = plt.subplots(figsize=(8, 3.5))
        ax1.plot(t_eje, a_eje, color="#ff4b4b", linewidth=2, label="Curva de Decaimiento")
        ax1.scatter(tiempo_transcurrido, actividad_final, color="#1f77b4", s=120, zorder=5, label="Inyección")
        ax1.axhline(actividad_final, color="gray", linestyle="--", alpha=0.5)
        ax1.axvline(tiempo_transcurrido, color="gray", linestyle="--", alpha=0.5)
        ax1.set_xlabel("Tiempo (minutos)")
        ax1.set_ylabel("Actividad (mCi)")
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        st.pyplot(fig1)

        if porcentaje_remanente < 25:
            st.error(f"⚠️ **ALERTA CLÍNICA:** La dosis cayó al {porcentaje_remanente:.1f}%. La estadística de conteo en el tomógrafo será baja. Ajuste tiempos de adquisición.")
        else:
            st.success(f"✅ **Dosis Óptima:** Conserva el {porcentaje_remanente:.1f}% de la actividad original.")

# ==========================================
# PESTAÑA 2: EL ORDEÑO DEL GENERADOR
# ==========================================
with tab2:
    st.header("🐐 Simulación del Generador de Molibdeno-99 / Tecnecio-99m")
    st.write("El Tecnecio-99m se produce por el decaimiento del Molibdeno-99. Simulá el proceso de elución ('ordeño') y analizá el equilibrio transitorio.")

    # Parámetros físicos reales (en horas)
    t12_Mo = 66.0   # Molibdeno-99
    t12_Tc = 6.0    # Tecnecio-99m
    lambda_Mo = np.log(2) / t12_Mo
    lambda_Tc = np.log(2) / t12_Tc

    # Inicializar estado para guardar las eluciones en la sesión de Streamlit
    if 'hora_elucion' Novelty in st.session_state:
        st.session_state.hora_elucion = []

    col_izq2, col_der2 = st.columns([1, 2])

    with col_izq2:
        st.subheader("⏳ Control de Radiofarmacia")
        actividad_Mo0 = st.number_input("Actividad inicial de 99Mo en la columna (mCi):", min_value=100, value=1000, step=100)
        
        st.write("---")
        st.write("🤖 **Acción de Radiofarmacia:**")
        hora_actual_elucion = st.slider("Hora del día para realizar la elución:", min_value=0, max_value=72, value=24)
        
        if st.button("🧼 Realizar Elución (Ordeñar 99mTc)"):
            if hora_actual_elucion not in st.session_state.hora_elucion:
                st.session_state.hora_elucion.append(hora_actual_elucion)
                st.session_state.hora_elucion.sort()
                st.success(f"¡Generador eluido a las {hora_actual_elucion} hs!")

        if st.button("🔄 Reiniciar Generador"):
            st.session_state.hora_elucion = []
            st.rerun()

    with col_der2:
        # Cálculo de las curvas considerando las eluciones
        horas = np.linspace(0, 72, 1000)
        act_Mo = actividad_Mo0 * np.exp(-lambda_Mo * horas)
        
        # Ecuación de Bateman modificada por las eluciones puntuales
        act_Tc = np.zeros_like(horas)
        factor_rendimiento = 0.86  # Fracción de decaimiento de Mo a Tc-99m

        for i, h in enumerate(horas):
            # Buscar la última elución ocurrida antes de la hora 'h'
            eluciones_previas = [e for e in st.session_state.hora_elucion if e <= h]
            
            if not eluciones_previas:
                # Crecimiento estándar desde el inicio (t=0)
                t_desde_elucion = h
                Tc_inicial = 0
                Mo_inicial = actividad_Mo0
            else:
                # Crecimiento desde la última elución
                ultima_e = max(eluciones_previas)
                t_desde_elucion = h - ultima_e
                Tc_inicial = 0  # Suponemos eficiencia de elución del 100%
                Mo_inicial = actividad_Mo0 * np.exp(-lambda_Mo * ultima_e)

            # Ecuación de equilibrio transitorio
            termino_Mo = (factor_rendimiento * lambda_Tc * Mo_inicial) / (lambda_Tc - lambda_Mo)
            crecimiento = termino_Mo * (np.exp(-lambda_Mo * t_desde_elucion) - np.exp(-lambda_Tc * t_desde_elucion))
            decaimiento_Tc_libre = Tc_inicial * np.exp(-lambda_Tc * t_desde_elucion)
            act_Tc[i] = crecimiento + decaimiento_Tc_libre

        # Graficar las curvas de equilibrio transitorio
        fig2, ax2 = plt.subplots(figsize=(8, 3.5))
        ax2.plot(horas, act_Mo, color="#1f77b4", label="Actividad 99Mo (Madre)", linewidth=2)
        ax2.plot(horas, act_Tc, color="#ff7f0e", label="Actividad 99mTc (Hija)", linewidth=2, linestyle="--")
        
        # Dibujar líneas verticales en cada ordeño
        for e in st.session_state.hora_elucion:
            ax2.axvline(e, color="green", linestyle=":", alpha=0.8, label="Elución (Ordeño)" if e == st.session_state.hora_elucion[0] else "")

        ax2.set_xlabel("Tiempo acumulado (Horas)")
        ax2.set_ylabel("Actividad (mCi)")
        ax2.set_title("Dinámica del Generador y Equilibrio Transitorio")
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        st.pyplot(fig2)
        st.caption("Física aplicada: Observá cómo el Tecnecio (Hija) tarda unas 22-24 horas en alcanzar su máxima actividad acumulada nuevamente tras cada ordeño.")
