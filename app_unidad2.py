import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# Configuración de la página
st.set_page_config(page_title="Simulador Animado Multi-Ordeñe", layout="wide")

# 1. DEFINICIÓN DE LAS PESTAÑAS PRINCIPALES
tab1, tab2 = st.tabs(["📊 Laboratorio de Ordeñe", "🔄 Conversión de Unidades (Ci ↔ Bq)"])

# =========================================================================
# PESTAÑA 1: SIMULADOR DEL GENERADOR (HISTORIAL, ANIMACIONES Y ALERTAS)
# =========================================================================
with tab1:
    st.title("🧪 Laboratorio Virtual: Ordeñe Animado Semanal ($^{99}\\mathrm{Mo}/^{99\\mathrm{m}}\\mathrm{Tc}$)")
    st.markdown("**Unidad Nº 2:** Producción de Radioisótopos y Radiofarmacia")
    st.write("Simulá de forma visual y animada la rutina de una sala de radiofarmacia realizando múltiples ordeñes a lo largo de la semana.")

    # Inicializar el historial de ordeñes y el último vial en la sesión
    if 'historial_eluciones' not in st.session_state:
        st.session_state.historial_eluciones = []
    if 'ultimo_vial' not in st.session_state:
        st.session_state.ultimo_vial = None
    if 'error_elucion' not in st.session_state:
        st.session_state.error_elucion = None

    # Parámetros en la barra lateral
    st.sidebar.header("⚙️ Configuración del Generador")
    A_mo0 = st.sidebar.number_input("Actividad inicial de Mo-99 (GBq):", min_value=10.0, value=100.0, step=10.0)

    st.sidebar.write("---")
    st.sidebar.subheader("🧼 Control de Operación")
    hora_lavado = st.sidebar.slider("Seleccionar hora para el próximo ordeñe:", min_value=1, max_value=168, value=24, step=1)

    # Constantes físicas reales (en horas)
    t_half_mo = 66.0   
    t_half_tc = 6.005  
    lam_mo = np.log(2) / t_half_mo
    lam_tc = np.log(2) / t_half_tc
    F = 0.86  

    # Cálculo vectorial para el gráfico (168 horas)
    horas = np.linspace(0, 168, 1500)
    act_mo = A_mo0 * np.exp(-lam_mo * horas)
    act_tc = np.zeros_like(horas)

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
            tc_inicio_tramo = 0 

        termino_bateman = (F * lam_tc * mo_inicio_tramo / (lam_tc - lam_mo))
        crecimiento = termino_bateman * (np.exp(-lam_mo * t_tramo) - np.exp(-lam_tc * t_tramo))
        act_tc[i] = crecimiento + tc_inicio_tramo * np.exp(-lam_tc * t_tramo)

    # Determinar estado actual para las barras según el slider
    eluciones_antes_slider = [e for e in st.session_state.historial_eluciones if e <= hora_lavado]
    if not eluciones_antes_slider:
        t_slider = hora_lavado
        mo_ini_slider = A_mo0
    else:
        t_slider = hora_lavado - max(eluciones_antes_slider)
        mo_ini_slider = A_mo0 * np.exp(-lam_mo * max(eluciones_antes_slider))

    act_mo_columna = A_mo0 * np.exp(-lam_mo * hora_lavado)
    act_tc_columna = (F * lam_tc * mo_ini_slider / (lam_tc - lam_mo)) * (np.exp(-lam_mo * t_slider) - np.exp(-lam_tc * t_slider))

    # Lógica del botón de elución
    if st.sidebar.button("🧼 REALIZAR ORDEÑE"):
        st.session_state.error_elucion = None
        
        if hora_lavado in st.session_state.historial_eluciones:
            st.session_state.error_elucion = f"⚠️ **ERROR DE OPERACIÓN:** El generador ya fue eluido en la hora {hora_lavado}. No se puede duplicar la elución en el mismo instante térmico."
        elif act_tc_columna < 0.1:
            st.session_state.error_elucion = "⚠️ **RESTRICCIÓN RADIOLÓGICA:** Rendimiento de elución insuficiente. La actividad acumulada de $^{99\\mathrm{m}}\\mathrm{Tc}$ disponible en la columna de alúmina no cumple con el umbral mínimo para extracción clínica. Permita un mayor tiempo de crecimiento radiológico."
        else:
            with st.spinner("⏳ Pasando solución salina... eluyendo la columna de alúmina..."):
                time.sleep(2.0)
            
            st.balloons()
            st.session_state.historial_eluciones.append(hora_lavado)
            st.session_state.historial_eluciones.sort()
            
            eluciones_antes = [e for e in st.session_state.historial_eluciones if e < hora_lavado]
            if not eluciones_antes:
                t_acum = hora_lavado
                mo_ini = A_mo0
            else:
                t_acum = hora_lavado - max(eluciones_antes)
                mo_ini = A_mo0 * np.exp(-lam_mo * max(eluciones_antes))
            
            gbq_extraidos = (F * lam_tc * mo_ini / (lam_tc - lam_mo)) * (np.exp(-lam_mo * t_acum) - np.exp(-lam_tc * t_acum))
            
            st.session_state.ultimo_vial = {
                "actividad": gbq_extraidos,
                "hora": hora_lavado
            }
            st.sidebar.success(f"¡Elución completada con éxito!")
            st.rerun()

    if st.sidebar.button("🔄 Reiniciar Generador"):
        st.session_state.historial_eluciones = []
        st.session_state.ultimo_vial = None
        st.session_state.error_elucion = None
        st.rerun()

    # Interfaz gráfica de la pestaña 1
    col_visual, col_grafico = st.columns([1, 1.2])

    with col_visual:
        st.subheader("🏢 Animación de la Columna")
        st.write(f"Estado interno de la columna a las **{hora_lavado} horas**:")
        
        st.write("🔴 **Actividad de Mo-99 (Padre fijo en alúmina):**")
        porcentaje_mo = min(100, int((act_mo_columna / A_mo0) * 100))
        st.progress(porcentaje_mo / 100, text=f"{act_mo_columna:.2f} GBq retenidos")
        
        st.write("---")
        st.write("🔵 **Actividad de Tc-99m (Hijo acumulado para extraer):**")
        porcentaje_tc = min(100, int((act_tc_columna / max(0.1, act_mo_columna)) * 100))
        st.progress(porcentaje_tc / 100)
        
        # Métrica gigante solicitada
        st.metric(label="Masa Radiactiva Disponible en Columna", value=f"{act_tc_columna:.2f} GBq")
        
        if st.session_state.error_elucion is not None:
            st.error(st.session_state.error_elucion)
        
        st.write("---")
        if st.session_state.ultimo_vial is not None:
            st.markdown("### 📦 Último Vial de Recogida Obtenido:")
            texto_vial = f"""
            🧪 **Contenido del Vial:** Pertecnetato de Sodio ($^{{99m}}\\mathrm{{TcO}}_4^-$)
            
            🔥 **Actividad Extraída:** **{st.session_state.ultimo_vial['actividad']:.2f} GBq**
            
            ⏱️ **Momento del lavado:** {st.session_state.ultimo_vial['hora']} hs del ciclo.
            """
            st.info(texto_vial)
            st.metric(label="✨ Eficiencia de extracción del lavado", value="100% (Teórica)")
        else:
            st.warning("El generador está cargado. Seleccioná una hora en el slider lateral y presioná 'Ordeñar' para extraer la actividad al vial.")

    with col_grafico:
        st.subheader("📈 Historial del Equilibrio Transitorio Semanal")
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.plot(horas, act_mo, label="$^{99}$Mo (Padre en columna)", color="red", lw=2.5)
        ax.plot(horas, act_tc, label="$^{99\\mathrm{m}}$Tc (Hijo)", color="blue", lw=2)
        
        for e in st.session_state.historial_eluciones:
            ax.axvline(e, color="green", linestyle=":", lw=2, label="Elución realizada" if e == st.session_state.historial_eluciones[0] else "")
        
        ax.axvline(hora_lavado, color="orange", linestyle="--", lw=1.5, label=f"Línea de tiempo actual ({hora_lavado}h)")
        ax.set_xlabel("Tiempo acumulado de la semana (horas)")
        ax.set_ylabel("Actividad en la columna (GBq)")
        ax.set_xlim(0, 168)
        ax.legend(loc="upper right")
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
        
        if st.session_state.historial_eluciones:
            st.write("**Historial de ordeñes guardados:** " + ", ".join([f"{e}h" for e in st.session_state.historial_eluciones]))

# =========================================================================
# PESTAÑA 2: CALCULADORA DE CONVERSIÓN DE UNIDADES (CI <-> BQ)
# =========================================================================
with tab2:
    st.header("🔄 Calculadora de Equivalencias Radioactivas")
    st.write(
        "Herramienta de soporte para la resolución de la **Actividad 2**. "
        "Permite interactuar entre las unidades del Sistema Internacional (SI) exigidas por la ARN y el sistema tradicional."
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("De Histórico (Ci/mCi) a SI (Bq/MBq/GBq)")
        val_mci = st.number_input("Ingresá la actividad en milicuries (mCi):", min_value=0.0, value=10.0, step=1.0, key="mci_in")
        
        mbq_result = val_mci * 37.0
        gbq_result = mbq_result / 1000.0
        ci_equivalent = val_mci / 1000.0
        
        st.metric(label="Equivalencia en Megabecquerels (MBq)", value=f"{mbq_result:,.2f} MBq")
        st.metric(label="Equivalencia en Gigabecquerels (GBq)", value=f"{gbq_result:,.4f} GBq")
        st.caption(f"Equivale también a {ci_equivalent:.3f} Ci")

    with col2:
        st.subheader("De SI (Bq/MBq/GBq) a Histórico (Ci/mCi)")
        val_gbq = st.number_input("Ingresá la actividad en Gigabecquereles (GBq):", min_value=0.0, value=1.0, step=0.1, key="gbq_in")
        
        ci_result = val_gbq / 37.0
        mci_result = ci_result * 1000.0
        
        st.metric(label="Equivalencia en Curíes (Ci)", value=f"{ci_result:,.4f} Ci")
        st.metric(label="Equivalencia en Milicuries (mCi)", value=f"{mci_result:,.2f} mCi")

    st.markdown("---")
    st.info(
        "💡 **Recordatorio de Guardia:** \n\n"
        "* $1 \\text{ Ci} = 37 \\text{ GBq} = 37.000 \\text{ MBq}$\n"
        "* $1 \\text{ mCi} = 37 \\text{ MBq}$\n\n"
        "La ARN exige el reporte en Becquerels debido a su correspondencia directa con la tasa de desintegración por segundo ($1 \\text{ Bq} = 1 \\text{ desintegración/s}$)."
    )
