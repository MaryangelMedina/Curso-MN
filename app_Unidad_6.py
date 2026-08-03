# -*- coding: utf-8 -*-
"""
Laboratorio Virtual Nº 6
Dosimetría de fuentes externas e internas

Curso de Metodología y Aplicación de Radioisótopos
Disertante: Bioing. Héctor Agüero

IMPORTANTE:
Esta aplicación tiene finalidad exclusivamente educativa.
Los cálculos simplifican situaciones reales y no deben utilizarse
para decisiones clínicas, planificación terapéutica, diseño de
blindajes ni evaluaciones regulatorias.
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
    page_title="Laboratorio Virtual - Unidad 6",
    page_icon="☢️",
    layout="wide",
)

st.title("☢️ Laboratorio Virtual Nº 6")
st.header("Dosimetría de fuentes externas e internas")

st.markdown(
    """
    **Unidad Nº 6**  
    **Disertante:** Bioing. Héctor Agüero  
    **Duración estimada:** 18 horas
    """
)

st.write(
    """
    En este laboratorio se analizarán los conceptos fundamentales de dosis,
    tasa de dosis, kerma, exposición, ley del inverso del cuadrado,
    actividad acumulada, tiempo de residencia y metodología MIRD.
    """
)

st.warning(
    """
    ⚠️ **Uso educativo:** los modelos utilizados son ideales y simplificados.
    No consideran todas las variables geométricas, biológicas, físicas y
    dosimétricas necesarias en una evaluación real.
    """
)

st.markdown("---")


# =============================================================================
# DATOS DIDÁCTICOS
# =============================================================================

MATERIALES = {
    "Agua": {
        "densidad": 1.00,
        "mu": 0.096,
        "descripcion": "Material de referencia aproximado para tejido blando.",
    },
    "Aluminio": {
        "densidad": 2.70,
        "mu": 0.23,
        "descripcion": "Material metálico de número atómico intermedio.",
    },
    "Hormigón": {
        "densidad": 2.30,
        "mu": 0.15,
        "descripcion": "Material utilizado habitualmente en blindajes estructurales.",
    },
    "Plomo": {
        "densidad": 11.34,
        "mu": 1.70,
        "descripcion": "Material de número atómico elevado y alta capacidad de atenuación.",
    },
}


MAGNITUDES_DOSIMETRICAS = {
    "Exposición": {
        "definicion": (
            "Magnitud histórica que describe la ionización producida por fotones "
            "en una determinada masa de aire."
        ),
        "unidad_si": "C/kg",
        "medio": "Aire",
        "idea": "Carga eléctrica producida por unidad de masa de aire.",
    },
    "Kerma": {
        "definicion": (
            "Energía cinética inicial transferida por la radiación indirectamente "
            "ionizante a partículas cargadas, por unidad de masa."
        ),
        "unidad_si": "Gy = J/kg",
        "medio": "Cualquier medio",
        "idea": "Transferencia de energía desde los fotones hacia electrones secundarios.",
    },
    "Dosis absorbida": {
        "definicion": (
            "Energía impartida por la radiación ionizante a la materia, "
            "por unidad de masa."
        ),
        "unidad_si": "Gy = J/kg",
        "medio": "Cualquier medio",
        "idea": "Energía que finalmente queda depositada en el material.",
    },
}


BIODISTRIBUCIONES = {
    "Radiofármaco A · captación renal predominante": {
        "Riñones": 0.38,
        "Hígado": 0.16,
        "Tumor": 0.28,
        "Resto del cuerpo": 0.18,
    },
    "Radiofármaco B · captación hepática predominante": {
        "Riñones": 0.17,
        "Hígado": 0.42,
        "Tumor": 0.24,
        "Resto del cuerpo": 0.17,
    },
    "Radiofármaco C · alta captación tumoral": {
        "Riñones": 0.18,
        "Hígado": 0.14,
        "Tumor": 0.52,
        "Resto del cuerpo": 0.16,
    },
}


# =============================================================================
# FUNCIONES GENERALES
# =============================================================================

def convertir_a_gy(
    valor: float,
    unidad: str,
) -> float:
    """
    Convierte una dosis seleccionada a Gy.
    """

    factores = {
        "Gy": 1.0,
        "mGy": 1e-3,
        "µGy": 1e-6,
    }

    return valor * factores[unidad]


def convertir_desde_gy(
    valor_gy: float,
    unidad: str,
) -> float:
    """
    Convierte una dosis expresada en Gy a la unidad seleccionada.
    """

    factores = {
        "Gy": 1.0,
        "mGy": 1e3,
        "µGy": 1e6,
    }

    return valor_gy * factores[unidad]


def actividad_exponencial(
    actividad_inicial: float,
    lambda_efectiva: float,
    tiempo,
):
    """
    Actividad en función del tiempo.
    """

    return actividad_inicial * np.exp(
        -lambda_efectiva * tiempo
    )


def calcular_actividad_acumulada_analitica(
    actividad_inicial: float,
    lambda_efectiva: float,
    tiempo_final: float | None = None,
):
    """
    Calcula la actividad acumulada.

    Si tiempo_final es None, integra desde 0 hasta infinito.
    Si se especifica, integra desde 0 hasta tiempo_final.
    """

    if tiempo_final is None:

        return actividad_inicial / lambda_efectiva

    return (
        actividad_inicial
        / lambda_efectiva
        * (
            1
            - math.exp(
                -lambda_efectiva
                * tiempo_final
            )
        )
    )


def calcular_tiempo_efectivo(
    vida_media_fisica: float,
    vida_media_biologica: float,
):
    """
    Calcula la vida media efectiva:

    1 / Tef = 1 / Tf + 1 / Tb
    """

    return (
        vida_media_fisica
        * vida_media_biologica
        / (
            vida_media_fisica
            + vida_media_biologica
        )
    )


# =============================================================================
# PESTAÑAS PRINCIPALES
# =============================================================================

(
    tab_inicio,
    tab_dosis,
    tab_distancia,
    tab_atenuacion,
    tab_kerma,
    tab_actividad,
    tab_residencia,
    tab_mird,
    tab_biodistribucion,
    tab_mision,
) = st.tabs(
    [
        "🏁 Inicio",
        "1️⃣ Dosis y tasa",
        "2️⃣ Fuente puntual",
        "3️⃣ Atenuación y dosis",
        "4️⃣ Kerma y equilibrio",
        "5️⃣ Actividad acumulada",
        "6️⃣ Tiempo de residencia",
        "7️⃣ Metodología MIRD",
        "8️⃣ Biodistribución",
        "🎯 Misión final",
    ]
)


# =============================================================================
# INICIO
# =============================================================================

with tab_inicio:

    st.header("Recorrido del laboratorio")

    st.markdown(
        """
        ## Bloque A · Dosimetría de fuentes externas

        ### Estación 1 · Dosis y tasa de dosis

        Analizarás la relación entre dosis absorbida, tiempo y tasa de dosis.

        ### Estación 2 · Fuente gamma puntual

        Aplicarás la ley del inverso del cuadrado de la distancia.

        ### Estación 3 · Atenuación y dosis

        Calcularás la tasa de dosis y la dosis detrás de un material atenuador.

        ### Estación 4 · Exposición, kerma y dosis

        Diferenciarás las magnitudes y explorarás el concepto de equilibrio
        electrónico.

        ## Bloque B · Dosimetría de fuentes internas

        ### Estación 5 · Actividad acumulada

        Compararás la integración analítica con la integración numérica.

        ### Estación 6 · Tiempo de residencia

        Relacionarás actividad acumulada, actividad administrada y cinética
        biológica.

        ### Estación 7 · Metodología MIRD

        Calcularás dosis absorbida mediante actividad acumulada y factores S.

        ### Estación 8 · Biodistribución

        Compararás cómo distintos radiofármacos modifican la distribución
        de actividad y las dosis en los órganos.

        ### Misión final

        Resolverás un caso de fuente externa y otro de dosimetría interna.
        """
    )


# =============================================================================
# ESTACIÓN 1 · DOSIS Y TASA DE DOSIS
# =============================================================================

with tab_dosis:

    st.header("Estación 1 · Dosis, tasa de dosis y tiempo")

    st.write(
        """
        La dosis absorbida representa energía depositada por unidad de masa.
        La tasa de dosis indica con qué rapidez se entrega esa dosis.
        """
    )

    modo_calculo = st.radio(
        "¿Qué magnitud desea calcular?",
        [
            "Calcular tasa de dosis",
            "Calcular dosis absorbida",
            "Calcular tiempo de exposición",
        ],
        horizontal=True,
    )

    if modo_calculo == "Calcular tasa de dosis":

        columna_1, columna_2, columna_3 = st.columns(3)

        with columna_1:

            dosis_ingresada = st.number_input(
                "Dosis absorbida",
                min_value=0.0,
                value=10.0,
                step=1.0,
            )

        with columna_2:

            unidad_dosis = st.selectbox(
                "Unidad de dosis",
                [
                    "Gy",
                    "mGy",
                    "µGy",
                ],
            )

        with columna_3:

            tiempo_horas = st.number_input(
                "Tiempo de exposición (h)",
                min_value=0.001,
                value=2.0,
                step=0.5,
            )

        dosis_gy = convertir_a_gy(
            dosis_ingresada,
            unidad_dosis,
        )

        tasa_gy_h = (
            dosis_gy
            / tiempo_horas
        )

        tasa_unidad = convertir_desde_gy(
            tasa_gy_h,
            unidad_dosis,
        )

        st.latex(
            r"\dot{D}=\frac{D}{t}"
        )

        st.metric(
            "Tasa de dosis",
            f"{tasa_unidad:.4g} {unidad_dosis}/h",
        )

    elif modo_calculo == "Calcular dosis absorbida":

        columna_1, columna_2, columna_3 = st.columns(3)

        with columna_1:

            tasa_ingresada = st.number_input(
                "Tasa de dosis",
                min_value=0.0,
                value=5.0,
                step=1.0,
            )

        with columna_2:

            unidad_tasa = st.selectbox(
                "Unidad",
                [
                    "Gy",
                    "mGy",
                    "µGy",
                ],
                key="unidad_tasa",
            )

        with columna_3:

            tiempo_horas = st.number_input(
                "Tiempo de exposición (h)",
                min_value=0.0,
                value=2.0,
                step=0.5,
                key="tiempo_dosis",
            )

        tasa_gy_h = convertir_a_gy(
            tasa_ingresada,
            unidad_tasa,
        )

        dosis_calculada_gy = (
            tasa_gy_h
            * tiempo_horas
        )

        dosis_calculada = convertir_desde_gy(
            dosis_calculada_gy,
            unidad_tasa,
        )

        st.latex(
            r"D=\dot{D}\,t"
        )

        st.metric(
            "Dosis absorbida",
            f"{dosis_calculada:.4g} {unidad_tasa}",
        )

    else:

        columna_1, columna_2, columna_3 = st.columns(3)

        with columna_1:

            dosis_objetivo = st.number_input(
                "Dosis objetivo",
                min_value=0.0,
                value=10.0,
                step=1.0,
                key="dosis_objetivo",
            )

        with columna_2:

            tasa_disponible = st.number_input(
                "Tasa de dosis",
                min_value=0.001,
                value=5.0,
                step=1.0,
                key="tasa_disponible",
            )

        with columna_3:

            unidad_tiempo = st.selectbox(
                "Unidad común",
                [
                    "Gy",
                    "mGy",
                    "µGy",
                ],
                key="unidad_tiempo",
            )

        tiempo_requerido = (
            dosis_objetivo
            / tasa_disponible
        )

        st.latex(
            r"t=\frac{D}{\dot{D}}"
        )

        st.metric(
            "Tiempo requerido",
            f"{tiempo_requerido:.4g} h",
        )

    with st.expander("📝 Preguntas de observación"):

        st.markdown(
            """
            1. ¿Qué diferencia existe entre dosis y tasa de dosis?
            2. ¿Puede obtenerse la misma dosis utilizando tasas diferentes?
            3. ¿Qué ocurre con la dosis si se duplica el tiempo?
            4. ¿Por qué es indispensable informar las unidades?
            """
        )


# =============================================================================
# ESTACIÓN 2 · LEY DEL INVERSO DEL CUADRADO
# =============================================================================

with tab_distancia:

    st.header("Estación 2 · Fuente gamma puntual y distancia")

    st.write(
        """
        Para una fuente puntual ideal y sin atenuación, la tasa de kerma
        o de dosis disminuye con el cuadrado de la distancia.
        """
    )

    st.latex(
        r"\dot{K}_{aire}=\frac{\Gamma A}{r^2}"
    )

    columna_1, columna_2, columna_3 = st.columns(3)

    with columna_1:

        actividad_fuente = st.number_input(
            "Actividad de la fuente (GBq)",
            min_value=0.001,
            value=1.0,
            step=0.1,
        )

    with columna_2:

        constante_gamma = st.number_input(
            "Constante gamma (µSv·m² / GBq·h)",
            min_value=0.001,
            value=100.0,
            step=1.0,
            help=(
                "Valor configurable con finalidad didáctica. "
                "Debe sustituirse por el dato correspondiente a la fuente real."
            ),
        )

    with columna_3:

        distancia = st.slider(
            "Distancia a la fuente (m)",
            min_value=0.10,
            max_value=5.00,
            value=1.00,
            step=0.10,
        )

    tasa_distancia = (
        constante_gamma
        * actividad_fuente
        / distancia ** 2
    )

    tiempo_exposicion = st.slider(
        "Tiempo de permanencia (h)",
        min_value=0.0,
        max_value=8.0,
        value=1.0,
        step=0.25,
    )

    dosis_distancia = (
        tasa_distancia
        * tiempo_exposicion
    )

    metrica_1, metrica_2, metrica_3 = st.columns(3)

    metrica_1.metric(
        "Distancia",
        f"{distancia:.2f} m",
    )

    metrica_2.metric(
        "Tasa calculada",
        f"{tasa_distancia:.3f} µSv/h",
    )

    metrica_3.metric(
        "Dosis en el tiempo seleccionado",
        f"{dosis_distancia:.3f} µSv",
    )

    distancias = np.linspace(
        0.10,
        5.0,
        500,
    )

    tasas = (
        constante_gamma
        * actividad_fuente
        / distancias ** 2
    )

    figura_distancia, eje_distancia = plt.subplots(
        figsize=(9, 4.5)
    )

    eje_distancia.plot(
        distancias,
        tasas,
        linewidth=2.7,
        label="Tasa según distancia",
    )

    eje_distancia.scatter(
        [distancia],
        [tasa_distancia],
        s=100,
        zorder=5,
        label="Distancia seleccionada",
    )

    eje_distancia.set_xlabel(
        "Distancia (m)"
    )

    eje_distancia.set_ylabel(
        "Tasa relativa o µSv/h"
    )

    eje_distancia.set_title(
        "Ley del inverso del cuadrado"
    )

    eje_distancia.grid(
        alpha=0.30
    )

    eje_distancia.legend()

    st.pyplot(
        figura_distancia
    )

    st.subheader("Comparación rápida")

    tasa_1m = (
        constante_gamma
        * actividad_fuente
    )

    tabla_distancias = pd.DataFrame(
        {
            "Distancia": [
                "1 m",
                "2 m",
                "3 m",
                "4 m",
            ],
            "Tasa relativa respecto de 1 m": [
                "1",
                "1/4",
                "1/9",
                "1/16",
            ],
            "Tasa calculada (µSv/h)": [
                tasa_1m,
                tasa_1m / 4,
                tasa_1m / 9,
                tasa_1m / 16,
            ],
        }
    )

    st.dataframe(
        tabla_distancias,
        use_container_width=True,
        hide_index=True,
    )

    with st.expander("📝 Preguntas de observación"):

        st.markdown(
            """
            1. ¿Qué ocurre con la tasa al duplicar la distancia?
            2. ¿Por qué no disminuye simplemente a la mitad?
            3. ¿Qué condiciones debe cumplir aproximadamente una fuente puntual?
            4. ¿Qué limitaciones presenta este modelo en una situación real?
            """
        )


# =============================================================================
# ESTACIÓN 3 · ATENUACIÓN Y DOSIS
# =============================================================================

with tab_atenuacion:

    st.header("Estación 3 · Atenuación y dosis detrás de un material")

    st.write(
        """
        En esta estación, la atenuación exponencial se utiliza para calcular
        cómo cambia la tasa de dosis detrás de un material.
        """
    )

    st.latex(
        r"\dot{D}(x)=\dot{D}_0e^{-\mu x}"
    )

    st.latex(
        r"D(x)=\dot{D}(x)\,t"
    )

    columna_1, columna_2, columna_3 = st.columns(3)

    with columna_1:

        tasa_inicial = st.number_input(
            "Tasa inicial (µSv/h)",
            min_value=0.0,
            value=100.0,
            step=10.0,
        )

    with columna_2:

        material = st.selectbox(
            "Material",
            list(
                MATERIALES.keys()
            ),
        )

    with columna_3:

        tiempo_atenuacion = st.number_input(
            "Tiempo de exposición (h)",
            min_value=0.0,
            value=1.0,
            step=0.25,
        )

    mu_material = MATERIALES[
        material
    ]["mu"]

    densidad_material = MATERIALES[
        material
    ]["densidad"]

    mu_masico = (
        mu_material
        / densidad_material
    )

    hvl = (
        math.log(2)
        / mu_material
    )

    maximo_espesor = max(
        5 * hvl,
        0.1,
    )

    espesor = st.slider(
        "Espesor (cm)",
        min_value=0.0,
        max_value=float(
            maximo_espesor
        ),
        value=float(
            min(
                1.0,
                maximo_espesor,
            )
        ),
        step=float(
            max(
                maximo_espesor / 200,
                0.001,
            )
        ),
    )

    transmision = math.exp(
        -mu_material
        * espesor
    )

    tasa_final = (
        tasa_inicial
        * transmision
    )

    dosis_sin_material = (
        tasa_inicial
        * tiempo_atenuacion
    )

    dosis_con_material = (
        tasa_final
        * tiempo_atenuacion
    )

    reduccion_dosis = (
        dosis_sin_material
        - dosis_con_material
    )

    metrica_1, metrica_2, metrica_3, metrica_4 = st.columns(
        4
    )

    metrica_1.metric(
        "μ",
        f"{mu_material:.4g} cm⁻¹",
    )

    metrica_2.metric(
        "μ/ρ",
        f"{mu_masico:.4g} cm²/g",
    )

    metrica_3.metric(
        "HVL",
        f"{hvl:.4g} cm",
    )

    metrica_4.metric(
        "Transmisión",
        f"{100 * transmision:.2f} %",
    )

    metrica_5, metrica_6, metrica_7 = st.columns(
        3
    )

    metrica_5.metric(
        "Dosis sin material",
        f"{dosis_sin_material:.3f} µSv",
    )

    metrica_6.metric(
        "Dosis con material",
        f"{dosis_con_material:.3f} µSv",
    )

    metrica_7.metric(
        "Reducción de dosis",
        f"{reduccion_dosis:.3f} µSv",
    )

    espesores = np.linspace(
        0,
        maximo_espesor,
        400,
    )

    tasas_atenuadas = (
        tasa_inicial
        * np.exp(
            -mu_material
            * espesores
        )
    )

    figura_atenuacion, eje_atenuacion = plt.subplots(
        figsize=(9, 4.5)
    )

    eje_atenuacion.plot(
        espesores,
        tasas_atenuadas,
        linewidth=2.7,
    )

    eje_atenuacion.scatter(
        [espesor],
        [tasa_final],
        s=100,
        zorder=5,
    )

    eje_atenuacion.axvline(
        hvl,
        linestyle="--",
        label="HVL",
    )

    eje_atenuacion.set_xlabel(
        "Espesor (cm)"
    )

    eje_atenuacion.set_ylabel(
        "Tasa de dosis (µSv/h)"
    )

    eje_atenuacion.set_title(
        f"Atenuación de la tasa de dosis en {material}"
    )

    eje_atenuacion.grid(
        alpha=0.30
    )

    eje_atenuacion.legend()

    st.pyplot(
        figura_atenuacion
    )

    st.caption(
        """
        Modelo ideal de haz estrecho y monoenergético. No incorpora
        radiación dispersa, build-up, geometría ni emisión multienergética.
        """
    )


# =============================================================================
# ESTACIÓN 4 · EXPOSICIÓN, KERMA Y EQUILIBRIO ELECTRÓNICO
# =============================================================================

with tab_kerma:

    st.header("Estación 4 · Exposición, kerma, dosis y equilibrio electrónico")

    magnitud = st.selectbox(
        "Seleccioná una magnitud",
        list(
            MAGNITUDES_DOSIMETRICAS.keys()
        ),
    )

    datos_magnitud = MAGNITUDES_DOSIMETRICAS[
        magnitud
    ]

    columna_1, columna_2, columna_3 = st.columns(
        3
    )

    columna_1.metric(
        "Magnitud",
        magnitud,
    )

    columna_2.metric(
        "Unidad SI",
        datos_magnitud["unidad_si"],
    )

    columna_3.metric(
        "Medio de referencia",
        datos_magnitud["medio"],
    )

    st.info(
        datos_magnitud["definicion"]
    )

    st.write(
        f"**Idea central:** {datos_magnitud['idea']}"
    )

    st.markdown("---")

    st.subheader("Equilibrio electrónico")

    estado_equilibrio = st.radio(
        "Seleccioná la situación",
        [
            "Sin equilibrio electrónico",
            "Equilibrio electrónico aproximado",
        ],
        horizontal=True,
    )

    if estado_equilibrio == "Sin equilibrio electrónico":

        electrones_entran = st.slider(
            "Electrones que ingresan al volumen",
            min_value=0,
            max_value=100,
            value=40,
        )

        electrones_salen = st.slider(
            "Electrones que salen del volumen",
            min_value=0,
            max_value=100,
            value=70,
        )

        diferencia = (
            electrones_entran
            - electrones_salen
        )

        st.warning(
            """
            La energía transportada hacia el volumen y la que sale no se
            encuentran compensadas. En esta situación, kerma y dosis
            pueden diferir de forma importante.
            """
        )

    else:

        electrones_equilibrio = st.slider(
            "Cantidad relativa de electrones que ingresan y salen",
            min_value=0,
            max_value=100,
            value=60,
        )

        electrones_entran = electrones_equilibrio
        electrones_salen = electrones_equilibrio
        diferencia = 0

        st.success(
            """
            La energía transportada por partículas cargadas que ingresa
            al volumen es aproximadamente igual a la que sale.
            Bajo condiciones adicionales, la dosis puede aproximarse al kerma.
            """
        )

    tabla_equilibrio = pd.DataFrame(
        {
            "Flujo electrónico": [
                "Electrones que ingresan",
                "Electrones que salen",
            ],
            "Cantidad relativa": [
                electrones_entran,
                electrones_salen,
            ],
        }
    ).set_index(
        "Flujo electrónico"
    )

    st.bar_chart(
        tabla_equilibrio
    )

    st.metric(
        "Diferencia relativa",
        f"{diferencia}",
    )

    st.warning(
        """
        La relación D ≈ K requiere condiciones específicas. No debe
        interpretarse como una igualdad universal.
        """
    )


# =============================================================================
# ESTACIÓN 5 · ACTIVIDAD ACUMULADA
# =============================================================================

with tab_actividad:

    st.header("Estación 5 · Actividad acumulada")

    st.write(
        """
        La actividad acumulada corresponde al área bajo la curva
        actividad-tiempo.
        """
    )

    st.latex(
        r"\widetilde{A}=\int A(t)\,dt"
    )

    columna_1, columna_2, columna_3 = st.columns(
        3
    )

    with columna_1:

        actividad_inicial = st.number_input(
            "Actividad inicial en el órgano (MBq)",
            min_value=0.01,
            value=100.0,
            step=10.0,
        )

    with columna_2:

        vida_media_efectiva = st.number_input(
            "Vida media efectiva (h)",
            min_value=0.01,
            value=20.0,
            step=1.0,
        )

    with columna_3:

        tiempo_final_integracion = st.number_input(
            "Tiempo final de integración (h)",
            min_value=0.1,
            value=100.0,
            step=10.0,
        )

    lambda_efectiva = (
        math.log(2)
        / vida_media_efectiva
    )

    actividad_acumulada_infinita = calcular_actividad_acumulada_analitica(
        actividad_inicial,
        lambda_efectiva,
        None,
    )

    actividad_acumulada_finita = calcular_actividad_acumulada_analitica(
        actividad_inicial,
        lambda_efectiva,
        tiempo_final_integracion,
    )

    cantidad_puntos = st.slider(
        "Cantidad de mediciones para integración numérica",
        min_value=3,
        max_value=20,
        value=6,
        step=1,
    )

    tiempos_medicion = np.linspace(
        0,
        tiempo_final_integracion,
        cantidad_puntos,
    )

    actividades_medidas = actividad_exponencial(
        actividad_inicial,
        lambda_efectiva,
        tiempos_medicion,
    )

   actividad_acumulada_numerica = np.trapezoid(
    actividades_medidas,
    tiempos_medicion,
)

    error_numerico = (
        100
        * abs(
            actividad_acumulada_numerica
            - actividad_acumulada_finita
        )
        / actividad_acumulada_finita
    )

    metrica_1, metrica_2, metrica_3 = st.columns(
        3
    )

    metrica_1.metric(
        "Integral analítica hasta tiempo final",
        f"{actividad_acumulada_finita:.2f} MBq·h",
    )

    metrica_2.metric(
        "Integral numérica",
        f"{actividad_acumulada_numerica:.2f} MBq·h",
    )

    metrica_3.metric(
        "Diferencia relativa",
        f"{error_numerico:.2f} %",
    )

    st.metric(
        "Actividad acumulada hasta infinito",
        f"{actividad_acumulada_infinita:.2f} MBq·h",
    )

    tiempos_curva = np.linspace(
        0,
        tiempo_final_integracion,
        500,
    )

    actividades_curva = actividad_exponencial(
        actividad_inicial,
        lambda_efectiva,
        tiempos_curva,
    )

    figura_actividad, eje_actividad = plt.subplots(
        figsize=(9, 4.8)
    )

    eje_actividad.plot(
        tiempos_curva,
        actividades_curva,
        linewidth=2.7,
        label="Curva actividad-tiempo",
    )

    eje_actividad.scatter(
        tiempos_medicion,
        actividades_medidas,
        s=80,
        zorder=5,
        label="Mediciones simuladas",
    )

    eje_actividad.fill_between(
        tiempos_curva,
        actividades_curva,
        alpha=0.25,
        label="Actividad acumulada",
    )

    eje_actividad.set_xlabel(
        "Tiempo (h)"
    )

    eje_actividad.set_ylabel(
        "Actividad (MBq)"
    )

    eje_actividad.set_title(
        "Área bajo la curva actividad-tiempo"
    )

    eje_actividad.grid(
        alpha=0.30
    )

    eje_actividad.legend()

    st.pyplot(
        figura_actividad
    )

    st.info(
        """
        Al aumentar la cantidad de mediciones, la integración numérica
        generalmente se aproxima mejor al valor analítico de la curva ideal.
        """
    )


# =============================================================================
# ESTACIÓN 6 · TIEMPO DE RESIDENCIA
# =============================================================================

with tab_residencia:

    st.header("Estación 6 · Vida media efectiva y tiempo de residencia")

    columna_1, columna_2 = st.columns(
        2
    )

    with columna_1:

        vida_media_fisica = st.number_input(
            "Vida media física (h)",
            min_value=0.01,
            value=160.0,
            step=10.0,
        )

    with columna_2:

        vida_media_biologica = st.number_input(
            "Vida media biológica (h)",
            min_value=0.01,
            value=80.0,
            step=10.0,
        )

    vida_media_efectiva_calculada = calcular_tiempo_efectivo(
        vida_media_fisica,
        vida_media_biologica,
    )

    lambda_efectiva_residencia = (
        math.log(2)
        / vida_media_efectiva_calculada
    )

    actividad_administrada = st.number_input(
        "Actividad administrada A₀ (MBq)",
        min_value=0.01,
        value=7400.0,
        step=100.0,
    )

    fraccion_captacion = st.slider(
        "Fracción inicial captada por el órgano (%)",
        min_value=0.0,
        max_value=100.0,
        value=10.0,
        step=1.0,
    )

    actividad_inicial_organo = (
        actividad_administrada
        * fraccion_captacion
        / 100
    )

    actividad_acumulada_organo = (
        actividad_inicial_organo
        / lambda_efectiva_residencia
    )

    tiempo_residencia = (
        actividad_acumulada_organo
        / actividad_administrada
    )

    metrica_1, metrica_2, metrica_3 = st.columns(
        3
    )

    metrica_1.metric(
        "Vida media efectiva",
        f"{vida_media_efectiva_calculada:.2f} h",
    )

    metrica_2.metric(
        "Actividad acumulada en el órgano",
        f"{actividad_acumulada_organo:.2f} MBq·h",
    )

    metrica_3.metric(
        "Tiempo de residencia",
        f"{tiempo_residencia:.3f} h",
    )

    st.latex(
        r"\frac{1}{T_{\mathrm{ef}}}="
        r"\frac{1}{T_{\mathrm{fís}}}+"
        r"\frac{1}{T_{\mathrm{bio}}}"
    )

    st.latex(
        r"\tau=\frac{\widetilde{A}}{A_0}"
    )

    st.info(
        """
        El tiempo de residencia depende tanto de la actividad acumulada
        en la región fuente como de la actividad administrada al paciente.
        No es equivalente a la vida media física.
        """
    )


# =============================================================================
# ESTACIÓN 7 · METODOLOGÍA MIRD
# =============================================================================

with tab_mird:

    st.header("Estación 7 · Cálculo simplificado mediante metodología MIRD")

    st.write(
        """
        En el formalismo MIRD, la dosis promedio en un órgano blanco
        se obtiene sumando las contribuciones de las regiones fuente.
        """
    )

    st.latex(
        r"D(r_T)=\sum_{r_S}\widetilde{A}(r_S)"
        r"\,S(r_T\leftarrow r_S)"
    )

    st.subheader("Contribución de tres regiones fuente")

    columna_1, columna_2, columna_3 = st.columns(
        3
    )

    with columna_1:

        st.markdown("### Fuente 1 · Órgano blanco")

        actividad_acumulada_1 = st.number_input(
            "Actividad acumulada 1 (MBq·h)",
            min_value=0.0,
            value=1000.0,
            step=100.0,
        )

        factor_s_1 = st.number_input(
            "Factor S 1 (mGy / MBq·h)",
            min_value=0.0,
            value=0.0020,
            step=0.0001,
            format="%.4f",
        )

    with columna_2:

        st.markdown("### Fuente 2 · Órgano vecino")

        actividad_acumulada_2 = st.number_input(
            "Actividad acumulada 2 (MBq·h)",
            min_value=0.0,
            value=500.0,
            step=100.0,
        )

        factor_s_2 = st.number_input(
            "Factor S 2 (mGy / MBq·h)",
            min_value=0.0,
            value=0.0004,
            step=0.0001,
            format="%.4f",
        )

    with columna_3:

        st.markdown("### Fuente 3 · Resto del cuerpo")

        actividad_acumulada_3 = st.number_input(
            "Actividad acumulada 3 (MBq·h)",
            min_value=0.0,
            value=2000.0,
            step=100.0,
        )

        factor_s_3 = st.number_input(
            "Factor S 3 (mGy / MBq·h)",
            min_value=0.0,
            value=0.00005,
            step=0.00001,
            format="%.5f",
        )

    dosis_1 = (
        actividad_acumulada_1
        * factor_s_1
    )

    dosis_2 = (
        actividad_acumulada_2
        * factor_s_2
    )

    dosis_3 = (
        actividad_acumulada_3
        * factor_s_3
    )

    dosis_total_mgy = (
        dosis_1
        + dosis_2
        + dosis_3
    )

    dosis_total_gy = (
        dosis_total_mgy
        / 1000
    )

    tabla_mird = pd.DataFrame(
        {
            "Región fuente": [
                "Órgano blanco",
                "Órgano vecino",
                "Resto del cuerpo",
            ],
            "Actividad acumulada (MBq·h)": [
                actividad_acumulada_1,
                actividad_acumulada_2,
                actividad_acumulada_3,
            ],
            "Factor S (mGy/MBq·h)": [
                factor_s_1,
                factor_s_2,
                factor_s_3,
            ],
            "Contribución a la dosis (mGy)": [
                dosis_1,
                dosis_2,
                dosis_3,
            ],
        }
    )

    st.dataframe(
        tabla_mird,
        use_container_width=True,
        hide_index=True,
    )

    metrica_1, metrica_2 = st.columns(
        2
    )

    metrica_1.metric(
        "Dosis total",
        f"{dosis_total_mgy:.3f} mGy",
    )

    metrica_2.metric(
        "Dosis total",
        f"{dosis_total_gy:.6f} Gy",
    )

    tabla_contribuciones = tabla_mird[
        [
            "Región fuente",
            "Contribución a la dosis (mGy)",
        ]
    ].set_index(
        "Región fuente"
    )

    st.bar_chart(
        tabla_contribuciones
    )

    st.warning(
        """
        Los factores S dependen del radionúclido, la región fuente,
        el órgano blanco y el modelo anatómico utilizado. Los valores
        de esta estación son configurables y únicamente didácticos.
        """
    )


# =============================================================================
# ESTACIÓN 8 · BIODISTRIBUCIÓN
# =============================================================================

with tab_biodistribucion:

    st.header("Estación 8 · Mismo radionúclido, distinta biodistribución")

    st.write(
        """
        La dosis interna no depende únicamente del radionúclido.
        La molécula transportadora modifica la captación, retención
        y eliminación en cada tejido.
        """
    )

    radiofarmaco = st.selectbox(
        "Seleccioná una biodistribución conceptual",
        list(
            BIODISTRIBUCIONES.keys()
        ),
    )

    distribucion = BIODISTRIBUCIONES[
        radiofarmaco
    ]

    actividad_total_acumulada = st.number_input(
        "Actividad acumulada total disponible (MBq·h)",
        min_value=0.0,
        value=5000.0,
        step=500.0,
    )

    factor_s_comun = st.number_input(
        "Factor S didáctico común (mGy / MBq·h)",
        min_value=0.0,
        value=0.001,
        step=0.0001,
        format="%.4f",
    )

    filas = []

    for organo, fraccion in distribucion.items():

        actividad_organo = (
            actividad_total_acumulada
            * fraccion
        )

        dosis_organo = (
            actividad_organo
            * factor_s_comun
        )

        filas.append(
            {
                "Órgano o región": organo,
                "Fracción acumulada (%)": 100 * fraccion,
                "Actividad acumulada (MBq·h)": actividad_organo,
                "Dosis conceptual (mGy)": dosis_organo,
            }
        )

    tabla_biodistribucion = pd.DataFrame(
        filas
    )

    st.dataframe(
        tabla_biodistribucion,
        use_container_width=True,
        hide_index=True,
    )

    grafico_biodistribucion = tabla_biodistribucion[
        [
            "Órgano o región",
            "Actividad acumulada (MBq·h)",
        ]
    ].set_index(
        "Órgano o región"
    )

    st.bar_chart(
        grafico_biodistribucion
    )

    st.info(
        """
        Aunque se mantenga el mismo radionúclido, cambiar el radiofármaco
        puede modificar considerablemente la actividad acumulada y la dosis
        en cada órgano.
        """
    )


# =============================================================================
# MISIÓN FINAL
# =============================================================================

with tab_mision:

    st.header("🎯 Misión final · Dosimetría externa e interna")

    tab_mision_externa, tab_mision_interna = st.tabs(
        [
            "Parte A · Fuente externa",
            "Parte B · Fuente interna",
        ]
    )

    # -------------------------------------------------------------------------
    # MISIÓN EXTERNA
    # -------------------------------------------------------------------------

    with tab_mision_externa:

        st.subheader("Caso de exposición externa")

        st.markdown(
            """
            Una fuente gamma puntual se encuentra en una sala de trabajo.
            Se desea calcular la tasa de dosis y la dosis recibida por un
            trabajador situado detrás de un material atenuador.
            """
        )

        columna_1, columna_2, columna_3 = st.columns(
            3
        )

        with columna_1:

            actividad_ext = st.number_input(
                "Actividad (GBq)",
                min_value=0.001,
                value=2.0,
                step=0.1,
                key="actividad_ext",
            )

            gamma_ext = st.number_input(
                "Constante gamma (µSv·m²/GBq·h)",
                min_value=0.001,
                value=100.0,
                step=1.0,
                key="gamma_ext",
            )

        with columna_2:

            distancia_ext = st.number_input(
                "Distancia (m)",
                min_value=0.1,
                value=2.0,
                step=0.1,
                key="distancia_ext",
            )

            tiempo_ext = st.number_input(
                "Tiempo de permanencia (h)",
                min_value=0.0,
                value=1.0,
                step=0.25,
                key="tiempo_ext",
            )

        with columna_3:

            material_ext = st.selectbox(
                "Material",
                list(
                    MATERIALES.keys()
                ),
                key="material_ext",
            )

            espesor_ext = st.number_input(
                "Espesor (cm)",
                min_value=0.0,
                value=1.0,
                step=0.1,
                key="espesor_ext",
            )

        tasa_sin_blindaje = (
            gamma_ext
            * actividad_ext
            / distancia_ext ** 2
        )

        mu_ext = MATERIALES[
            material_ext
        ]["mu"]

        transmision_ext = math.exp(
            -mu_ext
            * espesor_ext
        )

        tasa_con_blindaje = (
            tasa_sin_blindaje
            * transmision_ext
        )

        dosis_ext = (
            tasa_con_blindaje
            * tiempo_ext
        )

        metrica_1, metrica_2, metrica_3 = st.columns(
            3
        )

        metrica_1.metric(
            "Tasa sin material",
            f"{tasa_sin_blindaje:.3f} µSv/h",
        )

        metrica_2.metric(
            "Tasa detrás del material",
            f"{tasa_con_blindaje:.3f} µSv/h",
        )

        metrica_3.metric(
            "Dosis durante la permanencia",
            f"{dosis_ext:.3f} µSv",
        )

        st.subheader("Consigna")

        st.markdown(
            f"""
            1. Explique cómo influyó la distancia de **{distancia_ext:.2f} m**.

            2. Interprete la transmisión de **{100 * transmision_ext:.2f} %**.

            3. Compare la tasa antes y después del material.

            4. Analice cómo cambiaría la dosis si se duplicara el tiempo.

            5. Señale las limitaciones de considerar una fuente puntual,
            monoenergética y sin dispersión.
            """
        )

    # -------------------------------------------------------------------------
    # MISIÓN INTERNA
    # -------------------------------------------------------------------------

    with tab_mision_interna:

        st.subheader("Caso de dosimetría interna")

        st.markdown(
            """
            Se administró un radiofármaco y se estimó una curva exponencial
            de actividad en un órgano fuente.
            """
        )

        columna_1, columna_2, columna_3 = st.columns(
            3
        )

        with columna_1:

            actividad_administrada_mision = st.number_input(
                "Actividad administrada (MBq)",
                min_value=0.01,
                value=7400.0,
                step=100.0,
                key="actividad_administrada_mision",
            )

        with columna_2:

            actividad_organo_mision = st.number_input(
                "Actividad inicial en el órgano (MBq)",
                min_value=0.01,
                value=740.0,
                step=10.0,
                key="actividad_organo_mision",
            )

        with columna_3:

            vida_media_efectiva_mision = st.number_input(
                "Vida media efectiva en el órgano (h)",
                min_value=0.01,
                value=50.0,
                step=5.0,
                key="vida_media_efectiva_mision",
            )

        factor_s_mision = st.number_input(
            "Factor S (mGy / MBq·h)",
            min_value=0.0,
            value=0.0015,
            step=0.0001,
            format="%.4f",
            key="factor_s_mision",
        )

        lambda_mision = (
            math.log(2)
            / vida_media_efectiva_mision
        )

        actividad_acumulada_mision = (
            actividad_organo_mision
            / lambda_mision
        )

        tiempo_residencia_mision = (
            actividad_acumulada_mision
            / actividad_administrada_mision
        )

        dosis_mird_mision = (
            actividad_acumulada_mision
            * factor_s_mision
        )

        metrica_1, metrica_2, metrica_3 = st.columns(
            3
        )

        metrica_1.metric(
            "Actividad acumulada",
            f"{actividad_acumulada_mision:.2f} MBq·h",
        )

        metrica_2.metric(
            "Tiempo de residencia",
            f"{tiempo_residencia_mision:.3f} h",
        )

        metrica_3.metric(
            "Dosis absorbida",
            f"{dosis_mird_mision:.3f} mGy",
        )

        st.subheader("Consigna")

        st.markdown(
            f"""
            1. Explique qué representa la actividad acumulada de
            **{actividad_acumulada_mision:.2f} MBq·h**.

            2. Interprete el tiempo de residencia obtenido.

            3. Describa cómo se utilizó el factor S para calcular la dosis.

            4. Analice qué ocurriría si la vida media biológica fuera menor.

            5. Explique por qué la dosis cambiaría si el mismo radionúclido
            estuviera unido a otro radiofármaco.

            6. Señale al menos tres simplificaciones del modelo utilizado.
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
