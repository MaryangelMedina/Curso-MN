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
    "🔎 Simulación educativa. Las lecturas y conversiones mostradas son representaciones didácticas "
    "y no reemplazan mediciones, calibraciones ni procedimientos reales."
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

    if "ionización" in region:

        st.write(
            """
            En esta región se recolectan principalmente los pares de iones
            producidos por la radiación.

            Una aplicación típica es el **activímetro**.
            """
        )

    elif "proporcional" in region.lower():

        st.write(
            """
            En esta región ocurre multiplicación gaseosa.

            La amplitud del pulso conserva información relacionada
            con la energía depositada.
            """
        )

    elif "Geiger" in region:

        st.write(
            """
            En la región Geiger-Müller cada evento produce una gran avalancha.

            El detector permite contar eventos, pero la amplitud del pulso
            ya no informa la energía de la radiación.
            """
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

    col1, col2 = st.columns(
        [1.45, 0.55]
    )

    with col2:

        isotopo_real = st.selectbox(
            "Radionucleido presente en la jeringa",
            [
                "Tc-99m",
                "F-18",
                "I-131",
                "Lu-177"
            ],
            key="iso_real_u7"
        )

        isotopo_equipo = st.selectbox(
            "Radionucleido seleccionado en el activímetro",
            [
                "Tc-99m",
                "F-18",
                "I-131",
                "Lu-177"
            ],
            key="iso_equipo_u7"
        )

        actividad = st.slider(
            "Actividad de la jeringa (MBq)",
            min_value=1,
            max_value=1200,
            value=600,
            key="actividad_u7"
        )

        fondo_activimetro = st.slider(
            "Fondo simulado del activímetro (MBq)",
            min_value=0.00,
            max_value=2.00,
            value=0.05,
            step=0.01,
            key="fondo_act_u7"
        )

        if isotopo_real == isotopo_equipo:

            st.success(
                "✅ Radionucleido seleccionado correctamente."
            )

        else:

            st.warning(
                "⚠️ El radionucleido seleccionado no coincide con la muestra."
            )

        st.caption(
            """
            El fondo y la respuesta con la jeringa fuera del pozo
            son valores didácticos.

            El blindaje del activímetro se representa de forma visual.
            """
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

        <meta charset="UTF-8">

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
            height: 760px;
        }}

        #equipo {{
            position: absolute;

            left: 50%;

            top: 285px;

            transform: translateX(-50%);

            width: 650px;

            height: 390px;

            border-radius: 34px;

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


        /* Blindaje esquemático */

        #blindaje1 {{
            position: absolute;

            left: 86px;

            top: 34px;

            width: 280px;

            height: 300px;

            border-radius: 42px;

            border: 18px solid #777;

            box-sizing: border-box;
        }}


        #blindaje2 {{
            position: absolute;

            left: 105px;

            top: 52px;

            width: 242px;

            height: 265px;

            border-radius: 36px;

            border: 10px solid #a2a2a2;

            box-sizing: border-box;
        }}


        #pozo {{
            position: absolute;

            left: 142px;

            top: 93px;

            width: 170px;

            height: 205px;

            background:
                linear-gradient(
                    90deg,
                    #5a5a5a,
                    #222,
                    #5a5a5a
                );

            border-radius:
                0 0 50px 50px;
        }}


        #boca {{
            position: absolute;

            left: 125px;

            top: 66px;

            width: 205px;

            height: 58px;

            background: #1a1a1a;

            border-radius: 50%;

            border: 6px solid #555;
        }}


        #entrada {{
            position: absolute;

            left: 160px;

            top: 82px;

            width: 135px;

            height: 34px;

            background: #050505;

            border-radius: 50%;
        }}


        #panel {{
            position: absolute;

            right: 38px;

            top: 85px;

            width: 190px;

            height: 210px;

            border-radius: 18px;

            background: #252525;

            box-shadow:
                inset 0 0 0 2px #111;
        }}


        #pantalla {{
            position: absolute;

            left: 15px;

            top: 18px;

            width: 160px;

            height: 92px;

            background: #cce9c6;

            border-radius: 8px;

            border: 3px solid #111;

            text-align: center;

            font-family: monospace;
        }}


        #lecturaMBq {{
            font-size: 20px;

            font-weight: bold;

            margin-top: 13px;

            line-height: 1.25;
        }}


        #lecturamCi {{
            font-size: 17px;

            margin-top: 4px;
        }}


        #iso {{
            position: absolute;

            top: 125px;

            width: 100%;

            text-align: center;

            color: white;

            font-weight: bold;
        }}


        .boton {{
            position: absolute;

            bottom: 24px;

            width: 22px;

            height: 22px;

            border-radius: 50%;

            background: #777;
        }}


        #b1 {{
            left: 42px;
        }}


        #b2 {{
            left: 82px;
        }}


        #b3 {{
            left: 122px;
        }}


        #jeringa {{
            position: absolute;

            left: calc(50% - 40px);

            top: 40px;

            width: 80px;

            height: 180px;

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

            height: 46px;

            background: #999;
        }}


        #etiqueta {{
            position: absolute;

            width: 360px;

            left: calc(50% - 180px);

            top: 8px;

            text-align: center;

            font-weight: bold;

            font-size: 18px;
        }}


        #estado {{
            position: absolute;

            width: 100%;

            bottom: 18px;

            text-align: center;

            font-size: 18px;

            font-weight: bold;
            
            color: white;
        }}


        #leyenda-blindaje {{
            position: absolute;

            left: 86px;

            top: 335px;

            width: 280px;

            text-align: center;

            font-size: 13px;

            color: #333;
        }}

        </style>

        </head>


        <body>


        <div id="lab">


            <div id="etiqueta">

                Jeringa con {isotopo_real}
                —
                {actividad} MBq

            </div>


            <div id="jeringa">

                <div id="embolo"></div>

                <div id="vastago"></div>

                <div id="cuerpo-jeringa"></div>

                <div id="liquido"></div>

                <div id="aguja"></div>

            </div>


            <div id="equipo">


                <div id="blindaje1"></div>


                <div id="blindaje2"></div>


                <div id="pozo"></div>


                <div id="boca"></div>


                <div id="entrada"></div>


                <div id="panel">


                    <div id="pantalla">


                        <div id="lecturaMBq">

                            0.00 MBq

                        </div>


                        <div id="lecturamCi">

                            0.000 mCi

                        </div>


                    </div>


                    <div id="iso">

                        {isotopo_equipo}

                    </div>


                    <div
                    class="boton"
                    id="b1"
                    ></div>


                    <div
                    class="boton"
                    id="b2"
                    ></div>


                    <div
                    class="boton"
                    id="b3"
                    ></div>


                </div>


                <div id="leyenda-blindaje">

                    Blindaje representado
                    de forma esquemática

                </div>


            </div>


            <div id="estado">

                🖱️ Arrastrá la jeringa hacia el pozo

            </div>


        </div>


        <script>


        const syringe =
            document.getElementById("jeringa");


        const well =
            document.getElementById("entrada");


        const readingMBq =
            document.getElementById("lecturaMBq");


        const readingMCi =
            document.getElementById("lecturamCi");


        const status =
            document.getElementById("estado");


        let dragging = false;


        let offsetX = 0;


        let offsetY = 0;


        function updateReading() {{


            const s =
                syringe.getBoundingClientRect();


            const w =
                well.getBoundingClientRect();


            const sx =
                s.left
                +
                s.width/2;


            const sy =
                s.top
                +
                s.height*0.76;


            const wx =
                w.left
                +
                w.width/2;


            const wy =
                w.top
                +
                w.height/2;


            const dx =
                sx - wx;


            const dy =
                sy - wy;


            const distance =
                Math.sqrt(
                    dx*dx
                    +
                    dy*dy
                );


            let geometry = 0;


            if (distance < 45) {{


                geometry = 1.0;


                status.innerHTML =
                    "✅ Jeringa correctamente posicionada dentro del pozo";


            }}


            else if (distance < 95) {{


                geometry = 0.35;


                status.innerHTML =
                    "⚠️ Jeringa parcialmente introducida";


            }}


            else if (distance < 165) {{


                geometry = 0.03;


                status.innerHTML =
                    "↘️ La jeringa está cerca del activímetro";


            }}


            else {{


                geometry = 0.001;


                status.innerHTML =
                    "🖱️ Jeringa fuera del pozo — lectura cercana al fondo";


            }}


            const activity =
                {actividad};


            const calibration =
                {factor_cal};


            const background =
                {fondo_activimetro};


            const contribution =
                activity
                *
                geometry
                *
                calibration;


            const valueMBq =
                background
                +
                contribution;


            const valueMCi =
                valueMBq
                /
                37.0;


            readingMBq.innerHTML =
                valueMBq.toFixed(2)
                +
                " MBq";


            readingMCi.innerHTML =
                valueMCi.toFixed(3)
                +
                " mCi";


        }}


        syringe.addEventListener(
            "mousedown",

            function(e) {{


                dragging = true;


                const r =
                    syringe.getBoundingClientRect();


                offsetX =
                    e.clientX
                    -
                    r.left;


                offsetY =
                    e.clientY
                    -
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
                    e.clientX
                    -
                    lab.left
                    -
                    offsetX;


                let y =
                    e.clientY
                    -
                    lab.top
                    -
                    offsetY;


                x =
                    Math.max(
                        0,
                        Math.min(
                            lab.width
                            -
                            syringe.offsetWidth,
                            x
                        )
                    );


                y =
                    Math.max(
                        0,
                        Math.min(
                            lab.height
                            -
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
            height=790,
            scrolling=False
        )


# =========================================================
# 3. GEIGER-MÜLLER ARRASTRABLE
# =========================================================

with tab3:

    st.header(
        "📟 Geiger-Müller frente a un derrame simulado de F-18"
    )

    st.write(
        """
        Arrastrá el detector con el mouse.

        Al soltarlo, se ubicará automáticamente
        en una de las posiciones disponibles:

        **0 m · 0,5 m · 1 m · 1,5 m · 2 m**
        """
    )

    col1, col2 = st.columns(
        [1.45, 0.55]
    )

    with col2:

        intensidad = st.slider(
            "Intensidad relativa del derrame",
            min_value=1,
            max_value=10,
            value=5,
            key="intensidad_geiger_u7"
        )

        fondo_geiger = st.number_input(
            "Fondo simulado (cps)",
            min_value=0.0,
            max_value=500.0,
            value=35.0,
            step=1.0,
            key="fondo_geiger_u7"
        )

        st.info(
            """
            La lectura en µSv/h se incluye únicamente
            como representación didáctica.

            No constituye un factor de conversión
            real de un instrumento.
            """
        )


    with col1:

        html_geiger = f"""

        <!DOCTYPE html>

        <html>

        <head>

        <meta charset="UTF-8">


        <style>


        body {{
            margin: 0;

            background: transparent;

            font-family: Arial, sans-serif;

            overflow: hidden;
        }}


        #scene {{
            position: relative;

            width: 100%;

            height: 720px;

            background: #efebe3;

            border: 2px solid #c9c4bb;

            border-radius: 26px;

            box-sizing: border-box;

            overflow: hidden;
        }}


        #guide {{
            position: absolute;

            left: 120px;

            right: 55px;

            top: 145px;

            border-top:
                2px dashed #999;
        }}


        .mark {{
            position: absolute;

            top: 104px;

            transform:
                translateX(-50%);

            text-align: center;

            font-size: 18px;

            font-weight: bold;

            color: #222;
        }}


        .tick {{
            position: absolute;

            top: 137px;

            width: 2px;

            height: 18px;

            background: #888;

            transform:
                translateX(-50%);
        }}


        #spill {{
            position: absolute;

            left: 65px;

            top: 430px;

            width: {95 + intensidad*5}px;

            height: {70 + intensidad*4}px;

            border-radius: 50%;

            background:
                radial-gradient(
                    circle,
                    rgba(215,90,90,.88),
                    rgba(145,35,35,.14)
                );
        }}


        #spill-label {{
            position: absolute;

            left: 48px;

            top: 545px;

            width: 190px;

            text-align: center;

            font-size: 18px;

            font-weight: bold;

            color: #222;
        }}


        #meter {{
            position: absolute;

            left: 120px;

            top: 305px;

            width: 215px;

            height: 175px;

            cursor: grab;

            user-select: none;

            z-index: 20;
        }}


        #meter:active {{
            cursor: grabbing;
        }}


        #body {{
            position: absolute;

            left: 0;

            top: 0;

            width: 150px;

            height: 130px;

            border-radius: 24px;

            background: #343434;

            border: 4px solid #111;

            box-sizing: border-box;
        }}


        #screen {{
            position: absolute;

            left: 18px;

            top: 20px;

            width: 114px;

            height: 72px;

            border-radius: 9px;

            background: #cce8c5;

            border: 2px solid #111;

            text-align: center;

            font-family: monospace;

            color: #111;
        }}


        #cps {{
            margin-top: 11px;

            font-size: 21px;

            font-weight: bold;
        }}


        #dose {{
            margin-top: 6px;

            font-size: 17px;
        }}


        #probe {{
            position: absolute;

            left: 146px;

            top: 47px;

            width: 68px;

            height: 34px;

            border-radius:
                0 17px 17px 0;

            background: #505050;

            border: 3px solid #111;

            box-sizing: border-box;
        }}


        #name {{
            position: absolute;

            left: -10px;

            top: 140px;

            width: 225px;

            text-align: center;

            font-size: 18px;

            font-weight: bold;

            color: #222;
        }}


        #distance-box {{
            position: absolute;

            left: 50%;

            transform:
                translateX(-50%);

            bottom: 34px;

            padding:
                9px 18px;

            border-radius: 10px;

            background:
                rgba(255,255,255,.75);

            font-size: 18px;

            font-weight: bold;

            color: #222;
        }}


        #hint {{
            position: absolute;

            left: 50%;

            transform:
                translateX(-50%);

            bottom: 78px;

            font-size: 16px;

            color: #444;
        }}


        #new-measurement {{
            position: absolute;

            right: 30px;

            bottom: 30px;

            padding:
                10px 14px;

            border-radius: 10px;

            border:
                1px solid #777;

            background: #f7f7f7;

            cursor: pointer;

            font-size: 14px;
        }}


        </style>


        </head>


        <body>


        <div id="scene">


            <div id="guide"></div>


            <div
            class="mark"
            id="m0"
            >
            0 m
            </div>


            <div
            class="mark"
            id="m05"
            >
            0,5 m
            </div>


            <div
            class="mark"
            id="m10"
            >
            1 m
            </div>


            <div
            class="mark"
            id="m15"
            >
            1,5 m
            </div>


            <div
            class="mark"
            id="m20"
            >
            2 m
            </div>


            <div
            class="tick"
            id="t0"
            ></div>


            <div
            class="tick"
            id="t05"
            ></div>


            <div
            class="tick"
            id="t10"
            ></div>


            <div
            class="tick"
            id="t15"
            ></div>


            <div
            class="tick"
            id="t20"
            ></div>


            <div id="spill"></div>


            <div id="spill-label">

                Derrame simulado de F-18

            </div>


            <div id="meter">


                <div id="body">


                    <div id="screen">


                        <div id="cps">

                            -- cps

                        </div>


                        <div id="dose">

                            -- µSv/h

                        </div>


                    </div>


                </div>


                <div id="probe"></div>


                <div id="name">

                    Geiger-Müller

                </div>


            </div>


            <div id="hint">

                🖱️ Arrastrá el detector
                y soltalo sobre una posición

            </div>


            <div id="distance-box">

                Distancia:

                <span id="distance-text">

                    0 m

                </span>

            </div>


            <button id="new-measurement">

                📟 Nueva medición

            </button>


        </div>


        <script>


        const scene =
            document.getElementById("scene");


        const meter =
            document.getElementById("meter");


        const cpsText =
            document.getElementById("cps");


        const doseText =
            document.getElementById("dose");


        const distanceText =
            document.getElementById("distance-text");


        const newMeasurement =
            document.getElementById("new-measurement");


        const intensity =
            {intensidad};


        const background =
            {float(fondo_geiger)};


        let dragging = false;


        let offsetX = 0;


        let currentIndex = 0;


        const distances = [

            0.0,

            0.5,

            1.0,

            1.5,

            2.0

        ];


        function getPositions() {{


            const width =
                scene.clientWidth;


            const start =
                110;


            const end =
                width - 250;


            const step =
                (end - start)
                /
                4;


            return [

                start,

                start + step,

                start + 2*step,

                start + 3*step,

                end

            ];


        }}


        function positionMarks() {{


            const positions =
                getPositions();


            const ids = [

                "0",

                "05",

                "10",

                "15",

                "20"

            ];


            positions.forEach(

                (x, i) => {{


                    document
                    .getElementById(
                        "m" + ids[i]
                    )
                    .style.left =
                        (x + 75)
                        +
                        "px";


                    document
                    .getElementById(
                        "t" + ids[i]
                    )
                    .style.left =
                        (x + 75)
                        +
                        "px";


                }}

            );


        }}


        function normalRandom() {{


            let u = 0;


            let v = 0;


            while (u === 0)
                u = Math.random();


            while (v === 0)
                v = Math.random();


            return (
                Math.sqrt(
                    -2.0
                    *
                    Math.log(u)
                )
                *
                Math.cos(
                    2.0
                    *
                    Math.PI
                    *
                    v
                )
            );


        }}


        function calculateReading() {{


            const d =
                distances[currentIndex];


            const effectiveDistance =
                (
                    d === 0.0
                )
                ?
                0.25
                :
                d;


            const signal =
                (
                    70
                    *
                    intensity
                )
                /
                (
                    effectiveDistance
                    *
                    effectiveDistance
                );


            const expected =
                signal
                +
                background;


            const fluctuation =
                normalRandom()
                *
                Math.sqrt(
                    Math.max(
                        expected,
                        1
                    )
                );


            const cps =
                Math.max(
                    0,
                    Math.round(
                        expected
                        +
                        fluctuation
                    )
                );


            /*
            Conversión exclusivamente didáctica.
            No corresponde a un factor real
            de calibración.
            */

            const dose =
                cps
                *
                0.002;


            cpsText.innerHTML =
                cps
                +
                " cps";


            doseText.innerHTML =
                dose.toFixed(2)
                +
                " µSv/h";


            if (d === 0.0) {{


                distanceText.innerHTML =
                    "0 m";


            }}

            else {{


                distanceText.innerHTML =
                    d
                    .toFixed(1)
                    .replace(
                        ".",
                        ","
                    )
                    +
                    " m";


            }}


        }}


        function snapTo(index) {{


            const positions =
                getPositions();


            currentIndex =
                Math.max(
                    0,
                    Math.min(
                        4,
                        index
                    )
                );


            meter.style.left =
                positions[currentIndex]
                +
                "px";


            calculateReading();


        }}


        meter.addEventListener(
            "mousedown",

            function(e) {{


                dragging = true;


                const r =
                    meter
                    .getBoundingClientRect();


                offsetX =
                    e.clientX
                    -
                    r.left;


            }}
        );


        document.addEventListener(
            "mousemove",

            function(e) {{


                if (!dragging)
                    return;


                const rect =
                    scene
                    .getBoundingClientRect();


                let x =
                    e.clientX
                    -
                    rect.left
                    -
                    offsetX;


                const positions =
                    getPositions();


                const minX =
                    positions[0];


                const maxX =
                    positions[4];


                x =
                    Math.max(
                        minX,
                        Math.min(
                            maxX,
                            x
                        )
                    );


                meter.style.left =
                    x
                    +
                    "px";


            }}
        );


        document.addEventListener(
            "mouseup",

            function() {{


                if (!dragging)
                    return;


                dragging = false;


                const currentX =
                    parseFloat(
                        meter.style.left
                        ||
                        "0"
                    );


                const positions =
                    getPositions();


                let closest = 0;


                let best =
                    Infinity;


                positions.forEach(

                    (x, i) => {{


                        const difference =
                            Math.abs(
                                currentX
                                -
                                x
                            );


                        if (
                            difference
                            <
                            best
                        ) {{


                            best =
                                difference;


                            closest =
                                i;


                        }}


                    }}

                );


                snapTo(
                    closest
                );


            }}
        );


        newMeasurement.addEventListener(
            "click",

            function() {{


                calculateReading();


            }}
        );


        window.addEventListener(
            "resize",

            function() {{


                positionMarks();


                snapTo(
                    currentIndex
                );


            }}
        );


        positionMarks();


        snapTo(0);


        </script>


        </body>

        </html>

        """

        st.components.v1.html(
            html_geiger,
            height=760,
            scrolling=False
        )


    st.caption(
        """
        El comportamiento del Geiger y la lectura equivalente
        se representan mediante un modelo educativo simplificado.

        Las magnitudes mostradas no deben interpretarse
        como factores de calibración de un instrumento real.
        """
    )
