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
            marker=dict(size=16),
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


# =========================================================
# 2. ACTIVÍMETRO ARRASTRABLE
# =========================================================

with tab2:

    st.header("💉 Activímetro virtual")

    st.write(
        """
        Arrastrá la jeringa con el mouse e introducila en el pozo del activímetro.
        La pantalla cambia según la posición de la jeringa.
        """
    )

    col1, col2 = st.columns([1.45, 0.55])

    with col2:

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

        if isotopo_real == isotopo_equipo:
            st.success("✅ Radionucleido seleccionado correctamente.")
        else:
            st.warning("⚠️ El radionucleido seleccionado no coincide con la muestra.")

        st.caption(
            "La lectura dentro del simulador es conceptual y depende de la posición de la jeringa."
        )

    factores = {
        "Tc-99m": 1.00,
        "F-18": 1.07,
        "I-131": 0.94,
        "Lu-177": 0.98
    }

    factor_cal = (
        factores[isotopo_real]
        /
        factores[isotopo_equipo]
    )

    with col1:

        html_activimetro = f"""
        <!DOCTYPE html>
        <html>

        <head>

        <style>

        body {{
            margin: 0;
            background: transparent;
            font-family: Arial, sans-serif;
            overflow: hidden;
        }}

        #lab {{
            position: relative;
            width: 100%;
            height: 700px;
        }}

        #equipo {{
            position: absolute;
            left: 50%;
            top: 245px;
            transform: translateX(-50%);
            width: 610px;
            height: 360px;
            border-radius: 32px;
            border: 4px solid #777;
            background:
                linear-gradient(
                    90deg,
                    #bdbdbd,
                    #f7f7f7,
                    #c3c3c3
                );
            box-shadow:
                0 12px 28px rgba(0,0,0,.25);
        }}

        #pozo {{
            position: absolute;
            left: 120px;
            top: 54px;
            width: 190px;
            height: 215px;
            background:
                linear-gradient(
                    90deg,
                    #5a5a5a,
                    #222,
                    #5a5a5a
                );
            border-radius: 0 0 55px 55px;
        }}

        #boca {{
            position: absolute;
            left: 108px;
            top: 28px;
            width: 215px;
            height: 55px;
            background: #1a1a1a;
            border-radius: 50%;
            border: 6px solid #555;
        }}

        #entrada {{
            position: absolute;
            left: 148px;
            top: 47px;
            width: 135px;
            height: 32px;
            background: #050505;
            border-radius: 50%;
        }}

        #panel {{
            position: absolute;
            right: 40px;
            top: 72px;
            width: 170px;
            height: 190px;
            border-radius: 18px;
            background: #252525;
            box-shadow:
                inset 0 0 0 2px #111;
        }}

        #pantalla {{
            position: absolute;
            left: 18px;
            top: 22px;
            width: 134px;
            height: 68px;
            background: #cce9c6;
            border-radius: 8px;
            border: 3px solid #111;
            text-align: center;
            font-family: monospace;
        }}

        #lectura {{
            font-size: 25px;
            font-weight: bold;
            margin-top: 9px;
        }}

        #unidad {{
            font-size: 15px;
        }}

        #iso {{
            position: absolute;
            top: 105px;
            width: 100%;
            text-align: center;
            color: white;
            font-weight: bold;
        }}

        .boton {{
            position: absolute;
            bottom: 26px;
            width: 22px;
            height: 22px;
            border-radius: 50%;
            background: #777;
        }}

        #b1 {{
            left: 35px;
        }}

        #b2 {{
            left: 72px;
        }}

        #b3 {{
            left: 109px;
        }}

        #jeringa {{
            position: absolute;
            left: calc(50% - 40px);
            top: 35px;
            width: 80px;
            height: 175px;
            cursor: grab;
            user-select: none;
            z-index: 50;
        }}

        #jeringa:active {{
            cursor: grabbing;
        }}

        #embolo {{
            position: absolute;
            left: 18px;
            top: 0;
            width: 44px;
            height: 15px;
            background: #d6d6d6;
            border-radius: 5px;
            border: 2px solid #888;
        }}

        #vastago {{
            position: absolute;
            left: 34px;
            top: 14px;
            width: 12px;
            height: 30px;
            background: #bbb;
        }}

        #cuerpo-jeringa {{
            position: absolute;
            left: 16px;
            top: 42px;
            width: 48px;
            height: 82px;
            border-radius: 8px;
            border: 3px solid #537180;
            background: #eaf7ff;
        }}

        #liquido {{
            position: absolute;
            left: 21px;
            top: 83px;
            width: 38px;
            height: 35px;
            background: #8fd0fa;
        }}

        #aguja {{
            position: absolute;
            left: 38px;
            top: 124px;
            width: 4px;
            height: 45px;
            background: #999;
        }}

        #etiqueta {{
            position: absolute;
            width: 300px;
            left: calc(50% - 150px);
            top: 8px;
            text-align: center;
            font-weight: bold;
            font-size: 18px;
        }}

        #estado {{
            position: absolute;
            width: 100%;
            bottom: 20px;
            text-align: center;
            font-size: 18px;
            font-weight: bold;
        }}

        </style>

        </head>

        <body>

        <div id="lab">

            <div id="etiqueta">
                Jeringa con {isotopo_real} — {actividad} MBq
            </div>

            <div id="jeringa">

                <div id="embolo"></div>

                <div id="vastago"></div>

                <div id="cuerpo-jeringa"></div>

                <div id="liquido"></div>

                <div id="aguja"></div>

            </div>


            <div id="equipo">

                <div id="pozo"></div>

                <div id="boca"></div>

                <div id="entrada"></div>

                <div id="panel">

                    <div id="pantalla">

                        <div id="lectura">
                            0.0
                        </div>

                        <div id="unidad">
                            MBq
                        </div>

                    </div>

                    <div id="iso">
                        {isotopo_equipo}
                    </div>

                    <div class="boton" id="b1"></div>

                    <div class="boton" id="b2"></div>

                    <div class="boton" id="b3"></div>

                </div>

            </div>

            <div id="estado">
                🖱️ Arrastrá la jeringa hacia el pozo
            </div>

        </div>


        <script>

        const syringe = document.getElementById("jeringa");

        const well = document.getElementById("entrada");

        const reading = document.getElementById("lectura");

        const status = document.getElementById("estado");

        let dragging = false;

        let offsetX = 0;

        let offsetY = 0;


        function updateReading() {{

            const s = syringe.getBoundingClientRect();

            const w = well.getBoundingClientRect();

            const sx = s.left + s.width/2;

            const sy = s.top + s.height*0.75;

            const wx = w.left + w.width/2;

            const wy = w.top + w.height/2;

            const dx = sx - wx;

            const dy = sy - wy;

            const distance = Math.sqrt(
                dx*dx +
                dy*dy
            );

            let geometry = 0;

            if (distance < 45) {{
                geometry = 1.0;
                status.innerHTML = "✅ Jeringa correctamente posicionada dentro del pozo";
            }}

            else if (distance < 100) {{
                geometry = 0.65;
                status.innerHTML = "⚠️ Jeringa parcialmente introducida";
            }}

            else if (distance < 170) {{
                geometry = 0.20;
                status.innerHTML = "↘️ Acercando la jeringa al detector";
            }}

            else {{
                geometry = 0.01;
                status.innerHTML = "🖱️ Arrastrá la jeringa hacia el pozo";
            }}

            const activity = {actividad};

            const calibration = {factor_cal};

            const value =
                activity *
                geometry *
                calibration;

            reading.innerHTML =
                value.toFixed(1);

        }}


        syringe.addEventListener(
            "mousedown",
            function(e) {{

                dragging = true;

                const r =
                    syringe.getBoundingClientRect();

                offsetX =
                    e.clientX -
                    r.left;

                offsetY =
                    e.clientY -
                    r.top;

            }}
        );


        document.addEventListener(
            "mousemove",
            function(e) {{

                if (!dragging)
                    return;

                const lab =
                    document
                    .getElementById("lab")
                    .getBoundingClientRect();

                let x =
                    e.clientX -
                    lab.left -
                    offsetX;

                let y =
                    e.clientY -
                    lab.top -
                    offsetY;

                x =
                    Math.max(
                        0,
                        Math.min(
                            lab.width -
                            syringe.offsetWidth,
                            x
                        )
                    );

                y =
                    Math.max(
                        0,
                        Math.min(
                            lab.height -
                            syringe.offsetHeight,
                            y
                        )
                    );

                syringe.style.left =
                    x + "px";

                syringe.style.top =
                    y + "px";

                updateReading();

            }}
        );


        document.addEventListener(
            "mouseup",
            function() {{

                dragging = false;

            }}
        );


        updateReading();

        </script>

        </body>

        </html>
        """

        st.components.v1.html(
            html_activimetro,
            height=730,
            scrolling=False
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
        y observá cómo cambia la tasa de conteo y la lectura equivalente simulada.
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
            100
            * intensidad
            / distancia**2
            + fondo
        )

        if st.button("📟 Tomar una medición"):

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
            + int(
                distancia * 1000
            )
            + intensidad * 77
        )

        rng = np.random.default_rng(
            semilla
        )

        cuentas = int(
            rng.poisson(
                esperado
            )
        )

        # Conversión únicamente educativa.
        factor_simulado = 0.002

        tasa_dosis = (
            cuentas
            * factor_simulado
        )

        st.metric(
            "Tasa de conteo",
            f"{cuentas} cps"
        )

        st.metric(
            "Lectura equivalente simulada",
            f"{tasa_dosis:.2f} µSv/h"
        )

        st.info(
            """
            La relación entre cps y µSv/h que aparece acá
            es solamente didáctica.

            En un equipo real depende de la respuesta energética
            y de la calibración del instrumento.
            """
        )


    with izquierda:

        posicion_detector = (
            160
            + (distancia - 0.5)
            / 1.5
            * 455
        )

        svg = f"""

        <svg
        viewBox="0 0 760 560"
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


        <rect
        x="25"
        y="60"
        width="710"
        height="430"
        rx="18"
        fill="#eeeae2"
        stroke="#c9c4bb"
        />


        <ellipse
        cx="115"
        cy="295"
        rx="{40 + intensidad*3}"
        ry="{28 + intensidad*2}"
        fill="url(#derrame)"
        />


        <text
        x="115"
        y="365"
        text-anchor="middle"
        font-size="18"
        font-weight="600"
        >

        Derrame F-18

        </text>


        <line
        x1="115"
        y1="120"
        x2="655"
        y2="120"
        stroke="#888"
        stroke-dasharray="6 6"
        />


        <text
        x="255"
        y="102"
        text-anchor="middle"
        font-size="16"
        >
        0,5 m
        </text>


        <text
        x="390"
        y="102"
        text-anchor="middle"
        font-size="16"
        >
        1 m
        </text>


        <text
        x="655"
        y="102"
        text-anchor="middle"
        font-size="16"
        >
        2 m
        </text>


        <g
        transform="translate({posicion_detector},250)"
        >

        <rect
        x="-72"
        y="-52"
        width="145"
        height="105"
        rx="18"
        fill="#343434"
        stroke="#111"
        stroke-width="3"
        />


        <rect
        x="-55"
        y="-38"
        width="110"
        height="58"
        rx="7"
        fill="#cce6c4"
        stroke="#111"
        />


        <text
        x="0"
        y="-14"
        text-anchor="middle"
        font-family="monospace"
        font-size="18"
        font-weight="600"
        >

        {cuentas} cps

        </text>


        <text
        x="0"
        y="10"
        text-anchor="middle"
        font-family="monospace"
        font-size="16"
        >

        {tasa_dosis:.2f} µSv/h

        </text>


        <rect
        x="73"
        y="-16"
        width="105"
        height="32"
        rx="14"
        fill="#4b4b4b"
        stroke="#111"
        stroke-width="2"
        />


        <text
        x="0"
        y="82"
        text-anchor="middle"
        font-size="17"
        font-weight="600"
        >

        Geiger-Müller

        </text>

        </g>


        <line
        x1="115"
        y1="425"
        x2="{posicion_detector}"
        y2="425"
        stroke="#333"
        stroke-width="3"
        />


        <text
        x="{(115 + posicion_detector)/2}"
        y="458"
        text-anchor="middle"
        font-size="19"
        >

        {distancia:.1f} m

        </text>

        </svg>

        """

        st.components.v1.html(
            svg,
            height=650,
            scrolling=False
        )

    st.caption(
        """
        El comportamiento mostrado es un modelo educativo simplificado.
        """
    )
