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

        # El slider representa de forma conceptual la distancia objeto-colimador.
        # Se usa una variable normalizada para que el alumno visualice tendencias geométricas.
        d_norm = (distancia - 1) / 9.0  # 0 = cerca, 1 = lejos

        if tipo == "Agujeros paralelos":
            # El tamaño se conserva aproximadamente; al alejarse empeora la resolución.
            escala = 1.0
            desenfoque = 0.6 + 4.2 * d_norm
            relacion_distancia = "Más lejos → menor nitidez / peor resolución espacial"
        elif tipo == "Convergente":
            # Representación didáctica: cerca = mayor magnificación; lejos = menor magnificación.
            escala = 1.65 - 0.55 * d_norm
            desenfoque = 0.6 + 1.4 * d_norm
            relacion_distancia = "Más cerca → mayor magnificación; más lejos → menor magnificación"
        elif tipo == "Divergente":
            # La reducción cambia con la geometría/distancia.
            escala = 0.55 + 0.25 * d_norm
            desenfoque = 0.6 + 1.2 * d_norm
            relacion_distancia = "La distancia modifica el grado de reducción de la imagen"
        else:
            # Pinhole: M=b/a. Al aumentar a (objeto más lejos), disminuye la magnificación.
            escala = 1.75 - 0.85 * d_norm
            desenfoque = 0.55 + 1.2 * d_norm
            relacion_distancia = "Pinhole: al acercar el objeto aumenta la magnificación; al alejarlo disminuye"

        rx_img = 42 * escala
        ry_img = 58 * escala

        # Marcador asimétrico: permite ver claramente la inversión del pinhole.
        punto_y_obj = 152
        punto_y_img = 180 + (180 - punto_y_obj) * escala if invertir else 180 + (punto_y_obj - 180) * escala

        estado_distancia = "MUY CERCA" if distancia <= 3 else ("INTERMEDIA" if distancia <= 7 else "MUY LEJOS")

        # El objeto también se desplaza visualmente hacia/desde el colimador.
        # Distancia 1 = próximo al colimador; distancia 10 = más alejado.
        objeto_x = 300 - 17 * distancia

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
          <ellipse cx="{objeto_x}" cy="180" rx="48" ry="66" fill="#ff9f68" stroke="#ffc89f" stroke-width="2"/>
          <circle cx="{objeto_x}" cy="{punto_y_obj}" r="12" fill="#ffcf33"/>
          <text x="{objeto_x}" y="285" fill="white" text-anchor="middle" font-size="18">Objeto / fuente</text>

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

          <text x="962" y="330" fill="#ffd166" text-anchor="middle" font-size="18">{etiqueta_imagen}</text>
          <text x="962" y="354" fill="#c9d6df" text-anchor="middle" font-size="15">Escala visual ≈ {escala:.2f}×</text>

          <text x="{objeto_x}" y="345" fill="#8bd3ff" text-anchor="middle" font-size="16">Objeto: {estado_distancia}</text>
          <text x="590" y="385" fill="#c9d6df" text-anchor="middle" font-size="15">{relacion_distancia}</text>
        </svg>
        </div>
        """
        components.html(html, height=450)

        st.markdown(f"**Qué está pasando:** {relacion_distancia}.")
        if tipo == "Pinhole":
            st.latex(r"M = \\frac{b}{a}")
            st.caption("En el modelo pinhole, a representa la distancia objeto-pinhole y b la distancia pinhole-detector. El dibujo mantiene b fija y modifica conceptualmente a con el slider.")

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
        st.subheader("🔄 SPECT de un cabezal: de las proyecciones a la imagen reconstruida")
        st.write(
            "Mové el ángulo del cabezal para recorrer la adquisición. "
            "A medida que aumenta el ángulo se incorporan nuevas proyecciones, "
            "se completa el sinograma y la reconstrucción se vuelve progresivamente más definida."
        )

        nproj = st.select_slider(
            "Número de proyecciones adquiridas durante 360°",
            options=[16, 32, 64, 128],
            value=64
        )
        paso_angular = 360.0 / nproj
        st.info(
            f"📐 **Paso angular = 360° / {nproj} = {paso_angular:.3f}°**  ·  "
            f"Esto significa que se adquieren **{nproj} imágenes planares (proyecciones)** "
            f"distribuidas a lo largo de 360°."
        )

        indice_proj = st.slider(
            "Proyección adquirida",
            0, nproj, 0, 1,
            help="Cada paso representa una nueva posición angular del cabezal y una nueva imagen planar."
        )
        ang = min(360.0, indice_proj * paso_angular)
        st.caption(
            f"Proyección {indice_proj} de {nproj} · posición angular ≈ {ang:.3f}° · "
            f"paso entre proyecciones = {paso_angular:.3f}°"
        )

        # Fracción conceptual de adquisición completada.
        progreso = min(1.0, ang / 360.0)
        adquiridas = indice_proj

        # Geometría del cabezal.
        cx, cy, R = 250, 205, 128
        x = cx + R * math.cos(math.radians(ang))
        y = cy + R * math.sin(math.radians(ang))

        # Perfil planar conceptual: dos focos cuya posición relativa cambia con el ángulo.
        rad = math.radians(ang)
        foco1 = 115 + 38 * math.cos(rad)
        foco2 = 115 - 27 * math.sin(rad)
        foco3 = 115 + 18 * math.cos(rad + 1.4)

        # Filas del sinograma ya adquiridas.
        filas_sino = []
        filas_totales = 42
        filas_visibles = round(filas_totales * progreso)
        for k in range(filas_totales):
            yy = 62 + k * 5.2
            fase = 2 * math.pi * k / filas_totales
            xx1 = 760 + 70 * math.sin(fase)
            xx2 = 760 + 42 * math.sin(fase + 1.7)
            op = 0.85 if k < filas_visibles else 0.08
            filas_sino.append(
                f'<circle cx="{xx1:.1f}" cy="{yy:.1f}" r="7" fill="#f6f6f6" opacity="{op}"/>'
                f'<circle cx="{xx2:.1f}" cy="{yy:.1f}" r="5" fill="#bfc9d2" opacity="{op*0.75:.2f}"/>'
            )
        sino_svg = "".join(filas_sino)

        # Reconstrucción conceptual progresiva.
        # Con pocas proyecciones se hacen visibles líneas radiales tipo streak.
        streaks = []
        n_streak = 14 if nproj == 16 else (9 if nproj == 32 else (5 if nproj == 64 else 2))
        streak_opacity = max(0.05, (1.0 - progreso) * 0.55 + (0.22 if nproj == 16 else 0.05))
        for k in range(n_streak):
            a = math.pi * k / max(1, n_streak)
            dx = 82 * math.cos(a)
            dy = 82 * math.sin(a)
            streaks.append(
                f'<line x1="{1015-dx:.1f}" y1="{185-dy:.1f}" '
                f'x2="{1015+dx:.1f}" y2="{185+dy:.1f}" '
                f'stroke="#d66cff" stroke-width="2" opacity="{streak_opacity:.2f}"/>'
            )
        streak_svg = "".join(streaks)

        # A mayor progreso, mayor definición y menor transparencia de los focos.
        op_img = 0.18 + 0.82 * progreso
        blur = max(1.0, 8.0 * (1.0 - progreso) + (2.8 if nproj == 16 else 0.8))
        pct = int(progreso * 100)

        html = f"""
        <div style="background:#0e1720;border:1px solid #29465d;border-radius:22px;
                    padding:14px;color:white;font-family:Arial">
        <svg viewBox="0 0 1200 430" width="100%" height="430">
          <defs>
            <filter id="blurRec">
              <feGaussianBlur stdDeviation="{blur:.2f}"/>
            </filter>
            <filter id="blurProj">
              <feGaussianBlur stdDeviation="5"/>
            </filter>
          </defs>

          <!-- títulos -->
          <text x="250" y="28" fill="#ffffff" text-anchor="middle" font-size="21" font-weight="bold">
            Sistema SPECT · vista superior
          </text>
          <text x="540" y="28" fill="#ffffff" text-anchor="middle" font-size="21" font-weight="bold">
            Proyección actual · {ang}°
          </text>
          <text x="760" y="28" fill="#ffffff" text-anchor="middle" font-size="21" font-weight="bold">
            Sinograma
          </text>
          <text x="1015" y="28" fill="#ffffff" text-anchor="middle" font-size="21" font-weight="bold">
            Reconstrucción transaxial
          </text>

          <!-- PANEL 1: paciente + cabezal -->
          <rect x="25" y="42" width="450" height="315" rx="16" fill="#09131c" stroke="#29465d"/>
          <circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="#55778e" stroke-width="3" stroke-dasharray="7 7"/>
          <ellipse cx="{cx}" cy="{cy}" rx="72" ry="98" fill="#d6a27c"/>
          <ellipse cx="{cx}" cy="{cy}" rx="52" ry="70" fill="#8f6c5a" opacity=".42"/>
          <circle cx="{cx-22}" cy="{cy-5}" r="13" fill="#ffb703"/>
          <circle cx="{cx+26}" cy="{cy+22}" r="9" fill="#ff7b00"/>
          <g transform="translate({x:.1f},{y:.1f}) rotate({ang+90})">
            <rect x="-54" y="-25" width="108" height="50" rx="8"
                  fill="#5aa9e6" stroke="#d8f0ff" stroke-width="4"/>
            <rect x="-46" y="-18" width="92" height="10" rx="3" fill="#8fd3a8"/>
          </g>
          <line x1="{x:.1f}" y1="{y:.1f}" x2="{cx}" y2="{cy}"
                stroke="#ffd166" stroke-width="3" stroke-dasharray="6 5"/>
          <text x="250" y="337" fill="#ffd166" text-anchor="middle" font-size="17">
            Cabezal actual: {ang}°
          </text>

          <!-- PANEL 2: proyección planar conceptual -->
          <rect x="490" y="42" width="175" height="315" rx="16" fill="#09131c" stroke="#29465d"/>
          <rect x="515" y="68" width="125" height="225" rx="8" fill="#020508"/>
          <g filter="url(#blurProj)">
            <ellipse cx="577" cy="{foco1:.1f}" rx="24" ry="37" fill="#f4f4f4" opacity=".62"/>
            <ellipse cx="558" cy="{foco2+80:.1f}" rx="15" ry="25" fill="#d8d8d8" opacity=".45"/>
            <ellipse cx="596" cy="{foco3+105:.1f}" rx="12" ry="19" fill="#ffffff" opacity=".55"/>
          </g>
          <text x="577" y="320" fill="#c9d6df" text-anchor="middle" font-size="14">
            Imagen planar adquirida
          </text>

          <!-- PANEL 3: sinograma conceptual -->
          <rect x="680" y="42" width="185" height="315" rx="16" fill="#09131c" stroke="#29465d"/>
          <rect x="700" y="60" width="120" height="225" rx="5" fill="#020508"/>
          {sino_svg}
          <line x1="700" y1="{62 + filas_visibles*5.2:.1f}" x2="820" y2="{62 + filas_visibles*5.2:.1f}"
                stroke="#ff4d5a" stroke-width="3" opacity="{1 if ang>0 else 0}"/>
          <text x="760" y="310" fill="#c9d6df" text-anchor="middle" font-size="14">
            {adquiridas} / {nproj} proyecciones
          </text>
          <text x="760" y="334" fill="#8bd3ff" text-anchor="middle" font-size="14">
            Se completa con cada ángulo
          </text>

          <!-- PANEL 4: reconstrucción progresiva -->
          <rect x="880" y="42" width="295" height="315" rx="16" fill="#09131c" stroke="#29465d"/>
          <rect x="918" y="67" width="194" height="218" rx="8" fill="#020508"/>
          {streak_svg}
          <g filter="url(#blurRec)" opacity="{op_img:.2f}">
            <ellipse cx="1015" cy="176" rx="78" ry="86" fill="#4b1677"/>
            <ellipse cx="1015" cy="176" rx="65" ry="72" fill="#1c67b1"/>
            <ellipse cx="986" cy="168" rx="23" ry="32" fill="#35c4b8"/>
            <ellipse cx="1048" cy="184" rx="27" ry="36" fill="#ff9f1c"/>
            <ellipse cx="1048" cy="184" rx="15" ry="21" fill="#ff3b30"/>
            <ellipse cx="1015" cy="142" rx="13" ry="21" fill="#b7e75f"/>
          </g>
          <text x="1015" y="310" fill="#ffd166" text-anchor="middle" font-size="15">
            Reconstrucción acumulada: {pct} %
          </text>
          <text x="1015" y="334" fill="#c9d6df" text-anchor="middle" font-size="14">
            {"Adquisición completa" if ang >= 360 else "Imagen aún incompleta"}
          </text>

          <!-- flujo inferior -->
          <line x1="465" y1="385" x2="1135" y2="385" stroke="#35576f" stroke-width="2"/>
          <text x="800" y="414" fill="#8bd3ff" text-anchor="middle" font-size="17">
            Proyección angular → sinograma → reconstrucción progresiva
          </text>
        </svg>
        </div>
        """
        components.html(html, height=475)

        st.progress(progreso)
        if ang == 0:
            st.info("Inicio de la adquisición: todavía no se ha completado ninguna proyección del recorrido.")
        elif ang < 360:
            st.info(
                f"Adquisición en curso: aproximadamente {adquiridas} de {nproj} proyecciones. "
                "Seguí moviendo el ángulo para observar cómo se completa el sinograma y mejora la reconstrucción."
            )
        else:
            st.success(
                f"Adquisición completa: {nproj} proyecciones alrededor de 360°. "
                "La imagen de la derecha representa el corte transaxial reconstruido final."
            )

        st.markdown("#### 🎞️ Proyecciones adquiridas")
        if adquiridas == 0:
            st.caption("Mové el ángulo para comenzar a adquirir proyecciones.")
        else:
            # Filmstrip conceptual de hasta 12 mini-proyecciones.
            mostrar = min(adquiridas, 12)
            cols = st.columns(mostrar)
            for k in range(mostrar):
                a_k = round((360 / nproj) * k)
                cols[k].markdown(
                    f"<div style='background:#111d29;border:1px solid #35576f;border-radius:8px;"
                    f"text-align:center;padding:8px 2px;font-size:12px'>"
                    f"<div style='height:36px;margin:auto;width:22px;border-radius:50%;"
                    f"background:radial-gradient(circle,#eee 0%,#888 35%,#111 75%)'></div>"
                    f"{a_k}°</div>",
                    unsafe_allow_html=True
                )

        if nproj == 16:
            st.warning("Con 16 proyecciones, la reconstrucción final conserva artefactos tipo estrella (streak) por submuestreo angular.")
        elif nproj == 32:
            st.warning("Con 32 proyecciones mejora el muestreo, aunque todavía pueden observarse artefactos por número limitado de proyecciones.")
        else:
            st.success("Al aumentar el número de proyecciones mejora el muestreo angular y disminuyen los artefactos asociados al submuestreo.")

        st.caption(
            "Las proyecciones, el sinograma y la reconstrucción son representaciones didácticas generadas en el código "
            "para visualizar el proceso; no corresponden a datos clínicos reales."
        )


        st.divider()
        st.subheader("🔄🔄 SPECT de doble cabezal: dos proyecciones simultáneas")
        st.write(
            "En este modelo didáctico, los dos cabezales están opuestos 180°. "
            "En cada posición angular se adquieren dos proyecciones simultáneamente: "
            "una por cada cabezal."
        )

        nproj_doble = st.select_slider(
            "Número total de proyecciones deseadas",
            options=[32, 64, 128],
            value=64,
            key="nproj_doble"
        )
        posiciones_doble = nproj_doble // 2
        paso_doble = 360.0 / nproj_doble
        paso_mecanico = 180.0 / posiciones_doble

        st.info(
            f"📐 **{nproj_doble} proyecciones totales** = {posiciones_doble} posiciones del sistema × 2 cabezales.  "
            f"Separación angular equivalente entre proyecciones = **{paso_doble:.3f}°**.  "
            f"Cada cabezal recorre aproximadamente **180°**."
        )

        pos_doble = st.slider(
            "Posición de adquisición del sistema",
            0, posiciones_doble, 0, 1,
            key="pos_doble"
        )
        ang_a = min(180.0, pos_doble * paso_mecanico)
        ang_b = (ang_a + 180.0) % 360.0
        adquiridas_doble = min(nproj_doble, pos_doble * 2)
        progreso_doble = min(1.0, adquiridas_doble / nproj_doble)

        cx2, cy2, r2 = 365, 205, 132
        xa = cx2 + r2 * math.cos(math.radians(ang_a))
        ya = cy2 + r2 * math.sin(math.radians(ang_a))
        xb = cx2 + r2 * math.cos(math.radians(ang_b))
        yb = cy2 + r2 * math.sin(math.radians(ang_b))

        # Sinograma conceptual del sistema de doble cabezal.
        filas_doble = []
        filas_totales_doble = 40
        filas_visibles_doble = round(filas_totales_doble * progreso_doble)
        for k in range(filas_totales_doble):
            yy = 67 + k * 5.0
            fase = 2 * math.pi * k / filas_totales_doble
            xx1 = 775 + 62 * math.sin(fase)
            xx2 = 775 + 39 * math.sin(fase + 1.65)
            op = 0.88 if k < filas_visibles_doble else 0.07
            filas_doble.append(
                f'<circle cx="{xx1:.1f}" cy="{yy:.1f}" r="6.5" fill="#f6f6f6" opacity="{op}"/>'
                f'<circle cx="{xx2:.1f}" cy="{yy:.1f}" r="4.5" fill="#bfc9d2" opacity="{op*0.75:.2f}"/>'
            )
        sino_doble_svg = "".join(filas_doble)

        # Reconstrucción progresiva didáctica, equivalente al esquema de un cabezal.
        streaks_doble = []
        n_streak_doble = 13 if nproj_doble == 32 else (6 if nproj_doble == 64 else 2)
        streak_op_doble = max(
            0.04,
            (1.0 - progreso_doble) * 0.52 + (0.18 if nproj_doble == 32 else 0.04)
        )
        for k in range(n_streak_doble):
            a = math.pi * k / max(1, n_streak_doble)
            dx = 72 * math.cos(a)
            dy = 72 * math.sin(a)
            streaks_doble.append(
                f'<line x1="{1080-dx:.1f}" y1="{180-dy:.1f}" '
                f'x2="{1080+dx:.1f}" y2="{180+dy:.1f}" '
                f'stroke="#d66cff" stroke-width="2" opacity="{streak_op_doble:.2f}"/>'
            )
        streak_doble_svg = "".join(streaks_doble)
        op_img_doble = 0.18 + 0.82 * progreso_doble
        blur_doble = max(
            1.0,
            8.0 * (1.0 - progreso_doble) + (2.2 if nproj_doble == 32 else 0.7)
        )

        # Dos proyecciones planares simultáneas, una por cada cabezal.
        fase_a = math.radians(ang_a)
        foco_a1 = 118 + 31 * math.cos(fase_a)
        foco_a2 = 190 - 22 * math.sin(fase_a)
        fase_b = math.radians(ang_b)
        foco_b1 = 118 + 31 * math.cos(fase_b)
        foco_b2 = 190 - 22 * math.sin(fase_b)

        html_doble = f"""
        <div style="background:#0e1720;border:1px solid #29465d;border-radius:22px;
                    padding:14px;color:white;font-family:Arial">
        <svg viewBox="0 0 1220 430" width="100%" height="430">
          <defs>
            <filter id="blurRecD">
              <feGaussianBlur stdDeviation="{blur_doble:.2f}"/>
            </filter>
            <filter id="blurProjD">
              <feGaussianBlur stdDeviation="4.5"/>
            </filter>
          </defs>

          <text x="225" y="28" fill="#fff" text-anchor="middle" font-size="20" font-weight="bold">
            Doble cabezal · vista superior
          </text>
          <text x="535" y="28" fill="#fff" text-anchor="middle" font-size="20" font-weight="bold">
            2 proyecciones simultáneas
          </text>
          <text x="785" y="28" fill="#fff" text-anchor="middle" font-size="20" font-weight="bold">
            Sinograma
          </text>
          <text x="1080" y="28" fill="#fff" text-anchor="middle" font-size="20" font-weight="bold">
            Reconstrucción transaxial
          </text>

          <!-- sistema de doble cabezal -->
          <rect x="20" y="45" width="410" height="305" rx="16" fill="#09131c" stroke="#29465d"/>
          <circle cx="{cx2}" cy="{cy2}" r="{r2}" fill="none" stroke="#55778e"
                  stroke-width="3" stroke-dasharray="7 7"/>
          <ellipse cx="{cx2}" cy="{cy2}" rx="70" ry="96" fill="#d6a27c"/>
          <circle cx="{cx2-23}" cy="{cy2-8}" r="13" fill="#ffb703"/>
          <circle cx="{cx2+27}" cy="{cy2+23}" r="9" fill="#ff7b00"/>

          <g transform="translate({xa:.1f},{ya:.1f}) rotate({ang_a+90:.1f})">
            <rect x="-56" y="-25" width="112" height="50" rx="8"
                  fill="#5aa9e6" stroke="#d8f0ff" stroke-width="4"/>
            <rect x="-47" y="-18" width="94" height="10" rx="3" fill="#8fd3a8"/>
          </g>
          <g transform="translate({xb:.1f},{yb:.1f}) rotate({ang_b+90:.1f})">
            <rect x="-56" y="-25" width="112" height="50" rx="8"
                  fill="#8b7cf6" stroke="#eeeaff" stroke-width="4"/>
            <rect x="-47" y="-18" width="94" height="10" rx="3" fill="#8fd3a8"/>
          </g>
          <line x1="{xa:.1f}" y1="{ya:.1f}" x2="{cx2}" y2="{cy2}"
                stroke="#ffd166" stroke-width="3" stroke-dasharray="6 5"/>
          <line x1="{xb:.1f}" y1="{yb:.1f}" x2="{cx2}" y2="{cy2}"
                stroke="#ffd166" stroke-width="3" stroke-dasharray="6 5"/>
          <text x="225" y="330" fill="#ffd166" text-anchor="middle" font-size="15">
            A: {ang_a:.2f}° · B: {ang_b:.2f}°
          </text>

          <!-- dos imágenes planares -->
          <rect x="448" y="45" width="205" height="305" rx="16" fill="#09131c" stroke="#29465d"/>
          <rect x="466" y="66" width="76" height="220" rx="6" fill="#020508"/>
          <rect x="559" y="66" width="76" height="220" rx="6" fill="#020508"/>
          <g filter="url(#blurProjD)">
            <ellipse cx="504" cy="{foco_a1:.1f}" rx="17" ry="29" fill="#f5f5f5" opacity=".66"/>
            <ellipse cx="504" cy="{foco_a2:.1f}" rx="11" ry="19" fill="#bfc9d2" opacity=".48"/>
            <ellipse cx="597" cy="{foco_b1:.1f}" rx="17" ry="29" fill="#f5f5f5" opacity=".66"/>
            <ellipse cx="597" cy="{foco_b2:.1f}" rx="11" ry="19" fill="#bfc9d2" opacity=".48"/>
          </g>
          <text x="504" y="310" fill="#5aa9e6" text-anchor="middle" font-size="14">Cabezal A</text>
          <text x="597" y="310" fill="#b7aaff" text-anchor="middle" font-size="14">Cabezal B</text>
          <text x="550" y="334" fill="#ffd166" text-anchor="middle" font-size="14">
            2 imágenes / posición
          </text>

          <!-- sinograma -->
          <rect x="675" y="45" width="210" height="305" rx="16" fill="#09131c" stroke="#29465d"/>
          <rect x="715" y="62" width="120" height="220" rx="5" fill="#020508"/>
          {sino_doble_svg}
          <line x1="715" y1="{67 + filas_visibles_doble*5.0:.1f}"
                x2="835" y2="{67 + filas_visibles_doble*5.0:.1f}"
                stroke="#ff4d5a" stroke-width="3" opacity="{1 if pos_doble>0 else 0}"/>
          <text x="780" y="310" fill="#c9d6df" text-anchor="middle" font-size="14">
            {adquiridas_doble} / {nproj_doble} proyecciones
          </text>
          <text x="780" y="334" fill="#8bd3ff" text-anchor="middle" font-size="14">
            se completa de a 2
          </text>

          <!-- reconstrucción -->
          <rect x="905" y="45" width="295" height="305" rx="16" fill="#09131c" stroke="#29465d"/>
          <rect x="970" y="67" width="220" height="218" rx="8" fill="#020508"/>
          {streak_doble_svg}
          <g filter="url(#blurRecD)" opacity="{op_img_doble:.2f}">
            <ellipse cx="1080" cy="176" rx="78" ry="86" fill="#4b1677"/>
            <ellipse cx="1080" cy="176" rx="65" ry="72" fill="#1c67b1"/>
            <ellipse cx="1051" cy="168" rx="23" ry="32" fill="#35c4b8"/>
            <ellipse cx="1113" cy="184" rx="27" ry="36" fill="#ff9f1c"/>
            <ellipse cx="1113" cy="184" rx="15" ry="21" fill="#ff3b30"/>
            <ellipse cx="1080" cy="142" rx="13" ry="21" fill="#b7e75f"/>
          </g>
          <text x="1080" y="310" fill="#ffd166" text-anchor="middle" font-size="15">
            Reconstrucción acumulada: {int(progreso_doble*100)} %
          </text>
          <text x="1080" y="334" fill="#c9d6df" text-anchor="middle" font-size="14">
            {"Adquisición completa" if progreso_doble >= 1 else "Imagen aún incompleta"}
          </text>

          <line x1="420" y1="385" x2="1170" y2="385" stroke="#35576f" stroke-width="2"/>
          <text x="795" y="414" fill="#8bd3ff" text-anchor="middle" font-size="16">
            2 proyecciones simultáneas → sinograma → reconstrucción progresiva
          </text>
        </svg>
        </div>
        """
        components.html(html_doble, height=475)
        st.progress(progreso_doble)
        if pos_doble == 0:
            st.info("Inicio: los dos cabezales están listos para adquirir simultáneamente.")
        elif progreso_doble < 1:
            st.info(
                f"Adquisición en curso: {adquiridas_doble} de {nproj_doble} proyecciones. "
                "Cada nueva posición incorpora dos imágenes planares y actualiza el sinograma y la reconstrucción."
            )
        else:
            st.success(
                f"Adquisición completa: {nproj_doble} proyecciones obtenidas con "
                f"{posiciones_doble} posiciones del sistema de doble cabezal. "
                "La imagen de la derecha representa la reconstrucción final."
            )

        st.markdown(
            f"**Comparación:** con un cabezal, una posición angular aporta una proyección. "
            f"Con dos cabezales opuestos, una posición del sistema aporta dos proyecciones simultáneas. "
            f"Para este ejemplo de {nproj_doble} proyecciones, el sistema necesita "
            f"{posiciones_doble} posiciones."
        )
        st.caption(
            "Esquema didáctico con dos cabezales opuestos 180°. La geometría exacta y el arco de adquisición "
            "pueden variar según el equipo y el protocolo."
        )

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
