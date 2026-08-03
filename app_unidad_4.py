# =============================================================================
# MISIÓN FINAL
# =============================================================================

with tab_mision:

    st.header(
        "🎯 Misión final · Caso integrador"
    )

    st.markdown(
        """
        El servicio de Medicina Nuclear debe analizar el comportamiento
        de distintos fotones al atravesar un material.

        Seleccioná una fuente, un material y un espesor fijo. Luego interpretá
        los resultados utilizando los conceptos de atenuación, semiespesor
        y selección de colimadores trabajados en las estaciones anteriores.
        """
    )

    columna_1, columna_2 = st.columns(
        2
    )

    with columna_1:

        fuente_caso = st.selectbox(
            "Fuente del caso",
            list(
                DATOS_ATENUACION.keys()
            ),
            key="fuente_caso",
        )

    with columna_2:

        material_caso = st.selectbox(
            "Material del caso",
            [
                "Agua",
                "Aluminio",
                "Hormigón",
                "Plomo",
            ],
            key="material_caso",
        )

    # -------------------------------------------------------------------------
    # DATOS DE LA FUENTE Y DEL MATERIAL
    # -------------------------------------------------------------------------

    energia_caso = DATOS_ATENUACION[
        fuente_caso
    ]["energia"]

    mu_caso = DATOS_ATENUACION[
        fuente_caso
    ]["mu"][material_caso]

    densidad_caso = MATERIALES[
        material_caso
    ]["densidad"]

    mu_masico_caso = (
        mu_caso
        / densidad_caso
    )

    hvl_caso = (
        math.log(2)
        / mu_caso
    )

    tvl_caso = (
        math.log(10)
        / mu_caso
    )

    # -------------------------------------------------------------------------
    # ESPESOR INDEPENDIENTE DEL HVL
    # -------------------------------------------------------------------------

    espesor_caso = st.number_input(
        "Espesor del material (cm)",
        min_value=0.0,
        value=1.0,
        step=0.1,
        key="espesor_caso",
        help=(
            "El espesor permanece fijo cuando cambia la fuente. "
            "Esto permite comparar cómo varía la transmisión con la energía."
        ),
    )

    # -------------------------------------------------------------------------
    # CÁLCULOS DE ATENUACIÓN
    # -------------------------------------------------------------------------

    transmision_caso = math.exp(
        -mu_caso
        * espesor_caso
    )

    porcentaje_transmitido_caso = (
        100.0
        * transmision_caso
    )

    porcentaje_atenuado_caso = (
        100.0
        * (
            1.0
            - transmision_caso
        )
    )

    numero_hvl_caso = (
        espesor_caso
        / hvl_caso
    )

    numero_tvl_caso = (
        espesor_caso
        / tvl_caso
    )

    # -------------------------------------------------------------------------
    # INTERACCIONES FÍSICAMENTE POSIBLES
    # -------------------------------------------------------------------------

    if energia_caso < 1022:

        procesos_posibles = (
            "Fotoeléctrico y Compton"
        )

    else:

        procesos_posibles = (
            "Fotoeléctrico, Compton "
            "y producción de pares"
        )

    # -------------------------------------------------------------------------
    # RESULTADOS
    # -------------------------------------------------------------------------

    st.subheader(
        "Resultados del caso"
    )

    metrica_1, metrica_2, metrica_3, metrica_4 = st.columns(
        4
    )

    metrica_1.metric(
        "Energía del fotón",
        f"{energia_caso:.0f} keV",
    )

    metrica_2.metric(
        "Coeficiente lineal μ",
        f"{mu_caso:.4g} cm⁻¹",
    )

    metrica_3.metric(
        "Coeficiente másico μ/ρ",
        f"{mu_masico_caso:.4g} cm²/g",
    )

    metrica_4.metric(
        "Procesos posibles",
        procesos_posibles,
    )

    metrica_5, metrica_6, metrica_7, metrica_8 = st.columns(
        4
    )

    metrica_5.metric(
        "Transmisión",
        f"{porcentaje_transmitido_caso:.2f} %",
    )

    metrica_6.metric(
        "Atenuación",
        f"{porcentaje_atenuado_caso:.2f} %",
    )

    metrica_7.metric(
        "HVL",
        f"{hvl_caso:.4g} cm",
    )

    metrica_8.metric(
        "Número de HVL",
        f"{numero_hvl_caso:.2f}",
    )

    # -------------------------------------------------------------------------
    # REPRESENTACIÓN VISUAL DEL HAZ
    # -------------------------------------------------------------------------

    st.subheader(
        "Representación visual del haz"
    )

    columna_haz_inicial, columna_material, columna_haz_final = st.columns(
        [1, 0.7, 1]
    )

    with columna_haz_inicial:

        st.markdown(
            "### Haz inicial"
        )

        st.progress(
            1.0
        )

        st.write(
            "**100 %**"
        )

    with columna_material:

        st.markdown(
            f"### {material_caso}"
        )

        st.write(
            f"Espesor: **{espesor_caso:.2f} cm**"
        )

        st.write(
            f"Equivale a **{numero_hvl_caso:.2f} HVL**"
        )

    with columna_haz_final:

        st.markdown(
            "### Haz transmitido"
        )

        st.progress(
            min(
                max(
                    transmision_caso,
                    0.0,
                ),
                1.0,
            )
        )

        st.write(
            f"**{porcentaje_transmitido_caso:.2f} %**"
        )

    st.info(
        f"""
        Para un espesor fijo de **{espesor_caso:.2f} cm** de
        **{material_caso}**, la transmisión calculada para
        **{fuente_caso}** es de aproximadamente
        **{porcentaje_transmitido_caso:.2f} %**.

        Ese espesor representa **{numero_hvl_caso:.2f} semiespesores**
        y **{numero_tvl_caso:.2f} capas décimorreductoras**.
        """
    )

    # -------------------------------------------------------------------------
    # CONSIGNA
    # -------------------------------------------------------------------------

    st.subheader(
        "📝 Consigna para entregar"
    )

    st.markdown(
        f"""
        1. Interprete físicamente el valor de transmisión obtenido para
        **{espesor_caso:.2f} cm** de **{material_caso}**.

        2. Explique qué significa que ese espesor represente
        **{numero_hvl_caso:.2f} semiespesores**.

        3. Mantenga fijo el material y el espesor. Cambie la fuente y compare
        cómo se modifica la transmisión. ¿Qué relación observa con la energía
        del fotón?

        4. Mantenga fija la fuente y el espesor. Cambie el material y compare
        los resultados. ¿Cómo influyen la densidad y el número atómico?

        5. Indique cuáles de los siguientes mecanismos pueden ocurrir con la
        energía seleccionada:

        - efecto fotoeléctrico;
        - efecto Compton;
        - producción de pares.

        Justifique su respuesta. No es necesario establecer cuál predomina.

        6. Proponga un colimador adecuado para la categoría energética de la
        fuente seleccionada y justifique la elección.

        7. Señale al menos dos limitaciones del modelo de atenuación utilizado.

        8. Explique la diferencia entre esta simulación didáctica y un cálculo
        real de blindaje o dosimetría.
        """
    )

    st.caption(
        """
        Para comparar correctamente distintas fuentes, mantenga constantes
        el material y el espesor. Para comparar materiales, mantenga constantes
        la fuente y el espesor.
        """
    )
