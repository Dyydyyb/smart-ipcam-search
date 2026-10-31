import os
import re

# Read original landing.html
with open("frontend/landing.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update CSS
old_header_css_pattern = re.compile(
    r'/\* =+ \s* HEADER & NAVEGACIÓN \s* =+ \*/.*?/\* =+ \s* HERO SECTION',
    re.DOTALL
)

new_header_css = """/* ==========================================================================
       HEADER & NAVEGACIÓN SAAS PREMIUM (FLOATING CAPSULE & SUITE)
       ========================================================================== */
    header.site-header {
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
    }

    /* ZONA 1: BRAND LOGO */
    .brand-logo {
      display: flex;
      align-items: center;
      gap: 12px;
      text-decoration: none;
      flex-shrink: 0;
    }

    .brand-icon-wrap {
      width: 40px;
      height: 40px;
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
      filter: drop-shadow(0 0 10px rgba(6, 182, 212, 0.45));
    }

    .brand-text {
      display: flex;
      flex-direction: column;
    }

    .brand-name {
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 1.22rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      color: #fff;
      line-height: 1.1;
    }

    .brand-tagline {
      font-size: 0.65rem;
      font-weight: 700;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--cyan-bright);
    }

    /* ZONA 2: CENTER CAPSULE PILL NAV */
    .nav-capsule-wrapper {
      display: flex;
      align-items: center;
      justify-content: center;
      flex: 1;
    }

    .nav-capsule {
      display: flex;
      align-items: center;
      gap: 0.25rem;
      background: rgba(13, 18, 30, 0.72);
      border: 1px solid rgba(255, 255, 255, 0.1);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border-radius: 9999px;
      padding: 0.3rem 0.55rem;
      box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.4), inset 0 1px 1px rgba(255, 255, 255, 0.08);
      list-style: none;
    }

    .nav-capsule li a {
      color: var(--text-muted);
      text-decoration: none;
      font-size: 0.88rem;
      font-weight: 500;
      padding: 0.42rem 0.82rem;
      border-radius: 9999px;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      display: inline-block;
      white-space: nowrap;
    }

    .nav-capsule li a:hover {
      color: #00f2fe;
      background: rgba(6, 182, 212, 0.1);
      box-shadow: 0 0 14px rgba(6, 182, 212, 0.25);
    }

    /* ZONA 3: CONTROLS SUITE & CTA */
    .nav-controls-suite {
      display: flex;
      align-items: center;
      gap: 0.65rem;
      flex-shrink: 0;
    }

    /* SEGMENTED SWITCHER PILLS (CURRENCY & LANGUAGE) */
    .segmented-pill {
      display: inline-flex;
      align-items: center;
      background: rgba(15, 23, 42, 0.75);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 9999px;
      padding: 3px;
      gap: 2px;
      backdrop-filter: blur(12px);
    }

    .segmented-btn {
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-family: inherit;
      font-size: 0.74rem;
      font-weight: 700;
      letter-spacing: 0.05em;
      padding: 0.32rem 0.62rem;
      border-radius: 9999px;
      cursor: pointer;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      line-height: 1;
    }

    .segmented-btn:hover {
      color: #f8fafc;
    }

    .segmented-btn.active {
      background: var(--gradient-brand);
      color: #060911;
      font-weight: 800;
      box-shadow: 0 0 14px rgba(6, 182, 212, 0.4);
    }

    /* ACTION BUTTONS */
    .btn-nav-demo {
      display: inline-flex;
      align-items: center;
      padding: 0.5rem 0.95rem;
      border-radius: 9999px;
      font-size: 0.85rem;
      font-weight: 600;
      text-decoration: none;
      color: #cbd5e1;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.12);
      transition: var(--transition-smooth);
      white-space: nowrap;
    }

    .btn-nav-demo:hover {
      color: #fff;
      background: rgba(255, 255, 255, 0.12);
      border-color: rgba(255, 255, 255, 0.28);
      transform: translateY(-1px);
    }

    .btn-nav-portal {
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
      padding: 0.52rem 1.15rem;
      border-radius: 9999px;
      font-size: 0.86rem;
      font-weight: 700;
      text-decoration: none;
      background: var(--gradient-brand);
      color: #060911;
      box-shadow: 0 0 20px rgba(6, 182, 212, 0.35);
      border: none;
      cursor: pointer;
      transition: var(--transition-smooth);
      white-space: nowrap;
    }

    .btn-nav-portal:hover {
      transform: translateY(-2px);
      box-shadow: 0 0 30px rgba(6, 182, 212, 0.6);
      filter: brightness(1.1);
    }

    /* HAMBURGER BUTTON (MOBILE / TABLET) */
    .mobile-menu-btn {
      display: none;
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid rgba(255, 255, 255, 0.15);
      color: #f8fafc;
      width: 42px;
      height: 42px;
      border-radius: 12px;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.2s ease;
      flex-shrink: 0;
    }

    .mobile-menu-btn:hover {
      border-color: var(--cyan-bright);
      box-shadow: 0 0 16px rgba(6, 182, 212, 0.35);
    }

    /* MOBILE SLIDE-DOWN DRAWER */
    .mobile-drawer {
      display: none;
      position: absolute;
      top: 100%;
      left: 0;
      width: 100%;
      background: rgba(6, 9, 16, 0.98);
      backdrop-filter: blur(24px);
      -webkit-backdrop-filter: blur(24px);
      border-bottom: 1px solid rgba(255, 255, 255, 0.12);
      box-shadow: 0 24px 48px rgba(0, 0, 0, 0.85);
      padding: 1.5rem 1.5rem 2rem;
      flex-direction: column;
      gap: 1.25rem;
      animation: drawerSlideDown 0.28s cubic-bezier(0.16, 1, 0.3, 1) forwards;
      z-index: 999;
    }

    @keyframes drawerSlideDown {
      from { opacity: 0; transform: translateY(-12px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .mobile-drawer.open {
      display: flex;
    }

    .mobile-nav-links {
      display: flex;
      flex-direction: column;
      gap: 0.45rem;
      list-style: none;
    }

    .mobile-nav-links a {
      color: #e2e8f0;
      text-decoration: none;
      font-size: 1.05rem;
      font-weight: 600;
      padding: 0.8rem 1.1rem;
      border-radius: 12px;
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.05);
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .mobile-nav-links a:hover {
      color: #00f2fe;
      border-color: rgba(6, 182, 212, 0.3);
      background: rgba(6, 182, 212, 0.08);
    }

    .mobile-controls-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
      padding-top: 0.8rem;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      flex-wrap: wrap;
    }

    .mobile-switchers-group {
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }

    .mobile-portal-btn {
      width: 100%;
      text-align: center;
      padding: 0.85rem;
      font-size: 1rem;
    }

    /* ==========================================================================
       HERO SECTION"""

html = old_header_css_pattern.sub(new_header_css, html)

# 2. Update Responsive Breakpoints in CSS
old_resp_pattern = re.compile(
    r'@media \(max-width: 1024px\).*?@media \(max-width: 768px\)\s*\{.*?\}',
    re.DOTALL
)

new_resp_css = """@media (max-width: 1080px) {
      .nav-capsule-wrapper { display: none; }
      .btn-nav-demo { display: none; }
      .mobile-menu-btn { display: flex; }
      .hero-title { font-size: 2.8rem; }
      .mockup-metrics-grid { grid-template-columns: repeat(2, 1fr); }
      .mockup-viewport-split { grid-template-columns: 1fr; }
      .pillars-grid { grid-template-columns: repeat(2, 1fr); }
      .pricing-grid { grid-template-columns: 1fr; max-width: 480px; margin: 0 auto; }
      .pricing-card.featured { transform: none; }
      .pricing-card.featured:hover { transform: translateY(-4px); }
      .hire-options-grid { grid-template-columns: 1fr; }
      .calculator-card { grid-template-columns: 1fr; gap: 2rem; }
      .portal-banner-card { flex-direction: column; text-align: center; }
      .portal-banner-actions { justify-content: center; }
      .portal-security-badge { justify-content: center; }
      .footer-grid { grid-template-columns: 1fr 1fr; }
    }

    @media (max-width: 768px) {
      .desktop-switchers { display: none !important; }
      .brand-name { font-size: 1.05rem; }
      .brand-tagline { font-size: 0.58rem; }
      .nav-wrapper { height: 64px; }
      .hero-title { font-size: 2.15rem; }
      .hero-subtitle { font-size: 0.98rem; }
      .comparison-grid { grid-template-columns: 1fr; }
      .pillars-grid { grid-template-columns: 1fr; }
      .footer-grid { grid-template-columns: 1fr; }
    }"""

html = old_resp_pattern.sub(new_resp_css, html)

# 3. Replace Header HTML
old_header_html_pattern = re.compile(
    r'<header class="site-header">.*?</header>',
    re.DOTALL
)

new_header_html = """<header class="site-header">
    <div class="container nav-wrapper">
      <!-- 1. Brand Logo -->
      <a href="#" class="brand-logo" aria-label="Baddgroup Vision AI">
        <div class="brand-icon-wrap">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100%" height="100%">
            <polygon points="50,4 92,26 92,74 50,96 8,74 8,26" fill="#1e293b" stroke="#00f2fe" stroke-width="2.5"/>
            <path d="M28 24 H48 C54.5 24 59 28 59 33.5 C59 37.5 56.5 41 52.5 42.5 C57.5 44 61 48 61 53.5 C61 60 55.5 64 48 64 H28 V24 Z" 
                  fill="none" stroke="#2563eb" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>
            <path d="M28 44 H48" stroke="#2563eb" stroke-width="4.5" stroke-linecap="round"/>
            <path d="M72 40 V62 C72 68 66 73 58 73 H46" 
                  fill="none" stroke="#00f2fe" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M58 58 H72" stroke="#00f2fe" stroke-width="4" stroke-linecap="round"/>
          </svg>
        </div>
        <div class="brand-text">
          <span class="brand-name">BADDGROUP</span>
          <span class="brand-tagline">VISION AI • SECURITY SAAS</span>
        </div>
      </a>

      <!-- 2. Floating Capsule Pill Nav (Center) -->
      <nav class="nav-capsule-wrapper" aria-label="Navegación principal">
        <ul class="nav-capsule">
          <li><a href="#que-es" data-i18n="nav_about">¿De qué trata?</a></li>
          <li><a href="#modalidades" data-i18n="nav_hire">Cómo Contratar</a></li>
          <li><a href="#planes" data-i18n="nav_pricing">Planes & Precios</a></li>
          <li><a href="#calculadora" data-i18n="nav_calculator">Cotizador</a></li>
          <li><a href="#faq" data-i18n="nav_faq">Preguntas</a></li>
        </ul>
      </nav>

      <!-- 3. Controls Suite (Right: Switchers + CTA + Mobile Toggle) -->
      <div class="nav-controls-suite">
        <!-- Currency & Language Switchers (Desktop) -->
        <div class="desktop-switchers" style="display: flex; align-items: center; gap: 0.5rem;">
          <!-- Currency Switcher Pill -->
          <div class="segmented-pill" title="Cambiar moneda / Change currency">
            <button type="button" class="segmented-btn active" id="currBtnARS" onclick="setCurrency('ARS')">ARS</button>
            <button type="button" class="segmented-btn" id="currBtnUSD" onclick="setCurrency('USD')">USD</button>
          </div>

          <!-- Language Switcher Pill -->
          <div class="segmented-pill" title="Cambiar idioma / Change language">
            <button type="button" class="segmented-btn active" id="langBtnES" onclick="setLanguage('es')">ES</button>
            <button type="button" class="segmented-btn" id="langBtnEN" onclick="setLanguage('en')">EN</button>
          </div>
        </div>

        <a href="#demo" class="btn-nav-demo" onclick="openDemoViewer(event)" data-i18n="nav_demo">Ver Demo</a>

        <!-- Dynamic Portal CTA Button (Requiere login para ver cámaras) -->
        <a href="/login?redirect=/cameras" id="dynamicPortalBtn" class="btn-nav-portal">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
            <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
          </svg>
          <span data-i18n="nav_client_login">Acceso Clientes</span>
        </a>

        <!-- Mobile Hamburger Button -->
        <button type="button" class="mobile-menu-btn" id="mobileMenuBtn" onclick="toggleMobileMenu()" aria-label="Abrir menú">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="3" y1="12" x2="21" y2="12"></line>
            <line x1="3" y1="6" x2="21" y2="6"></line>
            <line x1="3" y1="18" x2="21" y2="18"></line>
          </svg>
        </button>
      </div>
    </div>

    <!-- Mobile Slide-Down Drawer -->
    <div class="mobile-drawer" id="mobileDrawer">
      <ul class="mobile-nav-links">
        <li><a href="#que-es" onclick="closeMobileMenu()"><span data-i18n="nav_about">¿De qué trata?</span><span>→</span></a></li>
        <li><a href="#modalidades" onclick="closeMobileMenu()"><span data-i18n="nav_hire">Cómo Contratar</span><span>→</span></a></li>
        <li><a href="#planes" onclick="closeMobileMenu()"><span data-i18n="nav_pricing">Planes & Precios</span><span>→</span></a></li>
        <li><a href="#calculadora" onclick="closeMobileMenu()"><span data-i18n="nav_calculator">Cotizador</span><span>→</span></a></li>
        <li><a href="#faq" onclick="closeMobileMenu()"><span data-i18n="nav_faq">Preguntas</span><span>→</span></a></li>
        <li><a href="#demo" onclick="closeMobileMenu(); openDemoViewer(event);"><span data-i18n="nav_demo">Ver Demo</span><span>→</span></a></li>
      </ul>

      <div class="mobile-controls-row">
        <div class="mobile-switchers-group">
          <!-- Mobile Currency Switcher -->
          <div class="segmented-pill">
            <button type="button" class="segmented-btn active" id="currBtnARSMobile" onclick="setCurrency('ARS')">ARS</button>
            <button type="button" class="segmented-btn" id="currBtnUSDMobile" onclick="setCurrency('USD')">USD</button>
          </div>
          <!-- Mobile Language Switcher -->
          <div class="segmented-pill">
            <button type="button" class="segmented-btn active" id="langBtnESMobile" onclick="setLanguage('es')">ES</button>
            <button type="button" class="segmented-btn" id="langBtnENMobile" onclick="setLanguage('en')">EN</button>
          </div>
        </div>

        <a href="/login?redirect=/cameras" id="dynamicPortalBtnMobile" class="btn-nav-portal" onclick="closeMobileMenu()">
          <span data-i18n="nav_client_login">Acceso Clientes</span>
        </a>
      </div>
    </div>
  </header>"""

html = old_header_html_pattern.sub(new_header_html, html)

# Let's save and inspect step 1
with open("frontend/landing.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Header HTML and CSS updated successfully.")
