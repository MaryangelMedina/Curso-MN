# -*- coding: utf-8 -*-
"""
Laboratorio Virtual Nº 4
Interacción de la Radiación con la Materia

Curso de Metodología y Aplicación de Radioisótopos
Disertante: Dr. Roberto Isoardi

IMPORTANTE:
Los coeficientes y modelos utilizados tienen finalidad educativa.
No deben utilizarse para cálculos clínicos, dosimétricos,
regulatorios o para diseño real de blindajes.
"""

import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st


# =============================================================================
# CONFIGURACIÓN GENERAL DE LA APLICACIÓN
# =============================================================================

st.set_page_config(
    page_title="Laboratorio Virtual - Unidad 4",
    page_icon="🧪",
    layout="wide",
)

st.title("🧪 Laboratorio Virtual Nº 4")
st.header("Interacción de la Radiación con la Materia")

st.markdown(
    """
    **Unidad Nº 4**  
    **Disertante:** Dr. Roberto Isoardi  
    **Duración estimada:** 6 horas
    """
)

st.write(
    """
    En este laboratorio analizaremos cómo las partículas cargadas y los fotones
    interactúan con distintos materiales. Modificá las variables de cada estación
    y observá los cambios en tiempo real.
    """
)

st.warning(
    """
    ⚠️ **Uso educativo:** los valores y modelos de esta aplicación son
    aproximaciones didácticas. No reemplazan tablas de coeficientes validadas,
    cálculos dosimétricos ni evaluaciones regulatorias.
    """
)

st.markdown("---")


# =============================================================================
# BASE DE DATOS DIDÁCTICA
# =============================================================================

MATERIALES = {
    "Aire": {
        "densidad": 0.001225,
        "z_efectivo": 7.6,
    },
    "Agua": {
        "densidad": 1.00,
        "z_efectivo": 7.4,
    },
    "Aluminio": {
        "densidad": 2.70,
        "z_efectivo": 13.0,
    },
    "Hormigón": {
        "densidad": 2.30,
        "z_efectivo": 13.0,
    },
    "Plomo": {
        "densidad": 11.34,
        "z_efectivo": 82.0,
    },
}


# Coeficientes lineales aproximados μ en cm⁻¹.
# Se utilizan exclusivamente como valores didácticos.
DATOS_ATENUACION = {
    "Tecnecio-99m (99mTc) · 140 keV": {
        "energia": 140.0,
        "mu": {
            "Aire": 0.00018,
            "Agua": 0.154,
            "Aluminio": 0.40,
            "Hormigón": 0.32,
            "Plomo": 23.0,
        },
    },
    "Lutecio-177 (177Lu) · 208 keV": {
        "energia": 208.0,
        "mu": {
            "Aire": 0.00015,
            "Agua": 0.137,
            "Aluminio": 0.32,
            "Hormigón": 0.25,
            "Plomo": 10.9,
        },
    },
    "Yodo-131 (131I) · 364 keV": {
        "energia": 364.0,
        "mu": {
            "Aire": 0.00012,
            "Agua": 0.111,
            "Aluminio": 0.25,
            "Hormigón": 0.18,
            "Plomo": 2.30,
        },
    },
    "Galio-68 (68Ga) · 511 keV": {
        "energia": 511.0,
        "mu": {
            "Aire": 0.000105,
            "Agua": 0.096,
            "Aluminio": 0.23,
            "Hormigón": 0.15,
            "Plomo": 1.70,
        },
    },
}


COLIMADORES = {
    "LEHR": {
        "nombre": "Low Energy High Resolution",
        "categoria": "Baja energía",
        "resolucion": 92,
        "sensibilidad": 42,
        "proteccion_septal": 30,
        "descripcion": (
            "Colimador de baja energía que prioriza la resolución espacial. "
            "Se utiliza cuando se desean imágenes con buen detalle."
        ),
    },
    "LEGP": {
        "nombre": "Low Energy General Purpose",
        "categoria": "Baja energía",
        "resolucion": 70,
        "sensibilidad": 72,
        "proteccion_septal": 35,
        "descripcion": (
            "Colimador de propósito general para fotones de baja energía. "
            "Equilibra resolución espacial y sensibilidad."
        ),
    },
    "MEGP": {
        "nombre": "Medium Energy General Purpose",
        "categoria": "Energía media",
        "resolucion": 55,
        "sensibilidad": 55,
        "proteccion_septal": 76,
        "descripcion": (
            "Posee septos más gruesos para reducir la penetración de fotones "
            "de energía media."
        ),
    },
    "HEGP": {
        "nombre": "High Energy General Purpose",
        "categoria": "Alta energía",
        "resolucion": 40,
        "sensibilidad": 35,
        "proteccion_septal": 95,
        "descripcion": (
            "Diseñado para fotones de alta energía. Sus septos son más largos "
            "y gruesos para limitar la penetración septal."
        ),
    },
}


# =============================================================================
# FUNCIONES DE CÁLCULO
# =============================================================================

def calcular_alcance_particula(
    particula: str,
    energia_mev: float,
    material: str,
) -> float:
    """
    Estima de manera didáctica el alcance de una partícula cargada.

    El resultado se expresa en centímetros y permite comparar tendencias.
    No debe interpretarse como un cálculo dosimétrico exacto.
    """

    densidad = MATERIALES[material]["densidad"]

    if particula == "Alfa (α)":
        alcance_en_agua = 0.00056 * energia_mev ** 1.5

    elif particula in ("Beta negativa (β−)", "Beta positiva (β+)"):
        alcance_en_agua = max(
            0.001,
            0.412 * energia_mev ** 1.265 - 0.0954,
        )

    else:  # Protón
        alcance_en_agua = 0.0022 * energia_mev ** 1.77

    alcance_material = alcance_en_agua / max(densidad, 1e-9)

    return min(alcance_material, 5000.0)


def calcular_perfil_perdida(
    particula: str,
    cantidad_puntos: int = 400,
):
    """
    Genera un perfil normalizado de pérdida de energía.

    Para alfa y protones se representa cualitativamente un aumento
    de la deposición hacia el final del recorrido.

    Para beta se representa una pérdida más irregular.
    """

    profundidad = np.linspace(0, 1, cantidad_puntos)

    if particula in ("Alfa (α)", "Protón"):
        perdida = (
            0.20
            + 0.80
            / np.sqrt(
                np.maximum(
                    1 - 0.965 * profundidad,
                    0.025,
                )
            )
        )

    else:
        perdida = (
            np.exp(-1.45 * profundidad)
            * (
                1
                + 0.18
                * np.sin(14 * profundidad) ** 2
            )
        )

    perdida = perdida / perdida.max()

    return profundidad, perdida


def calcular_procesos_particula(
    particula: str,
    material: str,
    energia_mev: float,
):
    """
    Devuelve porcentajes conceptuales para visualizar los procesos
    de interacción de partículas cargadas.
    """

    z = MATERIALES[material]["z_efectivo"]

    if particula in ("Alfa (α)", "Protón"):

        colisiones_suaves = 58.0
        colisiones_fuertes = 37.0
        campo_nuclear = 5.0
        bremsstrahlung = 0.0

    else:

        bremsstrahlung = min(
            45.0,
            0.50 * z * math.log1p(energia_mev),
        )

        campo_nuclear = 18.0 + min(
            20.0,
            z / 5.0,
        )

        colisiones_fuertes = 24.0

        colisiones_suaves = max(
            5.0,
            100.0
            - bremsstrahlung
            - campo_nuclear
            - colisiones_fuertes,
        )

    valores = np.array(
        [
            colisiones_suaves,
            colisiones_fuertes,
            campo_nuclear,
            bremsstrahlung,
        ],
        dtype=float,
    )

    valores = 100.0 * valores / valores.sum()

    return valores


def calcular_predominancia_foton(
    energia_kev: float,
    material: str,
):
    """
    Modelo conceptual para representar la predominancia relativa
    del efecto fotoeléctrico, Compton y producción de pares.

    No representa probabilidades tabuladas reales.
    """

    z = MATERIALES[material]["z_efectivo"]
    energia_mev = energia_kev / 1000.0

    fotoelectrico = (
        (z / 10.0) ** 3.7
        / max(
            energia_mev ** 3.1,
            1e-6,
        )
    )

    compton = (
        7.5
        * (z / 10.0)
        / (
            1
            + 1.5 * energia_mev
        )
    )

    if energia_mev <= 1.022:
        produccion_pares = 0.0

    else:
        produccion_pares = (
            4.0
            * (z / 10.0) ** 2
            * math.log1p(
                (energia_mev - 1.022)
                * 3.5
            )
        )

    valores = np.array(
        [
            fotoelectrico,
            compton,
            produccion_pares,
        ],
        dtype=float,
    )

    valores = np.maximum(
        valores,
        0,
    )

    valores = (
        100.0
        * valores
        / valores.sum()
    )

    return valores


def calcular_energia_compton(
    energia_inicial_kev: float,
    angulo_grados: float,
) -> float:
    """
    Calcula la energía del fotón dispersado mediante la ecuación de Compton.
    """

    angulo_radianes = math.radians(
        angulo_grados
    )

    energia_dispersada = (
        energia_inicial_kev
        / (
            1
            + (
                energia_inicial_kev
                / 511.0
            )
            * (
                1
                - math.cos(
                    angulo_radianes
                )
            )
        )
    )

    return energia_dispersada


# =============================================================================
# FUNCIONES DE VISUALIZACIÓN
# =============================================================================

def dibujar_interaccion_foton(
    tipo_interaccion: str,
    energia_kev: float,
    angulo_grados: float,
):
    """
    Dibuja un esquema didáctico simple del efecto seleccionado.
    """

    figura, eje = plt.subplots(
        figsize=(8, 4.5)
    )

    eje.set_xlim(
        0,
        10,
    )

    eje.set_ylim(
        -3.5,
        3.5,
    )

    eje.axis("off")

    # Núcleo
    nucleo = plt.Circle(
        (6.2, 0),
        0.42,
        alpha=0.85,
    )

    eje.add_patch(
        nucleo
    )

    # Capas electrónicas
    for radio in (
        1.0,
        1.7,
        2.3,
    ):

        orbita = plt.Circle(
            (6.2, 0),
            radio,
            fill=False,
            alpha=0.30,
        )

        eje.add_patch(
            orbita
        )

    # Electrones
    eje.scatter(
        [5.2, 7.3, 6.2],
        [0, 1.3, -2.3],
        s=45,
    )

    # Fotón incidente
    eje.annotate(
        "",
        xy=(4.8, 0),
        xytext=(0.5, 0),
        arrowprops=dict(
            arrowstyle="->",
            linewidth=2.5,
        ),
    )

    eje.text(
        1.3,
        0.40,
        "Fotón incidente",
        fontsize=11,
    )

    if tipo_interaccion == "Efecto fotoeléctrico":

        eje.annotate(
            "",
            xy=(8.9, 2.4),
            xytext=(6.0, 0.2),
            arrowprops=dict(
                arrowstyle="->",
                linewidth=2.5,
            ),
        )

        eje.text(
            8.0,
            2.75,
            "Fotoelectrón",
            ha="center",
            fontsize=11,
        )

        eje.text(
            3.6,
            -3.0,
            "El fotón es absorbido completamente.",
            fontsize=11,
        )

    elif tipo_interaccion == "Efecto Compton":

        angulo_radianes = math.radians(
            angulo_grados
        )

        final_x = (
            6.0
            + 3.0
            * math.cos(
                angulo_radianes
            )
        )

        final_y = (
            3.0
            * math.sin(
                angulo_radianes
            )
        )

        eje.annotate(
            "",
            xy=(final_x, final_y),
            xytext=(6.0, 0),
            arrowprops=dict(
                arrowstyle="->",
                linewidth=2.5,
            ),
        )

        eje.text(
            final_x,
            final_y + 0.35,
            "Fotón dispersado",
            ha="center",
            fontsize=10,
        )

        eje.annotate(
            "",
            xy=(8.7, -2.0),
            xytext=(6.0, 0),
            arrowprops=dict(
                arrowstyle="->",
                linewidth=2.5,
            ),
        )

        eje.text(
            8.0,
            -2.40,
            "Electrón de retroceso",
            ha="center",
            fontsize=10,
        )

    else:

        eje.annotate(
            "",
            xy=(8.7, 1.8),
            xytext=(6.0, 0),
            arrowprops=dict(
                arrowstyle="->",
                linewidth=2.5,
            ),
        )

        eje.annotate(
            "",
            xy=(8.7, -1.8),
            xytext=(6.0, 0),
            arrowprops=dict(
                arrowstyle="->",
                linewidth=2.5,
            ),
        )

        eje.text(
            8.7,
            2.15,
            "Electrón (e−)",
            ha="center",
            fontsize=10,
        )

        eje.text(
            8.7,
            -2.20,
            "Positrón (e+)",
            ha="center",
            fontsize=10,
        )

        eje.text(
            3.9,
            -3.0,
            "Energía mínima: 1022 keV",
            fontsize=11,
        )

    eje.set_title(
        f"{tipo_interaccion} · Energía: {energia_kev:.0f} keV"
    )

    return figura


# =============================================================================
# PESTAÑAS PRINCIPALES
# =============================================================================

tab_inicio, tab_particulas, tab_fotones, tab_atenuacion, tab_colimadores, tab_mision = st.tabs(
    [
        "🏁 Inicio",
        "1️⃣ Partículas cargadas",
        "2️⃣ Interacción de fotones",
        "3️⃣ Atenuación",
        "4️⃣ Colimadores",
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
        ### Estación 1: partículas cargadas

        Compararás el alcance, la ionización, la trayectoria y los mecanismos
        de pérdida de energía de partículas alfa, beta y protones.

        ### Estación 2: interacción de fotones

        Visualizarás los efectos fotoeléctrico y Compton, además de la
        producción de pares.

        ### Estación 3: atenuación

        Aplicarás la ley exponencial y calcularás:

        - coeficiente de atenuación lineal;
        - coeficiente de atenuación másico;
        - transmisión;
        - semiespesor o HVL;
        - TVL.

        ### Estación 4: colimadores

        Analizarás el compromiso entre:

        - resolución;
        - sensibilidad;
        - penetración septal.

        ### Misión final

        Resolverás un caso integrador relacionado con Medicina Nuclear.
        """
    )


# =============================================================================
# ESTACIÓN 1: PARTÍCULAS CARGADAS
# =============================================================================

with tab_particulas:

    st.header(
        "Estación 1 · Interacción de partículas cargadas"
    )

    st.write(
        """
        Las partículas cargadas interactúan continuamente con los electrones
        y núcleos de los átomos del medio. Seleccioná una partícula y observá
        cómo cambia su comportamiento.
        """
    )

    columna_1, columna_2, columna_3 = st.columns(
        3
    )

    with columna_1:

        particula = st.selectbox(
            "Tipo de partícula",
            [
                "Alfa (α)",
                "Beta negativa (β−)",
                "Beta positiva (β+)",
                "Protón",
            ],
        )

    with columna_2:

        if particula == "Protón":

            energia_maxima = 150.0
            energia_predeterminada = 50.0

        elif particula == "Alfa (α)":

            energia_maxima = 10.0
            energia_predeterminada = 5.0

        else:

            energia_maxima = 10.0
            energia_predeterminada = 1.0

        energia_particula = st.slider(
            "Energía cinética (MeV)",
            min_value=0.1,
            max_value=energia_maxima,
            value=energia_predeterminada,
            step=0.1,
        )

    with columna_3:

        material_particula = st.selectbox(
            "Material atravesado",
            [
                "Aire",
                "Agua",
                "Aluminio",
                "Plomo",
            ],
        )

    alcance = calcular_alcance_particula(
        particula,
        energia_particula,
        material_particula,
    )

    if particula == "Alfa (α)":

        ionizacion = "Muy alta"
        trayectoria = "Corta y casi rectilínea"
        dispersion = "Baja"

    elif particula == "Protón":

        ionizacion = "Alta"
        trayectoria = "Relativamente definida"
        dispersion = "Baja a intermedia"

    elif particula == "Beta positiva (β+)":

        ionizacion = "Intermedia"
        trayectoria = "Tortuosa"
        dispersion = "Alta"

    else:

        ionizacion = "Intermedia"
        trayectoria = "Tortuosa"
        dispersion = "Alta"

    metrica_1, metrica_2, metrica_3, metrica_4 = st.columns(
        4
    )

    metrica_1.metric(
        "Alcance aproximado",
        f"{alcance:.4g} cm",
    )

    metrica_2.metric(
        "Ionización específica",
        ionizacion,
    )

    metrica_3.metric(
        "Trayectoria",
        trayectoria,
    )

    metrica_4.metric(
        "Dispersión",
        dispersion,
    )

    avance_particula = st.slider(
        "Avance visual de la partícula (%)",
        min_value=0,
        max_value=100,
        value=55,
        step=1,
    )

    profundidad_normalizada, perdida_relativa = calcular_perfil_perdida(
        particula
    )

    profundidad_cm = (
        profundidad_normalizada
        * alcance
    )

    posicion_actual = (
        alcance
        * avance_particula
        / 100.0
    )

    columna_grafico, columna_procesos = st.columns(
        [1.4, 1]
    )

    with columna_grafico:

        st.subheader(
            "Pérdida de energía durante el recorrido"
        )

        figura_1, eje_1 = plt.subplots(
            figsize=(8, 4.3)
        )

        eje_1.plot(
            profundidad_cm,
            perdida_relativa,
            linewidth=2.7,
            label="Pérdida de energía relativa",
        )

        eje_1.axvline(
            posicion_actual,
            linestyle="--",
            linewidth=2,
            label="Posición actual",
        )

        eje_1.fill_between(
            profundidad_cm,
            0,
            perdida_relativa,
            where=profundidad_cm <= posicion_actual,
            alpha=0.25,
        )

        eje_1.set_xlabel(
            "Profundidad recorrida (cm)"
        )

        eje_1.set_ylabel(
            "Pérdida de energía relativa"
        )

        eje_1.set_title(
            f"{particula} en {material_particula}"
        )

        eje_1.grid(
            alpha=0.30
        )

        eje_1.legend()

        st.pyplot(
            figura_1
        )

    with columna_procesos:

        st.subheader(
            "Procesos de interacción"
        )

        contribuciones = calcular_procesos_particula(
            particula,
            material_particula,
            energia_particula,
        )

        tabla_procesos = pd.DataFrame(
            {
                "Proceso": [
                    "Colisiones suaves",
                    "Colisiones fuertes",
                    "Interacción con el campo nuclear",
                    "Radiación de frenado",
                ],
                "Contribución conceptual (%)": contribuciones,
            }
        )

        tabla_procesos = tabla_procesos.set_index(
            "Proceso"
        )

        st.bar_chart(
            tabla_procesos
        )

    if particula == "Beta positiva (β+)":

        st.info(
            """
            El positrón pierde energía mediante interacciones coulombianas.
            Cuando alcanza energías bajas puede aniquilarse con un electrón,
            generando dos fotones de 511 keV.
            """
        )

    if (
        particula
        in (
            "Beta negativa (β−)",
            "Beta positiva (β+)",
        )
        and material_particula == "Plomo"
    ):

        st.warning(
            """
            En materiales de número atómico elevado aumenta la importancia
            relativa de la radiación de frenado o bremsstrahlung.
            """
        )

    with st.expander(
        "📝 Preguntas de observación"
    ):

        st.markdown(
            """
            1. ¿Qué partícula presenta el alcance más corto?
            2. ¿Qué partícula produce mayor ionización específica?
            3. ¿Por qué la trayectoria de las partículas beta es más tortuosa?
            4. ¿Qué diferencia existe entre una colisión suave y una fuerte?
            5. ¿Cómo cambia el bremsstrahlung al utilizar plomo?
            """
        )


# =============================================================================
# ESTACIÓN 2: INTERACCIÓN DE FOTONES
# =============================================================================

with tab_fotones:

    st.header(
        "Estación 2 · Interacción de la radiación electromagnética"
    )

    st.write(
        """
        Seleccioná la energía del fotón, el material y el mecanismo de
        interacción que querés analizar.
        """
    )

    columna_1, columna_2, columna_3 = st.columns(
        3
    )

    with columna_1:

        energia_foton = st.slider(
            "Energía del fotón (keV)",
            min_value=20,
            max_value=2000,
            value=140,
            step=10,
        )

    with columna_2:

        material_foton = st.selectbox(
            "Material absorbente",
            [
                "Agua",
                "Aluminio",
                "Hormigón",
                "Plomo",
            ],
            key="material_foton",
        )

    with columna_3:

        tipo_interaccion = st.selectbox(
            "Interacción a visualizar",
            [
                "Efecto fotoeléctrico",
                "Efecto Compton",
                "Producción de pares",
            ],
        )

    angulo_compton = 60

    if tipo_interaccion == "Efecto Compton":

        angulo_compton = st.slider(
            "Ángulo de dispersión del fotón (grados)",
            min_value=0,
            max_value=180,
            value=60,
            step=5,
        )

    if (
        tipo_interaccion
        == "Producción de pares"
        and energia_foton < 1022
    ):

        st.error(
            """
            La producción de pares no puede ocurrir con esta energía.
            El fotón necesita al menos 1022 keV.
            """
        )

    columna_esquema, columna_resultados = st.columns(
        [1.3, 1]
    )

    with columna_esquema:

        st.subheader(
            "Representación del proceso"
        )

        figura_foton = dibujar_interaccion_foton(
            tipo_interaccion,
            energia_foton,
            angulo_compton,
        )

        st.pyplot(
            figura_foton
        )

    with columna_resultados:

        st.subheader(
            "Predominancia según energía y material"
        )

        predominancias = calcular_predominancia_foton(
            energia_foton,
            material_foton,
        )

        nombres_interacciones = [
            "Fotoeléctrico",
            "Compton",
            "Producción de pares",
        ]

        tabla_interacciones = pd.DataFrame(
            {
                "Interacción": nombres_interacciones,
                "Predominancia conceptual (%)": predominancias,
            }
        )

        tabla_interacciones = tabla_interacciones.set_index(
            "Interacción"
        )

        st.bar_chart(
            tabla_interacciones
        )

        indice_dominante = int(
            np.argmax(
                predominancias
            )
        )

        interaccion_dominante = nombres_interacciones[
            indice_dominante
        ]

        st.success(
            f"Interacción conceptualmente predominante: "
            f"**{interaccion_dominante}**"
        )

        if tipo_interaccion == "Efecto fotoeléctrico":

            energia_enlace = st.slider(
                "Energía de enlace del electrón (keV)",
                min_value=0.0,
                max_value=min(
                    150.0,
                    float(
                        energia_foton - 0.1
                    ),
                ),
                value=min(
                    20.0,
                    float(
                        energia_foton - 0.1
                    ),
                ),
                step=0.5,
            )

            energia_fotoelectron = (
                energia_foton
                - energia_enlace
            )

            st.metric(
                "Energía cinética del fotoelectrón",
                f"{energia_fotoelectron:.1f} keV",
            )

            st.latex(
                r"E_c=E_\gamma-E_{\mathrm{enlace}}"
            )

        elif tipo_interaccion == "Efecto Compton":

            energia_dispersada = calcular_energia_compton(
                energia_foton,
                angulo_compton,
            )

            energia_electron = (
                energia_foton
                - energia_dispersada
            )

            st.metric(
                "Energía del fotón dispersado",
                f"{energia_dispersada:.1f} keV",
            )

            st.metric(
                "Energía transferida al electrón",
                f"{energia_electron:.1f} keV",
            )

        else:

            energia_cinetica_disponible = max(
                0.0,
                energia_foton - 1022.0,
            )

            st.metric(
                "Energía cinética disponible",
                f"{energia_cinetica_disponible:.1f} keV",
            )

            st.latex(
                r"E_{\gamma,\min}=2m_ec^2=1022\ \mathrm{keV}"
            )

    with st.expander(
        "📝 Preguntas de observación"
    ):

        st.markdown(
            """
            1. ¿Cómo cambia el efecto fotoeléctrico al aumentar el número atómico?
            2. ¿Por qué el efecto Compton es importante en energías intermedias?
            3. ¿Qué representa físicamente el umbral de 1022 keV?
            4. ¿Cómo cambia la energía del fotón Compton con el ángulo?
            5. ¿Por qué la producción de pares no aparece a 511 keV?
            """
        )


# =============================================================================
# ESTACIÓN 3: ATENUACIÓN
# =============================================================================

with tab_atenuacion:

    st.header(
        "Estación 3 · Atenuación, coeficientes y semiespesor"
    )

    st.latex(
        r"I(x)=I_0e^{-\mu x}"
    )

    st.write(
        """
        Seleccioná una fuente, un material y un espesor. La aplicación
        calculará la intensidad transmitida y los principales parámetros
        de atenuación.
        """
    )

    columna_1, columna_2, columna_3 = st.columns(
        3
    )

    with columna_1:

        fuente = st.selectbox(
            "Fuente o energía",
            list(
                DATOS_ATENUACION.keys()
            ),
        )

    with columna_2:

        material_atenuacion = st.selectbox(
            "Material absorbente",
            list(
                MATERIALES.keys()
            ),
            key="material_atenuacion",
        )

    with columna_3:

        intensidad_inicial = st.number_input(
            "Intensidad inicial I₀",
            min_value=1.0,
            value=100.0,
            step=1.0,
        )

    energia_fuente = DATOS_ATENUACION[
        fuente
    ]["energia"]

    coeficiente_lineal = DATOS_ATENUACION[
        fuente
    ]["mu"][material_atenuacion]

    densidad_material = MATERIALES[
        material_atenuacion
    ]["densidad"]

    coeficiente_masico = (
        coeficiente_lineal
        / densidad_material
    )

    hvl = (
        math.log(2)
        / coeficiente_lineal
    )

    tvl = (
        math.log(10)
        / coeficiente_lineal
    )

    maximo_espesor = max(
        5.0 * hvl,
        0.1,
    )

    espesor = st.slider(
        "Espesor atravesado (cm)",
        min_value=0.0,
        max_value=float(
            maximo_espesor
        ),
        value=float(
            min(
                hvl,
                maximo_espesor,
            )
        ),
        step=float(
            max(
                maximo_espesor / 200.0,
                0.001,
            )
        ),
    )

    transmision = math.exp(
        -coeficiente_lineal
        * espesor
    )

    intensidad_final = (
        intensidad_inicial
        * transmision
    )

    porcentaje_transmitido = (
        100.0
        * transmision
    )

    porcentaje_atenuado = (
        100.0
        * (
            1.0
            - transmision
        )
    )

    numero_hvl = (
        espesor
        / hvl
    )

    metrica_1, metrica_2, metrica_3, metrica_4 = st.columns(
        4
    )

    metrica_1.metric(
        "Coeficiente lineal μ",
        f"{coeficiente_lineal:.4g} cm⁻¹",
    )

    metrica_2.metric(
        "Coeficiente másico μ/ρ",
        f"{coeficiente_masico:.4g} cm²/g",
    )

    metrica_3.metric(
        "Semiespesor HVL",
        f"{hvl:.4g} cm",
    )

    metrica_4.metric(
        "TVL",
        f"{tvl:.4g} cm",
    )

    metrica_5, metrica_6, metrica_7, metrica_8 = st.columns(
        4
    )

    metrica_5.metric(
        "Intensidad transmitida",
        f"{intensidad_final:.3g}",
    )

    metrica_6.metric(
        "Transmisión",
        f"{porcentaje_transmitido:.2f} %",
    )

    metrica_7.metric(
        "Atenuación",
        f"{porcentaje_atenuado:.2f} %",
    )

    metrica_8.metric(
        "Número de HVL",
        f"{numero_hvl:.2f}",
    )

    valores_espesor = np.linspace(
        0,
        maximo_espesor,
        400,
    )

    valores_intensidad = (
        intensidad_inicial
        * np.exp(
            -coeficiente_lineal
            * valores_espesor
        )
    )

    columna_curva, columna_capas = st.columns(
        [1.4, 1]
    )

    with columna_curva:

        st.subheader(
            "Curva de atenuación"
        )

        figura_atenuacion, eje_atenuacion = plt.subplots(
            figsize=(8, 4.3)
        )

        eje_atenuacion.plot(
            valores_espesor,
            valores_intensidad,
            linewidth=2.7,
            label="Intensidad transmitida",
        )

        eje_atenuacion.scatter(
            [espesor],
            [intensidad_final],
            s=100,
            zorder=5,
            label="Espesor seleccionado",
        )

        eje_atenuacion.axvline(
            hvl,
            linestyle="--",
            linewidth=2,
            label="1 HVL",
        )

        eje_atenuacion.axvline(
            tvl,
            linestyle=":",
            linewidth=2,
            label="1 TVL",
        )

        eje_atenuacion.set_xlabel(
            "Espesor del material (cm)"
        )

        eje_atenuacion.set_ylabel(
            "Intensidad relativa"
        )

        eje_atenuacion.set_title(
            f"{fuente} atravesando {material_atenuacion}"
        )

        eje_atenuacion.grid(
            alpha=0.30
        )

        eje_atenuacion.legend()

        st.pyplot(
            figura_atenuacion
        )

    with columna_capas:

        st.subheader(
            "Atenuación por semiespesores"
        )

        for cantidad_hvl in range(
            0,
            6,
        ):

            porcentaje = (
                100.0
                * (
                    0.5
                    ** cantidad_hvl
                )
            )

            st.write(
                f"**{cantidad_hvl} HVL:** "
                f"{porcentaje:.3f} %"
            )

            st.progress(
                porcentaje / 100.0
            )

    st.info(
        f"""
        El espesor seleccionado representa **{numero_hvl:.2f} HVL**.
        Después de atravesar ese espesor queda aproximadamente
        **{porcentaje_transmitido:.2f} %** del haz primario.
        """
    )

    st.caption(
        """
        La ecuación exponencial representa la atenuación de un haz primario
        monoenergético y estrecho. No incluye radiación dispersa, build-up,
        geometrías extendidas ni espectros complejos.
        """
    )

    with st.expander(
        "📝 Preguntas de observación"
    ):

        st.markdown(
            """
            1. ¿Qué diferencia existe entre μ y μ/ρ?
            2. ¿Qué unidades tiene cada coeficiente?
            3. ¿Qué porcentaje del haz queda después de 1, 2 y 3 HVL?
            4. ¿Cómo cambia la atenuación al modificar el material?
            5. ¿Cómo influye la energía del fotón?
            6. ¿Qué limitaciones presenta este modelo exponencial?
            """
        )


# =============================================================================
# ESTACIÓN 4: COLIMADORES
# =============================================================================

with tab_colimadores:

    st.header(
        "Estación 4 · Selección de colimadores"
    )

    st.write(
        """
        Compará los principales tipos de colimadores utilizados en cámaras
        gamma y observá el compromiso entre resolución, sensibilidad y
        protección frente a la penetración septal.
        """
    )

    colimador_seleccionado = st.selectbox(
        "Seleccioná un colimador",
        list(
            COLIMADORES.keys()
        ),
    )

    datos_colimador = COLIMADORES[
        colimador_seleccionado
    ]

    st.subheader(
        f"{colimador_seleccionado} · "
        f"{datos_colimador['nombre']}"
    )

    st.info(
        datos_colimador[
            "descripcion"
        ]
    )

    metrica_1, metrica_2, metrica_3 = st.columns(
        3
    )

    metrica_1.metric(
        "Resolución relativa",
        f"{datos_colimador['resolucion']} / 100",
    )

    metrica_2.metric(
        "Sensibilidad relativa",
        f"{datos_colimador['sensibilidad']} / 100",
    )

    metrica_3.metric(
        "Protección septal",
        f"{datos_colimador['proteccion_septal']} / 100",
    )

    tabla_colimador = pd.DataFrame(
        {
            "Característica": [
                "Resolución",
                "Sensibilidad",
                "Protección septal",
            ],
            "Valor relativo": [
                datos_colimador[
                    "resolucion"
                ],
                datos_colimador[
                    "sensibilidad"
                ],
                datos_colimador[
                    "proteccion_septal"
                ],
            ],
        }
    )

    tabla_colimador = tabla_colimador.set_index(
        "Característica"
    )

    st.bar_chart(
        tabla_colimador
    )

    categoria_energia = st.radio(
        "Categoría energética del radionúclido",
        [
            "Baja energía",
            "Energía media",
            "Alta energía",
        ],
        horizontal=True,
    )

    seleccion_correcta = False

    if (
        categoria_energia
        == "Baja energía"
        and colimador_seleccionado
        in (
            "LEHR",
            "LEGP",
        )
    ):

        seleccion_correcta = True

    elif (
        categoria_energia
        == "Energía media"
        and colimador_seleccionado
        == "MEGP"
    ):

        seleccion_correcta = True

    elif (
        categoria_energia
        == "Alta energía"
        and colimador_seleccionado
        == "HEGP"
    ):

        seleccion_correcta = True

    if seleccion_correcta:

        st.success(
            """
            ✅ La selección del colimador es coherente con la categoría
            energética indicada.
            """
        )

    else:

        st.warning(
            """
            ⚠️ Revisá la selección. Un colimador inadecuado puede producir
            penetración septal o una pérdida innecesaria de resolución
            y sensibilidad.
            """
        )

    with st.expander(
        "📝 Preguntas de observación"
    ):

        st.markdown(
            """
            1. ¿Por qué un colimador de alta energía requiere septos más gruesos?
            2. ¿Qué relación existe entre resolución y sensibilidad?
            3. ¿Qué ocurriría si se utilizara un LEHR con fotones de energía media?
            4. ¿Por qué un HEGP suele presentar menor resolución?
            """
        )


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
