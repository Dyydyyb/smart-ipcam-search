import os

file_path = 'frontend/landing.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update header.site-header and .nav-wrapper CSS
old_header_css = '''    header.site-header {
      position: sticky;
      top: 0;
      z-index: 100;
      background: rgba(6, 9, 16, 0.88);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      transition: var(--transition-smooth);
    }

    .nav-wrapper {
      display: flex;
      align-items: center;
      justify-content: space-between;
      height: 74px;
      gap: 1rem;
    }'''

new_header_css = '''    header.site-header {
      position: sticky;
      top: 0;
      z-index: 1000;
      background: rgba(6, 9, 16, 0.92);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      transition: var(--transition-smooth);
      width: 100%;
    }

    .nav-wrapper {
      display: flex;
      align-items: center;
      justify-content: space-between;
      height: 76px;
      width: 100%;
      padding: 0 clamp(1.25rem, 2.5vw, 3rem);
      gap: 1.5rem;
    }'''

# 2. Update .nav-controls-suite with divider support
old_controls_css = '''    /* ZONA 3: CONTROLS SUITE & CTA */
    .nav-controls-suite {
      display: flex;
      align-items: center;
      gap: 0.65rem;
      flex-shrink: 0;
    }'''

new_controls_css = '''    /* ZONA 3: CONTROLS SUITE & CTA */
    .nav-controls-suite {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      flex-shrink: 0;
      justify-content: flex-end;
    }

    .nav-actions-divider {
      width: 1px;
      height: 24px;
      background: rgba(255, 255, 255, 0.14);
      margin: 0 0.15rem;
    }'''

# 3. Responsive media queries for header
old_responsive_css = '''    @media (max-width: 1080px) {
      .nav-capsule-wrapper { display: none; }
      .btn-nav-demo { display: none; }
      .mobile-menu-btn { display: flex; }'''

new_responsive_css = '''    @media (max-width: 1260px) {
      .nav-capsule li a {
        padding: 0.38rem 0.62rem;
        font-size: 0.82rem;
      }
      .nav-wrapper {
        gap: 0.85rem;
        padding: 0 1.25rem;
      }
    }

    @media (max-width: 1100px) {
      .nav-capsule-wrapper { display: none; }
      .btn-nav-demo { display: none; }
      .nav-actions-divider { display: none; }
      .mobile-menu-btn { display: flex; }'''

# 4. Remove .container constraint from .nav-wrapper in markup
old_header_markup = '''  <header class="site-header">
    <div class="container nav-wrapper">'''

new_header_markup = '''  <header class="site-header">
    <div class="nav-wrapper">'''

# 5. Add vertical divider in nav-controls-suite
old_suite_markup = '''        </div>

        <a href="#demo" class="btn-nav-demo" onclick="openDemoViewer(event)" data-i18n="nav_demo">Ver Demo</a>'''

new_suite_markup = '''        </div>

        <div class="nav-actions-divider"></div>

        <a href="#demo" class="btn-nav-demo" onclick="openDemoViewer(event)" data-i18n="nav_demo">Ver Demo</a>'''

# 6. Clean logged in user label so it does not overflow
old_user_label = '''          // Cliente Autenticado -> va directo a sus cámaras
          const label = `${dict.nav_my_cameras} (${user.username || 'Cliente'})`;
          navBtns.forEach(btn => {
            if (btn) {
              btn.href = "/cameras";
              btn.innerHTML = `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M23 7l-7 5 7 5V7z"></path><rect x="1" y="5" width="15" height="14" rx="2" ry="2"></rect></svg><span>${label}</span>`;
            }
          });'''

new_user_label = '''          // Cliente Autenticado -> va directo a sus cámaras (nombre limpio en tooltip)
          navBtns.forEach(btn => {
            if (btn) {
              btn.href = "/cameras";
              btn.title = `Conectado como: ${user.username || 'Cliente'}`;
              btn.innerHTML = `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M23 7l-7 5 7 5V7z"></path><rect x="1" y="5" width="15" height="14" rx="2" ry="2"></rect></svg><span>${dict.nav_my_cameras}</span>`;
            }
          });'''

assert old_header_css in content, "old_header_css not found"
assert old_controls_css in content, "old_controls_css not found"
assert old_responsive_css in content, "old_responsive_css not found"
assert old_header_markup in content, "old_header_markup not found"
assert old_suite_markup in content, "old_suite_markup not found"
assert old_user_label in content, "old_user_label not found"

content = content.replace(old_header_css, new_header_css)
content = content.replace(old_controls_css, new_controls_css)
content = content.replace(old_responsive_css, new_responsive_css)
content = content.replace(old_header_markup, new_header_markup)
content = content.replace(old_suite_markup, new_suite_markup)
content = content.replace(old_user_label, new_user_label)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully updated landing.html header layout!")
