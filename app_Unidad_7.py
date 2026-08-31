import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Unidad 7 - Detección y medición",
    page_icon="☢️",
    layout="wide"
)

st.title("☢️ Unidad 7 — Detección y medición de las radiaciones")

st.write(
    """
    En este laboratorio virtual vas a explorar de forma interactiva
    el funcionamiento de distintos detectores utilizados en Medicina Nuclear.
    """
)

st.info(
    "🔎 Simulación educativa. Las lecturas son representaciones didácticas y no reemplazan mediciones reales."
)

tab1, tab2, tab3 = st.tabs(
    [
        "⚡ Detectores gaseosos",
        "💉 Activímetro",
        "📟 Geiger-Müller"
    ]
)

# =========================================================
# 1. DETECTORES GASEOSOS
# =========================================================

with tab1:

    st.header("⚡ Respuesta de los detectores gaseosos")

    st.write(
        """
        Modificá la tensión aplicada y observá cómo cambia la respuesta
        del detector gaseoso.

        Las distintas regiones corresponden al comportamiento típico de:

        **Cámara de ionización → Contador proporcional → Geiger-Müller**
        """
    )

    voltage = st.slider(
        "Tensión aplicada al detector (V)",
        min_value=0,
        max_value=1650,
        value=250,
        step=10
    )

    def detectar_region(v):

        if v < 100:
            return "I — Región de recombinación"

        elif v < 320:
            return "II — Cámara de ionización"

        elif v < 800:
            return "III — Región proporcional"

        elif v < 980:
            return "IV — Proporcionalidad limitada"

        elif v < 1450:
            return "V — Región Geiger-Müller"

        else:
            return "VI — Descarga continua"

    x = np.linspace(0, 1650, 600)

    y_beta = np.piecewise(

        x,

        [
            x < 100,
            (x >= 100) & (x < 320),
            (x >= 320) & (x < 800),
            (x >= 800) & (x < 980),
            (x >= 980) & (x < 1450),
            x >= 1450
        ],

        [
            lambda z: 10 ** (2.2 + 0.01*z),
            lambda z: 10 ** 3.2,
            lambda z: 10 ** (3.2 + (z-320)/160),
            lambda z: 10 ** (6.2 + (z-800)/58),
            lambda z: 10 ** 9.35,
            lambda z: 10 ** (9.35 + (z-1450)/55)
        ]
    )

    y_alpha = y_beta * 1300

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y_alpha,
            mode="lines",
            name="Partícula α"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y_beta,
            mode="lines",
            name="Partícula β"
        )
    )

    regiones = [

        (0, 100, "I"),

        (100, 320, "II"),

        (320, 800, "III"),

        (800, 980, "IV"),

        (980, 1450, "V"),

        (1450, 1650, "VI")
    ]

    for inicio, fin, nombre in regiones:

        fig.add_vrect(
            x0=inicio,
            x1=fin,
            opacity=0.06,
            line_width=0
        )

        fig.add_annotation(
            x=(inicio + fin)/2,
            y=1e14,
            text=nombre,
            showarrow=False
        )

    valor_y = float(
        np.interp(
            voltage,
            x,
            y_beta
        )
    )

    fig.add_trace(

        go.Scatter(

            x=[voltage],

            y=[valor_y],

            mode="markers",

            marker=dict(
                size=16
            ),

            name="Punto de operación"
        )
    )

    fig.update_yaxes(
        type="log",
        title="Pares de iones recolectados"
    )

    fig.update_xaxes(
        title="Tensión aplicada (V)"
    )

    fig.update_layout(
        height=520
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    region = detectar_region(voltage)

    st.success(
        f"📍 Región actual: **{region}**"
    )

    if "ionización" in region:

        st.write(
            """
            En esta región se recolectan principalmente
            los pares de iones producidos por la radiación.

            Una aplicación típica es el **activímetro**.
            """
        )

    elif "proporcional" in region.lower():

        st.write(
            """
            En esta región ocurre multiplicación gaseosa.

            La amplitud del pulso conserva información
            relacionada con la energía depositada.
            """
        )

    elif "Geiger" in region:

        st.write(
            """
            En la región Geiger-Müller cada evento produce
            una avalancha importante.

            El detector permite contar eventos,
            pero la amplitud del pulso ya no informa
            la energía de la radiación.
            """
        )


# =========================================================
# 2. ACTIVÍMETRO
# =========================================================

with tab2:

    st.header("💉 Activímetro virtual")

    st.write(
        """
        Simulá la medición de una jeringa dentro
        de una cámara de ionización tipo pozo.
        """
    )

    izquierda, derecha = st.columns(
        [1.25, 0.75]
    )

    with derecha:

        isotopo_real = st.selectbox(

            "Radionucleido presente en la jeringa",

            [
                "Tc-99m",
                "F-18",
                "I-131",
                "Lu-177"
            ]
        )

        isotopo_equipo = st.selectbox(

            "Radionucleido seleccionado en el activímetro",

            [
                "Tc-99m",
                "F-18",
                "I-131",
                "Lu-177"
            ]
        )

        actividad = st.slider(

            "Actividad de la jeringa (MBq)",

            min_value=1,

            max_value=1200,

            value=600
        )

        entrada = st.slider(

            "Introducir la jeringa en el activímetro",

            min_value=0,

            max_value=100,

            value=0,

            step=5
        )

        factores = {

            "Tc-99m": 1.00,

            "F-18": 1.07,

            "I-131": 0.94,

            "Lu-177": 0.98
        }

        geometria = (

            0.03 +

            0.97 *

            (entrada/100)**1.6
        )

        lectura = (

            actividad *

            geometria *

            (
                factores[isotopo_real] /

                factores[isotopo_equipo]
            )
        )

        st.metric(

            "Pantalla del activímetro",

            f"{lectura:,.1f} MBq"
        )

        if entrada < 85:

            st.warning(
                "💉 La jeringa todavía no está completamente dentro del pozo."
            )

        elif isotopo_real != isotopo_equipo:

            st.error(
                "⚠️ El radionucleido seleccionado en el activímetro no coincide con la muestra."
            )

        else:

            st.success(
                "✅ La jeringa está posicionada y el radionucleido seleccionado es correcto."
            )


    with izquierda:

        posicion_jeringa = (
            65 +
            entrada * 2.35
        )

        svg = f"""

        <svg
        viewBox="0 0 700 500"
        width="100%"
        >

        <defs>

        <linearGradient
        id="cuerpo"
        x1="0"
        x2="1"
        >

        <stop
        offset="0%"
        stop-color="#c7c7c7"
        />

        <stop
        offset="50%"
        stop-color="#f5f5f5"
        />

        <stop
        offset="100%"
        stop-color="#999"
        />

        </linearGradient>

        </defs>


        <!-- cuerpo activimetro -->

        <rect
        x="160"
        y="155"
        width="380"
        height="290"
        rx="22"
        fill="url(#cuerpo)"
        stroke="#777"
        stroke-width="3"
        />


        <!-- pozo -->

        <ellipse
        cx="300"
        cy="205"
        rx="70"
        ry="24"
        fill="#222"
        />

        <rect
        x="230"
        y="205"
        width="140"
        height="165"
        fill="#444"
        />

        <ellipse
        cx="300"
        cy="370"
        rx="70"
        ry="24"
        fill="#666"
        />

        <ellipse
        cx="300"
        cy="205"
        rx="40"
        ry="12"
        fill="#050505"
        />


        <!-- pantalla -->

        <rect
        x="425"
        y="205"
        width="95"
        height="105"
        rx="8"
        fill="#2c2c2c"
        />

        <rect
        x="438"
        y="220"
        width="68"
        height="33"
        rx="4"
        fill="#cce6c4"
        />

        <text
        x="472"
        y="242"
        text-anchor="middle"
        font-family="monospace"
        font-size="15"
        >

        {lectura:06.1f}

        </text>

        <text
        x="472"
        y="275"
        text-anchor="middle"
        font-size="13"
        fill="white"
        >

        MBq

        </text>

        <text
        x="472"
        y="296"
        text-anchor="middle"
        font-size="12"
        fill="white"
        >

        {isotopo_equipo}

        </text>


        <!-- jeringa -->

        <g
        transform="translate(0,{posicion_jeringa})"
        >

        <rect
        x="280"
        y="-55"
        width="40"
        height="72"
        rx="6"
        fill="#eaf6ff"
        stroke="#516773"
        stroke-width="2"
        />

        <rect
        x="284"
        y="-18"
        width="32"
        height="31"
        fill="#9fd8ff"
        />

        <line
        x1="300"
        y1="17"
        x2="300"
        y2="56"
        stroke="#777"
        stroke-width="3"
        />

        <rect
        x="274"
        y="-64"
        width="52"
        height="9"
        rx="3"
        fill="#d0d0d0"
        />

        <rect
        x="294"
        y="-83"
        width="12"
        height="19"
        fill="#c0c0c0"
        />

        </g>


        <text
        x="300"
        y="42"
        text-anchor="middle"
        font-size="18"
        font-weight="600"
        >

        Jeringa con {isotopo_real}

        </text>

        <text
        x="300"
        y="67"
        text-anchor="middle"
        font-size="14"
        >

        {actividad} MBq

        </text>

        </svg>

        """

        st.components.v1.html(
            svg,
            height=510
        )

    st.caption(
        "La variación con la posición y los factores mostrados forman parte de un modelo conceptual del simulador."
    )


# =========================================================
# 3. GEIGER
# =========================================================

with tab3:

    st.header(
        "📟 Geiger-Müller frente a un derrame simulado de F-18"
    )

    st.write(
        """
        Mové el detector con respecto al derrame
        y observá cómo cambia la tasa de conteo.
        """
    )

    izquierda, derecha = st.columns(
        [1.25, 0.75]
    )

    with derecha:

        distancia = st.slider(

            "Distancia al derrame (m)",

            min_value=0.5,

            max_value=2.0,

            value=1.0,

            step=0.1
        )

        intensidad = st.slider(

            "Intensidad relativa del derrame",

            min_value=1,

            max_value=10,

            value=5
        )

        fondo = st.number_input(

            "Fondo (cps)",

            min_value=0.0,

            max_value=500.0,

            value=35.0,

            step=1.0
        )

        esperado = (

            100 *

            intensidad /

            distancia**2

            +

            fondo
        )

        if st.button(
            "📟 Tomar una medición"
        ):

            st.session_state["medicion"] = (

                st.session_state.get(
                    "medicion",
                    0
                )

                + 1
            )

        semilla = (

            st.session_state.get(
                "medicion",
                0
            )

            +

            int(
                distancia * 1000
            )

            +

            intensidad * 77
        )

        rng = np.random.default_rng(
            semilla
        )

        observado = int(
            rng.poisson(
                esperado
            )
        )

        st.metric(

            "Pantalla del Geiger",

            f"{observado} cps"
        )

        st.write(
            f"""
            **Distancia:** {distancia:.1f} m

            **Fondo:** {fondo:.0f} cps
            """
        )


    with izquierda:

        posicion_detector = (

            160 +

            (distancia - 0.5)

            / 1.5

            * 455
        )

        svg = f"""

        <svg
        viewBox="0 0 760 500"
        width="100%"
        >

        <defs>

        <radialGradient
        id="derrame"
        >

        <stop
        offset="0%"
        stop-color="#d56b6b"
        stop-opacity=".9"
        />

        <stop
        offset="100%"
        stop-color="#8b1e1e"
        stop-opacity=".15"
        />

        </radialGradient>

        </defs>


        <!-- piso -->

        <rect
        x="25"
        y="60"
        width="710"
        height="380"
        rx="18"
        fill="#eeeae2"
        stroke="#c9c4bb"
        />


        <!-- derrame -->

        <ellipse

        cx="115"

        cy="270"

        rx="{40 + intensidad*3}"

        ry="{28 + intensidad*2}"

        fill="url(#derrame)"

        />


        <text

        x="115"

        y="335"

        text-anchor="middle"

        font-size="18"

        font-weight="600"

        >

        Derrame F-18

        </text>


        <!-- referencias -->

        <line

        x1="115"

        y1="115"

        x2="655"

        y2="115"

        stroke="#888"

        stroke-dasharray="6 6"

        />


        <text
        x="255"
        y="98"
        text-anchor="middle"
        >

        0,5 m

        </text>


        <text
        x="390"
        y="98"
        text-anchor="middle"
        >

        1 m

        </text>


        <text
        x="655"
        y="98"
        text-anchor="middle"
        >

        2 m

        </text>


        <!-- detector geiger -->

        <g

        transform="translate({posicion_detector},230)"

        >

        <rect

        x="-55"

        y="-35"

        width="110"

        height="70"

        rx="15"

        fill="#343434"

        stroke="#111"

        stroke-width="2"

        />


        <rect

        x="-33"

        y="-23"

        width="66"

        height="29"

        rx="4"

        fill="#cce6c4"

        />


        <text

        x="0"

        y="-3"

        text-anchor="middle"

        font-family="monospace"

        font-size="15"

        >

        {observado} cps

        </text>


        <rect

        x="55"

        y="-12"

        width="86"

        height="24"

        rx="10"

        fill="#4b4b4b"

        stroke="#111"

        />


        <text

        x="0"

        y="58"

        text-anchor="middle"

        font-size="16"

        font-weight="600"

        >

        Geiger-Müller

        </text>

        </g>


        <!-- distancia -->

        <line

        x1="115"

        y1="380"

        x2="{posicion_detector}"

        y2="380"

        stroke="#333"

        stroke-width="3"

        />


        <line

        x1="115"

        y1="370"

        x2="115"

        y2="390"

        stroke="#333"

        stroke-width="3"

        />


        <line

        x1="{posicion_detector}"

        y1="370"

        x2="{posicion_detector}"

        y2="390"

        stroke="#333"

        stroke-width="3"

        />


        <text

        x="{(115 + posicion_detector)/2}"

        y="410"

        text-anchor="middle"

        font-size="18"

        >

        {distancia:.1f} m

        </text>

        </svg>

        """

        st.components.v1.html(
            svg,
            height=510
        )

    st.caption(
        """
        El comportamiento de la distancia se representa mediante
        un modelo simplificado para facilitar la comprensión conceptual.
        """
    )
