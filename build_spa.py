#!/usr/bin/env python3
"""
AV Master Course - SPA Assembler
Combines all 5 HTML pages into a single-file SPA.
"""
import re, os

BASE = r'F:\Essentials\Claude Dev\Courses\av-master-course'

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def extract_body(html):
    m = re.search(r'<body[^>]*>(.*)</body>', html, re.DOTALL | re.IGNORECASE)
    return m.group(1).strip() if m else html

def strip_scripts(html):
    return re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)

def strip_links(html):
    return re.sub(r'<link[^>]*>', '', html, flags=re.IGNORECASE)

def scope_root(css, view_id):
    """Replace :root { with #view_id { so CSS variables scope correctly"""
    return re.sub(r':root\s*\{', '#' + view_id + ' {', css)

def strip_google_import(css):
    # Match @import url(...) including URLs that contain semicolons (e.g. wght@300;400;500)
    return re.sub(r"@import\s+url\([^)]+\)\s*;", '', css)

def fix_portal_links(html):
    replacements = [
        ('href="audio-course/#stage7"', "href=\"#\" onclick=\"showView('view-audio'); return false;\""),
        ('href="audio-course/#stage6"', "href=\"#\" onclick=\"showView('view-audio'); return false;\""),
        ('href="matrix-course/#module4"', "href=\"#\" onclick=\"showView('view-matrix'); return false;\""),
        ('href="matrix-course/#module6"', "href=\"#\" onclick=\"showView('view-matrix'); return false;\""),
        ('href="audio-course/"', "href=\"#\" onclick=\"showView('view-audio'); return false;\""),
        ('href="matrix-course/"', "href=\"#\" onclick=\"showView('view-matrix'); return false;\""),
        ('href="led-course/"', "href=\"#\" onclick=\"showView('view-led'); return false;\""),
        ('href="cctv-course/"', "href=\"#\" onclick=\"showView('view-cctv'); return false;\""),
    ]
    for old, new in replacements:
        html = html.replace(old, new)
    return html

def fix_back_link(html):
    html = html.replace('href="../"', "href=\"#\" onclick=\"showView('view-portal'); return false;\"")
    html = html.replace("href='../'", "href='#' onclick=\"showView('view-portal'); return false;\"")
    return html

def prepare_course(html_path):
    html = read_file(html_path)
    body = extract_body(html)
    body = strip_scripts(body)
    body = strip_links(body)
    body = fix_back_link(body)
    return body.strip()

def prepare_css(css_path, view_id):
    css = read_file(css_path)
    css = strip_google_import(css)
    css = scope_root(css, view_id)
    return css

# ── Read & prepare all content ──────────────────────────────────
print("Reading source files...")
audio_content  = prepare_course(f'{BASE}/audio-course/index.html')
matrix_content = prepare_course(f'{BASE}/matrix-course/index.html')
led_content    = prepare_course(f'{BASE}/led-course/index.html')
cctv_content   = prepare_course(f'{BASE}/cctv-course/index.html')

audio_css  = prepare_css(f'{BASE}/audio-course/styles.css',    'view-audio')
matrix_css = prepare_css(f'{BASE}/matrix-course/styles.css',   'view-matrix')
led_css    = prepare_css(f'{BASE}/led-course/styles.css',      'view-led')
cctv_css   = prepare_css(f'{BASE}/cctv-course/css/styles.css', 'view-cctv')

cctv_js = read_file(f'{BASE}/cctv-course/js/script.js')
# Scope CCTV nav-link queries to its own view to avoid cross-course matches
cctv_js = cctv_js.replace(
    "document.querySelectorAll('.nav-link')",
    "document.querySelectorAll('#view-cctv .nav-link')"
)
# Track CCTV current section so SPA router can restore it
cctv_js = cctv_js.replace(
    "localStorage.setItem('cctvCompleted',",
    "localStorage.setItem('av_cctv', sectionId); localStorage.setItem('cctvCompleted',"
)

# ── Portal HTML ─────────────────────────────────────────────────
portal_full = read_file(f'{BASE}/index.html')

portal_style_m = re.search(r'<style>(.*?)</style>', portal_full, re.DOTALL)
portal_style = portal_style_m.group(1) if portal_style_m else ''

portal_body = extract_body(portal_full)
portal_scripts = re.findall(r'<script>(.*?)</script>', portal_body, re.DOTALL)
portal_script = '\n'.join(portal_scripts)
portal_body_clean = re.sub(r'<script>.*?</script>', '', portal_body, flags=re.DOTALL)
portal_body_clean = fix_portal_links(portal_body_clean)

# ── Unified course controller ───────────────────────────────────
CTRL_JS = """
/* ═══════════════════════════════════════════════════════════════
   UNIFIED COURSE CONTROLLER
   Handles navigation for Audio (stages), Matrix (modules), LED
   All queries scoped to each view container — zero ID conflicts
═══════════════════════════════════════════════════════════════ */
function initStageCourse(cfg) {
    var C = document.getElementById(cfg.viewId);
    if (!C) return;
    function $(id) { return C.querySelector('#' + id); }
    function $$(s)  { return C.querySelectorAll(s); }

    function showItem(n) {
        $$('.stage, .module').forEach(function(el) { el.classList.remove('active'); });
        var target = $(cfg.prefix + n);
        if (target) target.classList.add('active');
        $$('.nav-link').forEach(function(l) {
            var num = parseInt(l.dataset.stage || l.dataset.module || 0);
            l.classList.toggle('active', num === n);
        });
        localStorage.setItem(cfg.key, n);
        updateProg(n);
        window.scrollTo(0, 0);
    }

    function updateProg(n) {
        var pct = Math.round(n / cfg.total * 100);
        var bar = $('progressBar');
        var txt = $('progressPct');
        if (bar) bar.style.width = pct + '%';
        if (txt) txt.textContent = pct + '%';
    }

    $$('.nav-link').forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            showItem(parseInt(this.dataset.stage || this.dataset.module || 1));
        });
    });

    document.addEventListener('keydown', function(e) {
        if (!C || C.style.display === 'none') return;
        var n = parseInt(localStorage.getItem(cfg.key) || 1);
        if (e.key === 'ArrowLeft' && n > 1) showItem(n - 1);
        if (e.key === 'ArrowRight' && n < cfg.total) showItem(n + 1);
    });

    showItem(parseInt(localStorage.getItem(cfg.key) || 1));
}

var _inited = {};
var _courseInit = {
    'view-audio':  function() { initStageCourse({viewId:'view-audio',  total:9,  prefix:'stage',   key:'av_audio'}); },
    'view-matrix': function() { initStageCourse({viewId:'view-matrix', total:10, prefix:'module',  key:'av_matrix'}); },
    'view-led':    function() { initStageCourse({viewId:'view-led',    total:13, prefix:'section', key:'av_led'}); },
    'view-cctv':   function() {
        var saved = localStorage.getItem('av_cctv') || 'module1';
        if (typeof loadSection === 'function') loadSection(saved);
    }
};
"""

# ── Router ──────────────────────────────────────────────────────
ROUTER_JS = """
/* ═══════════════════════════════════════════════════════════════
   SPA ROUTER
═══════════════════════════════════════════════════════════════ */
function showView(viewId) {
    document.querySelectorAll('.spa-view').forEach(function(v) {
        v.style.display = 'none';
    });
    var target = document.getElementById(viewId);
    if (!target) return;
    target.style.display = 'block';
    window.scrollTo(0, 0);
    // Init course on first visit
    if (viewId !== 'view-portal' && !_inited[viewId] && _courseInit[viewId]) {
        _inited[viewId] = true;
        setTimeout(function() { _courseInit[viewId](); }, 10);
    }
    history.pushState({}, '', '#' + viewId);
}

// Browser back/forward
window.addEventListener('popstate', function() {
    var hash = (location.hash || '').replace('#', '');
    if (hash && document.getElementById(hash)) showView(hash);
});

// Handle deep-link on load
(function() {
    var hash = (location.hash || '').replace('#', '');
    if (hash && document.getElementById(hash)) showView(hash);
})();
"""

# ── Assemble final SPA ──────────────────────────────────────────
print("Assembling SPA...")

SPA = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AV Master | Professional Audio-Visual &amp; CCTV Training</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Playfair+Display:wght@700;900&display=swap" rel="stylesheet">

    <!-- Portal styles -->
    <style>
{portal_style}
    </style>

    <!-- Audio course styles (accent: #ef4444) -->
    <style>
{audio_css}
    </style>

    <!-- Matrix course styles (accent: #3b82f6) -->
    <style>
{matrix_css}
    </style>

    <!-- LED course styles (accent: #10b981) -->
    <style>
{led_css}
    </style>

    <!-- CCTV course styles (accent: #8b5cf6) -->
    <style>
{cctv_css}
    </style>

    <style>
        /* ── SPA Shell ───────────────────────────────────────── */
        .spa-view {{ display: none; }}
        #view-portal {{ display: block; }}
    </style>
</head>
<body>

<!-- ═══════════════════════════ PORTAL ═══════════════════════════ -->
<div id="view-portal" class="spa-view">
{portal_body_clean}
</div>

<!-- ═══════════════════════ AUDIO COURSE ════════════════════════ -->
<div id="view-audio" class="spa-view">
{audio_content}
</div>

<!-- ══════════════════════ MATRIX COURSE ════════════════════════ -->
<div id="view-matrix" class="spa-view">
{matrix_content}
</div>

<!-- ════════════════════════ LED COURSE ═════════════════════════ -->
<div id="view-led" class="spa-view">
{led_content}
</div>

<!-- ════════════════════════ CCTV COURSE ════════════════════════ -->
<div id="view-cctv" class="spa-view">
{cctv_content}
</div>

<!-- ═══════════════════════════ SCRIPTS ═════════════════════════ -->
<script>
{CTRL_JS}
</script>

<script>
{cctv_js}
</script>

<script>
{ROUTER_JS}
</script>

<script>
{portal_script}
</script>

</body>
</html>"""

out = f'{BASE}/index-spa.html'
write_file(out, SPA)
size = os.path.getsize(out)
print(f"\nDONE: SPA written to index-spa.html")
print(f"Size: {size:,} bytes ({size//1024:,} KB)")
print(f"\nViews assembled:")
print(f"  Portal   : {len(portal_body_clean):,} chars")
print(f"  Audio    : {len(audio_content):,} chars")
print(f"  Matrix   : {len(matrix_content):,} chars")
print(f"  LED      : {len(led_content):,} chars")
print(f"  CCTV     : {len(cctv_content):,} chars")
