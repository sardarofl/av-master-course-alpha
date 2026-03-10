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

# Read & process MATV course
matv_html = read_file(f'{BASE}/matv-course/index.html')
matv_body = extract_body(matv_html)
matv_body = strip_scripts(matv_body)
matv_body = strip_links(matv_body)
matv_body = fix_back_link(matv_body)
matv_body = matv_body.strip()

matv_css_raw = read_file(f'{BASE}/matv-course/styles.css')
matv_css = strip_google_import(matv_css_raw)
matv_css = scope_root(matv_css, 'view-matv')

print(f"MATV body: {len(matv_body):,} chars")
print(f"MATV CSS:  {len(matv_css):,} chars")

# Read index.html (the SPA)
spa = read_file(f'{BASE}/index.html')
original_len = len(spa)

# 1. Inject MATV CSS before SPA Shell style block
matv_css_block = (
    "\n    <!-- MATV & IPTV course styles (accent: #06b6d4) -->\n"
    "    <style>\n"
    + matv_css +
    "\n    </style>\n\n    "
)
spa = spa.replace(
    '\n    <style>\n        /* \u2500\u2500 SPA Shell',
    matv_css_block + '<style>\n        /* \u2500\u2500 SPA Shell'
)

# 2. Add portal CSS rule for .course-card.matv
spa = spa.replace(
    "        .course-card.fire   { --course-color: #f97316; --course-glow: rgba(249,115,22,0.15); }",
    "        .course-card.fire   { --course-color: #f97316; --course-glow: rgba(249,115,22,0.15); }\n"
    "        .course-card.matv   { --course-color: #06b6d4; --course-glow: rgba(6,182,212,0.15); }"
)

# 3. Add _courseInit entry for view-matv
old_init = "    'view-fire':   function() { initStageCourse({viewId:'view-fire',   total:16, prefix:'stage', key:'av_fire'}); }\n};"
new_init = (
    "    'view-fire':   function() { initStageCourse({viewId:'view-fire',   total:16, prefix:'stage', key:'av_fire'}); },\n"
    "    'view-matv':   function() { initStageCourse({viewId:'view-matv',   total:16, prefix:'stage', key:'av_matv'}); }\n"
    "};"
)
spa = spa.replace(old_init, new_init)

# 4. Add portal card for MATV course (before courses grid close)
matv_card = r"""
                <!-- MATV & IPTV -->
                <div class="course-card matv reveal reveal-delay-2">
                    <div class="course-banner"></div>
                    <div class="course-card-inner">
                        <div class="course-header-row">
                            <div class="course-icon-wrap">
                                <svg width="36" height="36" viewBox="0 0 36 36" fill="none">
                                    <rect x="4" y="6" width="28" height="18" rx="3" stroke="#06b6d4" stroke-width="1.8" fill="rgba(6,182,212,0.1)"/>
                                    <line x1="13" y1="24" x2="23" y2="24" stroke="#06b6d4" stroke-width="1.8" stroke-linecap="round"/>
                                    <line x1="18" y1="24" x2="18" y2="30" stroke="#06b6d4" stroke-width="1.8" stroke-linecap="round"/>
                                    <line x1="12" y1="30" x2="24" y2="30" stroke="#06b6d4" stroke-width="1.8" stroke-linecap="round"/>
                                    <circle cx="26" cy="10" r="2.5" fill="rgba(6,182,212,0.3)" stroke="#06b6d4" stroke-width="1.2"/>
                                    <path d="M29 7 C31 8 31 12 29 13" stroke="#06b6d4" stroke-width="1.2" stroke-linecap="round" fill="none"/>
                                    <path d="M31 5 C34 7 34 13 31 15" stroke="#06b6d4" stroke-width="1" stroke-linecap="round" fill="none" opacity="0.6"/>
                                </svg>
                            </div>
                            <span class="course-badge">16 Stages</span>
                        </div>
                        <h3 class="course-name">MATV &amp; IPTV</h3>
                        <p class="course-description">
                            Professional broadcast distribution from RF fundamentals to full IPTV deployment.
                            Satellite dish farms, DVB standards, video encoding, IGMP multicast, middleware,
                            DRM, hospitality systems, and a complete 200-room hotel design capstone.
                        </p>
                        <div class="course-topics">
                            <span class="topic-tag">RF / dBμV</span>
                            <span class="topic-tag">DVB-T2/S2</span>
                            <span class="topic-tag">H.264 / HEVC</span>
                            <span class="topic-tag">Multicast IGMP</span>
                            <span class="topic-tag">Middleware EPG</span>
                            <span class="topic-tag">DRM Widevine</span>
                        </div>
                        <div class="course-meta">
                            <div class="course-meta-item">
                                <span class="meta-value" style="color:#06b6d4">16</span>
                                <span class="meta-label">Stages</span>
                            </div>
                            <div class="course-meta-item">
                                <span class="meta-value">60+</span>
                                <span class="meta-label">Diagrams</span>
                            </div>
                            <div class="course-meta-item">
                                <span class="meta-value">Beginner</span>
                                <span class="meta-label">&#x2192; Expert</span>
                            </div>
                        </div>
                        <a href="#" onclick="showView('view-matv'); return false;" class="course-link" style="background:#06b6d4">
                            Start MATV &amp; IPTV Course
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
                        </a>
                    </div>
                </div>

"""

# Find the end of the courses grid (before FEATURES section)
courses_end = '\n            </div>\n        </div>\n    </section>\n\n    <!-- \u2550\u2550 FEATURES \u2550\u2550 -->'
spa = spa.replace(courses_end, matv_card + courses_end, 1)

# 5. Add footer nav link
old_footer = "                        <li><a href=\"#\" onclick=\"showView('view-fire'); return false;\">Fire Alarm Systems</a></li>\n                    </ul>"
new_footer = (
    "                        <li><a href=\"#\" onclick=\"showView('view-fire'); return false;\">Fire Alarm Systems</a></li>\n"
    "                        <li><a href=\"#\" onclick=\"showView('view-matv'); return false;\">MATV &amp; IPTV</a></li>\n"
    "                    </ul>"
)
spa = spa.replace(old_footer, new_footer)

# 6. Inject view-matv div before SCRIPTS comment
matv_view = (
    "\n<!-- \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 MATV & IPTV \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 -->\n"
    "<div id=\"view-matv\" class=\"spa-view\">\n"
    + matv_body +
    "\n</div>\n\n"
)
scripts_match = re.search(r'\n+<!-- [=\u2550]+ SCRIPTS [=\u2550]+ -->', spa)
if scripts_match:
    insert_pos = scripts_match.start()
    spa = spa[:insert_pos] + matv_view + spa[insert_pos:]
    print(f"Injected view-matv at position {insert_pos}")
else:
    scripts_match2 = re.search(r'<!-- .{5,30} SCRIPTS .{5,30} -->', spa)
    if scripts_match2:
        insert_pos = scripts_match2.start()
        spa = spa[:insert_pos] + matv_view + spa[insert_pos:]
        print(f"Injected view-matv (fallback) at position {insert_pos}")
    else:
        print("ERROR: SCRIPTS comment not found!")

# Verify all injections
checks = [
    ('MATV CSS block',    'MATV & IPTV course styles (accent: #06b6d4)'),
    ('.course-card.matv', '--course-color: #06b6d4'),
    ('view-matv init',    "view-matv"),
    ('MATV portal card',  'course-card matv reveal'),
    ('Footer link',       'MATV &amp; IPTV'),
    ('view-matv div',     'id="view-matv" class="spa-view"'),
]
print()
for name, needle in checks:
    found = needle in spa
    print(f"  {'OK' if found else 'FAIL'} {name}")

write_file(f'{BASE}/index.html', spa)
print(f"\nFile written: {original_len:,} -> {len(spa):,} chars (+{len(spa)-original_len:,})")
