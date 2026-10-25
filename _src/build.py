#!/usr/bin/env python3
"""Build the MiniatureNestStudio site from _src/source.html.

source.html is the single-page master (both languages, inline CSS/JS/images).
This script splits it into separate English and Spanish pages, moves CSS, JS
and images into /assets, and writes sitemap.xml and 404.html.
Run from the repo root:  python3 _src/build.py
(_src/ starts with an underscore, so GitHub Pages does not publish it.)
"""
import base64, hashlib, os, re, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://miniatureneststudio.com"
GOAT = "https://miniatureneststudio.goatcounter.com/count"
src = open(os.path.join(ROOT, "_src", "source.html"), encoding="utf-8").read()

# ---------- pull CSS, JS and body blocks out of the master ----------
styles = re.findall(r"<style>(.*?)</style>", src, re.S)
css = "\n".join(styles)
js = re.search(r"<script>(.*)</script>", src, re.S).group(1)
body = src[src.index("<body>") + 6: src.index("<script>")]

def block(start, end):
    a = body.index(start); b = body.index(end, a)
    return body[a:b].rstrip() + "\n"

BLOCKS = {
    "hero": block("<!-- ================= HERO", "<div class=\"trim trim-pink\""),
    "start": block("<!-- ================= START HERE", "<!-- ================= GALLERY"),
    "gallery": block("<!-- ================= GALLERY", "<!-- ================= SCALE"),
    "scale": block("<!-- ================= SCALE", "<!-- ================= PRINTABLES"),
    "printables": block("<!-- ================= PRINTABLES", "<!-- ================= ROOM BOX"),
    "roombox": block("<!-- ================= ROOM BOX", "<!-- ================= PUERTO RICO"),
    "puertorico": block("<!-- ================= PUERTO RICO", "<!-- ================= WHICH SCALE"),
    "which": block("<!-- ================= WHICH SCALE", "<!-- ================= SCALE RULER"),
    "ruler": block("<!-- ================= SCALE RULER", "<!-- ================= GLUE GUIDE"),
    "glue": block("<!-- ================= GLUE GUIDE", "<!-- ================= FAQ"),
    "faq": block("<!-- ================= FAQ", "<!-- ================= COLMADO BUILD"),
    "colmado": block("<!-- ================= COLMADO BUILD", "<!-- ================= SHOP"),
    "shop": block("<!-- ================= SHOP", "<!-- ================= ABOUT"),
    "about": block("<!-- ================= ABOUT", "<div class=\"trim trim-yellow\""),
}

# ---------- move every embedded image into /assets/img ----------
os.makedirs(os.path.join(ROOT, "assets", "img"), exist_ok=True)
EXT = {"jpeg": "jpg", "png": "png", "svg+xml": "svg"}
def externalize(text):
    def rep(m):
        kind, b64, data = m.group(1), m.group(2), m.group(3)
        raw = base64.b64decode(data) if b64 else urllib.parse.unquote(data).encode()
        name = hashlib.sha1(raw).hexdigest()[:12] + "." + EXT[kind]
        path = os.path.join(ROOT, "assets", "img", name)
        if not os.path.exists(path):
            open(path, "wb").write(raw)
        return "/assets/img/" + name
    return re.sub(r"data:image/(jpeg|png|svg\+xml)(;base64)?,([^\"')\s]+)", rep, text)

css = externalize(css)
js = externalize(js)
BLOCKS = {k: externalize(v) for k, v in BLOCKS.items()}

css += """
/* ---------- multi-page additions ---------- */
.lang a { font: 600 var(--s-xs)/1 var(--f-mono); letter-spacing: .06em; text-decoration: none; color: var(--on-mat-muted); padding: .45rem .7rem; border-radius: 999px; }
.lang a[aria-current="true"] { background: var(--brass); color: var(--on-brass); }
.nav a[aria-current="page"] { color: var(--on-mat); background: rgba(255,255,255,.12); }
.plaque h1 { font-family: var(--f-display); font-weight: 400; font-size: clamp(1.35rem, 3.6vw, 2.25rem); line-height: 1.1; margin: 0; }
.explore { padding-block: clamp(2.5rem, 6vw, 4rem); }
.explore h2 { font-family: var(--f-display); font-weight: 400; font-size: clamp(1.8rem, 4vw, 2.4rem); line-height: 1.1; }
.ex-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1rem; margin-top: 1.4rem; }
@media (max-width: 900px) { .ex-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (max-width: 560px) { .ex-grid { grid-template-columns: minmax(0, 1fr); } }
.ex-card { display: grid; gap: .35rem; align-content: start; text-decoration: none; color: var(--fg); background: var(--surface); border: 1px solid var(--line); border-top: 4px solid var(--mat); border-radius: 12px; padding: 1.1rem 1.2rem 1.2rem; }
.ex-card:hover { border-color: var(--mark); }
.ex-card h3 { font-size: 1.1rem; }
.ex-card p { color: var(--muted); font-size: var(--s-sm); }
.ex-card span.go { color: var(--mark); font-weight: 600; font-size: var(--s-sm); margin-top: .3rem; }
.pager { display: flex; justify-content: flex-end; margin-top: 2.4rem; }
.pager a { text-decoration: none; font-weight: 600; color: var(--mark); border: 1px solid var(--line); background: var(--surface); padding: .7rem 1.1rem; border-radius: 999px; }
.pager a:hover { border-color: var(--mark); }
.notfound { padding-block: clamp(3rem, 8vw, 6rem); display: grid; gap: 1rem; justify-items: start; }
footer .wrap.foot-nav { display: block; padding-top: 0; padding-bottom: 2rem; }
.foot-nav { font-size: var(--s-sm); color: var(--on-mat-muted); line-height: 2; }
.foot-nav a { color: var(--on-mat-muted); text-decoration: none; white-space: nowrap; }
.foot-nav a:hover { color: var(--on-mat); text-decoration: underline; }
.ex-h2 { margin-top: 2.6rem; }
.ex-grid4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }
@media (max-width: 900px) { .ex-grid4 { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (max-width: 560px) { .ex-grid4 { grid-template-columns: minmax(0, 1fr); } }
.ex-tool { border-top-color: var(--brass); background: var(--tint); }
.notfound h1 { font-family: var(--f-display); font-weight: 400; font-size: clamp(2rem, 5vw, 3rem); }
"""

# ---------- make the shared script work on any page ----------
JS_FIX = [
    ('var lang = "en";\n  try { var saved = localStorage.getItem("mns-lang"); if (saved === "es" || saved === "en") lang = saved; } catch (e) {}',
     'var lang = root.getAttribute("data-lang") || "en";'),
    ('    document.getElementById("lang-en").setAttribute("aria-pressed", String(l === "en"));\n    document.getElementById("lang-es").setAttribute("aria-pressed", String(l === "es"));\n    try { localStorage.setItem("mns-lang", l); } catch (e) {}\n',
     ''),
    ('  function convert() {\n', '  function convert() {\n    if (!val) return;\n'),
    ('  val.addEventListener("input", convert);', '  if (val) {\n  val.addEventListener("input", convert);'),
    ('  document.getElementById("conv").addEventListener("submit", function (e) { e.preventDefault(); });',
     '  document.getElementById("conv").addEventListener("submit", function (e) { e.preventDefault(); });\n  }'),
]
for a, b in JS_FIX:
    assert js.count(a) == 1, a[:60]
    js = js.replace(a, b)

os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
open(os.path.join(ROOT, "assets", "site.css"), "w", encoding="utf-8").write(css)
open(os.path.join(ROOT, "assets", "site.js"), "w", encoding="utf-8").write(js)
# version stamps so browsers fetch new CSS/JS right after each update
CSS_V = hashlib.sha1(css.encode()).hexdigest()[:8]
JS_V = hashlib.sha1(js.encode()).hexdigest()[:8]

# ---------- pages ----------
PAGES = [  # key, en path, es path, blocks, nav en, nav es, title en, title es, desc en, desc es, card en, card es
    ("home", "/", "/es/", ["hero", "trim", "explore", "gallery"], "", "",
     "MiniatureNestStudio · Dollhouse miniature tips & guides", "MiniatureNestStudio · Consejos y guías para miniaturas",
     "Free tips and tools for 1:6, 1:12 and 1:24 dollhouse rooms, in English and Spanish: scale converter, wallpaper planner, printables how-to and a Puerto Rican house guide.",
     "Consejos y herramientas gratis para cuartos de casas de muñecas en 1:6, 1:12 y 1:24, en español e inglés: convertidor de escala, planificador de papel tapiz, imprimibles y guía de la casa puertorriqueña.",
     "", ""),
    ("start", "/start-here/", "/es/empieza-aqui/", ["start"], "Start here", "Empieza aquí",
     "Start Here: Beginner's Guide to Dollhouse Miniatures", "Empieza aquí: guía para principiantes de miniaturas",
     "A starter tool checklist, your first four projects in order, beginner mistakes to skip and an English–Spanish miniature glossary.",
     "Lista de herramientas para empezar, tus primeros cuatro proyectos en orden, errores de principiante y un glosario de miniaturas en inglés y español.",
     "Tools to gather, your first projects and a bilingual glossary", "Herramientas, primeros proyectos y un glosario bilingüe"),
    ("scale", "/scale/", "/es/escala/", ["scale"], "Scale", "Escala",
     "Dollhouse Scale Converter: 1:6, 1:12, 1:24 and 1:48", "Convertidor de escala para casas de muñecas: 1:6, 1:12, 1:24 y 1:48",
     "Convert real sizes to dollhouse scale, see everyday furniture sizes at 1:6, 1:12 and 1:24, and learn to check a piece's scale before you buy.",
     "Convierte medidas reales a escala de casa de muñecas, mira medidas comunes de muebles en 1:6, 1:12 y 1:24 y aprende a revisar la escala antes de comprar.",
     "Scale converter and everyday sizes from 1:6 to 1:48", "Convertidor de escala y medidas comunes de 1:6 a 1:48"),
    ("printables", "/printables/", "/es/imprimibles/", ["printables"], "Printables", "Imprimibles",
     "How to Print, Cut and Assemble Dollhouse Printables", "Cómo imprimir, cortar y armar imprimibles de miniaturas",
     "Seven steps from PDF to finished piece: printing at 100%, paper weights, cutting, scoring, edge coloring and gluing, with how-it's-made photos.",
     "Siete pasos del PDF a la pieza terminada: imprimir al 100%, gramaje del papel, cortar, marcar, colorear bordes y pegar, con fotos del proceso.",
     "Print, cut, fold and glue paper pieces so they fit", "Imprime, corta, dobla y pega piezas que encajen"),
    ("roombox", "/room-boxes/", "/es/roombox/", ["roombox"], "Room boxes", "Roombox",
     "How to Build a Room Box + Dollhouse Wallpaper Planner", "Cómo construir un roombox + planificador de papel tapiz",
     "The right build order for a miniature room box, and a free planner that works out how many wallpaper sheets you need and where every seam lands.",
     "El orden correcto para construir un roombox en miniatura y un planificador gratis que calcula cuántas hojas de papel tapiz necesitas y dónde cae cada unión.",
     "Build order, wall details and the wallpaper planner", "Orden de construcción, detalles de pared y el planificador de papel tapiz"),
    ("puertorico", "/puerto-rican-house/", "/es/casa-puertorriquena/", ["puertorico"], "Puerto Rico", "Puerto Rico",
     "The Puerto Rican House in Miniature", "La casa puertorriqueña en miniatura",
     "Zinc roofs, rejas, ventanas Miami and the details of the Puerto Rican cocina, sala, balcón and colmado, with measurements at 1:6, 1:12 and 1:24.",
     "Techos de zinc, rejas, ventanas Miami y los detalles de la cocina, sala, balcón y colmado puertorriqueños, con medidas en 1:6, 1:12 y 1:24.",
     "Zinc roofs, rejas and the rooms of a Puerto Rican home", "Techos de zinc, rejas y los cuartos de una casa boricua"),
    ("which", "/which-scale/", "/es/que-escala/", ["which"], "Which scale?", "¿Qué escala?",
     "Which Dollhouse Scale Should I Start With? (Quiz)", "¿Con qué escala de casa de muñecas empiezo? (Prueba)",
     "Answer four quick questions and get a suggested miniature scale (1:6, 1:12 or 1:24), with the size of a typical room at that scale.",
     "Contesta cuatro preguntas rápidas y te sugerimos una escala de miniaturas (1:6, 1:12 o 1:24), con el tamaño de un cuarto típico en esa escala.",
     "A 4-question quiz to pick your first scale", "Una prueba de 4 preguntas para escoger tu escala"),
    ("ruler", "/scale-ruler/", "/es/regla-de-escala/", ["ruler"], "Scale ruler", "Regla de escala",
     "Free Printable Miniature Scale Ruler (1:6, 1:12, 1:24, 1:48)", "Regla de escala imprimible gratis (1:6, 1:12, 1:24, 1:48)",
     "A free one-page PDF with dollhouse scale rulers in feet and metres. Hold it up to any piece and read its real-life size. US Letter and A4.",
     "Un PDF gratis de una página con reglas de escala en pies y metros. Ponla al lado de cualquier pieza y lee su tamaño real. Tamaño carta y A4.",
     "Free printable PDF: read any piece's real size", "PDF gratis: lee el tamaño real de cualquier pieza"),
    ("glue", "/glue-guide/", "/es/guia-de-pegamentos/", ["glue"], "Glue guide", "Guía de pegamentos",
     "Which Glue for Miniatures? Glue Guide for Dollhouse Building", "¿Qué pegamento usar en miniaturas? Guía de pegamentos",
     "Which glue to use for paper, wallpaper, wood, fabric, plastic, metal and foam in dollhouse miniatures, what to avoid, and how long each takes to hold.",
     "Qué pegamento usar para papel, papel tapiz, madera, tela, plástico, metal y foam en miniaturas, qué evitar y cuánto tarda cada uno.",
     "Which glue for paper, wood, fabric, plastic and foam", "Qué pegamento para papel, madera, tela, plástico y foam"),
    ("faq", "/faq/", "/es/preguntas/", ["faq"], "FAQ", "Preguntas",
     "Dollhouse Miniatures FAQ for Beginners", "Preguntas frecuentes de miniaturas para principiantes",
     "Short answers to beginner questions about dollhouse miniatures: cost, scale, where to buy, mixing scales, lighting without wiring and fixing wallpaper.",
     "Respuestas cortas a preguntas de principiantes: costo, escala, dónde comprar, mezclar escalas, luces sin cables y cómo arreglar el papel tapiz.",
     "Questions beginners ask, answered", "Respuestas a preguntas de principiantes"),
    ("colmado", "/colmado-build/", "/es/diario-colmado/", ["colmado"], "Colmado build", "Diario del colmado",
     "Colmado Doña Carmen: a 1:12 Puerto Rican Corner Store Build Diary", "Colmado Doña Carmen: diario de construcción de un colmado 1:12",
     "Step-by-step photos of a 1:12 Puerto Rican colmado room box: printed paper groceries, shelf strips for tiny bottles, rolled cans and a Christmas storefront.",
     "Fotos paso a paso de un colmado puertorriqueño en roombox 1:12: compra de papel impresa, tiras de botellas, latas enrolladas y una fachada navideña.",
     "A 1:12 corner store, step by step", "Un colmado 1:12, paso a paso"),
    ("shop", "/shop/", "/es/tienda/", ["shop"], "Shop", "Tienda",
     "Shop: Printable Dollhouse Room Planners · MiniatureNestStudio", "Tienda: planificadores imprimibles para casas de muñecas · MiniatureNestStudio",
     "Printable PDF room planners for 1:6, 1:12 and 1:24 dollhouse rooms, plus a 1:24 kitchen planner. Undated, GoodNotes-friendly, instant download.",
     "Planificadores de cuartos en PDF para casas de muñecas en 1:6, 1:12 y 1:24, más un planificador de cocina 1:24. Sin fechas, para GoodNotes, descarga inmediata.",
     "Printable room planners for 1:6, 1:12 and 1:24", "Planificadores imprimibles para 1:6, 1:12 y 1:24"),
    ("about", "/about/", "/es/sobre-mi/", ["about"], "About", "Sobre mí",
     "About Janice · MiniatureNestStudio", "Sobre mí · MiniatureNestStudio",
     "Meet Janice, the Puerto Rican maker behind MiniatureNestStudio's dollhouse planners and guides.",
     "Conoce a Janice, la creadora puertorriqueña detrás de los planificadores y guías de MiniatureNestStudio.",
     "Meet Janice, the maker behind the shop", "Conoce a Janice, la creadora detrás de la tienda"),
]
P = {p[0]: p for p in PAGES}
SECTIONS = [p for p in PAGES if p[0] != "home"]
NAV = [P[k] for k in ("start", "scale", "printables", "roombox", "puertorico", "shop", "about")]
TOOLS = [P[k] for k in ("which", "ruler", "glue", "faq")]
ORDER = [P[k] for k in ("start", "which", "scale", "ruler", "printables", "glue", "roombox", "puertorico", "colmado", "faq", "shop", "about")]
L = {"en": 1, "es": 2}

def strip_lang(html, lang):
    other = "es" if lang == "en" else "en"
    html = re.sub(r'<span data-l="%s">.*?</span>' % other, "", html, flags=re.S)
    html = re.sub(r'<span data-l="%s">(.*?)</span>' % lang, r"\1", html, flags=re.S)
    assert "data-l=" not in html
    return html

def explore(lang):
    i = 10 if lang == "en" else 11
    cards = "".join(
        f'<a class="ex-card" href="{p[L[lang]]}"><h3>{p[4] if lang == "en" else p[5]}</h3><p>{p[i]}</p>'
        f'<span class="go">{"Read" if lang == "en" else "Ver"} →</span></a>' for p in NAV)
    tools = "".join(
        f'<a class="ex-card ex-tool" href="{p[L[lang]]}"><h3>{p[4] if lang == "en" else p[5]}</h3><p>{p[i]}</p>'
        f'<span class="go">{"Open" if lang == "en" else "Abrir"} →</span></a>' for p in TOOLS)
    head = "Explore the guides" if lang == "en" else "Explora las guías"
    head2 = "Beginner toolkit" if lang == "en" else "Herramientas para principiantes"
    return (f'<section class="explore"><div class="wrap"><h2>{head}</h2><div class="ex-grid">{cards}</div>'
            f'<h2 class="ex-h2">{head2}</h2><div class="ex-grid ex-grid4">{tools}</div></div></section>\n')

def header(cur, lang):
    links = "".join(
        f'\n      <a href="{p[L[lang]]}"' + (' aria-current="page"' if p[0] == cur else "") + f'>{p[4] if lang == "en" else p[5]}</a>'
        for p in NAV)
    gal = P["home"][L[lang]] + "#gallery"
    links = f'\n      <a href="{gal}">{"Gallery" if lang == "en" else "Galería"}</a>' + links
    pg = P[cur] if cur in P else P["home"]
    en_cur = ' aria-current="true"' if lang == "en" else ""
    es_cur = ' aria-current="true"' if lang == "es" else ""
    return f'''<header class="top" id="top">
  <div class="wrap">
    <a class="brand" href="{P["home"][L[lang]]}">Miniature<b>Nest</b>Studio</a>
    <nav class="nav" aria-label="{"Sections" if lang == "en" else "Secciones"}">{links}
    </nav>
    <div class="lang" role="group" aria-label="Language / Idioma">
      <a id="lang-en" href="{pg[1]}" hreflang="en" lang="en"{en_cur}>EN</a>
      <a id="lang-es" href="{pg[2]}" hreflang="es" lang="es"{es_cur}>ES</a>
    </div>
  </div>
</header>
<div class="ruler" aria-hidden="true" id="ruler"></div>
'''

FOOTER = BLOCKS_FOOT = externalize(body[body.index('<div class="trim trim-yellow"'):])

def pager(cur, lang):
    keys = [p[0] for p in ORDER]
    if cur not in keys: return ""
    i = keys.index(cur)
    if i == len(keys) - 1: return ""
    n = ORDER[i + 1]
    label = ("Next: " if lang == "en" else "Siguiente: ") + (n[4] if lang == "en" else n[5])
    return f'<div class="wrap"><div class="pager"><a href="{n[L[lang]]}">{label} →</a></div></div>\n'

def foot_nav(lang):
    links = " · ".join(f'<a href="{p[L[lang]]}">{p[4] if lang == "en" else p[5]}</a>' for p in ORDER)
    return f'  <div class="wrap foot-nav">{links}</div>\n'

def promote_h1(html):
    return html.replace("<h2>", "<h1>", 1).replace("</h2>", "</h1>", 1)

REDIRECT = '''<script>(function(){var m=%s;var h=location.hash.slice(1);if(m[h])location.replace(m[h]);})();</script>'''

def page(key, lang, content, title, desc, path_en, path_es, noindex=False):
    path = path_en if lang == "en" else path_es
    alt = "" if noindex else f'''<link rel="canonical" href="{SITE}{path}">
<link rel="alternate" hreflang="en" href="{SITE}{path_en}">
<link rel="alternate" hreflang="es" href="{SITE}{path_es}">
<link rel="alternate" hreflang="x-default" href="{SITE}{path_en}">
'''
    robots = '<meta name="robots" content="noindex">\n' if noindex else ""
    html = f'''<!doctype html>
<html lang="{lang}" data-lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}{alt}<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="MiniatureNestStudio">
<meta property="og:locale" content="{"en_US" if lang == "en" else "es_US"}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gloock&family=Figtree:ital,wght@0,400;0,500;0,600;0,700;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="/assets/site.css?v={CSS_V}">
<script data-goatcounter="{GOAT}" async src="//gc.zgo.at/count.js"></script>
</head>
<body>
{header(key, lang)}
{content}
{FOOTER}
<script src="/assets/site.js?v={JS_V}"></script>
</body>
</html>
'''
    html = html.replace("</footer>", foot_nav(lang) + "</footer>", 1)
    html = strip_lang(html, lang)
    html = re.sub(r'href="@@(\w+)"', lambda m: f'href="{P[m.group(1)][L[lang]]}"', html)
    assert "@@" not in html
    html = html.replace('href="#top" data-go="top"', f'href="{P["home"][L[lang]]}"')
    return html.replace("&amp;amp;", "&amp;")

def write(path, html):
    out = os.path.join(ROOT, path.strip("/"), "index.html") if path.endswith("/") else os.path.join(ROOT, path.lstrip("/"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(html)
    return out

written = []
for p in PAGES:
    key = p[0]
    for lang in ("en", "es"):
        parts = []
        for b in p[3]:
            if b == "trim": parts.append('<div class="trim trim-pink" aria-hidden="true"></div>\n')
            elif b == "explore": parts.append(explore(lang))
            else:
                h = BLOCKS[b]
                if key != "home": h = promote_h1(h)
                parts.append(h)
        if key == "home":
            hero_btns = parts[0]
            hero_btns = hero_btns.replace('href="#start" data-go="start"', f'href="{P["start"][L[lang]]}"')
            hero_btns = hero_btns.replace('href="#printables" data-go="printables"', f'href="{P["printables"][L[lang]]}"')
            parts[0] = hero_btns
            m = {k: P[k][L[lang]] for k in ("start", "scale", "printables", "puertorico", "about")}
            m["roombox"] = P["roombox"][L[lang]]
            parts.insert(0, REDIRECT % str(m).replace("'", '"') + "\n")
        parts.append(pager(key, lang))
        title = p[6] if lang == "en" else p[7]
        desc = p[8] if lang == "en" else p[9]
        html = page(key, lang, "".join(parts), title.replace("&", "&amp;"), desc, p[1], p[2])
        written.append(write(p[L[lang]], html))

# 404 page (both languages on one page, not indexed)
nf = '''<section class="notfound"><div class="wrap" style="display:grid;gap:1rem;justify-items:start">
<h1>Page not found · Página no encontrada</h1>
<p>That page doesn't exist anymore. · Esa página ya no existe.</p>
<p><a class="btn solid" href="/">Home</a> <a class="btn solid" href="/es/">Inicio</a></p>
</div></section>
'''
written.append(write("/404.html", page("home", "en", nf, "Page not found · MiniatureNestStudio", "Page not found", "/", "/es/", noindex=True)))

# sitemap with language alternates
urls = []
for p in PAGES:
    for lang in ("en", "es"):
        loc = SITE + p[L[lang]]
        urls.append(f'''  <url>
    <loc>{loc}</loc>
    <xhtml:link rel="alternate" hreflang="en" href="{SITE}{p[1]}"/>
    <xhtml:link rel="alternate" hreflang="es" href="{SITE}{p[2]}"/>
  </url>''')
open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
    + "\n".join(urls) + "\n</urlset>\n")

for w in written:
    print(os.path.relpath(w, ROOT), os.path.getsize(w) // 1024, "KB")
print("assets/site.css", os.path.getsize(os.path.join(ROOT, "assets", "site.css")) // 1024, "KB")
print("images", len(os.listdir(os.path.join(ROOT, "assets", "img"))))
