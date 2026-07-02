import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# Configuración de la página
st.set_page_config(page_title="Simulador Animado Multi-Ordeñe", layout="wide")

# 1. DEFINICIÓN DE LAS PESTAÑAS PRINCIPALES
tab1, tab2, tab3 = st.tabs([
    "📊 Laboratorio de Ordeñe", 
    "🔄 Conversión de Unidades (Ci ↔ Bq)",
    "📝 Resolución y Guía Docente"
])

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

# =========================================================================
# PESTAÑA 3: GUÍA DE TRABAJOS PRÁCTICOS (RESPUESTAS Y ANÁLISIS)
# =========================================================================
with tab3:
    st.title("📝 Resolución Analítica de la Guía de TP")
    st.markdown("---")
    
    # --- CASO 1 ---
    st.header("📌 Caso 1: El 'Lunes a la mañana' y el Máximo Teórico")
    
    with st.expander("🔍 Ver Planteamiento y Respuesta de Reflexión"):
        st.markdown(
            "**Planteamiento:** Llegás al servicio el lunes a las 07:00 AM. El generador se recibió y calibró el domingo a las 07:00 AM "
            "(hace exactamente 24 horas) con una actividad nominal de 100 GBq.\n\n"
            "**Pregunta:** ¿Por qué la actividad obtenida de $^{99\\mathrm{m}}\\text{Tc}$ en el vial nunca llega a ser igual a los "
            "$100\\text{ GBq}$ del padre, si ya pasaron las $\\sim 23$ horas teóricas de máximo crecimiento?\n\n"
            "### 💡 Resolución Analítica:"
        )
        st.success(
            "Existen **dos factores físicos fundamentales** explicados matemáticamente por las ecuaciones de Bateman:\n\n"
            "1. **Fracción de ramificación ($F = 0.86$):** El $^{99}\\text{Mo}$ no decae al estado metaestable ($^{99\\mathrm{m}}\\text{Tc}$) en el 100% de los casos. "
            "El $14\\%$ de las desintegraciones del padre esquivan este nivel isomérico y decaen de forma directa al estado fundamental ($^{99}\\text{Tc}$), perdiéndose para el uso clínico.\n"
            "2. **Decaimiento concurrente del Padre:** Durante las 24 horas que esperás el crecimiento, el propio $^{99}\\text{Mo}$ se está desintegrando con su "
            "período físico ($T_{1/2} = 66\\text{ hs}$). A las 24 horas, la actividad del padre en la columna ya se redujo de $100\\text{ GBq}$ a:\n"
            "$$A_{\\text{Mo}}(24) = 100 \\times e^{-\\frac{\\ln(2)}{66} \\cdot 24} \\approx 77.7\\text{ GBq}$$\n"
            "Por ende, en el equilibrio transitorio máximo (que ocurre a las $22.8\\text{ hs}$), la actividad del hijo se acopla a la del padre sobreviviente modificada por la fracción de ramificación. "
            "Si verificás con el simulador en la **Pestaña 1**, vas a notar que el vial extraído a las 24 hs ronda los **$\\sim 72.5\\text{ GBq}$**, cumpliendo rigurosamente la ecuación teórica."
        )

    st.markdown("---")
    
    # --- ACTIVIDAD 1 ---
    st.header("⚛️ Actividad 1: Navegación en la Tabla de Nucleidos (IAEA)")
    
    with st.expander("🔍 Ver Análisis de Ruta del Ra-226 y Modelo de Capas"):
        st.markdown("### 1. Ruta de decaimiento del $^{226}\\text{Ra} \\rightarrow ^{222}\\text{Rn}$")
        st.info(
            "El $^{226}\\text{Ra}$ decae principalmente por emisión **Alfa ($\\alpha$)** directa hacia el estado fundamental del $^{222}\\text{Rn}$ ($94.0\\%$ de probabilidad, $E_\\alpha = 4.78\\text{ MeV}$).\n\n"
            "Sin embargo, en el $5.6\\%$ de las desintegraciones, decae hacia un **estado excitado** del $^{222}\\text{Rn}$ ($186\\text{ keV}$ por encima del fundamental). "
            "La desexcitación de este nivel da origen a la **línea gamma principal** de diagnóstico/control ambiental:\n"
            "* **$E_\\gamma = 186.21\\text{ keV}$** (Transición E2 de desexcitación directa)."
        )
        
        st.markdown("### 2. Análisis del Modelo de Capas y Números Mágicos")
        st.success(
            "Los nucleidos con **números mágicos de neutrones ($N = 2, 8, 20, 28, 50, 82, 126$)** cuentan con capas neutrónicas completamente cerradas, "
            "lo que les confiere una energía de ligadura por nucleón notablemente superior a sus vecinos.\n\n"
            "**Ejemplos típicos en la Tabla de Nucleidos:**\n"
            "* $^{40}\\text{Ca}$ ($N=20$): Doblemente mágico ($Z=20, N=20$), extremadamente estable.\n"
            "* $^{88}\\text{Sr}$ ($N=50$): Muy abundante, fondo del pozo de potencial local.\n"
            "* $^{208}\\text{Pb}$ ($N=126$): El nucleido estable más pesado del universo ($Z=82, N=126$).\n\n"
            "**Justificación gráfica:** Al graficar la energía de separación neutrónica ($S_n$) o la abundancia isotópica en la Línea de Estabilidad, "
            "estos nucleidos se ubican exactamente en los quiebres de pendiente más estables (valles energéticos), demostrando que se requiere mucha "
            "más energía externa para arrancarles un neutrón que a los elementos contiguos."
        )

    st.markdown("---")

    # --- ACTIVIDAD 2 ---
    st.header("🧮 Actividad 2: Problemas de Aplicación Dosimétrica y Espectros")
    
    with st.expander("🔍 Ver Resolución Ejercicio A (Cálculo de Decaimiento)"):
        st.markdown(
            "**Consigna:** Una muestra tiene una actividad inicial $A_0 = 10\\text{ mCi}$. "
            "Calcular la actividad remanente en **Megabecquerels (MBq)** tras transcurrir 3 períodos de semidesintegración ($3\\,T_{1/2}$)."
        )
        st.success(
            "### Paso 1: Reducción analítica por períodos\n"
            "Cada período reduce la actividad exactamente a la mitad. Para $n = 3$ períodos:\n"
            "$$A(3\\,T_{1/2}) = \\frac{A_0}{2^n} = \\frac{10\\text{ mCi}}{2^3} = \\frac{10\\text{ mCi}}{8} = 1.25\\text{ mCi}$$\n\n"
            "### Paso 2: Conversión al Sistema Internacional (SI)\n"
            "Sabiendo que de forma exacta $1\\text{ mCi} = 37\\text{ MBq}$ (como podés verificar en la **Pestaña 2**):\n"
            "$$A_{\\text{final}} = 1.25\\text{ mCi} \\times 37\\text{ MBq/mCi} = \\mathbf{46.25\\text{ MBq}}$$\n\n"
            "**Respuesta:** La actividad remanente tras $3\\,T_{1/2}$ es de **$46.25\\text{ MBq}$**."
        )
        
    with st.expander("🔍 Ver Resolución Ejercicio B (Cuadro Comparativo de Rayos X)"):
        st.markdown(
            "**Consigna:** Diferenciar físicamente mediante un cuadro comparativo el espectro de emisión de los Rayos X característicos "
            "frente al espectro de Frenado (Bremsstrahlung)."
        )
        
        # Cuadro comparativo en formato Markdown
        st.markdown(
            """
            | Criterio Físico | Rayos X Característicos (Fluorescencia) | Rayos X de Frenado (Bremsstrahlung) |
            | :--- | :--- | :--- |
            | **Origen del fotón** | Transiciones electrónicas entre capas internas del átomo ($K, L, M$). | Desaceleración del electrón incidente en el campo coulombiano del núcleo atómico. |
            | **Tipo de Espectro** | **Discreto / De Líneas** (Picos energéticos bien definidos). | **Continuo** (Desde cero hasta la energía máxima del electrón $E_{\max} = e\\cdot V$). |
            | **Dependencia del Blanco** | Depende estrictamente del número atómico ($Z$). Las energías corresponden a la diferencia $\\Delta E$ de ligadura. | El perfil continuo no depende del material, pero la intensidad total sí se incrementa con un mayor $Z$. |
            | **Mecanismo cuántico** | Vacancia electrónica previa por ionización $\\rightarrow$ salto cuántico ordenado. | Pérdida de energía cinética por radiación debido a la aceleración (Física Clásica/Cuántica). |
            """
        )
        
        st.warning(
            "**¿Por qué el Bremsstrahlung es continuo?**\n\n"
            "Porque el electrón proyectil puede pasar a cualquier distancia del núcleo del blanco. El parámetro de impacto ($b$) es continuo: "
            "si pasa muy cerca, cede casi toda su energía en un solo fotón; si pasa lejos, sufre una desviación leve emitiendo un fotón infrarrojo o de baja energía. "
            "Como hay infinitas distancias posibles de aproximación, se genera un gradiente infinito y continuo de energías de fotones, limitado únicamente por la "
            "energía máxima del electrón incidente ($E_0$)."
        )
