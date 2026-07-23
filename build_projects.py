import os
import re
base = r'C:/Users/joaqu/capsuladata'
src = os.path.join(base, 'lalinea.html')
with open(src, encoding='utf-8') as f:
    text = f.read()

project_sections = {
    'chile': {
        'title': 'Chile 1958–2026',
        'accent': '#ef4444',
        'accent2': '#f87171',
        'lead': 'Dashboard macroeconómico histórico con fuentes oficiales del Banco Central de Chile e INE.',
        'content': '''<section class="block" id="chile">
<h2 class="section-title">Dashboard Chile 1958–2026</h2>
<p class="section-sub">Datos reales del Banco Central de Chile e INE. Selecciona un indicador, filtra por presidente o rango de años.</p>
<div class="kpi-grid" id="kpiGrid"><div style="grid-column:1/-1;text-align:center;padding:1.5rem;color:var(--muted);font-size:0.8rem">Cargando datos BCCh...</div></div>
<div class="controls" style="margin-bottom:0.3rem">
<span style="font-size:0.65rem;color:var(--muted);margin-right:0.2rem">Indicador:</span><span id="indChips"></span>
</div>
<div class="controls">
<span style="font-size:0.65rem;color:var(--muted)">Fechas:</span>
<input type="number" class="date-input" id="dateFrom" value="1958" min="1958" max="2026">
<span style="color:var(--muted)">–</span>
<input type="number" class="date-input" id="dateTo" value="2026" min="1958" max="2026">
<button class="btn-sm" onclick="applyDateFilter()">Filtrar</button>
<button class="btn-sm outline" id="btnAgg" onclick="toggleAggregation()" title="Agregación anual automática para rangos largos">Auto</button>
</div>
<div class="chart-wrap"><canvas id="mainChart"></canvas></div>
<div class="data-note" id="dataNote"></div>
<div class="prez-bar" id="prezBar"></div>
<div class="prez-label" id="prezLabel"></div>
</section>'''
    },
    'cerezas': {
        'title': 'Exportaciones de cerezas',
        'accent': '#be185d',
        'accent2': '#ec4899',
        'lead': 'Análisis de exportaciones de cerezas frescas chilenas: mercados, precios y estacionalidad.',
        'content': '''<section class="block" id="cerezas">
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
</section>'''
    },
    'bombashormigon': {
        'title': 'Bombas de hormigón',
        'accent': '#ea580c',
        'accent2': '#f97316',
        'lead': 'Metodología para analizar importaciones de repuestos para bombas de hormigón en Chile.',
        'content': '''<section class="block" id="hormigon">
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
</section>'''
    }
}

minimal_nav = '<nav>\n<a href="../index.html">← La Línea</a>\n</nav>'

for name, cfg in project_sections.items():
    t = text
    # Theme
    t = t.replace('--accent:#60a5fa', f'--accent:{cfg["accent"]}')
    t = t.replace('--accent2:#38bdf8', f'--accent2:{cfg["accent2"]}')
    t = t.replace('--chile:#f87171', f'--chile:{cfg["accent"]}')
    t = t.replace('background:linear-gradient(120deg,#60a5fa,#38bdf8)', f'background:linear-gradient(120deg,{cfg["accent"]},{cfg["accent2"]})')
    # Title/hero
    t = t.replace('<title>La Línea — CápsulaData</title>', f'<title>{cfg["title"]} — CápsulaData</title>')
    t = t.replace('<div class="big">La Línea</div>', f'<div class="big">{cfg["title"]}</div>')
    t = t.replace('<p class="lead">Análisis de grandes volúmenes de datos para entender, diagnosticar y predecir la economía. Desde 1958 hasta hoy, con fuentes oficiales.</p>', f'<p class="lead">{cfg["lead"]}</p>')
    # Replace full nav with minimal back-only nav
    nav_start = t.find('<nav>')
    nav_end = t.find('</nav>') + len('</nav>')
    t = t[:nav_start] + minimal_nav + t[nav_end:]
    # Remove proyectos section entirely
    proy_start = t.find('<section class="block" id="proyectos">')
    if proy_start >= 0:
        proy_end = t.find('</section>', proy_start) + len('</section>')
        t = t[:proy_start] + t[proy_end:]
    # Remove mundo section entirely
    mundo_start = t.find('<section class="block" id="mundo">')
    if mundo_start >= 0:
        mundo_end = t.find('</section>', mundo_start) + len('</section>')
        t = t[:mundo_start] + t[mundo_end:]
    # Remove contacto-mini block
    t = t.replace('<div class="contacto-mini">\n<p style="margin-top:1.5rem;font-size:0.9rem">¿Quieres este tipo de análisis para tu empresa o proyecto?</p>\n<a href="https://www.linkedin.com/in/JoaquinAlmendra" target="_blank" rel="noopener" class="btn" style="margin-top:0.8rem;display:inline-block">Conéctemos en LinkedIn</a>\n</div>', '')
    # Replace CTA area with small back button
    cta_start = t.find('<div class="cta">')
    if cta_start >= 0:
        cta_end = t.find('</div>', cta_start) + len('</div>')
        t = t[:cta_start] + '<div class="cta">\n<a href="../index.html" class="btn outline">← Volver a La Línea</a>\n</div>' + t[cta_end:]
    # Insert project content before footer
    footer_idx = t.find('<footer id="contacto">')
    if footer_idx >= 0:
        t = t[:footer_idx] + cfg['content'] + '\n' + t[footer_idx:]
    # Footer title
    t = t.replace('<div class="brand">La Línea</div>', f'<div class="brand">{cfg["title"]}</div>')
    # Fix paths
    t = t.replace('src=".//vendor/chart.umd.min.js"', 'src="../../vendor/chart.umd.min.js"')
    t = t.replace('href="../servicios.html"', 'href="../../servicios.html"')
    t = t.replace('href="../index.html#contacto"', 'href="../../index.html#contacto"')
    t = t.replace('href="../lalinea.html"', 'href="../index.html"')
    t = t.replace("fetch('./data/chile-macro.json')", "fetch('../../data/chile-macro.json')")
    t = t.replace("fetch('./data/world-gdp.json')", "fetch('../../data/world-gdp.json')")
    t = t.replace("fetch('./data/world-pop.json')", "fetch('../../data/world-pop.json')")
    # Remove external project links if present anywhere
    t = t.replace('https://joago99.github.io/la-linea-web/cerezas/', './cerezas/')
    t = t.replace('https://joago99.github.io/la-linea-web/bombas-hormigon/', './bombashormigon/')
    # Ensure back link present
    if '<a href="../index.html"' not in t:
        footer_back = t.find('<footer id="contacto">')
        if footer_back >= 0:
            t = t[:footer_back] + '<div class="cta" style="margin-top:1.5rem"><a href="../index.html" class="btn outline">← Volver a La Línea</a></div>\n' + t[footer_back:]
    d = os.path.join(base, 'lalinea', name)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(t)
    print('wrote', name, len(t))

# Main lalinea.html: keep proyectos section + footer; remove detailed chile/mundo sections
main = text
main = main.replace('<section class="block" id="chile">', '<section class="block" id="chile" style="display:none">')
main = main.replace('<section class="block" id="mundo">', '<section class="block" id="mundo" style="display:none">')
main = main.replace('<div class="contacto-mini">\n<p style="margin-top:1.5rem;font-size:0.9rem">¿Quieres este tipo de análisis para tu empresa o proyecto?</p>\n<a href="https://www.linkedin.com/in/JoaquinAlmendra" target="_blank" rel="noopener" class="btn" style="margin-top:0.8rem;display:inline-block">Conéctemos en LinkedIn</a>\n</div>', '')
with open(src, 'w', encoding='utf-8') as f:
    f.write(main)
print('updated main lalinea.html')
