import os, re
base = r'C:/Users/joaqu/capsuladata'
src = os.path.join(base, 'lalinea.html')
text = open(src, encoding='utf-8').read()

# Preserve original Chile dashboard block to embed unchanged except paths
chile_match = re.search(r'<!-- CHILE DASHBOARD -->\s*<section class="block" id="chile">.*?</section>\s*\n', text, re.S)
chile_block = chile_match.group(0) if chile_match else ''

def theme_copy(original, title, accent, accent2, project_block, remove_proyectos=True, remove_mundo=True):
    t = original
    # Theme tokens
    t = t.replace('--accent:#60a5fa', f'--accent:{accent}')
    t = t.replace('--accent2:#38bdf8', f'--accent2:{accent2}')
    t = t.replace('--chile:#f87171', f'--chile:{accent}')
    t = t.replace('background:linear-gradient(120deg,#60a5fa,#38bdf8)', f'background:linear-gradient(120deg,{accent},{accent2})')
    # Branding on chart colors
    t = t.replace('#38bdf8', accent2)
    # Title + hero
    t = t.replace('<title>La Línea — CápsulaData</title>', f'<title>{title} — CápsulaData</title>')
    t = t.replace('<div class="big">La Línea</div>', f'<div class="big">{title}</div>')
    t = t.replace('<p class="lead">Análisis de grandes volúmenes de datos para entender, diagnosticar y predecir la economía. Desde 1958 hasta hoy, con fuentes oficiales.</p>', f'<p class="lead">Proyecto activo · datos públicos · fuentes oficiales · documentado y actualizado.</p>')
    # Nav works automatically with ../index.html back link
    # Remove sections
    if remove_proyectos:
        t = re.sub(r'<section class="block" id="proyectos">.*?</section>\s*\n', '', t, flags=re.S)
    if remove_mundo:
        t = re.sub(r'<section class="block" id="mundo">.*?</section>\s*\n', '', t, flags=re.S)
    # Contact mini strip optional
    t = t.replace('<div class="contacto-mini">\n<p style="margin-top:1.5rem;font-size:0.9rem">¿Quieres este tipo de análisis para tu empresa o proyecto?</p>\n<a href="https://www.linkedin.com/in/JoaquinAlmendra" target="_blank" rel="noopener" class="btn" style="margin-top:0.8rem;display:inline-block">Conéctemos en LinkedIn</a>\n</div>', '')
    # Paths: from subfolder /lalinea/<name>/ to root/assets
    t = t.replace('src=".//vendor/chart.umd.min.js"', 'src="../../vendor/chart.umd.min.js"')
    t = t.replace('href="../servicios.html"', 'href="../../servicios.html"')
    t = t.replace('href="../index.html#contacto"', 'href="../../index.html#contacto"')
    t = t.replace('href="../lalinea.html"', 'href="../index.html"')
    t = t.replace("fetch('./data/chile-macro.json')", "fetch('../../data/chile-macro.json')")
    t = t.replace("fetch('./data/world-gdp.json')", "fetch('../../data/world-gdp.json')")
    t = t.replace("fetch('./data/world-pop.json')", "fetch('../../data/world-pop.json')")
    # Insert project-specific section replacing original chile block if present
    if chile_block and '<!-- CHILE DASHBOARD -->' in t:
        t = t.replace(chile_block, project_block + '\n')
    else:
        t = t.replace('\n<footer', '\n' + project_block + '\n<footer')
    # Footer title
    t = t.replace('<div class="brand">La Línea</div>', f'<div class="brand">{title}</div>')
    return t

# Project blocks
chile_block_new = chile_block if chile_block else '<section class="block" id="chile"><h2 class="section-title">Dashboard Chile</h2></section>'

cerezas_block = """<section class="block" id="cerezas">
<h2 class="section-title">Exportaciones de cerezas frescas</h2>
<p class="section-sub">Serie histórica ODEPA · 2005–2026 · valor FOB, volumen, precio por tonelada.</p>
<div class="kpi-grid" id="kpiGrid">
  <div class="kpi-card"><div class="label">Valor FOB última temporada</div><div class="value">USD 3.147 M</div><div class="change">2023/24</div></div>
  <div class="kpi-card"><div class="label">Volumen última temporada</div><div class="value">233,4 kt</div><div class="change">2023/24</div></div>
  <div class="kpi-card"><div class="label">Precio FOB</div><div class="value">USD 13,5 /t</div><div class="change">2023/24</div></div>
  <div class="kpi-card"><div class="label">Destino principal</div><div class="value">China 87%</div><div class="change">valor</div></div>
</div>
<div class="controls"><span style="font-size:0.65rem;color:var(--muted)">Métrica:</span><span id="indChips"></span></div>
<div class="chart-wrap"><canvas id="mainChart"></canvas></div>
<div class="data-note" id="dataNote">Fuente: ODEPA · Matriz Detallada de Comercio Exterior · 2005–2026</div>
</section>"""

hormigon_block = """<section class="block" id="hormigon">
<h2 class="section-title">Bombas de hormigón y repuestos</h2>
<p class="section-sub">Partida 8413.91.00 · Aduana Chile · triangulación Trade Map / INAPI / ProChile.</p>
<div class="kpi-grid" id="kpiGrid">
  <div class="kpi-card"><div class="label">Partida arancelaria</div><div class="value">8413.91.00</div></div>
  <div class="kpi-card"><div class="label">Códigos de importación</div><div class="value">101 · 103 · 120 · 165</div></div>
  <div class="kpi-card"><div class="label">Marcas objetivo</div><div class="value">Putzmeister · Sany · Zoomlion · XCMG</div></div>
  <div class="kpi-card"><div class="label">Filtros semánticos</div><div class="value">W / R / WT</div></div>
</div>
<div class="controls"><span style="font-size:0.65rem;color:var(--muted)">Vista:</span><span id="indChips"></span></div>
<div class="chart-wrap"><canvas id="mainChart"></canvas></div>
<div class="data-note" id="dataNote">Fuente: Aduana Chile · Trade Map · INAPI · ProChile</div>
</section>"""

chile_html = theme_copy(text, 'Chile 1958–2026', '#ef4444', '#f87171', chile_block_new)
cerezas_html = theme_copy(text, 'Exportaciones de cerezas', '#be185d', '#ec4899', cerezas_block)
hormigon_html = theme_copy(text, 'Bombas de hormigón', '#ea580c', '#f97316', hormigon_block)

def write_project(name, html):
    d = os.path.join(base, 'lalinea', name)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    print('wrote', name, len(html))

write_project('chile', chile_html)
write_project('cerezas', cerezas_html)
write_project('bombashormigon', hormigon_html)

# Simplify main lalinea: keep only proyectos + footer
main = text
main = re.sub(r'<section class="block" id="chile">.*?</section>\s*\n', '', main, flags=re.S)
main = re.sub(r'<section class="block" id="mundo">.*?</section>\s*\n', '', main, flags=re.S)
with open(src, 'w', encoding='utf-8') as f:
    f.write(main)
print('updated main lalinea.html')
