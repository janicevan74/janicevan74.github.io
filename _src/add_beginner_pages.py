"""One-time script: adds the beginner toolkit pages (scale quiz, scale ruler,
glue guide, FAQ) to _src/source.html. Links written as @@key are turned into
the right English or Spanish page address by build.py."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "_src", "source.html")
s = open(P, encoding="utf-8").read()
assert 'id="which"' not in s

def t(en, es):
    return f'<span data-l="en">{en}</span><span data-l="es">{es}</span>'

SHOP = "https://www.etsy.com/listing/"
def shop_row(items):
    chips = "".join(f'<a class="shop-chip" href="{u}" target="_blank" rel="noopener">{t(en, es)} →</a>' for u, en, es in items)
    return f'    <div class="shop-row"><span class="shop-lab">{t("From the shop", "En la tienda")}</span><div class="shop-chips">{chips}</div></div>\n'

def band(sec, room, kick_en, kick_es, h_en, h_es, base="base"):
    return f'''<section class="part" id="{sec}">
  <div class="room {room}">
    <div class="plaque">
      <p class="kicker">{t(kick_en, kick_es)}</p>
      <h2>{t(h_en, h_es)}</h2>
    </div>
  </div>
  <div class="{base}" aria-hidden="true"></div>
  <div class="wrap">
'''
END = "  </div>\n</section>\n\n"
PLANNERS = "https://www.etsy.com/shop/MiniatureNestStudio?search_query=room+planner"

# ------------------------------------------------------------------ quiz
def q(name, en, es, opts):
    o = "".join(f'''
          <label class="qopt"><input type="radio" name="{name}" value="{v}"><span>{t(a, b)}</span></label>''' for v, a, b in opts)
    return f'''        <fieldset class="qq">
          <legend>{t(en, es)}</legend>{o}
        </fieldset>
'''
def res(scale, title_en, title_es, body_en, body_es, room_en, room_es, extra=""):
    return f'''        <div class="qres" data-res="{scale}" hidden>
          <p class="kicker">{t("Your suggested scale", "Tu escala sugerida")}</p>
          <h3>{t(title_en, title_es)}</h3>
          <p>{t(body_en, body_es)}</p>
          <p class="qroom"><b>{t("A 12 × 12 ft room with an 8 ft ceiling:", "Un cuarto de 12 × 12 pies con techo de 8 pies:")}</b> {t(room_en, room_es)}</p>
          <div class="qbtns">
            <a class="btn solid" href="@@scale">{t("See sizes at this scale", "Ver medidas en esta escala")}</a>
            {extra}
            <a class="btn" href="@@ruler">{t("Free scale ruler", "Regla de escala gratis")}</a>
          </div>
        </div>
'''
planner_btn = f'<a class="btn" href="{PLANNERS}" target="_blank" rel="noopener">{t("Plan it with a room planner", "Planifícalo con un planificador")} →</a>'
quiz = band("which", "room-dining", "Scale quiz", "Prueba de escala", "Which scale should I start with?", "¿Con qué escala empiezo?") + f'''    <div class="part-head">
      <p>{t("Answer four quick questions and get a suggested scale, with the size of a typical room at that scale.",
            "Contesta cuatro preguntas rápidas y te sugerimos una escala, con el tamaño de un cuarto típico en esa escala.")}</p>
    </div>
    <div class="quiz-wrap">
      <form id="quiz" class="quiz" novalidate>
''' + q("q1", "1. What do you want to make first?", "1. ¿Qué quieres hacer primero?", [
        ("12:2,24:1", "A single room box", "Un roombox de un solo cuarto"),
        ("12:2,24:1", "A whole dollhouse", "Una casa de muñecas completa"),
        ("6:4", "A scene for fashion dolls I own", "Una escena para mis muñecas de moda"),
        ("24:3,48:1", "A book nook or a scene for a shelf", "Un book nook o una escena para una repisa")]) \
    + q("q2", "2. How much display space do you have?", "2. ¿Cuánto espacio tienes para exhibirlo?", [
        ("6:2,12:1", "A table or a big shelf", "Una mesa o una repisa grande"),
        ("12:2,24:1", "A regular shelf", "Una repisa normal"),
        ("24:2,48:1", "Very little", "Muy poco")]) \
    + q("q3", "3. How do you feel about tiny details?", "3. ¿Qué tal te llevas con los detalles chiquitos?", [
        ("24:2,48:2", "The tinier the better", "Mientras más chiquito, mejor"),
        ("12:2", "I like detail, but nothing too fiddly", "Me gustan los detalles, pero nada muy minucioso"),
        ("6:2,12:1", "I want pieces that are easy to handle", "Prefiero piezas fáciles de manejar")]) \
    + q("q4", "4. Do you already have any minis or dolls?", "4. ¿Ya tienes miniaturas o muñecas?", [
        ("6:4", "Fashion dolls (about 11–12 in tall)", "Muñecas de moda (unas 11–12 pulg de alto)"),
        ("12:4", "1:12 furniture or a 1:12 kit", "Muebles o un kit en 1:12"),
        ("24:4", "1:24 furniture or a small kit house", "Muebles en 1:24 o una casita en kit"),
        ("12:1", "Nothing yet", "Nada todavía")]) + f'''        <p class="qmsg" id="quiz-msg" hidden>{t("Answer all four questions to see your scale.", "Contesta las cuatro preguntas para ver tu escala.")}</p>
        <div class="qbtns"><button type="submit" class="btn solid" id="quiz-go">{t("Show my scale", "Ver mi escala")}</button>
        <button type="reset" class="btn" id="quiz-reset">{t("Start over", "Empezar de nuevo")}</button></div>
      </form>
      <div class="qout" id="quiz-out" aria-live="polite">
        <div class="qres qwait" data-res="wait">
          <p>{t("Your result will show up here.", "Tu resultado aparecerá aquí.")}</p>
        </div>
''' + res("12", "1:12, one-inch scale", "1:12, escala de una pulgada",
          "The classic dollhouse scale and the easiest place to start. It has the widest choice of furniture, kits and printables, and pieces are small but still easy to handle.",
          "La escala clásica de casas de muñecas y la más fácil para empezar. Tiene la mayor variedad de muebles, kits e imprimibles, y las piezas son pequeñas pero fáciles de manejar.",
          "12 × 12 × 8 in", "12 × 12 × 8 pulg", planner_btn) \
    + res("24", "1:24, half scale", "1:24, media escala",
          "Half the size of 1:12, so it fits on almost any shelf and works well for book nooks and small kit houses. Pieces are tiny, so keep tweezers handy.",
          "La mitad de 1:12, así que cabe en casi cualquier repisa y es ideal para book nooks y casitas en kit. Las piezas son diminutas, así que ten unas pinzas a mano.",
          "6 × 6 × 4 in", "6 × 6 × 4 pulg", planner_btn) \
    + res("6", "1:6, playscale", "1:6, escala de muñecas",
          "The scale of fashion dolls. Rooms are big and pieces are easy to handle, but you'll need more display space.",
          "La escala de las muñecas de moda. Los cuartos son grandes y las piezas fáciles de manejar, pero necesitarás más espacio para exhibir.",
          "24 × 24 × 16 in", "24 × 24 × 16 pulg", planner_btn) \
    + res("48", "1:48, quarter scale", "1:48, escala de un cuarto",
          "Very small and very detailed, often used for a dollhouse inside a dollhouse. Many beginners start in 1:12 or 1:24 and try 1:48 later.",
          "Muy pequeña y muy detallada; se usa a menudo para una casita dentro de otra casa de muñecas. Muchos principiantes empiezan en 1:12 o 1:24 y prueban 1:48 después.",
          "3 × 3 × 2 in", "3 × 3 × 2 pulg") + '''      </div>
    </div>
''' + shop_row([(PLANNERS, "Room planners (1:6, 1:12, 1:24)", "Planificadores de cuartos (1:6, 1:12, 1:24)"),
                (SHOP + "4580590401", "Furniture Scale Guide", "Guía de muebles a escala")]) + END

# ------------------------------------------------------------------ ruler
ruler = band("ruler", "room-kitchen", "Free printable", "Imprimible gratis", "Miniature scale ruler", "Regla de escala para miniaturas") + f'''    <div class="part-head">
      <p>{t("Hold it up to any piece and read its real-life size. Six rulers on one page: 1:6, 1:12, 1:24 and 1:48 in feet, plus 1:12 and 1:24 in metres.",
            "Ponla al lado de cualquier pieza y lee su tamaño en la vida real. Seis reglas en una página: 1:6, 1:12, 1:24 y 1:48 en pies, más 1:12 y 1:24 en metros.")}</p>
    </div>
    <div class="dl-grid">
      <figure class="dl-prev"><img src="/assets/img/ruler-preview.png" width="1210" height="935" alt="Preview of the printable scale ruler page with six rulers" loading="lazy"></figure>
      <div class="dl-card">
        <h3>{t("Download the ruler", "Descarga la regla")}</h3>
        <p>{t("One page, PDF. Free for personal use.", "Una página en PDF. Gratis para uso personal.")}</p>
        <div class="dl-btns">
          <a class="btn solid" href="/downloads/MiniatureNestStudio_Scale_Ruler_Letter.pdf" download>{t("US Letter (PDF)", "Carta (PDF)")}</a>
          <a class="btn solid" href="/downloads/MiniatureNestStudio_Scale_Ruler_A4.pdf" download>A4 (PDF)</a>
        </div>
        <p class="dl-note">{t("Print in landscape at 100% (“Actual size”).", "Imprime en horizontal al 100% (“Tamaño real”).")}</p>
      </div>
    </div>
    <div class="two">
      <div>
        <h3>{t("How to use it", "Cómo usarla")}</h3>
        <ol class="plain-steps">
          <li>{t("Print it at 100%, not “Fit to page.”", "Imprímela al 100%, no en “Ajustar a la página”.")}</li>
          <li>{t("Measure the two squares at the top: they should be exactly 1 in and 2 cm. If not, check your print settings.", "Mide los dos cuadrados de arriba: deben medir exactamente 1 pulg y 2 cm. Si no, revisa la configuración de impresión.")}</li>
          <li>{t("Cut out the rulers on the dashed lines and glue them to cardstock so they stay stiff.", "Recorta las reglas por las líneas punteadas y pégalas en cartulina para que queden firmes.")}</li>
          <li>{t("Line up 0 with the edge of the piece and read the number: that's its size in real life.", "Pon el 0 en el borde de la pieza y lee el número: ese es su tamaño en la vida real.")}</li>
        </ol>
      </div>
      <div class="callout" style="margin-top:0">
        <h3>{t("Try it", "Pruébala")}</h3>
        <ul class="ticks">
          <li>{t("<b>Check a chair.</b> On the 1:12 ruler, a dining chair seat should land near the half-foot mark after 1, about 1½ ft (18 in). Much lower or higher means a different scale.", "<b>Mide una silla.</b> En la regla 1:12, el asiento de una silla de comedor debe quedar cerca de la marca de medio pie después del 1, alrededor de 1½ pies (18 pulg). Si queda muy por debajo o por encima, es de otra escala.")}</li>
          <li>{t("<b>Check doll furniture.</b> On the 1:6 ruler, the top of a dining table for fashion dolls should read about 2½ ft (30 in).", "<b>Revisa muebles de muñecas.</b> En la regla 1:6, el tope de una mesa de comedor para muñecas de moda debe dar unos 2½ pies (30 pulg).")}</li>
          <li>{t("<b>Shop secondhand with confidence.</b> Take the ruler to yard sales and thrift stores to check pieces before you buy.", "<b>Compra de segunda mano con confianza.</b> Lleva la regla a ventas de garaje y tiendas de segunda mano para revisar las piezas antes de comprar.")}</li>
        </ul>
      </div>
    </div>
''' + shop_row([(SHOP + "4580590401", "Furniture Scale Guide (1:6 to 1:48)", "Guía de muebles a escala (1:6 a 1:48)"),
                (SHOP + "4580324948", "Scale Conversion Cheat Sheet", "Hoja rápida de conversión de escalas")]) + END

# ------------------------------------------------------------------ glue
G = [
 ("Paper to paper", "Papel con papel", "labels, boxes, books", "etiquetas, cajitas, libros",
  "Glue stick for flat pieces; tacky glue spread thin for tabs and 3D folds", "Pegamento en barra para piezas planas; pegamento blanco espeso, en capa fina, para pestañas y piezas 3D",
  "Super glue (stains paper and makes it brittle); hot glue (lumpy)", "Super glue (mancha el papel y lo pone quebradizo); silicón caliente (deja grumos)"),
 ("Wallpaper to wood or cardboard", "Papel tapiz en madera o cartón", "", "",
  "Glue stick, spray adhesive or wallpaper paste", "Pegamento en barra, adhesivo en aerosol o pasta para papel tapiz",
  "Watery white glue straight from the bottle (makes paper ripple)", "Pegamento blanco aguado directo del pote (arruga el papel)"),
 ("Wood to wood", "Madera con madera", "", "",
  "Wood glue or tacky glue; hold or clamp it while it sets", "Pegamento para madera o pegamento blanco espeso; aguanta o usa una prensita mientras fragua",
  "Glue stick (won't hold)", "Pegamento en barra (no aguanta)"),
 ("Fabric", "Tela", "curtains, bedding, rugs", "cortinas, ropa de cama, alfombras",
  "Fabric glue or tacky glue, applied thin", "Pegamento para tela o pegamento blanco espeso, en capa fina",
  "Super glue (soaks in and hardens the fabric)", "Super glue (se absorbe y endurece la tela)"),
 ("Hard plastic", "Plástico duro", "model parts, styrene sheet", "piezas de modelismo, láminas de estireno",
  "Plastic cement or super glue", "Cemento para plástico o super glue",
  "White and tacky glue (they peel off smooth plastic)", "Pegamento blanco (se despega del plástico liso)"),
 ("Clear plastic “glass”", "“Cristal” de plástico transparente", "windows, display cases", "ventanas, vitrinas",
  "A clear-drying glue made for clear parts, used sparingly", "Un pegamento transparente hecho para piezas claras, en poca cantidad",
  "Super glue (its fumes can fog clear plastic white)", "Super glue (sus vapores pueden empañar de blanco el plástico)"),
 ("Metal, beads and tiny findings", "Metal, cuentas y piececitas", "", "",
  "Super glue gel or two-part epoxy", "Super glue en gel o epoxi de dos partes",
  "Glue stick or white glue", "Pegamento en barra o blanco"),
 ("Foam board and craft foam", "Foam board y foami", "", "",
  "Tacky glue, white glue or low-temperature hot glue", "Pegamento blanco espeso, pegamento blanco o silicón caliente de baja temperatura",
  "Plastic cement and solvent-based glues (they can melt foam)", "Cemento para plástico y pegamentos con solvente (pueden derretir el foam)"),
 ("Things you may want to move later", "Cosas que quizás muevas después", "", "",
  "Museum putty or museum wax", "Masilla o cera de museo",
  "Any permanent glue", "Cualquier pegamento permanente"),
]
rows = ""
for a, b, c, d, e, f, g, h in G:
    sub = f'<br><small>{t(c, d)}</small>' if c else ""
    rows += f'            <tr><td><b>{t(a, b)}</b>{sub}</td><td>{t(e, f)}</td><td>{t(g, h)}</td></tr>\n'
glue = band("glue", "room-peg", "Glue guide", "Guía de pegamentos", "Which glue for which job", "Qué pegamento usar para cada cosa", base="base base-bench") + f'''    <div class="part-head">
      <p>{t("The right glue keeps a piece clean and makes it last. The wrong one wrinkles paper, fogs clear plastic or melts foam. Find what you're joining and use the glue in the middle column.",
            "El pegamento correcto deja la pieza limpia y hace que dure. El incorrecto arruga el papel, empaña el plástico transparente o derrite el foam. Busca lo que vas a unir y usa el pegamento de la columna del medio.")}</p>
    </div>
    <div class="tbl glue-tbl" style="margin-top:2rem">
      <table>
        <caption>{t("Glue chart", "Tabla de pegamentos")}</caption>
        <thead><tr><th>{t("Joining", "Para unir")}</th><th>{t("Use", "Usa")}</th><th>{t("Avoid", "Evita")}</th></tr></thead>
        <tbody>
{rows}        </tbody>
      </table>
    </div>
    <div class="two">
      <div class="callout" style="margin-top:0">
        <h3>{t("How long until it holds?", "¿Cuánto tarda en pegar?")}</h3>
        <ul class="ticks">
          <li>{t("<b>Glue stick:</b> grabs right away, and you can slide the piece for a minute.", "<b>Pegamento en barra:</b> pega enseguida y puedes mover la pieza por un minuto.")}</li>
          <li>{t("<b>White and tacky glue:</b> sets in about 10 to 30 minutes; full strength in about a day.", "<b>Pegamento blanco:</b> fragua en unos 10 a 30 minutos; aguanta del todo en más o menos un día.")}</li>
          <li>{t("<b>Super glue:</b> grabs in seconds, so get the position right first.", "<b>Super glue:</b> pega en segundos, así que acomoda bien la pieza primero.")}</li>
          <li>{t("<b>Epoxy:</b> depends on the type (5-minute or slow-setting). Always check the label.", "<b>Epoxi:</b> depende del tipo (de 5 minutos o lento). Siempre lee la etiqueta.")}</li>
        </ul>
      </div>
      <div>
        <h3>{t("Tips for clean results", "Trucos para un acabado limpio")}</h3>
        <ul class="ticks">
          <li>{t("<b>Less is more.</b> Spread a thin layer with a toothpick instead of squeezing straight from the bottle.", "<b>Menos es más.</b> Extiende una capa fina con un palillo en vez de echarlo directo del pote.")}</li>
          <li>{t("<b>Test on a scrap</b> of the same material before gluing the real piece.", "<b>Prueba en un pedacito</b> del mismo material antes de pegar la pieza de verdad.")}</li>
          <li>{t("<b>Dry-fit first.</b> Put the pieces together without glue to check that they line up.", "<b>Prueba sin pegamento.</b> Junta las piezas sin pegar para ver que encajan.")}</li>
          <li>{t("<b>Open a window</b> when using super glue, epoxy or spray adhesive, and spray outdoors when you can.", "<b>Abre una ventana</b> cuando uses super glue, epoxi o adhesivo en aerosol, y rocía afuera cuando puedas.")}</li>
          <li>{t("<b>Super glue on your fingers?</b> Acetone nail polish remover loosens it.", "<b>¿Super glue en los dedos?</b> El removedor de esmalte con acetona lo despega.")}</li>
        </ul>
      </div>
    </div>
''' + shop_row([(SHOP + "4582734954", "Materials Reference Pack", "Paquete de referencia de materiales"),
                (SHOP + "4580530286", "Miniature Room Build Journal", "Diario de construcción")]) + END

# ------------------------------------------------------------------ faq
F = [
 ("Do I need to know how to build or draw?", "¿Tengo que saber construir o dibujar?",
  "No. Kits come with step-by-step instructions, and printables only need cutting, folding and gluing. Start with something small and you'll learn as you go. The <a href=\"@@start\">Start here</a> page has a supply list and first projects.",
  "No. Los kits traen instrucciones paso a paso y los imprimibles solo necesitan cortar, doblar y pegar. Empieza con algo pequeño y vas aprendiendo. La página <a href=\"@@start\">Empieza aquí</a> tiene una lista de materiales y primeros proyectos."),
 ("How much does it cost to start?", "¿Cuánto cuesta empezar?",
  "Less than most people think. Scissors, a ruler, a glue stick and printer paper are enough for a first printable project. A craft knife, cutting mat and tacky glue are a small one-time purchase. Kits and furniture range from budget to collector prices, so it helps to set a budget for each project.",
  "Menos de lo que mucha gente cree. Unas tijeras, una regla, pegamento en barra y papel de impresora bastan para un primer proyecto imprimible. Una cuchilla de precisión, una base de corte y pegamento blanco espeso son una compra pequeña que haces una vez. Los kits y muebles van de precios económicos a precios de colección, así que ayuda ponerle un presupuesto a cada proyecto."),
 ("Which scale should I choose?", "¿Qué escala debo escoger?",
  "Most beginners do well in 1:12, the standard dollhouse scale. If you're not sure, take the <a href=\"@@which\">scale quiz</a>.",
  "A la mayoría de los principiantes les va bien en 1:12, la escala estándar de casas de muñecas. Si no estás segura, toma la <a href=\"@@which\">prueba de escala</a>."),
 ("Where do I find furniture and kits?", "¿Dónde consigo muebles y kits?",
  "Craft and hobby stores, online marketplaces like Etsy, and kit makers. Printables let you make your own accessories at home. Always check the scale on a listing, and use the <a href=\"@@ruler\">free scale ruler</a> when you shop in person.",
  "En tiendas de manualidades, mercados en línea como Etsy y con fabricantes de kits. Con imprimibles puedes hacer tus propios accesorios en casa. Siempre revisa la escala en el anuncio y usa la <a href=\"@@ruler\">regla de escala gratis</a> cuando compres en persona."),
 ("Can I mix scales?", "¿Puedo mezclar escalas?",
  "Usually not: a 1:24 chair in a 1:12 room looks like a child's chair. The one exception is forced perspective, where slightly smaller pieces at the back of a scene make it look deeper.",
  "Por lo general no: una silla 1:24 en un cuarto 1:12 parece silla de niño. La excepción es la perspectiva forzada, donde piezas un poco más pequeñas al fondo hacen que la escena se vea más profunda."),
 ("How do I light a room box without wiring?", "¿Cómo ilumino un roombox sin cablear?",
  "Battery LED fairy lights, LED tea lights and small battery LED strips all work. Pick warm white and hide the battery pack behind or under the box. See the <a href=\"@@roombox\">room box guide</a> for where lighting fits in the build order.",
  "Sirven las lucecitas LED de baterías, las velitas LED y las tiras LED pequeñas de baterías. Escoge blanco cálido y esconde las baterías detrás o debajo de la caja. Mira la <a href=\"@@roombox\">guía de roombox</a> para saber cuándo poner la luz."),
 ("My wallpaper bubbled or wrinkled. Can I fix it?", "Mi papel tapiz hizo burbujas o se arrugó. ¿Tiene arreglo?",
  "For a small bubble, prick it with a pin and press it flat with a soft cloth. Wrinkles usually come from too much wet glue; next time use a glue stick or spray adhesive and smooth from the center out. The <a href=\"@@glue\">glue guide</a> has more.",
  "Para una burbuja pequeña, pínchala con un alfiler y aplánala con un paño suave. Las arrugas casi siempre vienen de usar demasiado pegamento húmedo; la próxima vez usa pegamento en barra o adhesivo en aerosol y alisa del centro hacia afuera. La <a href=\"@@glue\">guía de pegamentos</a> tiene más."),
 ("How do I make it look real?", "¿Cómo hago que se vea real?",
  "Keep everything in one scale, use warm light, age new pieces a little with a dry brush, and leave a bit of everyday life around: a cup on the table, an open book, a towel over a chair.",
  "Mantén todo en una sola escala, usa luz cálida, envejece un poco las piezas nuevas con pincel seco y deja un poco de vida diaria: una taza en la mesa, un libro abierto, un paño en una silla."),
 ("How long does a project take?", "¿Cuánto tarda un proyecto?",
  "A printable box takes an evening, a simple room box a weekend or two, and a kit house a few weeks. There's no rush: many miniaturists have a project going for months.",
  "Una cajita imprimible toma una noche, un roombox sencillo uno o dos fines de semana y una casita en kit unas semanas. No hay prisa: muchos miniaturistas tienen un proyecto en marcha por meses."),
]
items = "".join(f'''      <details class="faq-item">
        <summary>{t(a, b)}</summary>
        <p>{t(c, d)}</p>
      </details>
''' for a, b, c, d in F)
faq = band("faq", "room-living", "FAQ", "Preguntas frecuentes", "Questions beginners ask", "Preguntas de principiantes") + f'''    <div class="part-head">
      <p>{t("Short answers to the questions people ask most when they're starting out. Tap a question to open it.",
            "Respuestas cortas a las preguntas más comunes al empezar. Toca una pregunta para abrirla.")}</p>
    </div>
    <div class="faq">
{items}    </div>
''' + shop_row([(SHOP + "4580332681", "Planner Bundle", "Paquete de planificadores"),
                (SHOP + "4580324948", "Scale Conversion Cheat Sheet", "Hoja rápida de conversión de escalas")]) + END

new = ("<!-- ================= WHICH SCALE ================= -->\n" + quiz
       + "<!-- ================= SCALE RULER ================= -->\n" + ruler
       + "<!-- ================= GLUE GUIDE ================= -->\n" + glue
       + "<!-- ================= FAQ ================= -->\n" + faq)
anchor = "<!-- ================= ABOUT ================= -->"
assert s.count(anchor) == 1
s = s.replace(anchor, new + anchor)

# beginner toolkit row on the Start here page
tool = f'''
    <div class="toolkit">
      <h3>{t("Beginner toolkit", "Herramientas para principiantes")}</h3>
      <div class="tk-grid">
        <a class="tk" href="@@which"><b>{t("Which scale?", "¿Qué escala?")}</b><span>{t("Take the 4-question quiz", "Toma la prueba de 4 preguntas")}</span></a>
        <a class="tk" href="@@ruler"><b>{t("Scale ruler", "Regla de escala")}</b><span>{t("Free printable PDF", "PDF imprimible gratis")}</span></a>
        <a class="tk" href="@@glue"><b>{t("Glue guide", "Guía de pegamentos")}</b><span>{t("Which glue for which job", "Qué pegamento para cada cosa")}</span></a>
        <a class="tk" href="@@faq"><b>{t("FAQ", "Preguntas")}</b><span>{t("Questions beginners ask", "Preguntas de principiantes")}</span></a>
      </div>
    </div>
'''
a = '''    </div>

    <div class="sup-head">'''
assert s.count(a) == 1
s = s.replace(a, "    </div>\n" + tool + "\n    <div class=\"sup-head\">")

css = '''
/* ---------- beginner toolkit pages ---------- */
.toolkit { margin-top: 2rem; }
.toolkit h3 { font-family: var(--f-display); font-weight: 400; font-size: clamp(1.4rem, 3vw, 1.8rem); }
.tk-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: .8rem; margin-top: .9rem; }
@media (max-width: 860px) { .tk-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
.tk { display: grid; gap: .2rem; text-decoration: none; color: var(--fg); background: var(--tint); border: 1px solid var(--line); border-radius: 12px; padding: .9rem 1rem; }
.tk:hover { border-color: var(--mark); }
.tk b { font-size: 1.02rem; }
.tk span { font-size: var(--s-sm); color: var(--muted); }
.quiz-wrap { display: grid; grid-template-columns: minmax(0, 1.2fr) minmax(0, 1fr); gap: clamp(1.2rem, 3vw, 2.4rem); margin-top: 2rem; align-items: start; }
@media (max-width: 860px) { .quiz-wrap { grid-template-columns: minmax(0, 1fr); } }
.quiz { display: grid; gap: 1.1rem; }
.qq { border: 1px solid var(--line); border-radius: 12px; padding: 1rem 1.1rem; margin: 0; background: var(--surface); display: grid; gap: .45rem; }
.qq legend { font-weight: 700; padding: 0 .3rem; }
.qopt { display: flex; gap: .6rem; align-items: center; padding: .45rem .6rem; border-radius: 8px; cursor: pointer; }
.qopt:hover { background: var(--tint); }
.qopt input { width: 1.1rem; height: 1.1rem; accent-color: var(--mat); flex: none; }
.qmsg { color: var(--mark); font-weight: 600; }
.qbtns { display: flex; flex-wrap: wrap; gap: .6rem; }
.quiz .btn { color: var(--fg); border-color: var(--line); cursor: pointer; font: inherit; font-weight: 600; background: var(--surface); }
.quiz .btn.solid, .qres .btn.solid, .dl-card .btn.solid { background: var(--mat); color: var(--on-mat); border-color: var(--mat); }
.qres .btn { color: var(--fg); border-color: var(--line); }
.qout { position: sticky; top: 4.5rem; }
.qres { background: var(--surface); border: 1px solid var(--line); border-top: 5px solid var(--mat); border-radius: 12px; padding: 1.3rem; display: grid; gap: .7rem; }
.qres h3 { font-family: var(--f-display); font-weight: 400; font-size: clamp(1.6rem, 3.4vw, 2.1rem); }
.qres .qroom { color: var(--muted); }
.qwait { color: var(--muted); border-top-color: var(--line); }
.dl-grid { display: grid; grid-template-columns: minmax(0, 1.5fr) minmax(0, 1fr); gap: clamp(1.2rem, 3vw, 2.4rem); margin-top: 2rem; align-items: center; }
@media (max-width: 820px) { .dl-grid { grid-template-columns: minmax(0, 1fr); } }
.dl-prev { margin: 0; background: #fff; border: 1px solid var(--line); border-radius: 12px; padding: .6rem; box-shadow: 0 14px 30px -20px rgba(60,20,30,.45); }
.dl-prev img { display: block; width: 100%; height: auto; }
.dl-card { background: var(--tint); border-radius: 14px; padding: 1.4rem; display: grid; gap: .8rem; }
.dl-card h3 { font-family: var(--f-display); font-weight: 400; font-size: 1.7rem; }
.dl-btns { display: flex; flex-wrap: wrap; gap: .6rem; }
.dl-note { font-size: var(--s-sm); color: var(--muted); }
.plain-steps { margin: .9rem 0 0; padding-left: 1.3rem; display: grid; gap: .6rem; }
.glue-tbl td { min-width: 11rem; }
.glue-tbl td small { color: var(--muted); font-size: var(--s-xs); }
.faq { margin-top: 2rem; display: grid; gap: .7rem; max-width: 52rem; }
.faq-item { background: var(--surface); border: 1px solid var(--line); border-radius: 12px; padding: 0 1.1rem; }
.faq-item summary { cursor: pointer; font-weight: 700; padding: 1rem 0; list-style: none; display: flex; justify-content: space-between; gap: 1rem; }
.faq-item summary::-webkit-details-marker { display: none; }
.faq-item summary::after { content: "+"; color: var(--mark); font-weight: 700; }
.faq-item[open] summary::after { content: "−"; }
.faq-item p { padding-bottom: 1rem; color: var(--fg); }
.faq-item a, .callout a { color: var(--mark); }
'''
i = s.rindex("</style>"); s = s[:i] + css + s[i:]

js = r'''
// ---- scale quiz ----
(function () {
  var f = document.getElementById("quiz"); if (!f) return;
  var out = document.getElementById("quiz-out"), msg = document.getElementById("quiz-msg");
  function show(key) {
    out.querySelectorAll("[data-res]").forEach(function (d) { d.hidden = d.getAttribute("data-res") !== key; });
  }
  f.addEventListener("submit", function (e) {
    e.preventDefault();
    var score = { "12": 0, "24": 0, "6": 0, "48": 0 }, answered = 0;
    ["q1", "q2", "q3", "q4"].forEach(function (n) {
      var c = f.querySelector('input[name="' + n + '"]:checked'); if (!c) return;
      answered++;
      c.value.split(",").forEach(function (p) { var kv = p.split(":"); score[kv[0]] += Number(kv[1]); });
    });
    if (answered < 4) { msg.hidden = false; return; }
    msg.hidden = true;
    var best = "12";
    ["12", "24", "6", "48"].forEach(function (k) { if (score[k] > score[best]) best = k; });
    show(best);
    if (window.innerWidth < 860) out.scrollIntoView({ behavior: "smooth", block: "start" });
  });
  f.addEventListener("reset", function () { msg.hidden = true; show("wait"); });
})();
'''
k = s.rindex("</script>"); s = s[:k] + js + s[k:]
open(P, "w", encoding="utf-8").write(s)
print("ok", len(s) // 1024, "KB")
