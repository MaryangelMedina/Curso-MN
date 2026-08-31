import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="Unidad 8 - Dosimetría personal",
    page_icon="☢️",
    layout="wide"
)

st.title("☢️ Unidad 8 — Instrumentación para dosimetría personal")

st.write(
    """
    En este laboratorio virtual vas a explorar el uso, funcionamiento
    y lectura de distintos dosímetros empleados para la vigilancia
    radiológica personal.
    """
)

st.info(
    "🔎 Simulación educativa. Los valores utilizados son conceptuales "
    "y no sustituyen procedimientos de dosimetría, calibración ni protección radiológica reales."
)

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "👤 ¿Dónde llevo mi dosímetro?",
        "💎 TLD interactivo",
        "🔬 Comparador de dosímetros",
        "📐 Calibración"
    ]
)


# ============================================================
# TAB 1
# UBICACIÓN DE LOS DOSÍMETROS
# ============================================================

with tab1:

    st.header("👤 ¿Dónde llevo mi dosímetro?")

    st.write(
        """
        Arrastrá cada dosímetro con el mouse hasta la región correspondiente
        del trabajador.

        **Cuerpo entero · Extremidad · Cristalino**
        """
    )

    html = """

    <!DOCTYPE html>

    <html>

    <head>

    <meta charset="UTF-8">

    <style>

    body {
        margin: 0;
        background: transparent;
        font-family: Arial, sans-serif;
        overflow: hidden;
        color: white;
    }

    #laboratorio {

        position: relative;

        width: 100%;

        height: 820px;

        background:
            linear-gradient(
                135deg,
                #111923,
                #0d1117
            );

        border-radius: 26px;

        border: 1px solid #35404d;

        overflow: hidden;
    }


    #titulo {

        position: absolute;

        top: 20px;

        width: 100%;

        text-align: center;

        font-size: 25px;

        font-weight: bold;

        color: white;
    }


    #instruccion {

        position: absolute;

        top: 62px;

        width: 100%;

        text-align: center;

        font-size: 16px;

        color: #cbd5df;
    }


    /* ===========================================
       PERSONA
       =========================================== */

    #persona {

        position: absolute;

        left: 5%;

        top: 112px;

        width: 55%;

        height: 610px;
    }


    #cabeza {

        position: absolute;

        left: calc(50% - 62px);

        top: 8px;

        width: 124px;

        height: 145px;

        border-radius: 50% 50% 45% 45%;

        background: #d6a47e;

        border: 3px solid #9b7257;
    }


    #cabello {

        position: absolute;

        left: -3px;

        top: -4px;

        width: 130px;

        height: 52px;

        border-radius: 65px 65px 25px 25px;

        background: #3a2c27;
    }


    #lente-izq,
    #lente-der {

        position: absolute;

        top: 56px;

        width: 42px;

        height: 28px;

        border: 4px solid #3e4850;

        border-radius: 10px;

        background:
            rgba(190,225,240,.16);
    }


    #lente-izq {
        left: 13px;
    }


    #lente-der {
        right: 13px;
    }


    #puente {

        position: absolute;

        top: 68px;

        left: 55px;

        width: 14px;

        height: 4px;

        background: #3e4850;
    }


    #cuello {

        position: absolute;

        left: calc(50% - 29px);

        top: 137px;

        width: 58px;

        height: 50px;

        background: #c79270;
    }


    #torso {

        position: absolute;

        left: calc(50% - 138px);

        top: 177px;

        width: 276px;

        height: 350px;

        border-radius: 42px 42px 20px 20px;

        background:
            linear-gradient(
                90deg,
                #dedede,
                #fafafa,
                #dedede
            );

        border: 3px solid #aaa;
    }


    #remera {

        position: absolute;

        left: calc(50% - 43px);

        top: 181px;

        width: 86px;

        height: 93px;

        background: #164d68;

        clip-path:
            polygon(
                0 0,
                100% 0,
                70% 100%,
                30% 100%
            );

        z-index: 2;
    }


    #solapa1 {

        position: absolute;

        left: calc(50% - 100px);

        top: 181px;

        width: 100px;

        height: 100px;

        background: white;

        clip-path:
            polygon(
                0 0,
                100% 0,
                100% 100%
            );

        z-index: 3;
    }


    #solapa2 {

        position: absolute;

        left: 50%;

        top: 181px;

        width: 100px;

        height: 100px;

        background: white;

        clip-path:
            polygon(
                0 0,
                100% 0,
                0 100%
            );

        z-index: 3;
    }


    #brazo-izq,
    #brazo-der {

        position: absolute;

        top: 205px;

        width: 74px;

        height: 326px;

        background: #ececec;

        border: 3px solid #aaa;

        border-radius: 38px;
    }


    #brazo-izq {

        left: calc(50% - 203px);

        transform: rotate(4deg);
    }


    #brazo-der {

        left: calc(50% + 129px);

        transform: rotate(-4deg);
    }


    #mano-izq,
    #mano-der {

        position: absolute;

        top: 500px;

        width: 70px;

        height: 94px;

        border-radius: 30px 30px 38px 38px;

        background: #d6a47e;

        border: 3px solid #9b7257;
    }


    #mano-izq {

        left: calc(50% - 201px);
    }


    #mano-der {

        left: calc(50% + 131px);
    }


    /* ===========================================
       ZONAS DE DESTINO
       =========================================== */

    .zona {

        position: absolute;

        border: 3px dashed;

        border-radius: 16px;

        box-sizing: border-box;

        display: flex;

        align-items: center;

        justify-content: center;

        text-align: center;

        font-size: 14px;

        font-weight: bold;

        z-index: 20;
    }


    #zona-ojos {

        left: calc(50% + 65px);

        top: 42px;

        width: 110px;

        height: 75px;

        border-color: #f3a536;

        color: #f3a536;
    }


    #zona-pecho {

        left: calc(50% - 65px);

        top: 300px;

        width: 130px;

        height: 115px;

        border-color: #4ca4ff;

        color: #4ca4ff;
    }


    #zona-mano {

        left: calc(50% + 118px);

        top: 485px;

        width: 105px;

        height: 120px;

        border-color: #75c85d;

        color: #75c85d;
    }


    /* ===========================================
       PANEL
       =========================================== */

    #panel {

        position: absolute;

        right: 3%;

        top: 120px;

        width: 35%;

        height: 560px;

        border-radius: 22px;

        background: #151e27;

        border: 1px solid #3b4a59;

        padding: 22px;

        box-sizing: border-box;
    }


    #panel h2 {

        margin: 0 0 7px 0;

        text-align: center;

        font-size: 22px;
    }


    #panel-sub {

        text-align: center;

        color: #aeb9c4;

        margin-bottom: 20px;
    }


    .tarjeta {

        position: relative;

        height: 128px;

        margin-bottom: 17px;

        border-radius: 17px;

        border: 1px solid #455567;

        background: #101820;

        padding-left: 120px;

        padding-top: 22px;

        padding-right: 10px;

        box-sizing: border-box;
    }


    .tarjeta-titulo {

        font-size: 16px;

        font-weight: bold;

        margin-bottom: 8px;
    }


    .descripcion {

        font-size: 13px;

        color: #c1c9d1;

        line-height: 1.4;
    }


    /* ===========================================
       DOSÍMETROS
       =========================================== */

    .dosimetro {

        position: absolute;

        cursor: grab;

        z-index: 100;

        user-select: none;
    }


    .dosimetro:active {
        cursor: grabbing;
    }


    /* Badge cuerpo entero */

    #dos-cuerpo {

        left: 27px;

        top: 27px;

        width: 62px;

        height: 80px;

        border-radius: 8px;

        background:
            linear-gradient(
                #2585cf,
                #146092
            );

        border: 3px solid #7abff2;

        box-shadow:
            0 6px 12px rgba(0,0,0,.35);
    }


    #dos-cuerpo:before {

        content: "";

        position: absolute;

        left: 18px;

        top: -14px;

        width: 25px;

        height: 18px;

        background: #aaa;

        border-radius: 5px;
    }


    #dos-cuerpo:after {

        content: "";

        position: absolute;

        left: 12px;

        top: 20px;

        width: 38px;

        height: 43px;

        border-radius: 4px;

        background: #e8e8e8;
    }


    /* Anillo */

    #dos-anillo {

        left: 28px;

        top: 31px;

        width: 62px;

        height: 62px;

        border-radius: 50%;

        border: 14px solid #78bd63;

        box-sizing: border-box;

        background: transparent;

        box-shadow:
            0 5px 10px rgba(0,0,0,.3);
    }


    #dos-anillo:after {

        content: "";

        position: absolute;

        top: -13px;

        left: 8px;

        width: 18px;

        height: 14px;

        border-radius: 4px;

        background: #d8e8d2;
    }


    /* Cristalino / gafas */

    #dos-ojos {

        left: 15px;

        top: 38px;

        width: 86px;

        height: 43px;
    }


    #cristal-l {

        position: absolute;

        left: 0;

        top: 5px;

        width: 35px;

        height: 24px;

        border: 5px solid #d28c2c;

        border-radius: 10px;
    }


    #cristal-r {

        position: absolute;

        right: 0;

        top: 5px;

        width: 35px;

        height: 24px;

        border: 5px solid #d28c2c;

        border-radius: 10px;
    }


    #cristal-puente {

        position: absolute;

        left: 35px;

        top: 16px;

        width: 16px;

        height: 5px;

        background: #d28c2c;
    }


    #sensor-ojo {

        position: absolute;

        right: 5px;

        top: 0;

        width: 18px;

        height: 18px;

        border-radius: 3px;

        background: #444;

        border: 2px solid #eee;
    }


    /* ===========================================
       MENSAJE
       =========================================== */

    #mensaje {

        position: absolute;

        bottom: 33px;

        left: 5%;

        width: 55%;

        min-height: 62px;

        border-radius: 14px;

        border: 1px solid #3b4a59;

        background: #121a22;

        display: flex;

        align-items: center;

        justify-content: center;

        text-align: center;

        font-size: 17px;

        color: white;

        padding: 10px 18px;

        box-sizing: border-box;
    }


    #contador {

        position: absolute;

        right: 3%;

        bottom: 46px;

        width: 35%;

        text-align: center;

        color: #c3ccd5;

        font-size: 17px;
    }


    .correcto {

        box-shadow:
            0 0 0 5px rgba(88,205,108,.30);

        pointer-events: none;
    }


    </style>

    </head>


    <body>


    <div id="laboratorio">


        <div id="titulo">

            Ubicación de los dosímetros personales

        </div>


        <div id="instruccion">

            Arrastrá cada dosímetro hasta la región correspondiente.

        </div>


        <div id="persona">


            <div id="cabeza">

                <div id="cabello"></div>

                <div id="lente-izq"></div>

                <div id="lente-der"></div>

                <div id="puente"></div>

            </div>


            <div id="cuello"></div>

            <div id="torso"></div>

            <div id="remera"></div>

            <div id="solapa1"></div>

            <div id="solapa2"></div>

            <div id="brazo-izq"></div>

            <div id="brazo-der"></div>

            <div id="mano-izq"></div>

            <div id="mano-der"></div>


            <div
            class="zona"
            id="zona-ojos"
            >

                CRISTALINO

            </div>


            <div
            class="zona"
            id="zona-pecho"
            >

                CUERPO<br>ENTERO

            </div>


            <div
            class="zona"
            id="zona-mano"
            >

                EXTREMIDAD

            </div>


        </div>


        <div id="panel">


            <h2>
                Dosímetros disponibles
            </h2>


            <div id="panel-sub">
                Arrastrá cada uno hacia el trabajador
            </div>


            <div class="tarjeta">


                <div
                class="dosimetro"
                id="dos-cuerpo"
                ></div>


                <div
                class="tarjeta-titulo"
                style="color:#56aaff;"
                >
                    DOSÍMETRO DE CUERPO ENTERO
                </div>


                <div class="descripcion">
                    Registra la exposición personal acumulada
                    durante el período de utilización.
                </div>


            </div>


            <div class="tarjeta">


                <div
                class="dosimetro"
                id="dos-anillo"
                ></div>


                <div
                class="tarjeta-titulo"
                style="color:#84ce6b;"
                >
                    DOSÍMETRO DE EXTREMIDAD
                </div>


                <div class="descripcion">
                    Evalúa la exposición localizada
                    de manos y dedos.
                </div>


            </div>


            <div class="tarjeta">


                <div
                class="dosimetro"
                id="dos-ojos"
                >

                    <div id="cristal-l"></div>

                    <div id="cristal-r"></div>

                    <div id="cristal-puente"></div>

                    <div id="sensor-ojo"></div>

                </div>


                <div
                class="tarjeta-titulo"
                style="color:#e5a342;"
                >
                    DOSÍMETRO DE CRISTALINO
                </div>


                <div class="descripcion">
                    Evalúa la exposición localizada
                    en la región ocular.
                </div>


            </div>


        </div>


        <div id="mensaje">

            🖱️ Arrastrá uno de los dosímetros para comenzar.

        </div>


        <div id="contador">

            Ubicaciones correctas:
            <span id="numero">0</span>
            / 3

        </div>


    </div>


    <script>


    const lab =
        document.getElementById("laboratorio");


    const mensaje =
        document.getElementById("mensaje");


    const numero =
        document.getElementById("numero");


    let colocados = {

        "dos-cuerpo": false,

        "dos-anillo": false,

        "dos-ojos": false

    };


    const configuracion = {


        "dos-cuerpo": {

            zona: "zona-pecho",

            texto:
                "✅ Correcto. El dosímetro de cuerpo entero quedó ubicado en la región correspondiente."

        },


        "dos-anillo": {

            zona: "zona-mano",

            texto:
                "✅ Correcto. El dosímetro de extremidad quedó ubicado sobre la mano."

        },


        "dos-ojos": {

            zona: "zona-ojos",

            texto:
                "✅ Correcto. El dosímetro de cristalino quedó ubicado próximo a los ojos."

        }

    };


    function centro(elemento) {


        const r =
            elemento.getBoundingClientRect();


        return {

            x:
                r.left
                +
                r.width/2,

            y:
                r.top
                +
                r.height/2

        };

    }


    function dentro(elemento, zona) {


        const e =
            centro(elemento);


        const z =
            zona.getBoundingClientRect();


        return (

            e.x >= z.left

            &&

            e.x <= z.right

            &&

            e.y >= z.top

            &&

            e.y <= z.bottom

        );

    }


    function activarArrastre(id) {


        const item =
            document.getElementById(id);


        let dragging = false;

        let offsetX = 0;

        let offsetY = 0;


        item.addEventListener(

            "mousedown",

            function(e) {


                if (colocados[id])
                    return;


                dragging = true;


                const r =
                    item.getBoundingClientRect();


                const lr =
                    lab.getBoundingClientRect();


                offsetX =
                    e.clientX
                    -
                    r.left;


                offsetY =
                    e.clientY
                    -
                    r.top;


                item.style.left =
                    (
                        r.left
                        -
                        lr.left
                    )
                    +
                    "px";


                item.style.top =
                    (
                        r.top
                        -
                        lr.top
                    )
                    +
                    "px";


                lab.appendChild(item);

            }

        );


        document.addEventListener(

            "mousemove",

            function(e) {


                if (!dragging)
                    return;


                const lr =
                    lab.getBoundingClientRect();


                let x =
                    e.clientX
                    -
                    lr.left
                    -
                    offsetX;


                let y =
                    e.clientY
                    -
                    lr.top
                    -
                    offsetY;


                x =
                    Math.max(
                        0,
                        Math.min(
                            lr.width
                            -
                            item.offsetWidth,
                            x
                        )
                    );


                y =
                    Math.max(
                        0,
                        Math.min(
                            lr.height
                            -
                            item.offsetHeight,
                            y
                        )
                    );


                item.style.left =
                    x
                    +
                    "px";


                item.style.top =
                    y
                    +
                    "px";

            }

        );


        document.addEventListener(

            "mouseup",

            function() {


                if (!dragging)
                    return;


                dragging = false;


                const config =
                    configuracion[id];


                const zona =
                    document.getElementById(
                        config.zona
                    );


                if (
                    dentro(
                        item,
                        zona
                    )
                ) {


                    const zr =
                        zona.getBoundingClientRect();


                    const lr =
                        lab.getBoundingClientRect();


                    item.style.left =
                        (
                            zr.left
                            -
                            lr.left
                            +
                            zr.width/2
                            -
                            item.offsetWidth/2
                        )
                        +
                        "px";


                    item.style.top =
                        (
                            zr.top
                            -
                            lr.top
                            +
                            zr.height/2
                            -
                            item.offsetHeight/2
                        )
                        +
                        "px";


                    item.classList.add(
                        "correcto"
                    );


                    colocados[id] =
                        true;


                    mensaje.innerHTML =
                        config.texto;

                }


                else {


                    mensaje.innerHTML =
                        "⚠️ Esa región no corresponde a este dosímetro. Probá nuevamente.";

                }


                const total =
                    Object
                    .values(colocados)
                    .filter(Boolean)
                    .length;


                numero.innerHTML =
                    total;


                if (total === 3) {


                    mensaje.innerHTML =
                        "🎉 ¡Muy bien! Ubicaste correctamente los tres dosímetros.";

                }

            }

        );

    }


    activarArrastre("dos-cuerpo");

    activarArrastre("dos-anillo");

    activarArrastre("dos-ojos");


    </script>

    </body>

    </html>

    """

    st.components.v1.html(
        html,
        height=850,
        scrolling=False
    )


# ============================================================
# TAB 2
# TLD INTERACTIVO
# ============================================================

with tab2:

    st.header("💎 ¿Qué ocurre dentro de un TLD?")

    st.write(
        """
        El TLD almacena información de la exposición en estados
        de atrapamiento del material.

        Modificá la exposición y observá cómo aumenta la cantidad
        de electrones representados en las **trampas**.
        """
    )

    col1, col2 = st.columns(
        [1.25, 0.75]
    )

    with col2:

        dosis_tld = st.slider(
            "Exposición relativa del TLD",
            min_value=0,
            max_value=100,
            value=35,
            step=1
        )

        temperatura = st.slider(
            "Temperatura de lectura simulada (°C)",
            min_value=25,
            max_value=300,
            value=25,
            step=5
        )

        if temperatura < 70:

            st.info(
                "💎 La mayor parte de los portadores permanece atrapada."
            )

        elif temperatura < 150:

            st.warning(
                "🔥 Comienza la liberación progresiva de portadores atrapados."
            )

        elif temperatura < 230:

            st.success(
                "✨ Se produce una emisión luminosa importante durante la lectura."
            )

        else:

            st.info(
                "📉 La señal disminuye después de la región principal de emisión."
            )


    with col1:

        cantidad = int(
            dosis_tld / 5
        )

        puntos = ""

        posiciones = [

            (130,195),
            (180,210),
            (230,185),
            (285,218),
            (335,190),

            (145,265),
            (200,285),
            (255,258),
            (310,290),
            (355,260),

            (155,340),
            (215,325),
            (270,350),
            (325,330),
            (370,345),

            (180,395),
            (235,410),
            (295,390),
            (345,415),
            (390,395)

        ]


   for i in range(
    min(
        cantidad,
        len(posiciones)
    )
):

    px, py = posiciones[i]

    puntos += f"""

    <circle
        cx="{px}"
        cy="{py}"
        r="8"
        fill="#56b9ff"
        stroke="#d6f2ff"
        stroke-width="2"
    />

    """


        fraccion_liberada = max(
            0,
            min(
                1,
                (temperatura - 70)
                /
                140
            )
        )


        visibles = int(
            cantidad
            *
            (
                1
                -
                fraccion_liberada
            )
        )


        puntos_visibles = ""

       for i in range(
    min(
        visibles,
        len(posiciones)
    )
):

    px, py = posiciones[i]

    puntos_visibles += f"""

    <circle
        cx="{px}"
        cy="{py}"
        r="8"
        fill="#56b9ff"
        stroke="#d6f2ff"
        stroke-width="2"
    />

    """


        destellos = ""

        if temperatura >= 80:

            n_luz = max(
                2,
                cantidad - visibles
            )

            for i in range(
                min(
                    n_luz,
                    12
                )
            ):

                x_luz = 470 + (i % 4)*36

                y_luz = 190 + (i // 4)*58

                destellos += f"""

                <circle
                    cx="{x_luz}"
                    cy="{y_luz}"
                    r="9"
                    fill="#ffe65a"
                    opacity="0.85"
                />

                """


        svg_tld = f"""

        <svg
            viewBox="0 0 700 520"
            width="100%"
        >

        <rect
            x="25"
            y="25"
            width="650"
            height="460"
            rx="25"
            fill="#101820"
            stroke="#425466"
            stroke-width="2"
        />


        <text
            x="350"
            y="65"
            text-anchor="middle"
            fill="white"
            font-size="22"
            font-weight="bold"
        >
            Representación del material termoluminiscente
        </text>


        <rect
            x="80"
            y="100"
            width="360"
            height="50"
            rx="10"
            fill="#8d62d4"
        />


        <text
            x="260"
            y="132"
            text-anchor="middle"
            fill="white"
            font-size="17"
        >
            Banda de conducción
        </text>


        <rect
            x="80"
            y="435"
            width="360"
            height="35"
            rx="8"
            fill="#8d62d4"
        />


        <text
            x="260"
            y="459"
            text-anchor="middle"
            fill="white"
            font-size="16"
        >
            Banda de valencia
        </text>


        <rect
            x="110"
            y="175"
            width="300"
            height="250"
            rx="22"
            fill="#182734"
            stroke="#4c6a7e"
            stroke-width="2"
        />


        <text
            x="260"
            y="405"
            text-anchor="middle"
            fill="#bcd0dd"
            font-size="16"
        >
            Trampas electrónicas
        </text>


        {puntos_visibles}


        <text
            x="530"
            y="130"
            text-anchor="middle"
            fill="white"
            font-size="20"
            font-weight="bold"
        >
            LUZ EMITIDA
        </text>


        {destellos}


        <text
            x="530"
            y="405"
            text-anchor="middle"
            fill="#ffcb4d"
            font-size="17"
        >
            {temperatura} °C
        </text>


        <text
            x="530"
            y="435"
            text-anchor="middle"
            fill="#aebbc6"
            font-size="14"
        >
            calentamiento simulado
        </text>


        </svg>

        """


        st.components.v1.html(
            svg_tld,
            height=540,
            scrolling=False
        )


    # CURVA GLOW

    temp = np.linspace(
        25,
        300,
        500
    )

    amplitud = (
        dosis_tld
        /
        100
    )

    pico_principal = (
        amplitud
        *
        np.exp(
            -0.5
            *
            (
                (
                    temp
                    -
                    190
                )
                /
                26
            )
            ** 2
        )
    )

    pico_secundario = (
        0.28
        *
        amplitud
        *
        np.exp(
            -0.5
            *
            (
                (
                    temp
                    -
                    90
                )
                /
                17
            )
            ** 2
        )
    )

    brillo = (
        pico_principal
        +
        pico_secundario
    )


    fig = go.Figure()


    fig.add_trace(

        go.Scatter(

            x=temp,

            y=brillo,

            mode="lines",

            name="Curva Glow simulada"

        )

    )


    valor_actual = float(
        np.interp(
            temperatura,
            temp,
            brillo
        )
    )


    fig.add_trace(

        go.Scatter(

            x=[temperatura],

            y=[valor_actual],

            mode="markers",

            marker=dict(
                size=15
            ),

            name="Temperatura actual"

        )

    )


    fig.update_layout(

        title="Curva de brillo simulada",

        xaxis_title="Temperatura (°C)",

        yaxis_title="Intensidad luminosa relativa",

        height=420

    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    st.caption(
        """
        La forma de la curva es una representación didáctica.
        Su objetivo es visualizar la relación entre calentamiento
        y emisión luminosa durante la lectura de un TLD.
        """
    )


# ============================================================
# TAB 3
# COMPARADOR DE DOSÍMETROS
# ============================================================

with tab3:

    st.header(
        "🔬 Comparador de dosímetros"
    )

    st.write(
        """
        Seleccioná un dosímetro y observá qué ocurre desde que recibe
        radiación hasta que se obtiene la información dosimétrica.
        """
    )

    tipo = st.radio(

        "Seleccioná el tipo de dosímetro:",

        [
            "TLD",
            "OSLD",
            "Dosímetro electrónico"
        ],

        horizontal=True

    )


    if tipo == "TLD":

        st.subheader(
            "💎 Dosímetro termoluminiscente — TLD"
        )

        st.markdown(
            """
            ### Secuencia conceptual

            **Radiación → almacenamiento en trampas → calentamiento → emisión de luz → lectura**

            El material almacena parte de la información producida
            por la exposición. Posteriormente se induce la liberación
            de los portadores mediante calentamiento.
            """
        )


        html_comp = """

        <div style="
            background:#101820;
            border:1px solid #445566;
            border-radius:20px;
            padding:35px;
            color:white;
            font-family:Arial;
            text-align:center;
            font-size:20px;
            line-height:2.2;
        ">

        ☢️ Radiación

        &nbsp; → &nbsp;

        💎 Trampas

        &nbsp; → &nbsp;

        🔥 Calentamiento

        &nbsp; → &nbsp;

        ✨ Luz

        &nbsp; → &nbsp;

        📊 Dosis

        </div>

        """

        st.components.v1.html(
            html_comp,
            height=170
        )


        st.info(
            "La información no se observa directamente durante la exposición; "
            "requiere posteriormente un proceso de lectura."
        )


    elif tipo == "OSLD":

        st.subheader(
            "🔵 Dosímetro de luminiscencia ópticamente estimulada — OSLD"
        )

        st.markdown(
            """
            ### Secuencia conceptual

            **Radiación → almacenamiento → estimulación óptica → luminiscencia → lectura**

            En este caso, la liberación de la información almacenada
            se produce mediante **estimulación óptica**.
            """
        )


        html_comp = """

        <div style="
            background:#101820;
            border:1px solid #445566;
            border-radius:20px;
            padding:35px;
            color:white;
            font-family:Arial;
            text-align:center;
            font-size:20px;
            line-height:2.2;
        ">

        ☢️ Radiación

        &nbsp; → &nbsp;

        🔵 Almacenamiento

        &nbsp; → &nbsp;

        💡 Luz de estimulación

        &nbsp; → &nbsp;

        ✨ OSL

        &nbsp; → &nbsp;

        📊 Dosis

        </div>

        """

        st.components.v1.html(
            html_comp,
            height=170
        )


        st.info(
            "La presentación también aborda la estimulación OSL, "
            "su lector y la pérdida de señal asociada a múltiples lecturas."
        )


    else:

        st.subheader(
            "📟 Dosímetro electrónico de lectura directa"
        )

        st.markdown(
            """
            ### Secuencia conceptual

            **Radiación → detector → señal electrónica → procesamiento → lectura**

            A diferencia de los sistemas que requieren una lectura posterior,
            el dosímetro electrónico permite visualizar información durante
            su utilización.
            """
        )


        dosis_electronico = st.slider(
            "Dosis acumulada simulada (µSv)",
            min_value=0,
            max_value=500,
            value=25,
            step=5
        )


        tasa_electronico = st.slider(
            "Tasa de dosis simulada (µSv/h)",
            min_value=0,
            max_value=100,
            value=5,
            step=1
        )


        html_electronico = f"""

        <div style="
            width:430px;
            height:260px;
            margin:auto;
            background:#252525;
            border:4px solid #111;
            border-radius:24px;
            box-shadow:0 10px 24px rgba(0,0,0,.3);
            padding-top:35px;
            text-align:center;
            font-family:Arial;
        ">

            <div style="
                margin:auto;
                width:330px;
                height:115px;
                background:#cfe8c8;
                border:3px solid #111;
                border-radius:10px;
                font-family:monospace;
                color:#111;
                padding-top:15px;
            ">

                <div style="
                    font-size:29px;
                    font-weight:bold;
                ">
                    {dosis_electronico} µSv
                </div>

                <div style="
                    font-size:21px;
                    margin-top:12px;
                ">
                    {tasa_electronico} µSv/h
                </div>

            </div>

            <div style="
                color:white;
                font-size:18px;
                margin-top:26px;
                font-weight:bold;
            ">
                DOSÍMETRO ELECTRÓNICO
            </div>

        </div>

        """


        st.components.v1.html(
            html_electronico,
            height=300
        )


    st.divider()


    st.subheader(
        "Resumen rápido"
    )


    st.markdown(
        """
        | Tipo | ¿Almacena información? | Forma conceptual de lectura |
        |---|---|---|
        | **TLD** | Sí | Calentamiento → luz |
        | **OSLD** | Sí | Estimulación óptica → luz |
        | **Electrónico** | Procesamiento electrónico | Lectura directa |
        """
    )


# ============================================================
# TAB 4
# CALIBRACIÓN
# ============================================================

with tab4:

    st.header(
        "📐 Simulación conceptual de calibración"
    )

    st.write(
        """
        Un dosímetro debe relacionar su respuesta con una referencia conocida.

        En esta actividad vas a comparar una **dosis de referencia**
        con la lectura obtenida por distintos elementos de un dosímetro.
        """
    )

    st.warning(
        "⚠️ Los valores son exclusivamente didácticos. "
        "La actividad no representa un procedimiento real de irradiación o calibración."
    )


    dosis_referencia = st.slider(
        "Dosis de referencia simulada (mSv)",
        min_value=0.1,
        max_value=10.0,
        value=2.0,
        step=0.1
    )


    dispersion = st.slider(
        "Variación de sensibilidad entre elementos (%)",
        min_value=0,
        max_value=20,
        value=8,
        step=1
    )


    semilla = int(
        dosis_referencia * 100
        +
        dispersion * 31
    )


    rng = np.random.default_rng(
        semilla
    )


    respuestas = (
        dosis_referencia
        *
        (
            1
            +
            rng.normal(
                0,
                dispersion/100,
                4
            )
        )
    )


    promedio = float(
        np.mean(
            respuestas
        )
    )


    factor_correccion = (
        dosis_referencia
        /
        promedio
    )


    corregidas = (
        respuestas
        *
        factor_correccion
    )


    col1, col2 = st.columns(
        [1.2, 0.8]
    )


    with col1:

        fig_cal = go.Figure()


        fig_cal.add_trace(

            go.Bar(

                x=[
                    "Elemento 1",
                    "Elemento 2",
                    "Elemento 3",
                    "Elemento 4"
                ],

                y=respuestas,

                name="Lectura inicial"

            )

        )


        fig_cal.add_trace(

            go.Bar(

                x=[
                    "Elemento 1",
                    "Elemento 2",
                    "Elemento 3",
                    "Elemento 4"
                ],

                y=corregidas,

                name="Lectura corregida"

            )

        )


        fig_cal.add_hline(

            y=dosis_referencia,

            line_dash="dash",

            annotation_text="Referencia"

        )


        fig_cal.update_layout(

            title="Respuesta de los elementos",

            yaxis_title="Dosis simulada (mSv)",

            barmode="group",

            height=470

        )


        st.plotly_chart(
            fig_cal,
            use_container_width=True
        )


    with col2:

        st.metric(
            "Referencia",
            f"{dosis_referencia:.2f} mSv"
        )


        st.metric(
            "Promedio antes de corregir",
            f"{promedio:.2f} mSv"
        )


        st.metric(
            "Factor de corrección conceptual",
            f"{factor_correccion:.3f}"
        )


        promedio_corregido = float(
            np.mean(
                corregidas
            )
        )


        st.metric(
            "Promedio corregido",
            f"{promedio_corregido:.2f} mSv"
        )


    st.success(
        """
        La simulación muestra la idea de que distintos elementos pueden presentar
        respuestas diferentes y que la caracterización/calibración permite
        relacionar esa respuesta con una referencia.
        """
    )


    st.caption(
        """
        Esta actividad representa conceptualmente la homogeneización de la respuesta
        y los factores de sensibilidad. No reproduce el procedimiento de calibración
        de un servicio real.
        """
    )
