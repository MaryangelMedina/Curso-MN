import streamlit as st
import streamlit.components.v1 as components
import math
import time

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

        # Controles manuales + reproducción automática.
        if "spect_single_idx" not in st.session_state:
            st.session_state.spect_single_idx = 0
        if "spect_single_play" not in st.session_state:
            st.session_state.spect_single_play = False
        st.session_state.spect_single_idx = min(st.session_state.spect_single_idx, nproj)

        indice_proj = st.slider(
            "Proyección adquirida",
            0, nproj, key="spect_single_idx", step=1,
            help="También podés mover manualmente la barra. Cada paso representa una nueva posición angular y una nueva imagen planar."
        )
        ang = min(360.0, indice_proj * paso_angular)

        m1,m2,m3 = st.columns(3)
        m1.metric("Proyección manual", f"{indice_proj} / {nproj}")
        m2.metric("Ángulo manual", f"{ang:.3f}°")
        m3.metric("Paso angular", f"{paso_angular:.3f}°")
        st.caption("La barra sigue disponible para explorar manualmente cada proyección.")

        st.markdown("#### ▶️ Reproducción automática de la rotación")
        auto_html = f"""
        <div id="spectAuto" style="background:#0e1720;border:1px solid #29465d;border-radius:18px;padding:12px;color:white;font-family:Arial,sans-serif">
          <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px">
            <button id="spPlay" style="padding:8px 16px">▶️ Play</button>
            <button id="spPause" style="padding:8px 16px">⏸️ Pausa</button>
            <button id="spPrev" style="padding:8px 16px">⏮️ Atrás</button>
            <button id="spNext" style="padding:8px 16px">⏭️ Avanzar</button>
            <button id="spReset" style="padding:8px 16px">↩️ Inicio</button>
          </div>
          <div style="display:flex;gap:18px;flex-wrap:wrap;margin-bottom:8px;font-size:16px">
            <b>Proyección: <span id="spProj">0</span> / {nproj}</b>
            <b>Ángulo: <span id="spAng">0.000</span>°</b>
            <b>Paso: {paso_angular:.3f}°</b>
          </div>
          <svg viewBox="0 0 1050 500" width="100%" style="display:block;overflow:hidden">
            <rect x="20" y="15" width="1010" height="455" rx="16" fill="#071019"/>
            <text x="525" y="42" fill="white" text-anchor="middle" font-size="18">Rotación automática SPECT · un cabezal</text><text x="525" y="65" fill="#8bd3ff" text-anchor="middle" font-size="13">Simulación automática de adquisición</text>
            <circle cx="300" cy="225" r="92" fill="none" stroke="#29485d" stroke-width="3" stroke-dasharray="5 5"/>
            <ellipse cx="300" cy="225" rx="39" ry="55" fill="#d7a37d"/>
            <ellipse cx="288" cy="220" rx="10" ry="15" fill="#35c4b8" opacity=".8"/>
            <ellipse cx="316" cy="233" rx="12" ry="17" fill="#ff9f1c" opacity=".8"/>
            <line id="spRay" x1="300" y1="225" x2="392" y2="225" stroke="#ffd166" stroke-width="2.5"/>
            <g id="spHead" transform="translate(392 225) rotate(90)">
              <rect x="-34" y="-16" width="68" height="32" rx="6" fill="#7b61a8"/>
              <rect x="-28" y="-10" width="56" height="6" fill="#7ef29a"/>
              <text x="0" y="4" fill="white" text-anchor="middle" font-size="10">CÁMARA</text>
            </g>
            <rect x="575" y="85" width="360" height="285" rx="14" fill="#101c26" stroke="#29465d"/>
            <text x="755" y="120" fill="white" text-anchor="middle" font-size="16">Imagen planar actual</text>
            <ellipse id="spPlanar1" cx="755" cy="220" rx="31" ry="52" fill="#bbb" opacity=".75"/>
            <ellipse id="spPlanar2" cx="755" cy="225" rx="14" ry="29" fill="#eee" opacity=".8"/>
            <text x="755" y="345" fill="#8bd3ff" text-anchor="middle" font-size="13">El cabezal avanza una proyección por paso</text>
          </svg>
        </div>
        <script>
        (function(){{
          const root=document.getElementById("spectAuto");
          if(!root || root.dataset.ready==="1") return;
          root.dataset.ready="1";
          const N={nproj}, step=360/N, cx=300, cy=225, R=92;
          let i=0, timer=null;
          const head=root.querySelector("#spHead"), ray=root.querySelector("#spRay");
          const proj=root.querySelector("#spProj"), ang=root.querySelector("#spAng");
          const p1=root.querySelector("#spPlanar1"), p2=root.querySelector("#spPlanar2");
          function draw(){{
            const a=Math.min(i,N)*step;
            const rad=a*Math.PI/180;
            const x=cx+R*Math.cos(rad), y=cy+R*Math.sin(rad);
            head.setAttribute("transform",`translate(${{x}} ${{y}}) rotate(${{a+90}})`);
            ray.setAttribute("x2",x); ray.setAttribute("y2",y);
            proj.textContent=i; ang.textContent=a.toFixed(3);
            const squash=0.72+0.28*Math.abs(Math.cos(rad));
            p1.setAttribute("rx",(34*squash).toFixed(1));
            p2.setAttribute("cx",(755+18*Math.sin(rad)).toFixed(1));
          }}
          function stop(){{ if(timer){{clearInterval(timer);timer=null;}} }}
          function play(){{
            if(i>=N) i=0;
            stop();
            timer=setInterval(()=>{{
              if(i>=N){{stop();return;}}
              i++; draw();
            }},350);
          }}
          root.querySelector("#spPlay").addEventListener("click",play);
          root.querySelector("#spPause").addEventListener("click",stop);
          root.querySelector("#spPrev").addEventListener("click",()=>{{stop();i=Math.max(0,i-1);draw();}});
          root.querySelector("#spNext").addEventListener("click",()=>{{stop();i=Math.min(N,i+1);draw();}});
          root.querySelector("#spReset").addEventListener("click",()=>{{stop();i=0;draw();}});
          draw();
        }})();
        </script>
        """
        components.html(auto_html, height=545)

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

        if "spect_double_idx" not in st.session_state:
            st.session_state.spect_double_idx = 0
        if "spect_double_play" not in st.session_state:
            st.session_state.spect_double_play = False
        st.session_state.spect_double_idx = min(st.session_state.spect_double_idx, posiciones_doble)

        pos_doble = st.slider(
            "Posición de adquisición del sistema",
            0, posiciones_doble, key="spect_double_idx", step=1,
            help="Podés reproducir automáticamente o recorrer manualmente cada posición del sistema."
        )
        ang_a = min(180.0, pos_doble * paso_mecanico)
        ang_b = (ang_a + 180.0) % 360.0
        adquiridas_doble = min(nproj_doble, pos_doble * 2)
        progreso_doble = min(1.0, adquiridas_doble / nproj_doble)

        dm1,dm2,dm3,dm4 = st.columns(4)
        dm1.metric("Posición", f"{pos_doble} / {posiciones_doble}")
        dm2.metric("Proyecciones", f"{adquiridas_doble} / {nproj_doble}")
        dm3.metric("Cabezal A", f"{ang_a:.3f}°")
        dm4.metric("Cabezal B", f"{ang_b:.3f}°")
        st.caption(f"Paso angular equivalente entre proyecciones: {paso_doble:.3f}°")

        st.markdown("#### ▶️ Reproducción automática · doble cabezal")
        double_auto_html = f"""
        <div id="spectDoubleAuto" style="background:#0e1720;border:1px solid #29465d;border-radius:18px;padding:12px;color:white;font-family:Arial,sans-serif">
          <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px">
            <button id="sdPlay" style="padding:8px 16px">▶️ Play</button>
            <button id="sdPause" style="padding:8px 16px">⏸️ Pausa</button>
            <button id="sdPrev" style="padding:8px 16px">⏮️ Atrás</button>
            <button id="sdNext" style="padding:8px 16px">⏭️ Avanzar</button>
            <button id="sdReset" style="padding:8px 16px">↩️ Inicio</button>
          </div>
          <div style="display:flex;gap:18px;flex-wrap:wrap;margin-bottom:8px;font-size:15px">
            <b>Posición: <span id="sdPos">0</span> / {posiciones_doble}</b>
            <b>Proyecciones acumuladas: <span id="sdProj">0</span> / {nproj_doble}</b>
            <b>Cabezal A: <span id="sdAngA">0.000</span>°</b>
            <b>Cabezal B: <span id="sdAngB">180.000</span>°</b>
          </div>
          <svg viewBox="0 0 900 430" width="100%" style="display:block;overflow:hidden">
            <rect x="10" y="10" width="880" height="395" rx="16" fill="#071019"/>
            <text x="450" y="38" fill="white" text-anchor="middle" font-size="18">Rotación automática SPECT · doble cabezal</text>
            <text x="450" y="60" fill="#8bd3ff" text-anchor="middle" font-size="13">Los dos cabezales permanecen opuestos 180° y giran simultáneamente</text>

            <circle cx="330" cy="185" r="82" fill="none" stroke="#29485d" stroke-width="3" stroke-dasharray="5 5"/>
            <ellipse cx="330" cy="185" rx="36" ry="50" fill="#d7a37d"/>
            <ellipse cx="319" cy="181" rx="9" ry="14" fill="#35c4b8" opacity=".8"/>
            <ellipse cx="344" cy="193" rx="11" ry="16" fill="#ff9f1c" opacity=".8"/>

            <line id="sdRayA" x1="330" y1="185" x2="412" y2="185" stroke="#ffd166" stroke-width="2.5"/>
            <line id="sdRayB" x1="330" y1="185" x2="248" y2="185" stroke="#ffd166" stroke-width="2.5"/>

            <g id="sdHeadA" transform="translate(412 185) rotate(90)">
              <rect x="-34" y="-16" width="68" height="32" rx="6" fill="#7b61a8"/>
              <rect x="-28" y="-10" width="56" height="6" fill="#7ef29a"/>
              <text x="0" y="4" fill="white" text-anchor="middle" font-size="10">A</text>
            </g>
            <g id="sdHeadB" transform="translate(248 185) rotate(270)">
              <rect x="-34" y="-16" width="68" height="32" rx="6" fill="#5577a8"/>
              <rect x="-28" y="-10" width="56" height="6" fill="#7ef29a"/>
              <text x="0" y="4" fill="white" text-anchor="middle" font-size="10">B</text>
            </g>

            <rect x="535" y="75" width="285" height="220" rx="14" fill="#101c26" stroke="#29465d"/>
            <text x="677" y="105" fill="white" text-anchor="middle" font-size="16">Proyecciones simultáneas</text>
            <ellipse id="sdPlanA" cx="635" cy="180" rx="24" ry="42" fill="#bbb" opacity=".75"/>
            <ellipse id="sdPlanB" cx="720" cy="180" rx="24" ry="42" fill="#888" opacity=".75"/>
            <text x="635" y="250" fill="#ddd" text-anchor="middle" font-size="13">Cabezal A</text>
            <text x="720" y="250" fill="#ddd" text-anchor="middle" font-size="13">Cabezal B</text>
          </svg>
        </div>
        <script>
        (function(){{
          const root=document.getElementById("spectDoubleAuto");
          if(!root || root.dataset.ready==="1") return;
          root.dataset.ready="1";
          const P={posiciones_doble}, total={nproj_doble}, step=180/P, cx=330, cy=185, R=82;
          let i=0, timer=null;
          const hA=root.querySelector("#sdHeadA"), hB=root.querySelector("#sdHeadB");
          const rA=root.querySelector("#sdRayA"), rB=root.querySelector("#sdRayB");
          const pos=root.querySelector("#sdPos"), proj=root.querySelector("#sdProj");
          const aA=root.querySelector("#sdAngA"), aB=root.querySelector("#sdAngB");
          const pA=root.querySelector("#sdPlanA"), pB=root.querySelector("#sdPlanB");
          function draw(){{
            const a=i*step, b=a+180, ra=a*Math.PI/180, rb=b*Math.PI/180;
            const xa=cx+R*Math.cos(ra), ya=cy+R*Math.sin(ra);
            const xb=cx+R*Math.cos(rb), yb=cy+R*Math.sin(rb);
            hA.setAttribute("transform",`translate(${{xa}} ${{ya}}) rotate(${{a+90}})`);
            hB.setAttribute("transform",`translate(${{xb}} ${{yb}}) rotate(${{b+90}})`);
            rA.setAttribute("x2",xa); rA.setAttribute("y2",ya);
            rB.setAttribute("x2",xb); rB.setAttribute("y2",yb);
            pos.textContent=i; proj.textContent=Math.min(total,i*2);
            aA.textContent=a.toFixed(3); aB.textContent=b.toFixed(3);
            pA.setAttribute("rx",(27*(.72+.28*Math.abs(Math.cos(ra)))).toFixed(1));
            pB.setAttribute("rx",(27*(.72+.28*Math.abs(Math.cos(rb)))).toFixed(1));
          }}
          function stop(){{if(timer){{clearInterval(timer);timer=null;}}}}
          function play(){{
            if(i>=P) i=0;
            stop();
            timer=setInterval(()=>{{
              if(i>=P){{stop();return;}}
              i++; draw();
            }},350);
          }}
          root.querySelector("#sdPlay").addEventListener("click",play);
          root.querySelector("#sdPause").addEventListener("click",stop);
          root.querySelector("#sdPrev").addEventListener("click",()=>{{stop();i=Math.max(0,i-1);draw();}});
          root.querySelector("#sdNext").addEventListener("click",()=>{{stop();i=Math.min(P,i+1);draw();}});
          root.querySelector("#sdReset").addEventListener("click",()=>{{stop();i=0;draw();}});
          draw();
        }})();
        </script>
        """
        components.html(double_auto_html, height=555)

        # Geometría compacta: ambos cabezales permanecen dentro del primer recuadro.
        cx2, cy2, r2 = 225, 205, 102
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
        <svg viewBox="0 0 1220 430" width="100%" height="430" style="overflow:hidden">
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
          <ellipse cx="{cx2}" cy="{cy2}" rx="54" ry="74" fill="#d6a27c"/>
          <circle cx="{cx2-23}" cy="{cy2-8}" r="13" fill="#ffb703"/>
          <circle cx="{cx2+27}" cy="{cy2+23}" r="9" fill="#ff7b00"/>

          <g transform="translate({xa:.1f},{ya:.1f}) rotate({ang_a+90:.1f})">
            <rect x="-40" y="-19" width="80" height="38" rx="8"
                  fill="#5aa9e6" stroke="#d8f0ff" stroke-width="4"/>
            <rect x="-33" y="-13" width="66" height="8" rx="3" fill="#8fd3a8"/>
          </g>
          <g transform="translate({xb:.1f},{yb:.1f}) rotate({ang_b+90:.1f})">
            <rect x="-40" y="-19" width="80" height="38" rx="8"
                  fill="#8b7cf6" stroke="#eeeaff" stroke-width="4"/>
            <rect x="-33" y="-13" width="66" height="8" rx="3" fill="#8fd3a8"/>
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
        st.subheader("🧩 Reconstrucción SPECT: mirá qué hace cada método")
        st.write("Compará visualmente retroproyección simple, FBP e iterativa. Es un modelo didáctico, no un reconstructor clínico.")
        metodo = st.radio("Método de reconstrucción",
                          ["Retroproyección simple","Retroproyección filtrada (FBP)","Iterativa"],
                          horizontal=True)

        if metodo == "Retroproyección simple":
            nitidez, streak = 7.0, 0.52
            proceso = "Retroproyectar"
            detalle = "Las contribuciones se superponen y queda el borroneo característico."
            estado = "Sin filtrado previo"
        elif metodo == "Retroproyección filtrada (FBP)":
            corte = st.slider("Frecuencia de corte conceptual del filtro",20,100,65,5)
            nitidez, streak = max(1.2,6.0-corte/22), 0.16
            proceso = "Filtrar → retroproyectar"
            detalle = "El filtrado controla el borroneo antes de formar el corte."
            estado = f"Frecuencia de corte conceptual: {corte}%"
        else:
            it = st.slider("Número conceptual de iteraciones",1,10,4)
            nitidez, streak = max(0.8,6.5-0.58*it), max(0.04,0.35-0.03*it)
            proceso = "Estimar → comparar → corregir → repetir"
            detalle = "La estimación se actualiza progresivamente al comparar datos calculados y adquiridos."
            estado = f"Iteración conceptual: {it}"

        rayas=[]
        for k in range(12):
            aa=math.pi*k/12
            dx=72*math.cos(aa); dy=72*math.sin(aa)
            rayas.append(f'<line x1="{925-dx:.1f}" y1="{180-dy:.1f}" x2="{925+dx:.1f}" y2="{180+dy:.1f}" stroke="#d66cff" stroke-width="2" opacity="{streak:.2f}"/>')
        rayas_svg="".join(rayas)

        html_rec=f"""
        <div style="background:#0e1720;border:1px solid #29465d;border-radius:20px;padding:12px">
        <svg viewBox="0 0 1120 390" width="100%" height="390">
          <defs><filter id="br"><feGaussianBlur stdDeviation="{nitidez:.2f}"/></filter></defs>
          <text x="175" y="28" fill="white" text-anchor="middle" font-size="20" font-weight="bold">Proyecciones</text>
          <text x="465" y="28" fill="white" text-anchor="middle" font-size="20" font-weight="bold">Sinograma</text>
          <text x="710" y="28" fill="white" text-anchor="middle" font-size="20" font-weight="bold">Proceso</text>
          <text x="925" y="28" fill="white" text-anchor="middle" font-size="20" font-weight="bold">Corte reconstruido</text>
          <rect x="35" y="50" width="280" height="245" rx="14" fill="#071019" stroke="#29465d"/>
          <ellipse cx="95" cy="145" rx="25" ry="60" fill="#ddd"/><ellipse cx="155" cy="165" rx="22" ry="48" fill="#999"/>
          <ellipse cx="215" cy="130" rx="28" ry="65" fill="#eee"/><ellipse cx="270" cy="175" rx="18" ry="42" fill="#aaa"/>
          <text x="175" y="325" fill="#8bd3ff" text-anchor="middle" font-size="15">vistas desde distintos ángulos</text>
          <rect x="340" y="50" width="250" height="245" rx="14" fill="#071019" stroke="#29465d"/>
          <path d="M365 250 C405 80,455 80,565 245" fill="none" stroke="#eee" stroke-width="12" opacity=".8"/>
          <path d="M365 100 C435 250,505 250,565 105" fill="none" stroke="#999" stroke-width="8" opacity=".65"/>
          <text x="465" y="325" fill="#8bd3ff" text-anchor="middle" font-size="15">datos organizados por ángulo</text>
          <rect x="615" y="50" width="190" height="245" rx="14" fill="#071019" stroke="#29465d"/>
          <text x="710" y="130" fill="#ffd166" text-anchor="middle" font-size="15">{proceso}</text>
          <text x="710" y="180" fill="#fff" text-anchor="middle" font-size="38">→</text>
          <text x="710" y="225" fill="#c9d6df" text-anchor="middle" font-size="13">{estado}</text>
          <rect x="825" y="50" width="260" height="245" rx="14" fill="#020508" stroke="#29465d"/>
          {rayas_svg}
          <g filter="url(#br)">
            <ellipse cx="925" cy="175" rx="72" ry="82" fill="#4b1677"/><ellipse cx="925" cy="175" rx="60" ry="69" fill="#1c67b1"/>
            <ellipse cx="900" cy="165" rx="22" ry="31" fill="#35c4b8"/><ellipse cx="953" cy="185" rx="25" ry="34" fill="#ff9f1c"/>
            <ellipse cx="953" cy="185" rx="13" ry="20" fill="#ff3b30"/><ellipse cx="925" cy="142" rx="12" ry="19" fill="#b7e75f"/>
          </g>
          <text x="925" y="325" fill="#ffd166" text-anchor="middle" font-size="14">{metodo}</text>
          <text x="560" y="370" fill="#8bd3ff" text-anchor="middle" font-size="16">PROYECCIONES → SINOGRAMA → RECONSTRUCCIÓN → IMAGEN</text>
        </svg></div>"""
        components.html(html_rec,height=420)
        st.info(detalle)
        st.caption("Representación didáctica: los cambios de nitidez y artefactos permiten comparar visualmente los métodos.")

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
    p1,p2,p3,p4,p5,p6 = st.tabs(["1️⃣ Aniquilación","2️⃣ Eventos / Coincidencias","3️⃣ Detector PET","4️⃣ Tiempo muerto","5️⃣ Imagen PET","6️⃣ Preguntas"])

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
        st.subheader("📏 Eventos PET: verdaderos, dispersados y aleatorios")
        tipo_evento=st.radio("Elegí un evento",
            ["Coincidencia verdadera","Coincidencia dispersada","Coincidencia aleatoria"],horizontal=True)
        ang=st.slider("Orientación del evento",0,175,30,5,key="pet_event_angle")
        cx,cy,R=400,210,165
        dx=R*math.cos(math.radians(ang)); dy=R*math.sin(math.radians(ang))
        detectores="".join(f'<circle cx="{cx+R*math.cos(math.radians(q))}" cy="{cy+R*math.sin(math.radians(q))}" r="7" fill="#5aa9e6"/>' for q in range(0,360,10))
        if tipo_evento=="Coincidencia verdadera":
            trazos=f'<line x1="{cx-dx}" y1="{cy-dy}" x2="{cx+dx}" y2="{cy+dy}" stroke="#7ef29a" stroke-width="5"/><circle cx="{cx-dx}" cy="{cy-dy}" r="13" fill="#7ef29a"/><circle cx="{cx+dx}" cy="{cy+dy}" r="13" fill="#7ef29a"/>'
            mensaje="Mismo evento + ventana temporal → LOR correcta"; color="#7ef29a"
        elif tipo_evento=="Coincidencia dispersada":
            qx,qy=cx+45,cy-25
            trazos=f'<line x1="{cx}" y1="{cy}" x2="{qx}" y2="{qy}" stroke="#ffd166" stroke-width="4"/><line x1="{qx}" y1="{qy}" x2="{cx+dx}" y2="{cy+dy}" stroke="#ff9f1c" stroke-width="5"/><line x1="{cx}" y1="{cy}" x2="{cx-dx}" y2="{cy-dy}" stroke="#ffd166" stroke-width="4"/><circle cx="{qx}" cy="{qy}" r="10" fill="#ff9f1c"/><circle cx="{cx-dx}" cy="{cy-dy}" r="13" fill="#ff9f1c"/><circle cx="{cx+dx}" cy="{cy+dy}" r="13" fill="#ff9f1c"/>'
            mensaje="Un fotón cambia de dirección → LOR asignada incorrecta"; color="#ff9f1c"
        else:
            dx2=R*math.cos(math.radians(ang+55)); dy2=R*math.sin(math.radians(ang+55))
            trazos=f'<circle cx="{cx-45}" cy="{cy-35}" r="8" fill="#ff4d6d"/><circle cx="{cx+35}" cy="{cy+45}" r="8" fill="#ff4d6d"/><line x1="{cx-45}" y1="{cy-35}" x2="{cx-dx}" y2="{cy-dy}" stroke="#f06cff" stroke-width="4"/><line x1="{cx+35}" y1="{cy+45}" x2="{cx+dx2}" y2="{cy+dy2}" stroke="#f06cff" stroke-width="4"/><line x1="{cx-dx}" y1="{cy-dy}" x2="{cx+dx2}" y2="{cy+dy2}" stroke="#f06cff" stroke-width="3" stroke-dasharray="7 6"/><circle cx="{cx-dx}" cy="{cy-dy}" r="13" fill="#f06cff"/><circle cx="{cx+dx2}" cy="{cy+dy2}" r="13" fill="#f06cff"/>'
            mensaje="Eventos diferentes dentro de la ventana → coincidencia aleatoria"; color="#f06cff"
        html=f"""<div style="background:#0e1720;border-radius:20px"><svg viewBox="0 0 800 430" width="100%" height="430">
        <text x="400" y="28" fill="white" text-anchor="middle" font-size="24">{tipo_evento}</text>
        <circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="#29485d" stroke-width="25"/>{detectores}
        <ellipse cx="{cx}" cy="{cy}" rx="95" ry="125" fill="#d7a37d"/><circle cx="{cx}" cy="{cy}" r="8" fill="#ff4d6d"/>{trazos}
        <text x="400" y="405" fill="{color}" text-anchor="middle" font-size="17">{mensaje}</text></svg></div>"""
        components.html(html,height=460)
        ventana=st.slider("Ventana temporal conceptual de coincidencia",1,10,4,key="ventana_pet")
        st.progress(ventana/10)
        st.caption("Al ampliar la ventana temporal aumenta la posibilidad de aceptar detecciones no relacionadas. Control didáctico, sin valores de un equipo real.")

    with p3:
        st.subheader("💎 Cristales detectores PET: de los primeros sistemas a los actuales")
        st.write(
            "El cristal convierte la energía del fotón de 511 keV en luz. "
            "No existe un cristal perfecto: se busca un compromiso entre poder de frenado, "
            "cantidad de luz, rapidez, resolución energética, robustez y costo."
        )

        cristales = {
            "NaI(Tl)": {
                "nombre":"Yoduro de sodio dopado con talio", "formula":"NaI:Tl",
                "dens":"3.67", "zeff":"51", "luz":"≈38 000", "decay":"≈230 ns",
                "rob":"Higroscópico; requiere encapsulado",
                "epoca":"Histórico / primeros desarrollos PET",
                "pro":"Alta producción de luz y tecnología muy conocida.",
                "contra":"Baja densidad para 511 keV y respuesta relativamente lenta."
            },
            "BGO": {
                "nombre":"Germanato de bismuto", "formula":"Bi₄Ge₃O₁₂",
                "dens":"7.13", "zeff":"≈74–75", "luz":"≈9 000", "decay":"≈300 ns",
                "rob":"No higroscópico; mecánicamente robusto",
                "epoca":"Muy extendido desde la generación PET de los años 1980–1990",
                "pro":"Muy denso y excelente poder de frenado para 511 keV.",
                "contra":"Poca luz y decaimiento lento; menos favorable para TOF clásico."
            },
            "GSO": {
                "nombre":"Oxiortosilicato de gadolinio dopado con cerio", "formula":"Gd₂SiO₅:Ce",
                "dens":"≈6.7", "zeff":"≈59", "luz":"≈13 000", "decay":"≈50–65 ns",
                "rob":"No higroscópico",
                "epoca":"Generación intermedia de PET",
                "pro":"Más rápido que BGO y con buena densidad.",
                "contra":"Menor producción de luz y poder de frenado que LSO/LYSO."
            },
            "LSO": {
                "nombre":"Oxiortosilicato de lutecio dopado con cerio", "formula":"Lu₂SiO₅:Ce",
                "dens":"≈7.4", "zeff":"≈66", "luz":"≈26 000–31 000", "decay":"≈40 ns",
                "rob":"No higroscópico; robusto",
                "epoca":"PET moderno / base de sistemas TOF",
                "pro":"Denso, rápido y con buena producción de luz: muy favorable para TOF.",
                "contra":"Contiene lutecio y presenta radiactividad intrínseca; costo del material."
            },
            "LYSO": {
                "nombre":"Oxiortosilicato de lutecio-itrio dopado con cerio", "formula":"(Lu,Y)₂SiO₅:Ce",
                "dens":"≈7.1–7.2", "zeff":"≈60–65", "luz":"≈30 000–32 000", "decay":"≈40–41 ns",
                "rob":"No higroscópico; robusto",
                "epoca":"Muy utilizado en PET/CT y TOF contemporáneo",
                "pro":"Buen equilibrio entre densidad, luz y rapidez; excelente para temporización.",
                "contra":"Costo y radiactividad intrínseca asociada al lutecio."
            },
            "LaBr₃:Ce": {
                "nombre":"Bromuro de lantano dopado con cerio", "formula":"LaBr₃:Ce",
                "dens":"≈5.3", "zeff":"≈47", "luz":"≈60 000", "decay":"≈15–25 ns",
                "rob":"Higroscópico; necesita encapsulado",
                "epoca":"Investigación y desarrollos de temporización",
                "pro":"Muy alta producción de luz, rápido y excelente resolución energética.",
                "contra":"Menor poder de frenado que LSO/LYSO y es higroscópico."
            },
            "GAGG:Ce": {
                "nombre":"Granate de gadolinio-aluminio-galio dopado con cerio", "formula":"Gd₃(Al,Ga)₅O₁₂:Ce",
                "dens":"≈6.5–6.6", "zeff":"≈48–53", "luz":"≈46 000–58 000", "decay":"≈50–200 ns*",
                "rob":"No higroscópico; buena robustez",
                "epoca":"Material emergente / investigación PET",
                "pro":"Alta producción de luz, buena densidad y posibilidad de fabricación en cerámicas.",
                "contra":"La temporización depende mucho de composición/dopaje; no domina el PET clínico actual."
            }
        }

        sel = st.selectbox("Elegí un cristal para explorarlo", list(cristales.keys()), index=4)
        d = cristales[sel]

        st.markdown(
            f"""
            <div style="background:#0e1720;border:1px solid #35576f;border-radius:18px;padding:18px">
              <div style="font-size:27px;font-weight:700;color:#ffd166">{sel} · {d["formula"]}</div>
              <div style="font-size:17px;color:#c9d6df;margin-top:4px">{d["nombre"]}</div>
              <div style="font-size:15px;color:#8bd3ff;margin-top:7px">{d["epoca"]}</div>
            </div>
            """, unsafe_allow_html=True
        )

        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Densidad", f'{d["dens"]} g/cm³')
        c2.metric("Z efectivo", d["zeff"])
        c3.metric("Luz", f'{d["luz"]} fot/MeV')
        c4.metric("Decaimiento", d["decay"])

        cp,cc = st.columns(2)
        cp.success("**Ventaja principal**\n\n" + d["pro"])
        cc.warning("**Limitación principal**\n\n" + d["contra"])
        st.info("**Robustez / manejo del material:** " + d["rob"])

        st.markdown("#### ⏱️ ¿Qué significa TOF?")
        st.info(
            "**TOF = Time of Flight (tiempo de vuelo).** En una coincidencia PET, los dos fotones de 511 keV "
            "llegan a los detectores con una pequeñísima diferencia temporal. TOF utiliza esa diferencia para "
            "estimar en qué zona de la LOR ocurrió con mayor probabilidad la aniquilación. No elimina la LOR: "
            "agrega información de localización a lo largo de ella y mejora la relación señal/ruido de la reconstrucción."
        )
        st.markdown("**Cristales rápidos + mucha luz + fotodetectores rápidos (especialmente SiPM) → mejor resolución temporal → mejor aprovechamiento de TOF.**")

        st.markdown("#### 📊 Comparación rápida de cristales PET")
        st.markdown("""
| Cristal | Densidad | Decaimiento | Robustez | ¿Qué ventaja aporta en PET? | TOF |
|---|---:|---:|---|---|---|
| **NaI(Tl)** | 3.67 g/cm³ | ~230 ns | Higroscópico | Mucha luz y buena resolución energética, pero menor eficiencia de detección a 511 keV | Poco favorable |
| **BGO** | 7.13 g/cm³ | ~300 ns | Robusto, no higroscópico | **Muy alto poder de frenado** → buena eficiencia/sensibilidad para 511 keV | Limitado por su respuesta lenta |
| **GSO:Ce** | ~6.7 g/cm³ | ~50–65 ns | No higroscópico | Más rápido que BGO y con buena densidad; favorece mayores tasas de conteo | Mejor que BGO, no es el estándar TOF actual |
| **LSO:Ce** | ~7.4 g/cm³ | ~40 ns | Robusto, no higroscópico | **Alta densidad + buena luz + rapidez** → sensibilidad, altas tasas y buena temporización | **Muy favorable** |
| **LYSO:Ce** | ~7.1 g/cm³ | ~40 ns | Robusto, no higroscópico | Excelente equilibrio entre stopping power, luz y rapidez; ampliamente usado en PET moderno | **Muy favorable** |
| **LaBr₃:Ce** | ~5.3 g/cm³ | ~15–25 ns | Higroscópico | Muchísima luz, gran resolución energética y respuesta muy rápida | Excelente temporización, pero menor stopping power |
| **GAGG:Ce** | ~6.6 g/cm³ | variable | No higroscópico | Alta luz y buena densidad; interesante para nuevos diseños | Potencial / investigación |
        """)

        st.caption(
            "Los valores son representativos y pueden variar con composición, dopaje, fabricante y método de medición. "
            "La constante de decaimiento NO es el tiempo muerto: un cristal rápido favorece la temporización y altas tasas, "
            "pero el tiempo muerto es una propiedad del sistema detector/electrónica completo."
        )

        st.markdown("#### 🔗 Del cristal a la coincidencia")
        st.markdown("### `511 keV → CRISTAL → LUZ → PMT / SiPM → ELECTRÓNICA → COINCIDENCIA → LOR`")
        st.caption("En PET moderno, los SiPM permiten módulos compactos y una temporización adecuada para sistemas TOF.")

    with p4:
        st.subheader("⏱️ Tiempo muerto: ¿por qué se pierden eventos?")
        st.write(
            "Después de registrar un evento, el detector y la electrónica necesitan un intervalo muy breve para procesarlo. "
            "Durante ese intervalo el sistema puede no estar disponible para registrar otro evento. A eso llamamos **tiempo muerto**."
        )

        st.markdown("### 1️⃣ Miralo evento por evento")
        separacion = st.slider(
            "Separación conceptual entre dos eventos",
            1, 10, 7, 1,
            help="No son unidades reales: sirve para comparar la separación entre eventos con el tiempo de procesamiento."
        )
        tau_demo = 5
        segundo_registrado = separacion >= tau_demo

        x1 = 180
        x2 = 180 + separacion*55
        color2 = "#7ef29a" if segundo_registrado else "#ff4d6d"
        texto2 = "REGISTRADO" if segundo_registrado else "PERDIDO"

        html_dt=f"""
        <div style="background:#0e1720;border:1px solid #29465d;border-radius:18px;padding:12px">
        <svg viewBox="0 0 900 300" width="100%" height="300">
          <text x="450" y="32" fill="white" text-anchor="middle" font-size="22">Línea temporal del detector</text>
          <line x1="90" y1="155" x2="830" y2="155" stroke="#6f8798" stroke-width="4"/>

          <circle cx="{x1}" cy="155" r="15" fill="#7ef29a"/>
          <text x="{x1}" y="125" fill="#7ef29a" text-anchor="middle" font-size="15">Evento 1</text>

          <rect x="{x1+15}" y="137" width="{tau_demo*55}" height="36" rx="8" fill="#ffd166" opacity=".30"/>
          <text x="{x1+15+(tau_demo*55)/2}" y="205" fill="#ffd166" text-anchor="middle" font-size="14">
            sistema ocupado · tiempo muerto
          </text>

          <circle cx="{x2}" cy="155" r="15" fill="{color2}"/>
          <text x="{x2}" y="125" fill="{color2}" text-anchor="middle" font-size="15">Evento 2</text>
          <text x="{x2}" y="245" fill="{color2}" text-anchor="middle" font-size="18" font-weight="bold">{texto2}</text>
        </svg></div>
        """
        components.html(html_dt,height=330)

        if segundo_registrado:
            st.success("El segundo evento llega después de que terminó el intervalo de procesamiento → puede registrarse.")
        else:
            st.warning("El segundo evento llega mientras el sistema todavía está ocupado → en este modelo se pierde.")

        st.markdown("### 2️⃣ Ahora aumentá la tasa de eventos")
        tasa = st.slider("Tasa conceptual de eventos que llegan", 10, 100, 35, 5, key="deadtime_rate_v2")
        capacidad = 65
        registrados = min(tasa, capacidad)
        perdidos = max(0, tasa-capacidad)

        c1,c2,c3 = st.columns(3)
        c1.metric("Llegan", tasa)
        c2.metric("Se registran", registrados)
        c3.metric("Se pierden", perdidos)

        st.progress(registrados/100)
        if perdidos == 0:
            st.info("A esta tasa conceptual, los eventos están suficientemente separados para que el sistema los procese.")
        else:
            st.error(
                f"Al aumentar la tasa, los eventos llegan cada vez más juntos. "
                f"En este ejemplo conceptual {perdidos} eventos quedan sin registrar porque el sistema no alcanza a recuperarse."
            )

        st.markdown(
            "**Idea clave:** `más tasa de eventos → menor separación temporal → más probabilidad de que un evento llegue durante el tiempo muerto → pérdidas de cuentas`"
        )
        st.caption(
            "Es una representación cualitativa. El tiempo muerto real depende del conjunto cristal + fotodetector + electrónica + procesamiento; "
            "no se está simulando un modelo clínico paralyzable/no-paralyzable ni valores de un equipo real."
        )

    with p5:
        st.subheader("🧠 Reconstrucción PET: de las coincidencias a la imagen")
        st.write(
            "Seguí el proceso completo: las coincidencias forman LOR, los datos se organizan "
            "y el algoritmo genera una estimación de la distribución del trazador."
        )

        eventos=st.select_slider("Cantidad conceptual de coincidencias acumuladas",
                                 options=[100,500,1000,5000,10000,50000],value=5000)
        metodo_pet=st.radio("Método de reconstrucción PET",
                            ["Retroproyección conceptual","FBP","OSEM (iterativa)"],horizontal=True)
        usar_tof=st.toggle("Agregar información TOF",value=True)

        progreso=min(1.0,math.log10(eventos)/math.log10(50000))
        n_lor=max(5,min(28,int(5+23*progreso)))
        lors=[]
        for k in range(n_lor):
            aa=math.pi*k/n_lor+0.15*math.sin(k*1.7)
            off=22*math.sin(k*2.1)
            x1=165+125*math.cos(aa)-off*math.sin(aa); y1=170+125*math.sin(aa)+off*math.cos(aa)
            x2=165-125*math.cos(aa)-off*math.sin(aa); y2=170-125*math.sin(aa)+off*math.cos(aa)
            lors.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#ffd166" stroke-width="1.8" opacity=".42"/>')
            if usar_tof:
                mx=(x1+x2)/2+22*math.sin(k); my=(y1+y2)/2+16*math.cos(k*1.3)
                lors.append(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="3.5" fill="#7ef29a" opacity=".78"/>')
        lors_svg="".join(lors)

        # Parámetros visuales de la imagen final.
        if metodo_pet=="Retroproyección conceptual":
            blur_final=7.0; streak=.42; proceso="Retroproyectar las LOR"
            etapa_texto="Las LOR se distribuyen sobre la matriz; aparece borroneo y artefactos."
        elif metodo_pet=="FBP":
            filtro=st.slider("Frecuencia de corte conceptual PET",20,100,65,5,key="pet_fbp_cut")
            blur_final=max(1.3,5.5-filtro/24); streak=.15
            proceso="Filtrar los datos → retroproyectar"
            etapa_texto="Primero se filtran los datos para controlar el borroneo y luego se retroproyectan."
        else:
            it=st.slider("Iteración conceptual OSEM",1,10,5,key="pet_iter_v2")
            blur_final=max(.8,6.0-.5*it); streak=max(.03,.30-.025*it)
            proceso=f"OSEM: estimar → comparar → corregir · iteración {it}"
            etapa_texto="OSEM (Ordered Subsets Expectation Maximization) es una reconstrucción iterativa: divide los datos en subconjuntos ordenados y actualiza sucesivamente la estimación de la imagen."

        # El resultado final se representa sin rayos radiales artificiales.
        # Los artefactos se explican en el panel del proceso, no se dibujan como una estrella sobre la imagen.
        streak_svg=""

        # El panel central cambia según el algoritmo para mostrar ANTES → DURANTE → DESPUÉS.
        if metodo_pet=="Retroproyección conceptual":
            pasos=f"""
            <text x="610" y="92" fill="#c9d6df" text-anchor="middle" font-size="14">ANTES</text>
            <g opacity=".65"><line x1="555" y1="135" x2="665" y2="185" stroke="#ffd166" stroke-width="3"/>
            <line x1="555" y1="185" x2="665" y2="135" stroke="#ffd166" stroke-width="3"/>
            <line x1="610" y1="115" x2="610" y2="205" stroke="#ffd166" stroke-width="3"/></g>
            <text x="610" y="232" fill="#8bd3ff" text-anchor="middle" font-size="13">LOR</text>
            <text x="735" y="165" fill="white" text-anchor="middle" font-size="30">→</text>
            <text x="850" y="92" fill="#c9d6df" text-anchor="middle" font-size="14">DURANTE</text>
            <g opacity=".55"><ellipse cx="850" cy="160" rx="60" ry="68" fill="#245f9e"/>
            <line x1="790" y1="115" x2="910" y2="205" stroke="#d66cff" stroke-width="3"/>
            <line x1="790" y1="205" x2="910" y2="115" stroke="#d66cff" stroke-width="3"/></g>
            <text x="850" y="245" fill="#ffd166" text-anchor="middle" font-size="13">superposición</text>
            """
        elif metodo_pet=="FBP":
            pasos=f"""
            <text x="610" y="92" fill="#c9d6df" text-anchor="middle" font-size="14">ANTES</text>
            <path d="M555 190 C580 105,620 105,665 190" fill="none" stroke="#ddd" stroke-width="8"/>
            <text x="610" y="232" fill="#8bd3ff" text-anchor="middle" font-size="13">datos</text>
            <text x="735" y="165" fill="white" text-anchor="middle" font-size="30">→</text>
            <text x="850" y="92" fill="#c9d6df" text-anchor="middle" font-size="14">DURANTE</text>
            <path d="M795 190 L815 150 L835 180 L855 115 L875 180 L895 150 L915 190" fill="none" stroke="#7ef29a" stroke-width="5"/>
            <text x="855" y="232" fill="#7ef29a" text-anchor="middle" font-size="13">filtrado</text>
            """
        else:
            # Tres mini-imágenes que se hacen progresivamente más definidas.
            b1=7.0; b2=max(3.0,7.0-it*.35); b3=blur_final
            pasos=f"""
            <text x="585" y="82" fill="#c9d6df" text-anchor="middle" font-size="13">ESTIMACIÓN INICIAL</text>
            <g filter="url(#ib1)"><ellipse cx="585" cy="155" rx="48" ry="55" fill="#235f9e"/><circle cx="602" cy="165" r="17" fill="#ff9f1c"/></g>
            <text x="690" y="160" fill="white" text-anchor="middle" font-size="28">→</text>
            <text x="780" y="82" fill="#c9d6df" text-anchor="middle" font-size="13">COMPARAR</text>
            <g filter="url(#ib2)"><ellipse cx="780" cy="155" rx="48" ry="55" fill="#235f9e"/><circle cx="797" cy="165" r="16" fill="#ff9f1c"/><circle cx="762" cy="145" r="11" fill="#35c4b8"/></g>
            <text x="875" y="160" fill="white" text-anchor="middle" font-size="28">→</text>
            <text x="950" y="82" fill="#c9d6df" text-anchor="middle" font-size="13">CORREGIR</text>
            <g filter="url(#ib3)"><ellipse cx="950" cy="155" rx="48" ry="55" fill="#235f9e"/><circle cx="967" cy="165" r="15" fill="#ff3b30"/><circle cx="932" cy="145" r="11" fill="#35c4b8"/></g>
            <path d="M950 225 C900 270,650 270,585 225" fill="none" stroke="#ffd166" stroke-width="2.5" stroke-dasharray="7 5"/>
            <text x="770" y="282" fill="#ffd166" text-anchor="middle" font-size="13">repetir → nueva estimación</text>
            """

        html=f"""
        <div style="background:#0e1720;border:1px solid #29465d;border-radius:20px;padding:12px">
        <svg viewBox="0 0 1160 430" width="100%" height="430">
          <defs>
            <filter id="pf"><feGaussianBlur stdDeviation="{blur_final:.2f}"/></filter>
            <filter id="ib1"><feGaussianBlur stdDeviation="7"/></filter>
            <filter id="ib2"><feGaussianBlur stdDeviation="{max(2.5,blur_final+2):.2f}"/></filter>
            <filter id="ib3"><feGaussianBlur stdDeviation="{blur_final:.2f}"/></filter>
          </defs>

          <text x="165" y="28" fill="white" text-anchor="middle" font-size="20" font-weight="bold">1 · Coincidencias / LOR</text>
          <text x="430" y="28" fill="white" text-anchor="middle" font-size="20" font-weight="bold">2 · Datos</text>
          <text x="775" y="28" fill="white" text-anchor="middle" font-size="20" font-weight="bold">3 · Qué hace el algoritmo</text>
          <text x="1040" y="28" fill="white" text-anchor="middle" font-size="20" font-weight="bold">4 · Resultado</text>

          <rect x="20" y="48" width="290" height="280" rx="15" fill="#071019" stroke="#29465d"/>
          <circle cx="165" cy="170" r="125" fill="none" stroke="#29485d" stroke-width="16"/>
          <ellipse cx="165" cy="170" rx="62" ry="82" fill="#243746"/>{lors_svg}
          <text x="165" y="350" fill="#8bd3ff" text-anchor="middle" font-size="13">{"TOF agrega localización sobre la LOR" if usar_tof else "cada coincidencia aporta una LOR"}</text>

          <rect x="330" y="48" width="200" height="280" rx="15" fill="#071019" stroke="#29465d"/>
          <path d="M350 265 C375 90,420 90,510 260" fill="none" stroke="#eee" stroke-width="10" opacity=".78"/>
          <path d="M350 105 C400 270,455 255,510 105" fill="none" stroke="#999" stroke-width="7" opacity=".6"/>
          <text x="430" y="350" fill="#8bd3ff" text-anchor="middle" font-size="13">{eventos:,} coincidencias</text>

          <rect x="545" y="48" width="440" height="280" rx="15" fill="#071019" stroke="#29465d"/>
          {pasos}

          <rect x="1000" y="48" width="145" height="280" rx="15" fill="#020508" stroke="#29465d"/>
          {streak_svg}
          <g filter="url(#pf)" opacity="{0.45+0.55*progreso:.2f}">
            <ellipse cx="1072" cy="170" rx="55" ry="67" fill="#4b1677"/>
            <ellipse cx="1072" cy="170" rx="46" ry="57" fill="#1769aa"/>
            <ellipse cx="1055" cy="160" rx="17" ry="24" fill="#35c4b8"/>
            <ellipse cx="1093" cy="180" rx="20" ry="27" fill="#ff9f1c"/>
            <ellipse cx="1093" cy="180" rx="10" ry="15" fill="#ff3b30"/>
          </g>
          <text x="1072" y="350" fill="#ffd166" text-anchor="middle" font-size="12">imagen reconstruida</text>

          <text x="580" y="402" fill="#8bd3ff" text-anchor="middle" font-size="16">
            COINCIDENCIAS → DATOS → {proceso} → NUEVA ESTIMACIÓN / IMAGEN
          </text>
        </svg></div>"""
        components.html(html,height=465)
        st.info(etapa_texto)

        if metodo_pet=="OSEM (iterativa)":
            st.markdown(
                "**OSEM = Ordered Subsets Expectation Maximization.** Es una variante acelerada de MLEM. "
                "Divide los datos adquiridos en subconjuntos (*subsets*) y actualiza la estimación con cada subconjunto: "
                "**estimación → proyección calculada → comparación con los datos medidos → corrección → nueva estimación**."
            )
            st.info(
                "📌 **La nomenclatura no cambia por ser PET o SPECT:** FBP, MLEM y OSEM se utilizan en ambas modalidades. "
                "Lo que cambia es el modelo de adquisición y las correcciones que el algoritmo incorpora."
            )

        st.markdown("#### PET + CT: anatomía + función")
        fusion=st.slider("Fusión conceptual CT ↔ PET",0,100,50,key="fusion_pet_v2")
        c1,c2=st.columns(2)
        c1.info("**CT:** referencia anatómica.")
        c2.success("**PET:** distribución funcional/metabólica del trazador.")
        st.progress(fusion/100)
        st.caption("Representación didáctica. TOF aporta información temporal para localizar mejor el evento a lo largo de la LOR; no reemplaza la reconstrucción.")

    with p6:
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

