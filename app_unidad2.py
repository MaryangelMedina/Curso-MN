import streamlit as st
# ... acá van tus otros imports si tenías (matplotlib, numpy, etc.) ...

# 1. DEFINÍ LAS PESTAÑAS AL PRINCIPIO (Abajo de los imports)
tab1, tab2 = st.tabs(["📊 Laboratorio de Ordeñe", "🔄 Conversión de Unidades (Ci ↔ Bq)"])

# 2. METÉ TODO TU CÓDIGO ACTUAL ADENTRO DEL WITH TAB1
with tab1:
    # --- ACÁ VA TODO TU CÓDIGO VIEJO ---
    # Es decir, todo lo que armaba la barra lateral, el gráfico animado,
    # los sliders de las horas, los cálculos de las ecuaciones de Bateman, etc.
    # REQUISITO IMPORTANTE: Todo el código que metas acá adentro tiene que 
    # llevar un tabulado (4 espacios o un "Tab") hacia la derecha para que 
    # Python sepa que pertenece a la pestaña 1.
    
    st.title("Laboratorio Virtual: Ordeñe Animado Semanal")
    # ... (el resto de tu simulación actual con su sangría correspondiente) ...


# 3. PEGÁ ESTE BLOQUE AL FINAL DEL ARCHIVO (Sin sangría en la línea del 'with')
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
