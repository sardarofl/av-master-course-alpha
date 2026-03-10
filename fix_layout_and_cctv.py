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
# FIX 1: Change #view-X *, #view-X *::before, #view-X *::after
#         to :where(#view-X) *, ... so the CSS reset has
#         ZERO specificity and doesn't override .content { margin-left }
#
# Root cause: #view-X * has specificity (1,0,1) which beats
#             .content { margin-left: var(--sidebar-width) } (0,1,0)
# Fix: :where() reduces selector specificity to 0, so (0,0,1) < (0,1,0)
# ─────────────────────────────────────────────────────────
bad_selectors = [
    ('#view-access *, #view-access *::before, #view-access *::after',
     ':where(#view-access) *, :where(#view-access) *::before, :where(#view-access) *::after'),
    ('#view-fire *, #view-fire *::before, #view-fire *::after',
     ':where(#view-fire) *, :where(#view-fire) *::before, :where(#view-fire) *::after'),
    ('#view-matv *, #view-matv *::before, #view-matv *::after',
     ':where(#view-matv) *, :where(#view-matv) *::before, :where(#view-matv) *::after'),
]

fix1_count = 0
for bad, good in bad_selectors:
    if bad in content:
        content = content.replace(bad, good, 1)
        fix1_count += 1
        print(f'  OK: Fixed * selector specificity: {bad[:30]}...')
    elif good in content:
        print(f'  SAME: Already fixed: {good[:30]}...')
    else:
        print(f'  WARN: Not found: {bad[:50]}')

# ─────────────────────────────────────────────────────────
# FIX 2: CCTV sidebar links — href="#moduleX" changes the SPA hash
#         router and hides all views. Change to javascript:void(0)
#         so only the onclick="loadSection(...)" runs.
# ─────────────────────────────────────────────────────────
cctv_start = content.find('id="view-cctv"')
cctv_end_marker = '\n\n<!-- '  # next section comment
cctv_section_end = content.find(cctv_end_marker, cctv_start)
if cctv_section_end == -1:
    cctv_section_end = cctv_start + 500000  # fallback: large window

cctv_block = content[cctv_start:cctv_section_end]
original_cctv = cctv_block

# Replace href="#module..." and href="#capstone" with javascript:void(0)
# Also ensure onclick returns false to be safe
cctv_block = re.sub(
    r'href="#(module\d+|capstone)"(\s+class="nav-link[^"]*"\s+onclick="loadSection\([^)]+\)")',
    r'href="javascript:void(0)"\2',
    cctv_block
)

fix2_count = len(re.findall(r'javascript:void\(0\)', cctv_block)) - len(re.findall(r'javascript:void\(0\)', original_cctv))

if cctv_block != original_cctv:
    content = content[:cctv_start] + cctv_block + content[cctv_section_end:]
    print(f'  OK: Fixed {fix2_count} CCTV sidebar href anchors')
else:
    # Check if already fixed
    if 'javascript:void(0)' in content[cctv_start:cctv_start+10000]:
        print('  SAME: CCTV hrefs already fixed')
    else:
        print('  FAIL: Could not fix CCTV sidebar hrefs')

# ─────────────────────────────────────────────────────────
# Also update fix_css_and_nav.py to use :where() for future runs
# ─────────────────────────────────────────────────────────
fix_script = read_file(f'{BASE}/fix_css_and_nav.py')
old_star = "scope + ' *, ' + scope + ' *::before, ' + scope + ' *::after {'"
new_star = "':where(' + scope + ') *, :where(' + scope + ') *::before, :where(' + scope + ') *::after {'"
if old_star in fix_script:
    fix_script = fix_script.replace(old_star, new_star, 1)
    write_file(f'{BASE}/fix_css_and_nav.py', fix_script)
    print('  OK: Updated fix_css_and_nav.py to use :where() for * scoping')
elif new_star in fix_script:
    print('  SAME: fix_css_and_nav.py already uses :where()')
else:
    print('  WARN: Could not patch fix_css_and_nav.py')

# ─────────────────────────────────────────────────────────
# Verify
# ─────────────────────────────────────────────────────────
print()
checks = [
    ('No bare #view-access * selector',  '#view-access *,' not in content),
    ('No bare #view-fire * selector',    '#view-fire *,' not in content),
    ('No bare #view-matv * selector',    '#view-matv *,' not in content),
    (':where(#view-access) * present',   ':where(#view-access) *' in content),
    (':where(#view-fire) * present',     ':where(#view-fire) *' in content),
    (':where(#view-matv) * present',     ':where(#view-matv) *' in content),
    ('CCTV hrefs use void(0)',           'javascript:void(0)" class="nav-link' in content),
    ('No CCTV href="#module',            'href="#module' not in content[content.find('id="view-cctv"'):content.find('id="view-cctv"')+50000]),
]

all_ok = True
for name, result in checks:
    status = 'OK' if result else 'FAIL'
    if not result:
        all_ok = False
    print(f'  {status} {name}')

write_file(f'{BASE}/index.html', content)
print(f'\n{"ALL CHECKS PASSED" if all_ok else "SOME CHECKS FAILED"}')
print(f'File written: {original_len:,} -> {len(content):,} chars')
