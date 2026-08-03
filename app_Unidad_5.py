# -*- coding: utf-8 -*-
"""
Laboratorio Virtual Nº 5
Producción de Radioisótopos, Equilibrios y Generadores

Curso de Metodología y Aplicación de Radioisótopos
Disertante: Bioing. Emiliano Marino

IMPORTANTE:
La aplicación tiene finalidad educativa.
Los modelos simplifican procesos reales de producción,
separación, elución y marcación de radiofármacos.
"""

import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st


# =============================================================================
# CONFIGURACIÓN GENERAL
# =============================================================================

st.set_page_config(
    page_title="Laboratorio Virtual - Unidad 5",
    page_icon="⚛️",
    layout="wide",
)

st.title("⚛️ Laboratorio Virtual Nº 5")
st.header("Producción de Radioisótopos, Equilibrios y Generadores")

st.markdown(
    """
    **Unidad Nº 5**  
    **Disertante:** Bioing. Emiliano Marino  
    **Duración estimada:** 6 horas
    """
)

st.write(
    """
    En este laboratorio recorrerás el camino que sigue un radioisótopo
    desde su producción hasta su utilización en un servicio de Medicina Nuclear.
    """
)

st.warning(
    """
    ⚠️ **Uso educativo:** las representaciones y cálculos de esta aplicación
    simplifican procesos reales. No reemplazan procedimientos de producción,
    control de calidad, radiofarmacia ni decisiones clínicas.
    """
)

st.markdown("---")


# =============================================================================
# DATOS GENERALES
# =============================================================================

RADIOISOTOPOS = {
    "Tecnecio-99m (99mTc)": {
        "origen": "Generador 99Mo/99mTc",
        "produccion_primaria": "El 99Mo se produce principalmente en reactor nuclear",
        "reaccion": "Fisión de 235U o activación neutrónica de 98Mo",
        "vida_media": "6,01 horas",
        "uso": "Diagnóstico por cámara gamma y SPECT",
        "categoria": "Generador",
    },
    "Flúor-18 (18F)": {
        "origen": "Ciclotrón",
        "produccion_primaria": "Bombardeo de agua enriquecida con protones",
        "reaccion": "18O(p,n)18F",
        "vida_media": "109,8 minutos",
        "uso": "PET, principalmente 18F-FDG",
        "categoria": "Ciclotrón",
    },
    "Carbono-11 (11C)": {
        "origen": "Ciclotrón",
        "produccion_primaria": "Bombardeo de un blanco gaseoso con protones",
        "reaccion": "14N(p,α)11C",
        "vida_media": "20,3 minutos",
        "uso": "PET con radiofármacos de vida media corta",
        "categoria": "Ciclotrón",
    },
    "Nitrógeno-13 (13N)": {
        "origen": "Ciclotrón",
        "produccion_primaria": "Bombardeo de agua con protones",
        "reaccion": "16O(p,α)13N",
        "vida_media": "9,97 minutos",
        "uso": "PET de perfusión miocárdica",
        "categoria": "Ciclotrón",
    },
    "Oxígeno-15 (15O)": {
        "origen": "Ciclotrón",
        "produccion_primaria": "Reacciones con blancos gaseosos",
        "reaccion": "14N(d,n)15O",
        "vida_media": "2,04 minutos",
        "uso": "PET de flujo sanguíneo y metabolismo",
        "categoria": "Ciclotrón",
    },
    "Yodo-131 (131I)": {
        "origen": "Reactor nuclear",
        "produccion_primaria": "Fisión o activación neutrónica",
        "reaccion": "Fisión de 235U o 130Te(n,γ)131Te → 131I",
        "vida_media": "8,02 días",
        "uso": "Diagnóstico y tratamiento tiroideo",
        "categoria": "Reactor",
    },
    "Lutecio-177 (177Lu)": {
        "origen": "Reactor nuclear",
        "produccion_primaria": "Producción directa o indirecta por irradiación neutrónica",
        "reaccion": "176Lu(n,γ)177Lu o vía 176Yb",
        "vida_media": "6,65 días",
        "uso": "Terapia con radiofármacos dirigidos",
        "categoria": "Reactor",
    },
    "Galio-68 (68Ga)": {
        "origen": "Generador 68Ge/68Ga o ciclotrón",
        "produccion_primaria": "Decaimiento de 68Ge o producción con protones",
        "reaccion": "68Ge → 68Ga o 68Zn(p,n)68Ga",
        "vida_media": "67,7 minutos",
        "uso": "PET con péptidos y ligandos específicos",
        "categoria": "Generador / Ciclotrón",
    },
}


FAMILIAS_NATURALES = {
    "Familia del Uranio-238": [
        "238U",
        "234Th",
        "234Pa",
        "234U",
        "230Th",
        "226Ra",
        "222Rn",
        "218Po",
        "214Pb",
        "214Bi",
        "214Po",
        "210Pb",
        "210Bi",
        "210Po",
        "206Pb estable",
    ],
    "Familia del Torio-232": [
        "232Th",
        "228Ra",
        "228Ac",
        "228Th",
        "224Ra",
        "220Rn",
        "216Po",
        "212Pb",
        "212Bi",
        "208Tl / 212Po",
        "208Pb estable",
    ],
    "Familia del Uranio-235": [
        "235U",
        "231Th",
        "231Pa",
        "227Ac",
        "227Th",
        "223Ra",
        "219Rn",
        "215Po",
        "211Pb",
        "211Bi",
        "207Tl",
        "207Pb estable",
    ],
}


# =============================================================================
# FUNCIONES MATEMÁTICAS
# =============================================================================

def actividad_madre(
    actividad_inicial,
    lambda_madre,
    tiempo,
):
    """
    Actividad de la madre en función del tiempo.
    """

    return actividad_inicial * np.exp(
        -lambda_madre * tiempo
    )


def actividad_hija_bateman(
    actividad_madre_inicial,
    lambda_madre,
    lambda_hija,
    tiempo,
    fraccion_ramificacion=1.0,
):
    """
    Actividad de la hija suponiendo que inicialmente no hay hija.

    Se utiliza una forma simplificada de las ecuaciones de Bateman.
    """

    if math.isclose(
        lambda_madre,
        lambda_hija,
        rel_tol=1e-9,
    ):

        return (
            fraccion_ramificacion
            * actividad_madre_inicial
            * lambda_hija
            * tiempo
            * np.exp(
                -lambda_hija * tiempo
            )
        )

    actividad_hija = (
        fraccion_ramificacion
        * actividad_madre_inicial
        * lambda_hija
        / (
            lambda_hija
            - lambda_madre
        )
        * (
            np.exp(
                -lambda_madre * tiempo
            )
            - np.exp(
                -lambda_hija * tiempo
            )
        )
    )

    return np.maximum(
        actividad_hija,
        0,
    )


def clasificar_equilibrio(
    vida_media_madre,
    vida_media_hija,
):
    """
    Clasifica de manera didáctica la relación madre-hija.
    """

    relacion = (
        vida_media_madre
        / vida_media_hija
    )

    if relacion >= 100:

        return (
            "Equilibrio secular",
            (
                "La vida media de la madre es muchísimo mayor que la de la hija. "
                "La actividad de la hija termina siguiendo aproximadamente a la madre."
            ),
        )

    if relacion >= 3:

        return (
            "Equilibrio transitorio",
            (
                "La madre vive más que la hija, pero no de manera extremadamente superior. "
                "La hija crece, alcanza un máximo y luego ambas actividades disminuyen."
            ),
        )

    return (
        "No equilibrio",
        (
            "La vida media de la madre no es suficientemente mayor que la de la hija. "
            "No se establece una relación de equilibrio sostenida."
        ),
    )


def calcular_tc_generador(
    actividad_mo_inicial,
    tiempo_desde_elucion,
):
    """
    Calcula de forma simplificada el crecimiento de 99mTc
    a partir de 99Mo después de una elución completa.
    """

    vida_media_mo = 66.0
    vida_media_tc = 6.01

    lambda_mo = math.log(2) / vida_media_mo
    lambda_tc = math.log(2) / vida_media_tc

    fraccion_ramificacion = 0.86

    actividad_tc = (
        fraccion_ramificacion
        * actividad_mo_inicial
        * lambda_tc
        / (
            lambda_tc
            - lambda_mo
        )
        * (
            math.exp(
                -lambda_mo
                * tiempo_desde_elucion
            )
            - math.exp(
                -lambda_tc
                * tiempo_desde_elucion
            )
        )
    )

    actividad_mo_actual = (
        actividad_mo_inicial
        * math.exp(
            -lambda_mo
            * tiempo_desde_elucion
        )
    )

    return (
        max(
            actividad_tc,
            0.0,
        ),
        actividad_mo_actual,
    )


# =============================================================================
# PESTAÑAS
# =============================================================================

(
    tab_inicio,
    tab_produccion,
    tab_generador,
    tab_equilibrio,
    tab_vidas_medias,
    tab_radiofarmacos,
    tab_familias,
    tab_origen,
    tab_mision,
) = st.tabs(
    [
        "🏁 Inicio",
        "1️⃣ Producción",
        "2️⃣ Generador 99Mo/99mTc",
        "3️⃣ Equilibrios",
        "4️⃣ Vida media madre-hija",
        "5️⃣ Marcación",
        "6️⃣ Familias naturales",
        "7️⃣ Origen del radioisótopo",
        "🎯 Misión final",
    ]
)


# =============================================================================
# INICIO
# =============================================================================

with tab_inicio:

    st.header(
        "Recorrido del laboratorio"
    )

    st.markdown(
        """
        ### Estación 1 · Producción de radioisótopos

        Compararás los principios de producción en reactor nuclear
        y ciclotrón.

        ### Estación 2 · Generador 99Mo/99mTc

        Analizarás el crecimiento del 99mTc después de una elución.

        ### Estación 3 · Equilibrios radiactivos

        Compararás equilibrio secular, equilibrio transitorio
        y situaciones de no equilibrio.

        ### Estación 4 · Vida media madre-hija

        Modificarás las vidas medias para descubrir qué tipo
        de equilibrio se establece.

        ### Estación 5 · Marcación de radiofármacos

        Reconocerás las etapas rutinarias de preparación
        y control del producto.

        ### Estación 6 · Familias radiactivas naturales

        Explorarás las cadenas naturales del uranio y el torio.

        ### Estación 7 · Origen del radioisótopo

        Relacionarás cada radionúclido con su método de producción
        y aplicación clínica.

        ### Misión final

        Resolverás un caso asociado a la operación de un generador.
        """
    )


# =============================================================================
# ESTACIÓN 1: PRODUCCIÓN
# =============================================================================

with tab_produccion:

    st.header(
        "Estación 1 · ¿Cómo se producen los radioisótopos?"
    )

    metodo_produccion = st.radio(
        "Seleccioná el método de producción",
        [
            "Reactor nuclear",
            "Ciclotrón",
        ],
        horizontal=True,
    )

    columna_esquema, columna_comparacion = st.columns(
        [1.2, 1]
    )

    with columna_esquema:

        if metodo_produccion == "Reactor nuclear":

            st.subheader(
                "Producción en reactor"
            )

            st.markdown(
                """
                ### Neutrón

                ↓

                ### Núcleo blanco

                ↓

                ### Captura neutrónica o fisión

                ↓

                ### Radionúclido producido
                """
            )

            st.info(
                """
                Los reactores proporcionan flujos intensos de neutrones.
                La producción puede ocurrir mediante captura neutrónica,
                fisión u otras reacciones inducidas por neutrones.
                """
            )

            ejemplos_reactor = pd.DataFrame(
                {
                    "Radionúclido": [
                        "99Mo",
                        "131I",
                        "177Lu",
                    ],
                    "Ejemplo de producción": [
                        "Fisión de 235U o activación de 98Mo",
                        "Fisión o activación de 130Te",
                        "Irradiación de 176Lu o 176Yb",
                    ],
                    "Aplicación": [
                        "Padre del generador 99Mo/99mTc",
                        "Diagnóstico y terapia tiroidea",
                        "Terapia metabólica dirigida",
                    ],
                }
            )

            st.dataframe(
                ejemplos_reactor,
                use_container_width=True,
                hide_index=True,
            )

        else:

            st.subheader(
                "Producción en ciclotrón"
            )

            st.markdown(
                """
                ### Partícula cargada

                ↓

                ### Aceleración en campo magnético

                ↓

                ### Impacto sobre un blanco

                ↓

                ### Reacción nuclear

                ↓

                ### Radionúclido producido
                """
            )

            st.info(
                """
                El ciclotrón acelera protones, deuterones u otras partículas
                cargadas. Estas impactan sobre un material blanco y producen
                una reacción nuclear.
                """
            )

            ejemplos_ciclotron = pd.DataFrame(
                {
                    "Radionúclido": [
                        "18F",
                        "11C",
                        "13N",
                        "15O",
                        "68Ga",
                    ],
                    "Reacción": [
                        "18O(p,n)18F",
                        "14N(p,α)11C",
                        "16O(p,α)13N",
                        "14N(d,n)15O",
                        "68Zn(p,n)68Ga",
                    ],
                    "Aplicación": [
                        "PET con 18F-FDG",
                        "PET con moléculas marcadas con carbono",
                        "Perfusión miocárdica",
                        "Estudios de flujo y metabolismo",
                        "PET con ligandos específicos",
                    ],
                }
            )

            st.dataframe(
                ejemplos_ciclotron,
                use_container_width=True,
                hide_index=True,
            )

    with columna_comparacion:

        st.subheader(
            "Comparación"
        )

        tabla_comparativa = pd.DataFrame(
            {
                "Característica": [
                    "Partícula incidente",
                    "Ubicación habitual",
                    "Radionúclidos frecuentes",
                    "Vida media típica",
                    "Ejemplo clínico",
                ],
                "Reactor": [
                    "Neutrones",
                    "Instalación nuclear",
                    "99Mo, 131I, 177Lu",
                    "Horas o días",
                    "Producción de 99Mo",
                ],
                "Ciclotrón": [
                    "Protones o deuterones",
                    "Centro PET o instalación especializada",
                    "18F, 11C, 13N, 15O",
                    "Minutos u horas",
                    "Producción de 18F",
                ],
            }
        )

        st.dataframe(
            tabla_comparativa,
            use_container_width=True,
            hide_index=True,
        )

    with st.expander(
        "📝 Preguntas de observación"
    ):

        st.markdown(
            """
            1. ¿Qué tipo de partícula se utiliza en un reactor?
            2. ¿Qué tipo de partícula se acelera en un ciclotrón?
            3. ¿Por qué los radioisótopos de vida media muy corta deben producirse cerca del paciente?
            4. ¿Qué método se utiliza habitualmente para producir 18F?
            5. ¿Cómo se obtiene el 99Mo utilizado en los generadores?
            """
        )


# =============================================================================
# ESTACIÓN 2: GENERADOR 99Mo/99mTc
# =============================================================================

with tab_generador:

    st.header(
        "Estación 2 · Generador 99Mo/99mTc"
    )

    st.write(
        """
        Simulá el crecimiento del 99mTc después de una elución completa
        del generador.
        """
    )

    columna_parametros, columna_resultados = st.columns(
        [1, 1.5]
    )

    with columna_parametros:

        actividad_mo_inicial = st.number_input(
            "Actividad de 99Mo al momento de la elución (GBq)",
            min_value=1.0,
            value=100.0,
            step=5.0,
        )

        tiempo_desde_elucion = st.slider(
            "Tiempo desde la última elución (horas)",
            min_value=0.0,
            max_value=48.0,
            value=12.0,
            step=0.5,
        )

        eficiencia_elucion = st.slider(
            "Eficiencia de elución (%)",
            min_value=50,
            max_value=100,
            value=90,
            step=1,
        )

    actividad_tc_columna, actividad_mo_actual = calcular_tc_generador(
        actividad_mo_inicial,
        tiempo_desde_elucion,
    )

    actividad_tc_extraida = (
        actividad_tc_columna
        * eficiencia_elucion
        / 100.0
    )

    with columna_resultados:

        metrica_1, metrica_2, metrica_3 = st.columns(
            3
        )

        metrica_1.metric(
            "99Mo remanente",
            f"{actividad_mo_actual:.2f} GBq",
        )

        metrica_2.metric(
            "99mTc disponible",
            f"{actividad_tc_columna:.2f} GBq",
        )

        metrica_3.metric(
            "99mTc extraíble",
            f"{actividad_tc_extraida:.2f} GBq",
        )

        tiempos_generador = np.linspace(
            0,
            48,
            500,
        )

        actividades_tc = []
        actividades_mo = []

        for tiempo in tiempos_generador:

            tc_temporal, mo_temporal = calcular_tc_generador(
                actividad_mo_inicial,
                tiempo,
            )

            actividades_tc.append(
                tc_temporal
            )

            actividades_mo.append(
                mo_temporal
            )

        figura_generador, eje_generador = plt.subplots(
            figsize=(9, 4.5)
        )

        eje_generador.plot(
            tiempos_generador,
            actividades_mo,
            linewidth=2.5,
            label="99Mo",
        )

        eje_generador.plot(
            tiempos_generador,
            actividades_tc,
            linewidth=2.5,
            label="99mTc acumulado",
        )

        eje_generador.scatter(
            [tiempo_desde_elucion],
            [actividad_tc_columna],
            s=100,
            zorder=5,
            label="Momento seleccionado",
        )

        eje_generador.axvline(
            tiempo_desde_elucion,
            linestyle="--",
        )

        eje_generador.set_xlabel(
            "Tiempo desde la elución (horas)"
        )

        eje_generador.set_ylabel(
            "Actividad (GBq)"
        )

        eje_generador.set_title(
            "Crecimiento del 99mTc después de la elución"
        )

        eje_generador.grid(
            alpha=0.30
        )

        eje_generador.legend()

        st.pyplot(
            figura_generador
        )

    if tiempo_desde_elucion < 6:

        st.warning(
            """
            Ha transcurrido poco tiempo desde la elución. La actividad
            de 99mTc todavía se encuentra en crecimiento.
            """
        )

    elif tiempo_desde_elucion <= 24:

        st.success(
            """
            La actividad de 99mTc se encuentra en una región de crecimiento
            clínicamente relevante.
            """
        )

    else:

        st.info(
            """
            Aunque el 99mTc continúa estando disponible, el 99Mo también
            ha disminuido por decaimiento.
            """
        )

    with st.expander(
        "📝 Preguntas de observación"
    ):

        st.markdown(
            """
            1. ¿Por qué el 99mTc vuelve a crecer después de una elución?
            2. ¿Qué ocurre si se realizan eluciones demasiado próximas?
            3. ¿Por qué la actividad de 99mTc nunca supera indefinidamente a la del 99Mo?
            4. ¿Cómo influye la eficiencia de elución sobre la actividad obtenida?
            5. ¿Qué tipo de equilibrio presenta el sistema 99Mo/99mTc?
            """
        )


# =============================================================================
# ESTACIÓN 3: EQUILIBRIOS
# =============================================================================

with tab_equilibrio:

    st.header(
        "Estación 3 · Equilibrios radiactivos"
    )

    tipo_equilibrio = st.radio(
        "Seleccioná el caso",
        [
            "Equilibrio secular",
            "Equilibrio transitorio",
            "No equilibrio",
        ],
        horizontal=True,
    )

    if tipo_equilibrio == "Equilibrio secular":

        vida_media_madre = 1000.0
        vida_media_hija = 5.0

    elif tipo_equilibrio == "Equilibrio transitorio":

        vida_media_madre = 66.0
        vida_media_hija = 6.0

    else:

        vida_media_madre = 5.0
        vida_media_hija = 20.0

    actividad_inicial_madre = 100.0

    lambda_madre = (
        math.log(2)
        / vida_media_madre
    )

    lambda_hija = (
        math.log(2)
        / vida_media_hija
    )

    tiempo_maximo = max(
        5.0 * vida_media_madre,
        10.0 * vida_media_hija,
    )

    tiempos = np.linspace(
        0,
        tiempo_maximo,
        600,
    )

    actividad_m = actividad_madre(
        actividad_inicial_madre,
        lambda_madre,
        tiempos,
    )

    actividad_h = actividad_hija_bateman(
        actividad_inicial_madre,
        lambda_madre,
        lambda_hija,
        tiempos,
    )

    figura_equilibrio, eje_equilibrio = plt.subplots(
        figsize=(10, 5)
    )

    eje_equilibrio.plot(
        tiempos,
        actividad_m,
        linewidth=2.7,
        label="Actividad de la madre",
    )

    eje_equilibrio.plot(
        tiempos,
        actividad_h,
        linewidth=2.7,
        label="Actividad de la hija",
    )

    eje_equilibrio.set_xlabel(
        "Tiempo relativo"
    )

    eje_equilibrio.set_ylabel(
        "Actividad relativa"
    )

    eje_equilibrio.set_title(
        tipo_equilibrio
    )

    eje_equilibrio.grid(
        alpha=0.30
    )

    eje_equilibrio.legend()

    st.pyplot(
        figura_equilibrio
    )

    if tipo_equilibrio == "Equilibrio secular":

        st.info(
            """
            La vida media de la madre es muchísimo mayor que la de la hija.
            Después del crecimiento inicial, la actividad de la hija sigue
            aproximadamente a la actividad de la madre.
            """
        )

    elif tipo_equilibrio == "Equilibrio transitorio":

        st.info(
            """
            La madre tiene una vida media mayor que la hija, pero ambas
            disminuyen de manera apreciable durante el período analizado.
            """
        )

    else:

        st.info(
            """
            La relación entre las vidas medias no permite establecer
            un equilibrio sostenido entre madre e hija.
            """
        )


# =============================================================================
# ESTACIÓN 4: VIDA MEDIA MADRE-HIJA
# =============================================================================

with tab_vidas_medias:

    st.header(
        "Estación 4 · Exploración de vidas medias"
    )

    st.write(
        """
        Modificá las vidas medias y observá qué tipo de equilibrio
        se establece.
        """
    )

    columna_1, columna_2 = st.columns(
        2
    )

    with columna_1:

        vida_media_madre_usuario = st.slider(
            "Vida media de la madre (unidades de tiempo)",
            min_value=1.0,
            max_value=1000.0,
            value=100.0,
            step=1.0,
        )

    with columna_2:

        vida_media_hija_usuario = st.slider(
            "Vida media de la hija (unidades de tiempo)",
            min_value=1.0,
            max_value=200.0,
            value=10.0,
            step=1.0,
        )

    clasificacion, explicacion = clasificar_equilibrio(
        vida_media_madre_usuario,
        vida_media_hija_usuario,
    )

    relacion_vidas = (
        vida_media_madre_usuario
        / vida_media_hija_usuario
    )

    metrica_1, metrica_2 = st.columns(
        2
    )

    metrica_1.metric(
        "Relación T½ madre / T½ hija",
        f"{relacion_vidas:.2f}",
    )

    metrica_2.metric(
        "Clasificación",
        clasificacion,
    )

    st.success(
        explicacion
    )

    lambda_madre_usuario = (
        math.log(2)
        / vida_media_madre_usuario
    )

    lambda_hija_usuario = (
        math.log(2)
        / vida_media_hija_usuario
    )

    tiempo_maximo_usuario = max(
        5.0 * vida_media_madre_usuario,
        10.0 * vida_media_hija_usuario,
    )

    tiempos_usuario = np.linspace(
        0,
        tiempo_maximo_usuario,
        600,
    )

    actividad_m_usuario = actividad_madre(
        100.0,
        lambda_madre_usuario,
        tiempos_usuario,
    )

    actividad_h_usuario = actividad_hija_bateman(
        100.0,
        lambda_madre_usuario,
        lambda_hija_usuario,
        tiempos_usuario,
    )

    figura_usuario, eje_usuario = plt.subplots(
        figsize=(10, 5)
    )

    eje_usuario.plot(
        tiempos_usuario,
        actividad_m_usuario,
        linewidth=2.5,
        label="Madre",
    )

    eje_usuario.plot(
        tiempos_usuario,
        actividad_h_usuario,
        linewidth=2.5,
        label="Hija",
    )

    eje_usuario.set_xlabel(
        "Tiempo relativo"
    )

    eje_usuario.set_ylabel(
        "Actividad relativa"
    )

    eje_usuario.set_title(
        clasificacion
    )

    eje_usuario.grid(
        alpha=0.30
    )

    eje_usuario.legend()

    st.pyplot(
        figura_usuario
    )


# =============================================================================
# ESTACIÓN 5: MARCACIÓN
# =============================================================================

with tab_radiofarmacos:

    st.header(
        "Estación 5 · Aspectos rutinarios de marcación"
    )

    st.write(
        """
        Ordená mentalmente las etapas básicas de preparación de un
        radiofármaco. Esta estación representa un flujo general y no
        un protocolo específico.
        """
    )

    radiofarmaco = st.selectbox(
        "Preparación conceptual",
        [
            "99mTc + MDP",
            "99mTc + MIBI",
            "99mTc + DTPA",
            "68Ga + ligando",
            "177Lu + ligando terapéutico",
        ],
    )

    etapas = [
        "Verificar identidad e integridad del kit o precursor",
        "Comprobar actividad y radionúclido",
        "Realizar la incorporación del radionúclido",
        "Respetar condiciones de tiempo, temperatura y pH",
        "Realizar control de calidad",
        "Liberar únicamente si cumple las especificaciones",
    ]

    etapa_actual = st.slider(
        "Recorrido de preparación",
        min_value=1,
        max_value=len(etapas),
        value=1,
        step=1,
    )

    st.subheader(
        radiofarmaco
    )

    for indice, etapa in enumerate(
        etapas,
        start=1,
    ):

        if indice < etapa_actual:

            st.success(
                f"✅ {indice}. {etapa}"
            )

        elif indice == etapa_actual:

            st.info(
                f"➡️ {indice}. {etapa}"
            )

        else:

            st.write(
                f"⬜ {indice}. {etapa}"
            )

    st.warning(
        """
        La actividad administrada no depende únicamente de realizar la
        marcación. También deben verificarse pureza radioquímica, identidad,
        esterilidad, endotoxinas y demás requisitos aplicables.
        """
    )

    with st.expander(
        "📝 Preguntas de observación"
    ):

        st.markdown(
            """
            1. ¿Por qué es necesario realizar control de calidad antes de administrar?
            2. ¿Qué diferencia existe entre radionúclido y radiofármaco?
            3. ¿Por qué deben respetarse condiciones de tiempo, pH y temperatura?
            4. ¿Qué riesgos existen si la pureza radioquímica es insuficiente?
            """
        )


# =============================================================================
# ESTACIÓN 6: FAMILIAS NATURALES
# =============================================================================

with tab_familias:

    st.header(
        "Estación 6 · Familias radiactivas naturales"
    )

    familia = st.selectbox(
        "Seleccioná una familia",
        list(
            FAMILIAS_NATURALES.keys()
        ),
    )

    cadena = FAMILIAS_NATURALES[
        familia
    ]

    cantidad_nodos = st.slider(
        "Avance en la cadena",
        min_value=1,
        max_value=len(cadena),
        value=1,
        step=1,
    )

    st.subheader(
        familia
    )

    cadena_visible = cadena[
        :cantidad_nodos
    ]

    st.markdown(
        "  →  ".join(
            [
                f"**{nucleido}**"
                for nucleido in cadena_visible
            ]
        )
    )

    if cantidad_nodos == len(cadena):

        st.success(
            "La cadena alcanzó un nucleído estable."
        )

    else:

        st.info(
            f"El siguiente integrante de la familia es: "
            f"**{cadena[cantidad_nodos]}**"
        )

    with st.expander(
        "📝 Preguntas de observación"
    ):

        st.markdown(
            """
            1. ¿Por qué una familia radiactiva contiene varios nucleídos?
            2. ¿Qué significa que la cadena termine en un nucleído estable?
            3. ¿Qué importancia tiene el radón dentro de las familias naturales?
            4. ¿Por qué las actividades de los integrantes pueden alcanzar equilibrio?
            """
        )


# =============================================================================
# ESTACIÓN 7: ORIGEN DEL RADIOISÓTOPO
# =============================================================================

with tab_origen:

    st.header(
        "Estación 7 · ¿De dónde viene este radioisótopo?"
    )

    radioisotopo_seleccionado = st.selectbox(
        "Seleccioná un radioisótopo",
        list(
            RADIOISOTOPOS.keys()
        ),
    )

    ficha = RADIOISOTOPOS[
        radioisotopo_seleccionado
    ]

    st.subheader(
        radioisotopo_seleccionado
    )

    columna_1, columna_2 = st.columns(
        2
    )

    with columna_1:

        st.metric(
            "Origen",
            ficha["origen"],
        )

        st.metric(
            "Vida media",
            ficha["vida_media"],
        )

        st.metric(
            "Categoría",
            ficha["categoria"],
        )

    with columna_2:

        st.markdown(
            f"""
            **Producción:**  
            {ficha["produccion_primaria"]}

            **Reacción o vía principal:**  
            `{ficha["reaccion"]}`

            **Uso principal:**  
            {ficha["uso"]}
            """
        )


# =============================================================================
# MISIÓN FINAL
# =============================================================================

with tab_mision:

    st.header(
        "🎯 Misión final · Operación de un generador"
    )

    st.markdown(
        """
        El servicio de Medicina Nuclear debe decidir si resulta conveniente
        realizar una nueva elución del generador 99Mo/99mTc.
        """
    )

    columna_1, columna_2, columna_3 = st.columns(
        3
    )

    with columna_1:

        actividad_mo_mision = st.number_input(
            "Actividad de 99Mo luego de la última elución (GBq)",
            min_value=1.0,
            value=100.0,
            step=5.0,
            key="actividad_mo_mision",
        )

    with columna_2:

        horas_mision = st.slider(
            "Horas desde la última elución",
            min_value=0.0,
            max_value=48.0,
            value=18.0,
            step=0.5,
            key="horas_mision",
        )

    with columna_3:

        eficiencia_mision = st.slider(
            "Eficiencia de elución (%)",
            min_value=50,
            max_value=100,
            value=90,
            step=1,
            key="eficiencia_mision",
        )

    tc_disponible_mision, mo_actual_mision = calcular_tc_generador(
        actividad_mo_mision,
        horas_mision,
    )

    tc_extraible_mision = (
        tc_disponible_mision
        * eficiencia_mision
        / 100.0
    )

    metrica_1, metrica_2, metrica_3 = st.columns(
        3
    )

    metrica_1.metric(
        "99Mo remanente",
        f"{mo_actual_mision:.2f} GBq",
    )

    metrica_2.metric(
        "99mTc acumulado",
        f"{tc_disponible_mision:.2f} GBq",
    )

    metrica_3.metric(
        "99mTc extraíble",
        f"{tc_extraible_mision:.2f} GBq",
    )

    st.subheader(
        "📝 Consigna para entregar"
    )

    st.markdown(
        f"""
        1. Interprete la actividad de 99mTc disponible luego de
        **{horas_mision:.1f} horas**.

        2. Explique por qué el 99mTc vuelve a crecer después de una elución.

        3. Indique qué tipo de equilibrio presenta el sistema 99Mo/99mTc.

        4. Analice cómo cambiaría el resultado si la elución se hubiera
        realizado hace solamente 4 horas.

        5. Explique cómo se produce originalmente el 99Mo utilizado
        en el generador.

        6. Diferencie:

        - producción del radionúclido;
        - obtención mediante generador;
        - marcación del radiofármaco.

        7. Mencione qué controles deberían realizarse antes de utilizar
        el producto en un paciente.

        8. Explique las limitaciones de esta simulación respecto de la
        operación real de un generador.
        """
    )


# =============================================================================
# PIE DE PÁGINA
# =============================================================================

st.markdown("---")

st.caption(
    """
    Propuesta tecno-pedagógica desarrollada para el Curso de Metodología
    y Aplicación de Radioisótopos.
    """
)
