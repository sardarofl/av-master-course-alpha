import re, sys
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'F:\Essentials\Claude Dev\Courses\av-master-course'

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

content = read_file(f'{BASE}/index.html')
original_len = len(content)

# ─────────────────────────────────────────────────────────
# Helpers to work within a specific course <style> block
# ─────────────────────────────────────────────────────────
def get_style_block_bounds(html, comment_text):
    """Return (css_start, css_end) byte positions of CSS inside <style>...</style>
    that follows the given HTML comment."""
    marker_pos = html.find(f'<!-- {comment_text}')
    if marker_pos == -1:
        return None, None
    style_open = html.find('<style>', marker_pos)
    style_close = html.find('</style>', style_open)
    if style_open == -1 or style_close == -1:
        return None, None
    return style_open + 7, style_close

def remove_css_property(css, prop_name):
    """Remove a CSS property (e.g. 'display') from a CSS string."""
    return re.sub(r'\s*' + re.escape(prop_name) + r'\s*:[^;]+;', '', css)

course_css_markers = [
    ('MATV & IPTV course styles',    'view-matv'),
    ('Fire Alarm course styles',      'view-fire'),
    ('Access Control course styles',  'view-access'),
]

# ─────────────────────────────────────────────────────────
# FIX 1a: For each course CSS block, scope body/html/* correctly
#          • body {}  → #view-X {} but strip display & min-height (SPA controls those)
#          • html {}  → REMOVE entirely (scroll-behavior irrelevant for a div)
#          • * {}     → #view-X *, etc. (safe)
# ─────────────────────────────────────────────────────────
for comment_text, view_id in course_css_markers:
    cs, ce = get_style_block_bounds(content, comment_text)
    if cs is None:
        print(f'  SKIP: style block not found for {view_id}')
        continue

    css = content[cs:ce]
    original_css = css
    scope = '#' + view_id

    # --- html { ... } → strip entirely ---
    css = re.sub(r'(?<![\'"\w\-#.])html\s*\{[^}]*\}', '', css)

    # --- body { ... } → #view-X { ... } but without display and min-height ---
    def scope_body(m):
        block = m.group(0)   # full body { ... }
        props = m.group(1)   # just the properties
        props = re.sub(r'\s*display\s*:[^;]+;', '', props)
        props = re.sub(r'\s*min-height\s*:[^;]+;', '', props)
        return scope + ' {' + props + '}'
    css = re.sub(r'(?<![\'"\w\-#.])body\s*\{([^}]*)\}', scope_body, css)

    # --- *, *::before, *::after { ... } → #view-X *, ... ---
    css = re.sub(
        r'\*\s*,\s*\*::before\s*,\s*\*::after\s*\{',
        ':where(' + scope + ') *, :where(' + scope + ') *::before, :where(' + scope + ') *::after {',
        css
    )

    # --- If #view-X rule still has display: flex from a previous bad fix, remove it ---
    # (handles re-running on already-patched file)
    def clean_view_display(m):
        full = m.group(0)
        inner = m.group(1)
        inner = re.sub(r'\s*display\s*:\s*flex\s*;', '', inner)
        inner = re.sub(r'\s*min-height\s*:\s*100vh\s*;', '', inner)
        return scope + ' {' + inner + '}'
    css = re.sub(re.escape(scope) + r'\s*\{([^}]*)\}', clean_view_display, css)

    if css != original_css:
        content = content[:cs] + css + content[ce:]
        print(f'  OK: Fixed body/html scope for {view_id}')
    else:
        print(f'  SAME: No changes needed for {view_id}')

# ─────────────────────────────────────────────────────────
# FIX 2: MATV nav — .nav-item → .nav-link, data-stage="stageN" → data-stage="N"
# ─────────────────────────────────────────────────────────
matv_view_start = content.find('id="view-matv"')
nav_start = content.find('<nav class="stage-nav"', matv_view_start)
nav_end   = content.find('</nav>', nav_start) + 6

nav_block = content[nav_start:nav_end]
original_nav = nav_block

nav_block = nav_block.replace('class="nav-item"', 'class="nav-link"')
nav_block = nav_block.replace('class="nav-item active"', 'class="nav-link active"')

def replace_data_stage(m):
    num = re.sub(r'[^\d]', '', m.group(1))
    return f'data-stage="{num}"'
nav_block = re.sub(r'data-stage="(stage\d+)"', replace_data_stage, nav_block)

if nav_block != original_nav:
    content = content[:nav_start] + nav_block + content[nav_end:]
    print('  OK: Fixed MATV nav class + data-stage attributes')
else:
    print('  SAME: MATV nav already correct')

# ─────────────────────────────────────────────────────────
# FIX 3: Add window.nextStage / window.prevStage to initStageCourse
#         (idempotent — only adds if not already present)
# ─────────────────────────────────────────────────────────
if 'window.nextStage' not in content:
    old_init_end = "    showItem(parseInt(localStorage.getItem(cfg.key) || 1));\n}"
    new_init_end = """    showItem(parseInt(localStorage.getItem(cfg.key) || 1));
    // Global nav helpers (last-init course wins — safe: only one view active at a time)
    window.nextStage = window.nextModule = window.nextSection = function() {
        var n = parseInt(localStorage.getItem(cfg.key) || 1);
        if (n < cfg.total) showItem(n + 1);
    };
    window.prevStage = window.prevModule = window.prevSection = function() {
        var n = parseInt(localStorage.getItem(cfg.key) || 1);
        if (n > 1) showItem(n - 1);
    };
}"""
    if old_init_end in content:
        content = content.replace(old_init_end, new_init_end, 1)
        print('  OK: Added nextStage/prevStage to initStageCourse')
    else:
        print('  FAIL: Could not find initStageCourse end marker')
else:
    print('  SAME: nextStage already defined')

# ─────────────────────────────────────────────────────────
# Verify
# ─────────────────────────────────────────────────────────
print()

# Check no course CSS block has unscoped body/html rules
all_course_css = ''
for comment_text, view_id in course_css_markers:
    cs, ce = get_style_block_bounds(content, comment_text)
    if cs and ce:
        all_course_css += content[cs:ce]

unscoped_body = len(re.findall(r'(?<![\'"\w\-#.])body\s*\{', all_course_css))
unscoped_html = len(re.findall(r'(?<![\'"\w\-#.])html\s*\{', all_course_css))

# Check no #view-X { display: flex } (which would override SPA show/hide)
leaked_display = []
for view_id in ['view-matv', 'view-fire', 'view-access']:
    scope = '#' + view_id
    cs, ce = get_style_block_bounds(content,
        {'view-matv':'MATV & IPTV course styles','view-fire':'Fire Alarm course styles','view-access':'Access Control course styles'}[view_id])
    if cs and ce:
        block = content[cs:ce]
        # Find the scoped view rule
        m = re.search(re.escape(scope) + r'\s*\{([^}]*)\}', block)
        if m and 'display' in m.group(1):
            leaked_display.append(f'{view_id}: {m.group(1).strip()[:60]}')

checks = [
    ('Unscoped body rules in course CSS = 0', unscoped_body == 0),
    ('Unscoped html rules in course CSS = 0', unscoped_html == 0),
    ('No display in #view-X scoped rules',    len(leaked_display) == 0),
    ('MATV nav-link class present',           'class="nav-link" data-stage="1"' in content),
    ('MATV data-stage="16" present',          'data-stage="16"' in content[content.find('id="view-matv"'):]),
    ('nextStage global defined',              'window.nextStage' in content),
    ('prevStage global defined',              'window.prevStage' in content),
]

all_ok = True
for name, result in checks:
    status = 'OK' if result else 'FAIL'
    if not result:
        all_ok = False
    print(f'  {status} {name}')

if leaked_display:
    for d in leaked_display:
        print(f'    → {d}')

write_file(f'{BASE}/index.html', content)
print(f'\n{"ALL CHECKS PASSED" if all_ok else "SOME CHECKS FAILED"}')
print(f'File written: {original_len:,} -> {len(content):,} chars')
