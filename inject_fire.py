import sys, re
sys.stdout.reconfigure(encoding='utf-8')
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

def fix_back_link(html):
    html = html.replace('href="../"', 'href="#" onclick="showView(\'view-portal\'); return false;"')
    html = html.replace("href='../'", 'href="#" onclick="showView(\'view-portal\'); return false;"')
    return html

def strip_google_import(css):
    return re.sub(r"@import\s+url\([^)]+\)\s*;", '', css)

def scope_root(css, view_id):
    return re.sub(r':root\s*\{', '#' + view_id + ' {', css)

# Read & process fire course
fire_html = read_file(f'{BASE}/fire-course/index.html')
fire_body = extract_body(fire_html)
fire_body = strip_scripts(fire_body)
fire_body = strip_links(fire_body)
fire_body = fix_back_link(fire_body)
fire_body = fire_body.strip()

fire_css_raw = read_file(f'{BASE}/fire-course/styles.css')
fire_css = strip_google_import(fire_css_raw)
fire_css = scope_root(fire_css, 'view-fire')

print(f"Fire body: {len(fire_body):,} chars")
print(f"Fire CSS:  {len(fire_css):,} chars")

# Read index.html (the SPA)
spa = read_file(f'{BASE}/index.html')
original_len = len(spa)

# 1. Inject fire CSS before SPA Shell style block
fire_css_block = (
    "\n    <!-- Fire Alarm course styles (accent: #f97316) -->\n"
    "    <style>\n"
    + fire_css +
    "\n    </style>\n\n    "
)
spa = spa.replace(
    '\n    <style>\n        /* \u2500\u2500 SPA Shell',
    fire_css_block + '<style>\n        /* \u2500\u2500 SPA Shell'
)

# 2. Add portal CSS rule for .course-card.fire
spa = spa.replace(
    "        .course-card.access { --course-color: #f59e0b; --course-glow: rgba(245,158,11,0.15); }",
    "        .course-card.access { --course-color: #f59e0b; --course-glow: rgba(245,158,11,0.15); }\n"
    "        .course-card.fire   { --course-color: #f97316; --course-glow: rgba(249,115,22,0.15); }"
)

# 3. Add _courseInit entry for view-fire
old_init = "    'view-access': function() { initStageCourse({viewId:'view-access', total:16, prefix:'stage', key:'av_access'}); }\n};"
new_init = (
    "    'view-access': function() { initStageCourse({viewId:'view-access', total:16, prefix:'stage', key:'av_access'}); },\n"
    "    'view-fire':   function() { initStageCourse({viewId:'view-fire',   total:16, prefix:'stage', key:'av_fire'}); }\n"
    "};"
)
spa = spa.replace(old_init, new_init)

# 4. Add portal card for fire course (before courses grid close)
fire_card = r"""
                <!-- FIRE ALARM -->
                <div class="course-card fire reveal reveal-delay-2">
                    <div class="course-banner"></div>
                    <div class="course-card-inner">
                        <div class="course-header-row">
                            <div class="course-icon-wrap">
                                <svg width="36" height="36" viewBox="0 0 36 36" fill="none">
                                    <path d="M18 4 C18 4 24 10 24 18 C24 24.627 21.314 28 18 30 C18 30 20 26 18 22 C16 26 12 28 12 28 C10 25 10 22 12 18 C10 20 8 20 8 20 C8 12 14 6 18 4Z" stroke="#f97316" stroke-width="1.8" fill="rgba(249,115,22,0.15)" stroke-linejoin="round"/>
                                    <circle cx="18" cy="22" r="3" fill="#f97316"/>
                                </svg>
                            </div>
                            <span class="course-badge">16 Stages</span>
                        </div>
                        <h3 class="course-name">Fire Alarm Systems</h3>
                        <p class="course-description">
                            Professional fire alarm from fire science to system design. EN 54, NFPA 72, BS 5839,
                            UL standards, detector physics, addressable loops, cause &amp; effect, gaseous
                            suppression, EVCS, commissioning, and a full hospital ward capstone.
                        </p>
                        <div class="course-topics">
                            <span class="topic-tag">EN 54 / BS 5839</span>
                            <span class="topic-tag">NFPA 72</span>
                            <span class="topic-tag">Addressable Loops</span>
                            <span class="topic-tag">VESDA / ASD</span>
                            <span class="topic-tag">Cause &amp; Effect</span>
                            <span class="topic-tag">EVCS</span>
                        </div>
                        <div class="course-meta">
                            <div class="course-meta-item">
                                <span class="meta-value" style="color:#f97316">16</span>
                                <span class="meta-label">Stages</span>
                            </div>
                            <div class="course-meta-item">
                                <span class="meta-value">50+</span>
                                <span class="meta-label">Diagrams</span>
                            </div>
                            <div class="course-meta-item">
                                <span class="meta-value">Beginner</span>
                                <span class="meta-label">&#x2192; Expert</span>
                            </div>
                        </div>
                        <a href="#" onclick="showView('view-fire'); return false;" class="course-link" style="background:#f97316">
                            Start Fire Course
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
                        </a>
                    </div>
                </div>

"""

# Find the end of the courses grid (before FEATURES section)
courses_end = '\n            </div>\n        </div>\n    </section>\n\n    <!-- \u2550\u2550 FEATURES \u2550\u2550 -->'
spa = spa.replace(courses_end, fire_card + courses_end, 1)

# 5. Add footer nav link
old_footer = "                        <li><a href=\"#\" onclick=\"showView('view-access'); return false;\">Access Control</a></li>\n                    </ul>"
new_footer = (
    "                        <li><a href=\"#\" onclick=\"showView('view-access'); return false;\">Access Control</a></li>\n"
    "                        <li><a href=\"#\" onclick=\"showView('view-fire'); return false;\">Fire Alarm Systems</a></li>\n"
    "                    </ul>"
)
spa = spa.replace(old_footer, new_footer)

# 6. Inject view-fire div before SCRIPTS comment
fire_view = (
    "\n<!-- \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 FIRE ALARM \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 -->\n"
    "<div id=\"view-fire\" class=\"spa-view\">\n"
    + fire_body +
    "\n</div>\n\n"
)
scripts_match = re.search(r'\n+<!-- [=\u2550]+ SCRIPTS [=\u2550]+ -->', spa)
if scripts_match:
    insert_pos = scripts_match.start()
    spa = spa[:insert_pos] + fire_view + spa[insert_pos:]
    print(f"Injected view-fire at position {insert_pos}")
else:
    # Fallback: try plain equals
    scripts_match2 = re.search(r'<!-- .{5,30} SCRIPTS .{5,30} -->', spa)
    if scripts_match2:
        insert_pos = scripts_match2.start()
        spa = spa[:insert_pos] + fire_view + spa[insert_pos:]
        print(f"Injected view-fire (fallback) at position {insert_pos}")
    else:
        print("ERROR: SCRIPTS comment not found!")

# Verify all injections
checks = [
    ('Fire CSS block',    'Fire Alarm course styles (accent: #f97316)'),
    ('.course-card.fire', '--course-color: #f97316'),
    ('view-fire init',    "view-fire"),
    ('Fire portal card',  'course-card fire reveal'),
    ('Footer link',       'Fire Alarm Systems'),
    ('view-fire div',     'id="view-fire" class="spa-view"'),
]
print()
for name, needle in checks:
    found = needle in spa
    print(f"  {'OK' if found else 'FAIL'} {name}")

write_file(f'{BASE}/index.html', spa)
print(f"\nFile written: {original_len:,} -> {len(spa):,} chars (+{len(spa)-original_len:,})")
