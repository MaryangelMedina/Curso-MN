import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="Unidad 8 - Dosimetría personal",
    page_icon="☢️",
    layout="wide",
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

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "👤 ¿Dónde llevo mi dosímetro?",
        "💎 TLD interactivo",
        "🔬 Comparador de dosímetros",
        "📐 Calibración",
        "🧍 Magnitudes dosimétricas",
    ]
)


# ============================================================
# TAB 1 — UBICACIÓN DE LOS DOSÍMETROS
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

    html = r"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">

    <style>

    body{
        margin:0;
        background:transparent;
        font-family:Arial,sans-serif;
        overflow:hidden;
        color:white;
    }

    #laboratorio{
        position:relative;
        width:100%;
        height:820px;
        background:linear-gradient(135deg,#111923,#0d1117);
        border-radius:26px;
        border:1px solid #35404d;
        overflow:hidden;
    }

    #titulo{
        position:absolute;
        top:20px;
        width:100%;
        text-align:center;
        font-size:25px;
        font-weight:bold;
        color:white;
    }

    #instruccion{
        position:absolute;
        top:62px;
        width:100%;
        text-align:center;
        font-size:16px;
        color:#cbd5df;
    }

    #persona{
        position:absolute;
        left:5%;
        top:112px;
        width:55%;
        height:610px;
    }

    #cabeza{
        position:absolute;
        left:calc(50% - 62px);
        top:8px;
        width:124px;
        height:145px;
        border-radius:50% 50% 45% 45%;
        background:#d6a47e;
        border:3px solid #9b7257;
    }

    #cabello{
        position:absolute;
        left:-3px;
        top:-4px;
        width:130px;
        height:52px;
        border-radius:65px 65px 25px 25px;
        background:#3a2c27;
    }

    #lente-izq,
    #lente-der{
        position:absolute;
        top:56px;
        width:42px;
        height:28px;
        border:4px solid #3e4850;
        border-radius:10px;
        background:rgba(190,225,240,.16);
    }

    #lente-izq{
        left:13px;
    }

    #lente-der{
        right:13px;
    }

    #puente{
        position:absolute;
        top:68px;
        left:55px;
        width:14px;
        height:4px;
        background:#3e4850;
    }

    #cuello{
        position:absolute;
        left:calc(50% - 29px);
        top:137px;
        width:58px;
        height:50px;
        background:#c79270;
    }

    #torso{
        position:absolute;
        left:calc(50% - 138px);
        top:177px;
        width:276px;
        height:350px;
        border-radius:42px 42px 20px 20px;
        background:linear-gradient(90deg,#dedede,#fafafa,#dedede);
        border:3px solid #aaa;
    }

    #remera{
        position:absolute;
        left:calc(50% - 43px);
        top:181px;
        width:86px;
        height:93px;
        background:#164d68;
        clip-path:polygon(0 0,100% 0,70% 100%,30% 100%);
        z-index:2;
    }

    #solapa1{
        position:absolute;
        left:calc(50% - 100px);
        top:181px;
        width:100px;
        height:100px;
        background:white;
        clip-path:polygon(0 0,100% 0,100% 100%);
        z-index:3;
    }

    #solapa2{
        position:absolute;
        left:50%;
        top:181px;
        width:100px;
        height:100px;
        background:white;
        clip-path:polygon(0 0,100% 0,0 100%);
        z-index:3;
    }

    #brazo-izq,
    #brazo-der{
        position:absolute;
        top:205px;
        width:74px;
        height:326px;
        background:#ececec;
        border:3px solid #aaa;
        border-radius:38px;
    }

    #brazo-izq{
        left:calc(50% - 203px);
        transform:rotate(4deg);
    }

    #brazo-der{
        left:calc(50% + 129px);
        transform:rotate(-4deg);
    }

    #mano-izq,
    #mano-der{
        position:absolute;
        top:500px;
        width:70px;
        height:94px;
        border-radius:30px 30px 38px 38px;
        background:#d6a47e;
        border:3px solid #9b7257;
    }

    #mano-izq{
        left:calc(50% - 201px);
    }

    #mano-der{
        left:calc(50% + 131px);
    }

    .zona{
        position:absolute;
        border:3px dashed;
        border-radius:16px;
        box-sizing:border-box;
        display:flex;
        align-items:center;
        justify-content:center;
        text-align:center;
        font-size:14px;
        font-weight:bold;
        z-index:20;
    }

    #zona-ojos{
        left:calc(50% + 65px);
        top:42px;
        width:110px;
        height:75px;
        border-color:#f3a536;
        color:#f3a536;
    }

    #zona-pecho{
        left:calc(50% - 65px);
        top:300px;
        width:130px;
        height:115px;
        border-color:#4ca4ff;
        color:#4ca4ff;
    }

    #zona-mano{
        left:calc(50% + 118px);
        top:485px;
        width:105px;
        height:120px;
        border-color:#75c85d;
        color:#75c85d;
    }

    #panel{
        position:absolute;
        right:3%;
        top:120px;
        width:35%;
        height:560px;
        border-radius:22px;
        background:#151e27;
        border:1px solid #3b4a59;
        padding:22px;
        box-sizing:border-box;
    }

    #panel h2{
        margin:0 0 7px 0;
        text-align:center;
        font-size:22px;
    }

    #panel-sub{
        text-align:center;
        color:#aeb9c4;
        margin-bottom:20px;
    }

    .tarjeta{
        position:relative;
        height:128px;
        margin-bottom:17px;
        border-radius:17px;
        border:1px solid #455567;
        background:#101820;
        padding-left:120px;
        padding-top:22px;
        padding-right:10px;
        box-sizing:border-box;
    }

    .tarjeta-titulo{
        font-size:16px;
        font-weight:bold;
        margin-bottom:8px;
    }

    .descripcion{
        font-size:13px;
        color:#c1c9d1;
        line-height:1.4;
    }

    .dosimetro{
        position:absolute;
        cursor:grab;
        z-index:100;
        user-select:none;
    }

    .dosimetro:active{
        cursor:grabbing;
    }

    #dos-cuerpo{
        left:27px;
        top:27px;
        width:62px;
        height:80px;
        border-radius:8px;
        background:linear-gradient(#2585cf,#146092);
        border:3px solid #7abff2;
        box-shadow:0 6px 12px rgba(0,0,0,.35);
    }

    #dos-cuerpo:before{
        content:"";
        position:absolute;
        left:18px;
        top:-14px;
        width:25px;
        height:18px;
        background:#aaa;
        border-radius:5px;
    }

    #dos-cuerpo:after{
        content:"";
        position:absolute;
        left:12px;
        top:20px;
        width:38px;
        height:43px;
        border-radius:4px;
        background:#e8e8e8;
    }

    #dos-anillo{
        left:28px;
        top:31px;
        width:62px;
        height:62px;
        border-radius:50%;
        border:14px solid #78bd63;
        box-sizing:border-box;
        background:transparent;
        box-shadow:0 5px 10px rgba(0,0,0,.3);
    }

    #dos-anillo:after{
        content:"";
        position:absolute;
        top:-13px;
        left:8px;
        width:18px;
        height:14px;
        border-radius:4px;
        background:#d8e8d2;
    }

    #dos-ojos{
        left:15px;
        top:38px;
        width:86px;
        height:43px;
    }

    #cristal-l,
    #cristal-r{
        position:absolute;
        top:5px;
        width:35px;
        height:24px;
        border:5px solid #d28c2c;
        border-radius:10px;
    }

    #cristal-l{
        left:0;
    }

    #cristal-r{
        right:0;
    }

    #cristal-puente{
        position:absolute;
        left:35px;
        top:16px;
        width:16px;
        height:5px;
        background:#d28c2c;
    }

    #sensor-ojo{
        position:absolute;
        right:5px;
        top:0;
        width:18px;
        height:18px;
        border-radius:3px;
        background:#444;
        border:2px solid #eee;
    }

    #mensaje{
        position:absolute;
        bottom:33px;
        left:5%;
        width:55%;
        min-height:62px;
        border-radius:14px;
        border:1px solid #3b4a59;
        background:#121a22;
        display:flex;
        align-items:center;
        justify-content:center;
        text-align:center;
        font-size:17px;
        color:white;
        padding:10px 18px;
        box-sizing:border-box;
    }

    #contador{
        position:absolute;
        right:3%;
        bottom:46px;
        width:35%;
        text-align:center;
        color:#c3ccd5;
        font-size:17px;
    }

    .correcto{
        box-shadow:0 0 0 5px rgba(88,205,108,.30);
        pointer-events:none;
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

          <div class="zona" id="zona-ojos"></div>
          
          <div class="zona" id="zona-pecho"></div>
          
          <div class="zona" id="zona-mano"></div>

        </div>

        <div id="panel">

            <h2>Dosímetros disponibles</h2>

            <div id="panel-sub">
                Arrastrá cada uno hacia el trabajador
            </div>

            <div class="tarjeta">

                <div
                    class="dosimetro"
                    id="dos-cuerpo">
                </div>

                <div
                    class="tarjeta-titulo"
                    style="color:#56aaff;">
                    DOSÍMETRO DE CUERPO ENTERO
                </div>

                <div class="descripcion">
                    Registra la exposición personal acumulada durante el período de utilización.
                </div>

            </div>

            <div class="tarjeta">

                <div
                    class="dosimetro"
                    id="dos-anillo">
                </div>

                <div
                    class="tarjeta-titulo"
                    style="color:#84ce6b;">
                    DOSÍMETRO DE EXTREMIDAD
                </div>

                <div class="descripcion">
                    Evalúa la exposición localizada de manos y dedos.
                </div>

            </div>

            <div class="tarjeta">

                <div
                    class="dosimetro"
                    id="dos-ojos">

                    <div id="cristal-l"></div>
                    <div id="cristal-r"></div>
                    <div id="cristal-puente"></div>
                    <div id="sensor-ojo"></div>

                </div>

                <div
                    class="tarjeta-titulo"
                    style="color:#e5a342;">
                    DOSÍMETRO DE CRISTALINO
                </div>

                <div class="descripcion">
                    Evalúa la exposición localizada en la región ocular.
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
                r.width / 2,

            y:
                r.top
                +
                r.height / 2

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
                            zr.width / 2
                            -
                            item.offsetWidth / 2
                        )
                        +
                        "px";

                    item.style.top =
                        (
                            zr.top
                            -
                            lr.top
                            +
                            zr.height / 2
                            -
                            item.offsetHeight / 2
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


    activarArrastre(
        "dos-cuerpo"
    );

    activarArrastre(
        "dos-anillo"
    );

    activarArrastre(
        "dos-ojos"
    );

    </script>

    </body>
    </html>
    """

    st.components.v1.html(
        html,
        height=850,
        scrolling=False,
    )


# ============================================================
# TAB 2 — TLD INTERACTIVO
# ============================================================

with tab2:

    st.header(
        "💎 ¿Qué ocurre dentro de un TLD?"
    )

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
            step=1,
            key="dosis_tld_u8",
        )

        temperatura = st.slider(
            "Temperatura de lectura simulada (°C)",
            min_value=25,
            max_value=300,
            value=25,
            step=5,
            key="temperatura_tld_u8",
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

        posiciones = [

            (130, 195),

            (180, 210),

            (230, 185),

            (285, 218),

            (335, 190),

            (145, 265),

            (200, 285),

            (255, 258),

            (310, 290),

            (355, 260),

            (155, 340),

            (215, 325),

            (270, 350),

            (325, 330),

            (370, 345),

            (180, 395),

            (235, 410),

            (295, 390),

            (345, 415),

            (390, 395),

        ]


        fraccion_liberada = max(

            0.0,

            min(

                1.0,

                (
                    temperatura
                    -
                    70
                )
                /
                140,

            ),

        )


        visibles = int(

            cantidad
            *
            (
                1.0
                -
                fraccion_liberada
            )

        )


        puntos_visibles = ""


        for i in range(
            min(
                visibles,
                len(posiciones),
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
                cantidad - visibles,
            )

            for i in range(
                min(
                    n_luz,
                    12,
                )
            ):

                x_luz = (
                    470
                    +
                    (i % 4) * 36
                )

                y_luz = (
                    190
                    +
                    (i // 4) * 58
                )

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
    viewBox="0 0 700 560"
    width="100%"
    height="100%"
    preserveAspectRatio="xMidYMid meet"
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
            height=650,
            scrolling=False,
        )


    temp = np.linspace(
        25,
        300,
        500,
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

            name="Curva Glow simulada",

        )

    )


    valor_actual = float(

        np.interp(

            temperatura,

            temp,

            brillo,

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

            name="Temperatura actual",

        )

    )


    fig.update_layout(

        title="Curva de brillo simulada",

        xaxis_title="Temperatura (°C)",

        yaxis_title="Intensidad luminosa relativa",

        height=420,

    )


    st.plotly_chart(
        fig,
        use_container_width=True,
    )


    st.caption(
        """
        La forma de la curva es una representación didáctica.
        Su objetivo es visualizar la relación entre calentamiento
        y emisión luminosa durante la lectura de un TLD.
        """
    )


# ============================================================
# TAB 3 — COMPARADOR DE DOSÍMETROS
# ============================================================

with tab3:

    st.header("🔬 Comparador de dosímetros")

    st.write(
        """
        No todos los dosímetros personales entregan la información
        de la misma manera. Seleccioná cada tecnología y observá
        qué ocurre desde que el trabajador recibe la exposición
        hasta que obtiene el resultado dosimétrico.
        """
    )

    tipo = st.radio(
        "Seleccioná el dosímetro que utiliza el trabajador:",
        [
            "TLD",
            "OSLD",
            "Dosímetro electrónico",
        ],
        horizontal=True,
        key="comparador_u8",
    )

    # --------------------------------------------------------
    # Datos visuales según el tipo seleccionado
    # --------------------------------------------------------

    if tipo == "TLD":

        color = "#9b7be8"
        titulo = "TLD"
        nombre = "Dosímetro termoluminiscente"
        dispositivo = "TLD"

        etapa1 = "☢️ EXPOSICIÓN"
        etapa2 = "💎 TRAMPAS"
        etapa3 = "🔥 CALENTAMIENTO"
        etapa4 = "✨ LUZ"
        etapa5 = "📊 RESULTADO"

        resultado = "DIFERIDO"
        lectura = "Calentamiento"
        durante = "No"
        costo = "Menor"

        explicacion = """
        Durante el período de uso, la información queda almacenada
        en el material termoluminiscente. Para obtener el resultado,
        el dosímetro debe retirarse y procesarse en un sistema de lectura.
        El calentamiento libera los portadores atrapados y se produce
        una emisión luminosa relacionada con la exposición.
        """

    elif tipo == "OSLD":

        color = "#4ba6e8"
        titulo = "OSLD"
        nombre = "Dosímetro de luminiscencia ópticamente estimulada"
        dispositivo = "OSLD"

        etapa1 = "☢️ EXPOSICIÓN"
        etapa2 = "🔵 ALMACENAMIENTO"
        etapa3 = "💡 ESTIMULACIÓN ÓPTICA"
        etapa4 = "✨ LUZ"
        etapa5 = "📊 RESULTADO"

        resultado = "DIFERIDO"
        lectura = "Estimulación óptica"
        durante = "No"
        costo = "Menor / moderado"

        explicacion = """
        La información producida por la exposición queda almacenada
        en el material. Para realizar la lectura se utiliza una
        estimulación óptica que libera parte de esa información en
        forma de luminiscencia.
        """

    else:

        color = "#5fc46d"
        titulo = "ELECTRÓNICO"
        nombre = "Dosímetro electrónico de lectura directa"
        dispositivo = "DISPLAY"

        etapa1 = "☢️ EXPOSICIÓN"
        etapa2 = "⚡ SEÑAL"
        etapa3 = "🔌 ELECTRÓNICA"
        etapa4 = "📟 PANTALLA"
        etapa5 = "📊 RESULTADO"

        resultado = "INMEDIATO"
        lectura = "Electrónica"
        durante = "Sí"
        costo = "Mayor"

        explicacion = """
        La radiación produce una señal que es procesada electrónicamente.
        El trabajador puede disponer de información durante la utilización
        del equipo, sin esperar un procesamiento posterior del dosímetro.
        """

    # --------------------------------------------------------
    # Escena visual
    # --------------------------------------------------------

    html_comparador = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">

    <style>

    body {{
        margin: 0;
        background: transparent;
        font-family: Arial, sans-serif;
        color: white;
    }}

    .escena {{
        width: 100%;
        min-height: 620px;
        background: linear-gradient(135deg,#101820,#0d1117);
        border: 1px solid #394957;
        border-radius: 24px;
        padding: 28px;
        box-sizing: border-box;
    }}

    .titulo {{
        text-align: center;
        font-size: 25px;
        font-weight: bold;
        margin-bottom: 8px;
    }}

    .subtitulo {{
        text-align: center;
        color: #b7c3cc;
        font-size: 15px;
        margin-bottom: 28px;
    }}

    .contenido {{
        display: flex;
        gap: 25px;
        align-items: stretch;
    }}

    .trabajador {{
        flex: 0.8;
        min-height: 410px;
        background: #17212b;
        border: 1px solid #40505e;
        border-radius: 20px;
        position: relative;
        overflow: hidden;
    }}

    .persona {{
        position: relative;
        width: 260px;
        height: 370px;
        margin: 25px auto 0 auto;
    }}

    .cabeza {{
        position: absolute;
        left: 94px;
        top: 0;
        width: 72px;
        height: 82px;
        border-radius: 50%;
        background: #d5a47e;
        border: 3px solid #987158;
    }}

    .cabello {{
        position: absolute;
        left: -2px;
        top: -3px;
        width: 76px;
        height: 27px;
        border-radius: 40px 40px 15px 15px;
        background: #332824;
    }}

    .cuello {{
        position: absolute;
        left: 112px;
        top: 74px;
        width: 36px;
        height: 37px;
        background: #c99370;
    }}

    .torso {{
        position: absolute;
        left: 60px;
        top: 103px;
        width: 140px;
        height: 205px;
        border-radius: 35px 35px 18px 18px;
        background: linear-gradient(90deg,#e5e5e5,#ffffff,#e5e5e5);
        border: 3px solid #9d9d9d;
    }}

    .brazo-i,
    .brazo-d {{
        position: absolute;
        top: 120px;
        width: 45px;
        height: 195px;
        border-radius: 24px;
        background: #ececec;
        border: 3px solid #999;
    }}

    .brazo-i {{
        left: 24px;
        transform: rotate(5deg);
    }}

    .brazo-d {{
        right: 24px;
        transform: rotate(-5deg);
    }}

    .pierna-i,
    .pierna-d {{
        position: absolute;
        top: 295px;
        width: 52px;
        height: 70px;
        background: #384b5c;
    }}

    .pierna-i {{
        left: 72px;
    }}

    .pierna-d {{
        right: 72px;
    }}

    .badge {{
        position: absolute;
        left: 112px;
        top: 150px;
        width: 38px;
        height: 50px;
        border-radius: 6px;
        background: {color};
        border: 3px solid white;
        z-index: 10;
        box-shadow: 0 0 15px {color};
    }}

    .badge-display {{
        position: absolute;
        left: 5px;
        top: 10px;
        width: 28px;
        height: 16px;
        border-radius: 3px;
        background: #d4eccd;
        color: #111;
        font-size: 7px;
        text-align: center;
        line-height: 16px;
        font-weight: bold;
    }}

    .trabajador-texto {{
        position: absolute;
        bottom: 16px;
        width: 100%;
        text-align: center;
        font-size: 16px;
        color: #dbe5ec;
    }}

    .proceso {{
        flex: 1.7;
        min-height: 410px;
        background: #131c25;
        border: 1px solid #40505e;
        border-radius: 20px;
        padding: 22px;
        box-sizing: border-box;
    }}

    .proceso h3 {{
        text-align: center;
        margin-top: 0;
        color: {color};
        font-size: 21px;
    }}

    .flujo {{
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 18px;
    }}

    .etapa {{
        width: 82%;
        padding: 13px;
        margin: 4px 0;
        text-align: center;
        background: #1d2a35;
        border: 1px solid #465868;
        border-radius: 12px;
        font-size: 15px;
        font-weight: bold;
    }}

    .flecha {{
        color: {color};
        font-size: 21px;
        line-height: 20px;
    }}

    .resultado {{
        margin-top: 18px;
        background: {color};
        color: #111;
        padding: 14px;
        text-align: center;
        border-radius: 13px;
        font-size: 18px;
        font-weight: bold;
    }}

    .explicacion {{
        margin-top: 25px;
        background: #16222c;
        border-left: 5px solid {color};
        border-radius: 12px;
        padding: 18px;
        line-height: 1.55;
        color: #e0e7ec;
        font-size: 15px;
    }}

    </style>
    </head>

    <body>

    <div class="escena">

        <div class="titulo">
            {nombre}
        </div>

        <div class="subtitulo">
            Seguí el recorrido desde la exposición hasta la obtención del resultado
        </div>

        <div class="contenido">

            <div class="trabajador">

                <div class="persona">

                    <div class="cabeza">
                        <div class="cabello"></div>
                    </div>

                    <div class="cuello"></div>

                    <div class="torso"></div>

                    <div class="brazo-i"></div>

                    <div class="brazo-d"></div>

                    <div class="pierna-i"></div>

                    <div class="pierna-d"></div>

                    <div class="badge">

                        {
                            '<div class="badge-display">LIVE</div>'
                            if tipo == "Dosímetro electrónico"
                            else ""
                        }

                    </div>

                </div>

                <div class="trabajador-texto">
                    Personal ocupacionalmente expuesto<br>
                    <b>{titulo}</b>
                </div>

            </div>


            <div class="proceso">

                <h3>¿Qué ocurre con la información?</h3>

                <div class="flujo">

                    <div class="etapa">{etapa1}</div>

                    <div class="flecha">↓</div>

                    <div class="etapa">{etapa2}</div>

                    <div class="flecha">↓</div>

                    <div class="etapa">{etapa3}</div>

                    <div class="flecha">↓</div>

                    <div class="etapa">{etapa4}</div>

                    <div class="flecha">↓</div>

                    <div class="etapa">{etapa5}</div>

                </div>

                <div class="resultado">
                    RESULTADO {resultado}
                </div>

            </div>

        </div>

        <div class="explicacion">
            {explicacion}
        </div>

    </div>

    </body>
    </html>
    """

    st.components.v1.html(
        html_comparador,
        height=850,
        scrolling=False,
    )

    # --------------------------------------------------------
    # Comparación rápida
    # --------------------------------------------------------

    st.subheader("📋 Comparación rápida")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Resultado",
            resultado,
        )

    with c2:
        st.metric(
            "Forma de lectura",
            lectura,
        )

    with c3:
        st.metric(
            "Información durante el uso",
            durante,
        )

    with c4:
        st.metric(
            "Costo relativo",
            costo,
        )

    st.caption(
        """
        La comparación de costos es cualitativa y tiene fines didácticos.
        El costo real depende del sistema, proveedor, servicio de lectura
        y modalidad de vigilancia dosimétrica.
        """
    )

    # --------------------------------------------------------
    # Pregunta interactiva
    # --------------------------------------------------------

    st.divider()

    st.subheader("🧠 Aplicalo a una situación")

    st.write(
        """
        Un trabajador necesita conocer **durante una tarea**
        cómo está variando su exposición, sin esperar el procesamiento
        posterior del dosímetro.

        **¿Cuál sería la opción más adecuada entre estas tres tecnologías?**
        """
    )

    respuesta_comparador = st.radio(
        "Elegí una opción:",
        [
            "Todavía no respondí",
            "TLD",
            "OSLD",
            "Dosímetro electrónico",
        ],
        key="respuesta_comparador_u8",
    )

    if respuesta_comparador == "Dosímetro electrónico":

        st.success(
            """
            ✅ Correcto. En esta situación, el dosímetro electrónico
            permite disponer de información durante su utilización.

            En cambio, los sistemas TLD y OSLD almacenan información
            que posteriormente debe ser obtenida mediante un proceso
            de lectura.
            """
        )

    elif respuesta_comparador in ["TLD", "OSLD"]:

        st.warning(
            """
            🔎 Revisá el recorrido de la información.

            Este tipo de dosímetro almacena información y requiere
            posteriormente un proceso de lectura antes de obtener
            el resultado.
            """
        )


# ============================================================
# TAB 4 — CALIBRACIÓN
# ============================================================

with tab4:

    st.header("📐 ¿Por qué calibramos un dosímetro?")

    st.write(
        """
        En esta simulación, tres dosímetros son sometidos a una misma
        **condición de referencia virtual**.

        Tu objetivo es observar sus lecturas e identificar cuál presenta
        una respuesta claramente diferente.
        """
    )

    st.info(
        """
        🔎 Esta actividad representa solamente el concepto de comparación
        con una referencia. No reproduce un procedimiento real de calibración.
        """
    )

    # --------------------------------------------------------
    # Estado de la simulación
    # --------------------------------------------------------

    if "calibracion_realizada_u8" not in st.session_state:
        st.session_state.calibracion_realizada_u8 = False

    if "respuesta_calibracion_u8" not in st.session_state:
        st.session_state.respuesta_calibracion_u8 = "Todavía no respondí"

    referencia = 1.00

    lectura_a = 0.98
    lectura_b = 1.01
    lectura_c = 0.40

    # --------------------------------------------------------
    # Escena inicial
    # --------------------------------------------------------

    html_calibracion = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">

    <style>

    body {
        margin: 0;
        background: transparent;
        font-family: Arial, sans-serif;
        color: white;
    }

    .laboratorio {
        width: 100%;
        min-height: 440px;
        background: linear-gradient(135deg,#101820,#0c1117);
        border: 1px solid #3b4b59;
        border-radius: 24px;
        padding: 28px;
        box-sizing: border-box;
    }

    .titulo {
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
    }

    .subtitulo {
        text-align: center;
        color: #b8c3cc;
        font-size: 15px;
        margin-bottom: 30px;
    }

    .referencia {
        width: 260px;
        margin: auto;
        text-align: center;
        background: #202c37;
        border: 2px solid #e2b24a;
        border-radius: 18px;
        padding: 18px;
    }

    .simbolo {
        font-size: 42px;
    }

    .valor-ref {
        font-size: 27px;
        font-weight: bold;
        margin-top: 5px;
        color: #ffd466;
    }

    .flecha {
        text-align: center;
        font-size: 35px;
        color: #e2b24a;
        margin: 12px;
    }

    .dosimetros {
        display: flex;
        justify-content: center;
        gap: 45px;
        margin-top: 10px;
    }

    .dosimetro {
        width: 180px;
        height: 145px;
        border-radius: 18px;
        background: #252525;
        border: 3px solid #111;
        box-shadow: 0 8px 18px rgba(0,0,0,.30);
        text-align: center;
        padding-top: 18px;
        box-sizing: border-box;
    }

    .pantalla {
        width: 130px;
        height: 60px;
        margin: auto;
        border-radius: 7px;
        background: #cde7c7;
        border: 2px solid #111;
        color: #111;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: monospace;
        font-size: 18px;
        font-weight: bold;
    }

    .nombre {
        margin-top: 13px;
        font-size: 18px;
        font-weight: bold;
    }

    </style>

    </head>

    <body>

    <div class="laboratorio">

        <div class="titulo">
            Comparación con una referencia conocida
        </div>

        <div class="subtitulo">
            Los tres dosímetros reciben la misma condición de referencia virtual
        </div>

        <div class="referencia">

            <div class="simbolo">
                ☢️
            </div>

            <div>
                REFERENCIA
            </div>

            <div class="valor-ref">
                1,00 mSv
            </div>

        </div>

        <div class="flecha">
            ↓
        </div>

        <div class="dosimetros">

            <div class="dosimetro">

                <div class="pantalla">
                    DOSÍMETRO
                </div>

                <div class="nombre">
                    A
                </div>

            </div>

            <div class="dosimetro">

                <div class="pantalla">
                    DOSÍMETRO
                </div>

                <div class="nombre">
                    B
                </div>

            </div>

            <div class="dosimetro">

                <div class="pantalla">
                    DOSÍMETRO
                </div>

                <div class="nombre">
                    C
                </div>

            </div>

        </div>

    </div>

    </body>
    </html>
    """

    st.components.v1.html(
        html_calibracion,
        height=470,
        scrolling=False,
    )

    # --------------------------------------------------------
    # Botón de medición
    # --------------------------------------------------------

    centro_boton = st.columns(
        [1, 1, 1]
    )

    with centro_boton[1]:

        if st.button(
            "▶ REALIZAR COMPARACIÓN VIRTUAL",
            use_container_width=True,
            key="boton_calibracion_u8",
        ):

            st.session_state.calibracion_realizada_u8 = True
            st.session_state.respuesta_calibracion_u8 = "Todavía no respondí"

    # --------------------------------------------------------
    # Mostrar resultados
    # --------------------------------------------------------

    if st.session_state.calibracion_realizada_u8:

        st.subheader("📊 Lecturas obtenidas")

        col_a, col_b, col_c = st.columns(3)

        with col_a:

            st.metric(
                "Dosímetro A",
                f"{lectura_a:.2f} mSv",
            )

        with col_b:

            st.metric(
                "Dosímetro B",
                f"{lectura_b:.2f} mSv",
            )

        with col_c:

            st.metric(
                "Dosímetro C",
                f"{lectura_c:.2f} mSv",
            )

        # ----------------------------------------------------
        # Barras visuales
        # ----------------------------------------------------

        fig_comparacion = go.Figure()

        fig_comparacion.add_trace(
            go.Bar(
                x=[
                    "Referencia",
                    "Dosímetro A",
                    "Dosímetro B",
                    "Dosímetro C",
                ],
                y=[
                    referencia,
                    lectura_a,
                    lectura_b,
                    lectura_c,
                ],
                text=[
                    "1,00 mSv",
                    "0,98 mSv",
                    "1,01 mSv",
                    "0,40 mSv",
                ],
                textposition="outside",
                name="Lectura",
            )
        )

        fig_comparacion.update_layout(
            title="Comparación de las lecturas",
            yaxis_title="Lectura simulada (mSv)",
            yaxis=dict(
                range=[0, 1.2]
            ),
            height=430,
            showlegend=False,
        )

        st.plotly_chart(
            fig_comparacion,
            use_container_width=True,
        )

        st.subheader(
            "🧠 Analizá el resultado"
        )

        st.write(
            """
            Los tres dosímetros fueron sometidos a la misma condición
            de referencia virtual de **1,00 mSv**.

            **¿Cuál presenta una respuesta claramente diferente?**
            """
        )

        respuesta = st.radio(
            "Seleccioná un dosímetro:",
            [
                "Todavía no respondí",
                "Dosímetro A",
                "Dosímetro B",
                "Dosímetro C",
            ],
            key="respuesta_calibracion_u8",
        )

        if respuesta == "Dosímetro C":

            st.success(
                """
                ✅ Correcto.

                El **Dosímetro C** informa **0,40 mSv**, mientras que
                la referencia virtual es **1,00 mSv**.

                Su respuesta es claramente diferente de la esperada.
                """
            )

            # ------------------------------------------------
            # IMPORTANCIA DE LA CALIBRACIÓN
            # ------------------------------------------------

            st.markdown("### 📐 ¿Por qué es importante la calibración?")

            st.write(
                """
                Un dosímetro puede generar una lectura aunque su respuesta
                no represente adecuadamente la exposición recibida.

                La calibración permite relacionar la respuesta del dosímetro
                con una **referencia conocida** y comprobar que la información
                obtenida sea adecuada para la vigilancia dosimétrica.

                En esta simulación, la referencia es **1,00 mSv**, pero el
                Dosímetro C informa solamente **0,40 mSv**.

                Una diferencia de esta magnitud produciría una
                **subestimación de la exposición registrada**.
                """
            )

            st.markdown("### 🔎 Miralo de otra manera")

            col_real, col_lectura = st.columns(2)

            with col_real:

                st.metric(
                    "Referencia virtual",
                    "1,00 mSv",
                )

            with col_lectura:

                st.metric(
                    "Lectura informada",
                    "0,40 mSv",
                    delta="-0,60 mSv",
                )

            st.warning(
                """
                **El registro no representa adecuadamente la condición
                de referencia.**

                Por eso no alcanza con que un dosímetro simplemente
                produzca una lectura: es necesario conocer y verificar
                su respuesta.
                """
            )

        elif respuesta in [
            "Dosímetro A",
            "Dosímetro B",
        ]:

            st.warning(
                """
                🔎 Observá nuevamente las cuatro barras.

                Compará cada lectura con la referencia de **1,00 mSv**
                y buscá cuál se aleja de manera más evidente.
                """
            )


# ============================================================
# TAB 5 — MAGNITUDES DOSIMÉTRICAS
# ============================================================

with tab5:
    st.header("🧍 Magnitudes dosimétricas")

    st.write("""
    Usá esta calculadora para relacionar **dosis absorbida**, **dosis equivalente**
    y **dosis efectiva**.

    **Dosis absorbida (Gy) → wR → dosis equivalente (Sv) → wT → dosis efectiva (Sv)**
    """)

    factores_tejido = {
        "Médula ósea roja": 0.12,
        "Colon": 0.12,
        "Pulmón": 0.12,
        "Estómago": 0.12,
        "Mamas": 0.12,
        "Resto de tejidos": 0.12,
        "Gónadas": 0.08,
        "Vejiga": 0.04,
        "Hígado": 0.04,
        "Esófago": 0.04,
        "Tiroides": 0.04,
        "Piel": 0.01,
        "Superficie ósea": 0.01,
        "Cerebro": 0.01,
    }

    posiciones = {
        "Cerebro": (350, 100, 28, 20),
        "Tiroides": (350, 155, 16, 10),
        "Pulmón": (350, 220, 58, 48),
        "Mamas": (350, 235, 42, 18),
        "Médula ósea roja": (350, 290, 14, 90),
        "Esófago": (350, 215, 10, 60),
        "Hígado": (385, 292, 38, 23),
        "Estómago": (330, 312, 28, 23),
        "Colon": (350, 350, 45, 34),
        "Vejiga": (350, 410, 22, 18),
        "Gónadas": (350, 445, 20, 15),
        "Piel": (350, 285, 82, 190),
        "Superficie ósea": (350, 285, 58, 165),
        "Resto de tejidos": (350, 285, 70, 180),
    }

    col_fig, col_calc = st.columns([1.05, 0.95])

    with col_calc:
        organo = st.selectbox(
            "1️⃣ Seleccioná el órgano o tejido",
            list(factores_tejido.keys()),
            key="organo_mag_u8",
        )
        wt = factores_tejido[organo]
        st.metric("Factor de ponderación del tejido (wT)", f"{wt:.2f}")

        radiacion = st.selectbox(
            "2️⃣ Seleccioná el tipo de radiación",
            [
                "Fotones / gamma",
                "Electrones / beta",
                "Protones",
                "Partículas alfa",
                "Neutrones",
            ],
            key="radiacion_mag_u8",
        )

        if radiacion == "Fotones / gamma":
            wr = 1.0
        elif radiacion == "Electrones / beta":
            wr = 1.0
        elif radiacion == "Protones":
            wr = 2.0
        elif radiacion == "Partículas alfa":
            wr = 20.0
        else:
            energia_neutron = st.number_input(
                "Energía del neutrón (MeV)",
                min_value=0.001,
                max_value=10000.0,
                value=1.0,
                step=0.1,
                format="%.3f",
                key="energia_neutron_u8",
            )
            e = float(energia_neutron)
            if e < 1.0:
                wr = 2.5 + 18.2 * np.exp(-(np.log(e) ** 2) / 6.0)
            elif e <= 50.0:
                wr = 5.0 + 17.0 * np.exp(-(np.log(2.0 * e) ** 2) / 6.0)
            else:
                wr = 2.5 + 3.25 * np.exp(-(np.log(0.04 * e) ** 2) / 6.0)

        st.metric("Factor de ponderación de la radiación (wR)", f"{wr:.2f}")

        dosis_mgy = st.number_input(
            "3️⃣ Dosis absorbida en el órgano (mGy)",
            min_value=0.0,
            value=1.0,
            step=0.1,
            key="dosis_abs_mag_u8",
        )

        h_msv = dosis_mgy * wr
        e_msv = h_msv * wt

        c1, c2 = st.columns(2)
        with c1:
            st.metric("Dosis equivalente HT", f"{h_msv:.3f} mSv")
        with c2:
            st.metric("Contribución a dosis efectiva E", f"{e_msv:.3f} mSv")

    with col_fig:
        cx, cy, rx, ry = posiciones[organo]

        if organo in ["Piel", "Superficie ósea", "Resto de tejidos"]:
            resaltado = f"""
            <ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}"
            fill="none" stroke="#ffcc4d" stroke-width="8" opacity="0.95"/>
            """
        else:
            resaltado = f"""
            <ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}"
            fill="#ffcc4d" opacity="0.72" stroke="#ffffff" stroke-width="3"/>
            """

        svg_cuerpo = f"""
        <svg viewBox="0 0 700 560" width="100%" height="100%">
          <rect x="25" y="20" width="650" height="520" rx="28"
            fill="#101820" stroke="#415264" stroke-width="2"/>
          <text x="350" y="58" text-anchor="middle" fill="white"
            font-size="22" font-weight="bold">Selección anatómica</text>

          <circle cx="350" cy="105" r="46" fill="#d6a47e"/>
          <path d="M285 175 Q350 150 415 175 L438 365
                   Q420 395 390 385 L382 505 L350 505
                   L340 385 L310 505 L278 505 L310 385
                   Q280 395 262 365 Z"
                fill="#e9eef2" stroke="#9eabb5" stroke-width="4"/>

          <ellipse cx="350" cy="100" rx="27" ry="18" fill="#e5a1a8"/>
          <rect x="342" y="148" width="16" height="14" rx="5" fill="#e5a1a8"/>
          <ellipse cx="323" cy="220" rx="25" ry="46" fill="#d85c5c"/>
          <ellipse cx="377" cy="220" rx="25" ry="46" fill="#d85c5c"/>
          <rect x="346" y="185" width="8" height="78" rx="4" fill="#d8b07b"/>
          <ellipse cx="385" cy="292" rx="38" ry="23" fill="#8e3c34"/>
          <ellipse cx="329" cy="310" rx="27" ry="23" fill="#e7a66f"/>
          <rect x="315" y="330" width="70" height="55" rx="22"
            fill="none" stroke="#c89a63" stroke-width="10"/>
          <ellipse cx="350" cy="406" rx="21" ry="17" fill="#8cc9e8"/>
          <ellipse cx="338" cy="443" rx="9" ry="12" fill="#e6bd6a"/>
          <ellipse cx="362" cy="443" rx="9" ry="12" fill="#e6bd6a"/>
          <line x1="350" y1="178" x2="350" y2="390"
            stroke="#9ec5df" stroke-width="7" opacity="0.55"/>

          {resaltado}

          <text x="350" y="530" text-anchor="middle" fill="#ffcc4d"
            font-size="18" font-weight="bold">{organo} · wT = {wt:.2f}</text>
        </svg>
        """
        st.components.v1.html(svg_cuerpo, height=620, scrolling=False)

    st.subheader("🧮 Desarrollo del cálculo")
    st.latex(r"H_T = \sum_R w_R D_{T,R}")
    st.latex(
        rf"H_T = {dosis_mgy:.3f}\,\mathrm{{mGy}} \times {wr:.2f}"
        rf" = {h_msv:.3f}\,\mathrm{{mSv}}"
    )
    st.latex(r"E = \sum_T w_T H_T")
    st.latex(
        rf"E = {wt:.2f} \times {h_msv:.3f}\,\mathrm{{mSv}}"
        rf" = {e_msv:.3f}\,\mathrm{{mSv}}"
    )

    st.divider()
    st.subheader("➕ Calculadora de dosis equivalente total")

    exp1, exp2 = st.columns(2)
    opciones = ["Gamma", "Beta / electrones", "Alfa", "Protones"]
    wr_simples = {"Gamma": 1.0, "Beta / electrones": 1.0, "Alfa": 20.0, "Protones": 2.0}

    with exp1:
        tipo1 = st.selectbox("Radiación 1", opciones, key="tipo_exp1_u8")
        d1 = st.number_input(
            "Dosis 1 (mGy)", min_value=0.0, value=3.0, step=0.1, key="d1_u8"
        )

    with exp2:
        tipo2 = st.selectbox("Radiación 2", opciones, index=1, key="tipo_exp2_u8")
        d2 = st.number_input(
            "Dosis 2 (mGy)", min_value=0.0, value=1.0, step=0.1, key="d2_u8"
        )

    h1 = d1 * wr_simples[tipo1]
    h2 = d2 * wr_simples[tipo2]
    htotal = h1 + h2

    a, b, c = st.columns(3)
    with a:
        st.metric("Contribución 1", f"{h1:.3f} mSv")
    with b:
        st.metric("Contribución 2", f"{h2:.3f} mSv")
    with c:
        st.metric("Total", f"{htotal:.3f} mSv")

    st.divider()
    st.subheader("🧠 Ahora resolvelo vos")

    ejercicio = st.selectbox(
        "Seleccioná un ejercicio",
        [
            "1 mGy alfa vs 1 mGy beta",
            "3 mGy gamma + 1 mGy beta",
            "2 mGy gamma + 2 mGy alfa",
            "1 mGy electrones + 0,5 mGy gamma",
        ],
        key="ejercicio_mag_u8",
    )

    if ejercicio == "1 mGy alfa vs 1 mGy beta":
        st.write("¿1 mGy de radiación alfa es más dañino al tejido que 1 mGy de radiación beta?")
        r = st.number_input(
            "Dosis equivalente para 1 mGy alfa (mSv)",
            min_value=0.0, value=0.0, step=1.0, key="e1_u8"
        )
        if st.button("Comprobar", key="c1_u8"):
            if abs(r - 20.0) < 0.01:
                st.success("✅ Correcto: alfa = 20 mSv y beta = 1 mSv.")
            else:
                st.warning("Revisá el factor wR de las partículas alfa.")

    elif ejercicio == "3 mGy gamma + 1 mGy beta":
        st.write("Calcule la dosis equivalente total de 3 mGy gamma + 1 mGy beta.")
        r = st.number_input(
            "Resultado (mSv)", min_value=0.0, value=0.0, step=0.5, key="e2_u8"
        )
        if st.button("Comprobar", key="c2_u8"):
            if abs(r - 4.0) < 0.01:
                st.success("✅ Correcto: 3 mSv + 1 mSv = 4 mSv.")
            else:
                st.warning("Sumá las contribuciones equivalentes de ambas radiaciones.")

    elif ejercicio == "2 mGy gamma + 2 mGy alfa":
        st.write("Calcule la dosis equivalente total de 2 mGy gamma + 2 mGy alfa.")
        r = st.number_input(
            "Resultado (mSv)", min_value=0.0, value=0.0, step=1.0, key="e3_u8"
        )
        if st.button("Comprobar", key="c3_u8"):
            if abs(r - 42.0) < 0.01:
                st.success("✅ Correcto: 2 mSv + 40 mSv = 42 mSv.")
            else:
                st.warning("Revisá especialmente el wR de alfa.")

    else:
        st.write("Calcule la dosis equivalente total de 1 mGy electrones + 0,5 mGy gamma.")
        r = st.number_input(
            "Resultado (mSv)", min_value=0.0, value=0.0, step=0.1, key="e4_u8"
        )
        if st.button("Comprobar", key="c4_u8"):
            if abs(r - 1.5) < 0.01:
                st.success("✅ Correcto: 1 mSv + 0,5 mSv = 1,5 mSv.")
            else:
                st.warning("Para fotones y electrones, wR = 1.")

