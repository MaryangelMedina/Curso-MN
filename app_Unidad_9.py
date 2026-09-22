import streamlit as st
import streamlit.components.v1 as components
import math

st.set_page_config(page_title="Unidad 9 - SPECT y PET", page_icon="☢️", layout="wide")

st.markdown("""
<style>
.stApp {background:#0b1118;color:#eef6ff}
.block-container {max-width:1450px;padding-top:1.2rem}
div[data-testid="stMetric"] {background:#111d29;border:1px solid #284258;border-radius:14px;padding:10px}
</style>
""", unsafe_allow_html=True)

st.title("☢️ Unidad 9 - Instrumentación en Medicina Nuclear")
st.caption("Laboratorios virtuales educativos basados en el material del Dr. Roberto A. Isoardi")

def pregunta(key, texto, opciones, correcta, explicacion):
    st.markdown("**" + texto + "**")
    r = st.radio("Respuesta", opciones, key=key, label_visibility="collapsed")
    if st.button("Comprobar", key="btn_" + key):
        if r == correcta:
            st.success("✓ Correcto. " + explicacion)
        else:
            st.error("✗ Revisá la experiencia visual. " + explicacion)

lab_spect, lab_pet = st.tabs(["🔄 LAB 1 - Cámara Gamma / SPECT", "⭕ LAB 2 - PET"])

with lab_spect:
    st.header("🔄 Del fotón gamma al corte SPECT")
    s1,s2,s3,s4,s5 = st.tabs([
        "1️⃣ Cámara Gamma","2️⃣ Colimadores","3️⃣ Adquisición SPECT",
        "4️⃣ Reconstrucción","5️⃣ Preguntas"
    ])

    with s1:
        st.subheader("Seguí el fotón a través del cabezal")
        etapas = ["Fotón emitido","Colimador","Cristal NaI(Tl)","Centelleo","PMT","Electrónica X-Y-Z","Imagen"]
        etapa = st.select_slider("Etapa del proceso", options=etapas)
        i = etapas.index(etapa)

        elementos = [
            ("Colimador", 280, "#6c757d"),
            ("NaI(Tl)", 410, "#8fd3a8"),
            ("Luz", 535, "#ffe082"),
            ("PMT", 650, "#5aa9e6"),
            ("Imagen", 790, "#9b7ede"),
        ]
        partes = [
            '<svg viewBox="0 0 1000 390" width="100%" height="390">',
            '<text x="500" y="35" text-anchor="middle" fill="white" font-size="27" font-weight="bold">Cabezal de Cámara Gamma</text>',
            '<ellipse cx="110" cy="200" rx="60" ry="90" fill="#d7a37d"/>',
            '<circle cx="145" cy="190" r="9" fill="#ffb703"/>',
            '<line x1="155" y1="190" x2="260" y2="190" stroke="#ffd166" stroke-width="5"/>'
        ]
        for j,(nombre,x,color) in enumerate(elementos):
            activo = (i == j+1) or (i >= 5 and j == 4)
            if j == 4:
                # La salida final se representa como una imagen circular,
                # visualmente similar a la fuente del paciente.
                partes.append(
                    f'<circle cx="{x+70}" cy="195" r="72" fill="{color}" '
                    f'stroke="{"#ffd166" if activo else "#c9d6df"}" stroke-width="{6 if activo else 2}"/>'
                )
                partes.append(
                    f'<circle cx="{x+70}" cy="195" r="28" fill="#ffb703" opacity="0.95"/>'
                )
                partes.append(
                    f'<text x="{x+70}" y="315" fill="white" font-size="17" text-anchor="middle">Imagen</text>'
                )
            else:
                ancho = 100
                partes.append(
                    f'<rect x="{x}" y="105" width="{ancho}" height="180" rx="10" fill="{color}" '
                    f'stroke="{"#ffd166" if activo else "#c9d6df"}" stroke-width="{6 if activo else 2}"/>'
                )
                partes.append(
                    f'<text x="{x+ancho/2}" y="315" fill="white" font-size="17" text-anchor="middle">{nombre}</text>'
                )
        partes.append(f'<text x="500" y="365" fill="#ffd166" font-size="22" text-anchor="middle">Etapa actual: {etapa}</text>')
        partes.append('</svg>')
        components.html('<div style="background:#0e1720;border-radius:20px;padding:12px">' + "".join(partes) + '</div>', height=430)

        explicaciones = {
            "Fotón emitido":"La distribución de actividad emite fotones en distintas direcciones.",
            "Colimador":"Selecciona direcciones preferenciales antes de que la radiación alcance el cristal.",
            "Cristal NaI(Tl)":"El fotón aceptado deposita energía en el cristal.",
            "Centelleo":"La energía depositada produce luz de centelleo.",
            "PMT":"Los PMT reciben la luz y generan señales eléctricas.",
            "Electrónica X-Y-Z":"Las señales permiten estimar posición X-Y y energía Z.",
            "Imagen":"Los eventos aceptados se acumulan espacialmente y forman una proyección."
        }
        st.info(explicaciones[etapa])

    with s2:
        st.subheader("🔬 Colimadores: cambiá la geometría y observá la imagen resultante")
        st.caption("El objeto es asimétrico a propósito para que se vea claramente si la imagen se conserva, se magnifica, se reduce o se invierte.")

        tipo = st.selectbox(
            "Tipo de colimador",
            ["Agujeros paralelos","Convergente","Divergente","Pinhole"]
        )
        distancia = st.slider("Distancia relativa objeto-colimador", 1, 10, 4)

        descripcion = {
            "Agujeros paralelos":"Mantiene aproximadamente el tamaño del objeto. Al aumentar la distancia, la imagen se representa con menor nitidez.",
            "Convergente":"Produce una imagen magnificada.",
            "Divergente":"Produce una imagen reducida y permite abarcar un campo de visión mayor.",
            "Pinhole":"Produce magnificación e inversión de la imagen."
        }[tipo]
        st.info(descripcion)

        # Tamaño visual de la imagen según la geometría seleccionada.
        # Es una representación conceptual, no una simulación cuantitativa.
        if tipo == "Agujeros paralelos":
            escala = 1.0
            invertir = False
            etiqueta_imagen = "Tamaño aproximadamente conservado"
            rayos = (
                '<line x1="190" y1="125" x2="575" y2="125"/>'
                '<line x1="190" y1="180" x2="575" y2="180"/>'
                '<line x1="190" y1="235" x2="575" y2="235"/>'
            )
            colimador_svg = """
                <rect x="565" y="72" width="48" height="216" rx="4" fill="#737d86"/>
                <g stroke="#17212a" stroke-width="5">
                    <line x1="577" y1="82" x2="577" y2="278"/>
                    <line x1="589" y1="82" x2="589" y2="278"/>
                    <line x1="601" y1="82" x2="601" y2="278"/>
                </g>
            """
        elif tipo == "Convergente":
            escala = 1.45
            invertir = False
            etiqueta_imagen = "Imagen magnificada"
            rayos = (
                '<line x1="190" y1="135" x2="575" y2="95"/>'
                '<line x1="190" y1="180" x2="575" y2="180"/>'
                '<line x1="190" y1="225" x2="575" y2="265"/>'
            )
            colimador_svg = """
                <polygon points="560,70 615,95 615,265 560,290" fill="#737d86"/>
                <g stroke="#17212a" stroke-width="4">
                    <line x1="570" y1="88" x2="606" y2="108"/>
                    <line x1="570" y1="132" x2="606" y2="142"/>
                    <line x1="570" y1="180" x2="606" y2="180"/>
                    <line x1="570" y1="228" x2="606" y2="218"/>
                    <line x1="570" y1="272" x2="606" y2="252"/>
                </g>
            """
        elif tipo == "Divergente":
            escala = 0.68
            invertir = False
            etiqueta_imagen = "Imagen reducida"
            rayos = (
                '<line x1="190" y1="100" x2="575" y2="135"/>'
                '<line x1="190" y1="180" x2="575" y2="180"/>'
                '<line x1="190" y1="260" x2="575" y2="225"/>'
            )
            colimador_svg = """
                <polygon points="560,95 615,70 615,290 560,265" fill="#737d86"/>
                <g stroke="#17212a" stroke-width="4">
                    <line x1="570" y1="108" x2="606" y2="88"/>
                    <line x1="570" y1="142" x2="606" y2="132"/>
                    <line x1="570" y1="180" x2="606" y2="180"/>
                    <line x1="570" y1="218" x2="606" y2="228"/>
                    <line x1="570" y1="252" x2="606" y2="272"/>
                </g>
            """
        else:
            escala = 1.35
            invertir = True
            etiqueta_imagen = "Imagen invertida y magnificada"
            rayos = (
                '<line x1="190" y1="125" x2="520" y2="180"/>'
                '<line x1="190" y1="235" x2="520" y2="180"/>'
                '<line x1="520" y1="180" x2="630" y2="115"/>'
                '<line x1="520" y1="180" x2="630" y2="245"/>'
            )
            colimador_svg = """
                <polygon points="545,72 545,160 520,180 545,200 545,288 610,265 610,95"
                         fill="#737d86"/>
                <circle cx="520" cy="180" r="6" fill="#111820" stroke="#d7e1e8" stroke-width="2"/>
            """

        # La distancia modifica visualmente la nitidez del paralelo.
        desenfoque = min(5.0, 0.45 * distancia) if tipo == "Agujeros paralelos" else 0.7
        rx_img = 42 * escala
        ry_img = 58 * escala

        # Marcador asimétrico: en pinhole cambia de arriba a abajo para mostrar la inversión.
        punto_y_obj = 152
        punto_y_img = 180 + (180 - punto_y_obj) * escala if invertir else 180 + (punto_y_obj - 180) * escala

        html = f"""
        <div style="background:#0e1720;border:1px solid #29465d;border-radius:22px;padding:16px;color:white;font-family:Arial">
        <svg viewBox="0 0 1180 410" width="100%" height="410">
          <defs>
            <filter id="blurImagen">
              <feGaussianBlur stdDeviation="{desenfoque}"/>
            </filter>
          </defs>

          <text x="590" y="32" fill="white" text-anchor="middle" font-size="25" font-weight="bold">{tipo}</text>

          <!-- Objeto/fuente -->
          <ellipse cx="145" cy="180" rx="48" ry="66" fill="#ff9f68" stroke="#ffc89f" stroke-width="2"/>
          <circle cx="145" cy="{punto_y_obj}" r="12" fill="#ffcf33"/>
          <text x="145" y="285" fill="white" text-anchor="middle" font-size="18">Objeto / fuente</text>

          <!-- Rayos y colimador -->
          <g stroke="#ffd166" stroke-width="3">{rayos}</g>
          {colimador_svg}
          <text x="575" y="320" fill="white" text-anchor="middle" font-size="18">Colimador</text>

          <!-- Cristal -->
          <rect x="630" y="68" width="64" height="224" rx="5" fill="#8fd3a8" stroke="#c9f2d7" stroke-width="2"/>
          <text x="662" y="320" fill="white" text-anchor="middle" font-size="18">Cristal</text>

          <!-- Flecha hacia la imagen -->
          <line x1="715" y1="180" x2="790" y2="180" stroke="#6fbdf2" stroke-width="4"/>
          <polygon points="790,180 775,170 775,190" fill="#6fbdf2"/>

          <!-- Pantalla de imagen -->
          <rect x="805" y="62" width="315" height="245" rx="18" fill="#071019" stroke="#3a5c74" stroke-width="2"/>
          <text x="962" y="92" fill="#8bd3ff" text-anchor="middle" font-size="20" font-weight="bold">Imagen resultante</text>

          <g filter="url(#blurImagen)">
            <ellipse cx="962" cy="185" rx="{rx_img}" ry="{ry_img}" fill="#5f3f91" opacity="0.90"/>
            <ellipse cx="962" cy="185" rx="{rx_img*0.62}" ry="{ry_img*0.62}" fill="#a44eb8" opacity="0.90"/>
            <ellipse cx="962" cy="185" rx="{rx_img*0.34}" ry="{ry_img*0.34}" fill="#f07a2f" opacity="0.95"/>
            <circle cx="962" cy="{punto_y_img}" r="{max(7, 11*escala)}" fill="#ffd42a"/>
          </g>

          <text x="962" y="338" fill="#ffd166" text-anchor="middle" font-size="18">{etiqueta_imagen}</text>
          <text x="962" y="365" fill="#c9d6df" text-anchor="middle" font-size="15">Representación conceptual de la proyección</text>
        </svg>
        </div>
        """
        components.html(html, height=450)

        c1, c2, c3 = st.columns(3)
        if tipo == "Agujeros paralelos":
            c1.metric("Tamaño de imagen", "≈ conservado")
            c2.metric("Orientación", "Conservada")
            c3.metric("Distancia", f"{distancia} / 10")
        elif tipo == "Convergente":
            c1.metric("Tamaño de imagen", "Magnificado")
            c2.metric("Orientación", "Conservada")
            c3.metric("Campo de visión", "Menor")
        elif tipo == "Divergente":
            c1.metric("Tamaño de imagen", "Reducido")
            c2.metric("Orientación", "Conservada")
            c3.metric("Campo de visión", "Mayor")
        else:
            c1.metric("Tamaño de imagen", "Magnificado")
            c2.metric("Orientación", "Invertida")
            c3.metric("Geometría", "Pinhole")

        st.caption("La figura muestra cualitativamente el efecto geométrico de cada colimador; no representa una adquisición clínica cuantitativa.")

    with s3:
        st.subheader("🔄 Adquisición SPECT alrededor del paciente")
        nproj = st.select_slider("Número conceptual de proyecciones", options=[8,16,32,64,128], value=64)
        ang = st.slider("Ángulo del cabezal", 0, 359, 0)

        cx,cy,R = 360,205,145
        x = cx + R*math.cos(math.radians(ang))
        y = cy + R*math.sin(math.radians(ang))

        html = f"""
        <div style="background:#0e1720;border-radius:20px">
        <svg viewBox="0 0 720 420" width="100%" height="420">
          <text x="360" y="30" fill="white" text-anchor="middle" font-size="25">Adquisición SPECT - {ang} grados</text>
          <ellipse cx="{cx}" cy="{cy}" rx="75" ry="105" fill="#d7a37d"/>
          <circle cx="{cx-20}" cy="{cy}" r="13" fill="#ffb703"/>
          <circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="#526b7d" stroke-width="3" stroke-dasharray="7 7"/>
          <g transform="translate({x},{y}) rotate({ang+90})">
            <rect x="-62" y="-27" width="124" height="54" rx="8" fill="#5aa9e6" stroke="#d8f0ff" stroke-width="4"/>
          </g>
          <line x1="{x}" y1="{y}" x2="{cx}" y2="{cy}" stroke="#ffd166" stroke-width="3" stroke-dasharray="5 5"/>
          <text x="360" y="390" fill="#ffd166" text-anchor="middle" font-size="20">{nproj} proyecciones</text>
        </svg></div>
        """
        components.html(html, height=450)

        if nproj <= 16:
            st.warning("Pocas proyecciones: puede aumentar el artefacto tipo estrella (streak).")
        else:
            st.success("Un mayor muestreo angular reduce el artefacto asociado a un número insuficiente de proyecciones.")

    with s4:
        st.subheader("🧩 De las proyecciones al corte transversal")
        metodo = st.radio("Método de reconstrucción", ["Retroproyección","Retroproyección filtrada (FBP)","Iterativa"], horizontal=True)
        explicacion = {
            "Retroproyección":"Cada perfil se distribuye nuevamente sobre la matriz y aparece el borroneo característico.",
            "Retroproyección filtrada (FBP)":"Los perfiles se filtran antes de retroproyectarse para controlar el borroneo.",
            "Iterativa":"La estimación de imagen se actualiza comparando datos calculados con los datos adquiridos."
        }[metodo]
        st.info(explicacion)
        st.markdown("### `PROYECCIONES → SINOGRAMA → RECONSTRUCCIÓN → CORTE TRANSVERSAL`")
        st.caption("La clase también incluye normalización y correcciones de centro de rotación y uniformidad antes de reconstruir.")

    with s5:
        st.subheader("🧠 Comprobá lo aprendido")
        pregunta("s_q1","¿Qué componente selecciona direcciones preferenciales de los fotones?",
                 ["PMT","Colimador","Computadora","Camilla"],"Colimador",
                 "El colimador realiza la selección direccional antes del cristal.")
        pregunta("s_q2","Al aumentar la distancia con un colimador de agujeros paralelos, la resolución espacial...",
                 ["Mejora","Se degrada","No cambia"],"Se degrada",
                 "La resolución espacial se degrada cuando aumenta la distancia.")
        pregunta("s_q3","¿Qué puede aparecer si se adquieren muy pocas proyecciones?",
                 ["Artefactos tipo estrella","Coincidencias PET","Magnificación pinhole"],"Artefactos tipo estrella",
                 "El material muestra artefactos streak asociados a pocas proyecciones.")

with lab_pet:
    st.header("⭕ Del evento de aniquilación a la imagen PET")
    p1,p2,p3,p4,p5 = st.tabs(["1️⃣ Aniquilación","2️⃣ Coincidencia / LOR","3️⃣ Detector PET","4️⃣ Imagen PET","5️⃣ Preguntas"])

    with p1:
        st.subheader("💥 Aniquilación electrón-positrón")
        components.html("""
        <div style="background:#0e1720;border-radius:20px">
        <svg viewBox="0 0 900 370" width="100%" height="370">
          <text x="450" y="30" fill="white" text-anchor="middle" font-size="25">Evento de aniquilación</text>
          <ellipse cx="450" cy="195" rx="145" ry="115" fill="#263947"/>
          <circle cx="450" cy="195" r="11" fill="#ff4d6d"/>
          <line x1="450" y1="195" x2="150" y2="195" stroke="#ffd166" stroke-width="5"/>
          <line x1="450" y1="195" x2="750" y2="195" stroke="#ffd166" stroke-width="5"/>
          <text x="220" y="175" fill="#ffd166" font-size="21">gamma 511 keV</text>
          <text x="635" y="175" fill="#ffd166" font-size="21">gamma 511 keV</text>
          <text x="450" y="235" fill="white" text-anchor="middle">e+ + e-</text>
        </svg></div>
        """, height=400)
        st.info("El modelo visual representa la aniquilación electrón-positrón y los dos fotones de 511 keV mostrados en la presentación.")

    with p2:
        st.subheader("📏 Línea de respuesta (LOR)")
        ang = st.slider("Orientación de la LOR", 0, 175, 30, 5)
        cx,cy,R = 400,210,165
        dx = R*math.cos(math.radians(ang))
        dy = R*math.sin(math.radians(ang))
        detectores = "".join(
            f'<circle cx="{cx+R*math.cos(math.radians(q))}" cy="{cy+R*math.sin(math.radians(q))}" r="7" fill="#5aa9e6"/>'
            for q in range(0,360,10)
        )
        html = f"""
        <div style="background:#0e1720;border-radius:20px">
        <svg viewBox="0 0 800 430" width="100%" height="430">
          <text x="400" y="28" fill="white" text-anchor="middle" font-size="25">Anillo PET y línea de respuesta</text>
          <circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="#29485d" stroke-width="25"/>
          {detectores}
          <ellipse cx="{cx}" cy="{cy}" rx="95" ry="125" fill="#d7a37d"/>
          <circle cx="{cx}" cy="{cy}" r="9" fill="#ff4d6d"/>
          <line x1="{cx-dx}" y1="{cy-dy}" x2="{cx+dx}" y2="{cy+dy}" stroke="#ffd166" stroke-width="5"/>
          <circle cx="{cx-dx}" cy="{cy-dy}" r="13" fill="#7ef29a"/>
          <circle cx="{cx+dx}" cy="{cy+dy}" r="13" fill="#7ef29a"/>
          <text x="400" y="405" fill="#ffd166" text-anchor="middle" font-size="20">LOR entre detectores en coincidencia</text>
        </svg></div>
        """
        components.html(html, height=460)
        st.write("Mové la orientación: cambia el par de detectores y la línea de respuesta que atraviesa el evento.")

    with p3:
        st.subheader("🔎 ¿Qué hay dentro del anillo detector?")
        comp = st.selectbox("Explorá un componente", ["Cristal de centelleo","PMT / SiPM","Electrónica","Circuito de coincidencias"])
        info = {
            "Cristal de centelleo":"La presentación menciona materiales de centelleo empleados en detectores PET.",
            "PMT / SiPM":"El fotodetector transforma la señal luminosa del cristal en señal eléctrica.",
            "Electrónica":"Procesa las señales generadas por los bloques detectores.",
            "Circuito de coincidencias":"Asocia detecciones compatibles temporalmente con un evento de aniquilación."
        }[comp]
        st.info(info)
        st.markdown("### `511 keV → CRISTAL → LUZ → FOTODETECTOR → ELECTRÓNICA → COINCIDENCIA → LOR`")

    with p4:
        st.subheader("🧠 De muchas coincidencias a la imagen PET")
        eventos = st.select_slider("Cantidad conceptual de eventos", options=[100,1000,10000,100000], value=10000)
        metodo = st.radio("Reconstrucción", ["FBP","Iterativa","Deep Learning (mencionado en la presentación)"], horizontal=True)
        c1,c2 = st.columns(2)
        c1.metric("Eventos", f"{eventos:,}".replace(",","."))
        c2.metric("Reconstrucción", metodo)

        st.markdown("### PET + CT")
        fusion = st.slider("Fusión conceptual CT ↔ PET", 0, 100, 50)
        st.progress(fusion/100)
        st.caption("CT aporta referencia anatómica y PET representa la distribución funcional/metabólica del trazador.")

    with p5:
        st.subheader("🧠 Comprobá lo aprendido")
        pregunta("p_q1","¿Qué energía tienen los fotones de aniquilación mostrados en la presentación?",
                 ["140 keV","511 keV","662 keV"],"511 keV",
                 "Cada fotón de aniquilación mostrado tiene 511 keV.")
        pregunta("p_q2","¿Qué representa una LOR en este modelo PET?",
                 ["El recorrido del positrón","La línea entre dos detectores en coincidencia","Un septo del colimador"],
                 "La línea entre dos detectores en coincidencia",
                 "La coincidencia define una línea de respuesta entre el par de detectores.")
        pregunta("p_q3","¿Qué elemento destaca el sistema PET para asociar eventos?",
                 ["Circuito de coincidencias","Colimador pinhole","Órbita step-and-shoot"],
                 "Circuito de coincidencias",
                 "La presentación incluye el circuito de detección de coincidencias.")

st.divider()
st.caption("Simulación conceptual educativa basada en el material de clase. No reproduce parámetros clínicos ni controles operativos de un equipo real.")
