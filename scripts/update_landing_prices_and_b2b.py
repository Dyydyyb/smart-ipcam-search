import re

with open("frontend/landing.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update navigation capsule links in header and mobile drawer to include Empresas de Seguridad
nav_capsule_old = """        <ul class="nav-capsule">
          <li><a href="#que-es" data-i18n="nav_about">¿De qué trata?</a></li>
          <li><a href="#modalidades" data-i18n="nav_hire">Cómo Contratar</a></li>
          <li><a href="#planes" data-i18n="nav_pricing">Planes & Precios</a></li>
          <li><a href="#calculadora" data-i18n="nav_calculator">Cotizador</a></li>
          <li><a href="#faq" data-i18n="nav_faq">Preguntas</a></li>
        </ul>"""

nav_capsule_new = """        <ul class="nav-capsule">
          <li><a href="#que-es" data-i18n="nav_about">¿De qué trata?</a></li>
          <li><a href="#modalidades" data-i18n="nav_hire">Cómo Contratar</a></li>
          <li><a href="#empresas-seguridad" data-i18n="nav_b2b">Empresas de Seguridad</a></li>
          <li><a href="#planes" data-i18n="nav_pricing">Planes & Precios</a></li>
          <li><a href="#calculadora" data-i18n="nav_calculator">Cotizador</a></li>
          <li><a href="#faq" data-i18n="nav_faq">Preguntas</a></li>
        </ul>"""

html = html.replace(nav_capsule_old, nav_capsule_new)

# Mobile drawer links
mobile_drawer_old = """      <ul class="mobile-nav-links">
        <li><a href="#que-es" onclick="closeMobileMenu()"><span data-i18n="nav_about">¿De qué trata?</span><span>→</span></a></li>
        <li><a href="#modalidades" onclick="closeMobileMenu()"><span data-i18n="nav_hire">Cómo Contratar</span><span>→</span></a></li>
        <li><a href="#planes" onclick="closeMobileMenu()"><span data-i18n="nav_pricing">Planes & Precios</span><span>→</span></a></li>
        <li><a href="#calculadora" onclick="closeMobileMenu()"><span data-i18n="nav_calculator">Cotizador</span><span>→</span></a></li>
        <li><a href="#faq" onclick="closeMobileMenu()"><span data-i18n="nav_faq">Preguntas</span><span>→</span></a></li>
        <li><a href="#demo" onclick="closeMobileMenu(); openDemoViewer(event);"><span data-i18n="nav_demo">Ver Demo</span><span>→</span></a></li>
      </ul>"""

mobile_drawer_new = """      <ul class="mobile-nav-links">
        <li><a href="#que-es" onclick="closeMobileMenu()"><span data-i18n="nav_about">¿De qué trata?</span><span>→</span></a></li>
        <li><a href="#modalidades" onclick="closeMobileMenu()"><span data-i18n="nav_hire">Cómo Contratar</span><span>→</span></a></li>
        <li><a href="#empresas-seguridad" onclick="closeMobileMenu()"><span data-i18n="nav_b2b">Empresas de Seguridad</span><span>→</span></a></li>
        <li><a href="#planes" onclick="closeMobileMenu()"><span data-i18n="nav_pricing">Planes & Precios</span><span>→</span></a></li>
        <li><a href="#calculadora" onclick="closeMobileMenu()"><span data-i18n="nav_calculator">Cotizador</span><span>→</span></a></li>
        <li><a href="#faq" onclick="closeMobileMenu()"><span data-i18n="nav_faq">Preguntas</span><span>→</span></a></li>
        <li><a href="#demo" onclick="closeMobileMenu(); openDemoViewer(event);"><span data-i18n="nav_demo">Ver Demo</span><span>→</span></a></li>
      </ul>"""

html = html.replace(mobile_drawer_old, mobile_drawer_new)

# 2. Add New Section: Empresas de Seguridad & Centrales de Monitoreo
# Place right after </section> of #modalidades and before #planes
b2b_section_html = """
  <!-- ========================================================================
       SECCIÓN: EMPRESAS DE SEGURIDAD & CENTRALES DE MONITOREO (B2B PARTNERS)
       ======================================================================== -->
  <section class="section-security-companies" id="empresas-seguridad" style="padding: 6rem 0; position: relative; border-top: 1px solid var(--border-subtle); border-bottom: 1px solid var(--border-subtle); background: radial-gradient(circle at 50% 30%, rgba(37, 99, 235, 0.08) 0%, transparent 70%);">
    <div class="container">
      <div class="section-header" style="text-align: center; max-width: 860px; margin: 0 auto 3.5rem;">
        <span class="section-tag" style="background: rgba(37, 99, 235, 0.15); border-color: rgba(37, 99, 235, 0.4); color: #60a5fa;" data-i18n="b2b_tag">SOLUCIÓN B2B PARA EMPRESAS DE SEGURIDAD & MONITOREO</span>
        <h2 class="section-title" style="font-size: 2.6rem; margin: 0.8rem 0;" data-i18n="b2b_title">Potenciá tu Empresa de Seguridad con IA de Baddgroup</h2>
        <p class="section-desc" style="font-size: 1.05rem; line-height: 1.6; color: var(--text-muted);" data-i18n="b2b_desc">
          Te proveemos el software completo, tu propio panel máster multi-tenant, cuentas independientes para tus clientes e infraestructura en la nube. Vos vendés el servicio con tu marca a tus abonados y nosotros ponemos la inteligencia artificial pericial.
        </p>
      </div>

      <!-- Grid de Beneficios B2B -->
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; margin-bottom: 3rem;">
        <!-- Card 1: Panel Máster -->
        <div style="background: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: 16px; padding: 2rem 1.75rem; transition: var(--transition-smooth); box-shadow: var(--shadow-card);">
          <div style="width: 48px; height: 48px; border-radius: 12px; background: rgba(6, 182, 212, 0.12); border: 1px solid var(--border-cyan); display: flex; align-items: center; justify-content: center; margin-bottom: 1.25rem; color: var(--cyan-bright);">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
          </div>
          <h3 style="font-size: 1.25rem; font-weight: 700; margin-bottom: 0.6rem; color: #fff;" data-i18n="b2b_c1_title">Tu Propio Panel Máster Multi-Tenant</h3>
          <p style="font-size: 0.92rem; color: var(--text-muted); line-height: 1.5;" data-i18n="b2b_c1_desc">
            Centro de control administrativo total. Asigná cuentas a tus abonados, agregá cámaras remotas en segundos con su Safety Code y suspendé o reactivá servicios al instante.
          </p>
        </div>

        <!-- Card 2: Setup Inicial -->
        <div style="background: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: 16px; padding: 2rem 1.75rem; transition: var(--transition-smooth); box-shadow: var(--shadow-card);">
          <div style="width: 48px; height: 48px; border-radius: 12px; background: rgba(37, 99, 235, 0.15); border: 1px solid var(--border-glow); display: flex; align-items: center; justify-content: center; margin-bottom: 1.25rem; color: #60a5fa;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>
          </div>
          <h3 style="font-size: 1.25rem; font-weight: 700; margin-bottom: 0.6rem; color: #fff;" data-i18n="b2b_c2_title">Adelanto por Instalación de Software</h3>
          <p style="font-size: 0.92rem; color: var(--text-muted); line-height: 1.5;" data-i18n="b2b_c2_desc">
            Configuración integral, despliegue del software y asignación de servidores dedicados por un adelanto inicial de <strong style="color: var(--cyan-bright);">$300 USD (~$470.000 ARS)</strong> pago único.
          </p>
        </div>

        <!-- Card 3: Modelo Escalar por Cámara -->
        <div style="background: var(--bg-card); border: 1px solid rgba(6, 182, 212, 0.4); border-radius: 16px; padding: 2rem 1.75rem; transition: var(--transition-smooth); box-shadow: 0 0 25px rgba(6, 182, 212, 0.12);">
          <div style="width: 48px; height: 48px; border-radius: 12px; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); display: flex; align-items: center; justify-content: center; margin-bottom: 1.25rem; color: #34d399;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline></svg>
          </div>
          <h3 style="font-size: 1.25rem; font-weight: 700; margin-bottom: 0.6rem; color: #fff;" data-i18n="b2b_c3_title">Abono Base + Escala por Cámara Vendida</h3>
          <p style="font-size: 0.92rem; color: var(--text-muted); line-height: 1.5;" data-i18n="b2b_c3_desc">
            Precio base de plataforma de <strong style="color: #fff;">$95.000 ARS/mes ($60 USD/mo)</strong> + solo <strong style="color: #34d399;">$4.500 ARS/cámara ($3 USD/cámara)</strong>. Revendé a tus clientes con más de un 200% de margen.
          </p>
        </div>

        <!-- Card 4: Operativa Pericial -->
        <div style="background: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: 16px; padding: 2rem 1.75rem; transition: var(--transition-smooth); box-shadow: var(--shadow-card);">
          <div style="width: 48px; height: 48px; border-radius: 12px; background: rgba(245, 158, 11, 0.15); border: 1px solid rgba(245, 158, 11, 0.4); display: flex; align-items: center; justify-content: center; margin-bottom: 1.25rem; color: #fbbf24;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>
          </div>
          <h3 style="font-size: 1.25rem; font-weight: 700; margin-bottom: 0.6rem; color: #fff;" data-i18n="b2b_c4_title">Búsqueda Forense y Alertas en tu Central</h3>
          <p style="font-size: 0.92rem; color: var(--text-muted); line-height: 1.5;" data-i18n="b2b_c4_desc">
            Tus operadores no pierden horas mirando pantallas inactivas. Detección YOLOv11 en milisegundos y búsqueda forense en lenguaje natural para esclarecer incidentes al instante.
          </p>
        </div>
      </div>

      <!-- Banner de Alianza Comercial -->
      <div style="background: linear-gradient(135deg, rgba(13, 22, 45, 0.85) 0%, rgba(20, 32, 60, 0.75) 100%); border: 1px solid rgba(6, 182, 212, 0.3); border-radius: 20px; padding: 2.2rem 2.5rem; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1.5rem; box-shadow: 0 12px 35px rgba(0,0,0,0.5);">
        <div>
          <h4 style="font-size: 1.4rem; font-weight: 800; margin-bottom: 0.4rem; color: #fff;" data-i18n="b2b_banner_title">¿Sos dueño de una empresa de seguridad o central de monitoreo?</h4>
          <p style="color: var(--text-muted); font-size: 0.95rem; max-width: 680px;" data-i18n="b2b_banner_desc">
            Solicitá una demostración corporativa y conocé nuestro plan mayorista para equipar a todos tus abonados con tecnología de videovigilancia con IA.
          </p>
        </div>
        <button class="btn btn-primary" onclick="openContactModal('Alianza B2B Empresas de Seguridad')" style="padding: 0.9rem 1.8rem;">
          <span data-i18n="b2b_banner_btn">Solicitar Alianza para Empresas</span>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
        </button>
      </div>
    </div>
  </section>
"""

# Insert B2B section before section-pricing
target_pricing = '<section class="section-pricing" id="planes">'
if target_pricing in html:
    html = html.replace(target_pricing, b2b_section_html + "\n  " + target_pricing)
    print("Inserted B2B section successfully.")
else:
    print("WARNING: target_pricing not found.")

# 3. Update Pricing Section Header with Setup Fee Callout
pricing_header_old = """      <div class="section-header">
        <span class="section-tag" data-i18n="pricing_tag">TRANSPARENCIA TOTAL</span>
        <h2 class="section-title" data-i18n="pricing_title">Planes diseñados para cada escala</h2>
        <p class="section-desc" data-i18n="pricing_desc">
          Elegí la cobertura ideal para tu hogar, comercio o empresa. Todos los planes incluyen detección en tiempo real con IA.
        </p>
      </div>"""

pricing_header_new = """      <div class="section-header">
        <span class="section-tag" data-i18n="pricing_tag">TRANSPARENCIA TOTAL</span>
        <h2 class="section-title" data-i18n="pricing_title">Planes diseñados para cada escala</h2>
        <p class="section-desc" data-i18n="pricing_desc">
          Elegí la cobertura ideal para tu hogar, comercio o empresa. Todos los planes incluyen detección en tiempo real con IA.
        </p>
        <div class="pricing-setup-notice" style="margin-top: 1.25rem; display: inline-flex; align-items: center; gap: 0.6rem; background: rgba(6, 182, 212, 0.08); border: 1px solid rgba(6, 182, 212, 0.3); border-radius: 9999px; padding: 0.5rem 1.25rem; font-size: 0.85rem; color: #e2e8f0;">
          <span style="color: var(--cyan-bright); font-weight: 700;">💡 Onboarding & Activación:</span>
          <span data-i18n="pricing_setup_notice">Adelanto único por instalación y puesta en marcha de software: <strong>$300 USD (~$470.000 ARS)</strong></span>
        </div>
      </div>"""

html = html.replace(pricing_header_old, pricing_header_new)

# 4. Update Plan Features to mention the software setup fee
starter_features_old = """          <div class="plan-price-wrap">
            <span class="plan-currency" id="starterCurrSymbol">$</span>
            <span class="plan-amount" id="priceStarter">14.900</span>
            <span class="plan-period" id="starterPeriodLabel">ARS / mes</span>
          </div>"""

starter_features_new = """          <div class="plan-price-wrap">
            <span class="plan-currency" id="starterCurrSymbol">$</span>
            <span class="plan-amount" id="priceStarter">29.000</span>
            <span class="plan-period" id="starterPeriodLabel">ARS / mes</span>
          </div>
          <div style="font-size: 0.78rem; color: var(--cyan-bright); font-weight: 600; margin-top: -0.6rem; margin-bottom: 0.8rem;" data-i18n="plan_setup_sub">
            + $470.000 ARS ($300 USD) adelanto de software
          </div>"""

html = html.replace(starter_features_old, starter_features_new)

pro_features_old = """          <div class="plan-price-wrap">
            <span class="plan-currency" id="proCurrSymbol">$</span>
            <span class="plan-amount" id="pricePro">29.900</span>
            <span class="plan-period" id="proPeriodLabel">ARS / mes</span>
          </div>"""

pro_features_new = """          <div class="plan-price-wrap">
            <span class="plan-currency" id="proCurrSymbol">$</span>
            <span class="plan-amount" id="pricePro">59.000</span>
            <span class="plan-period" id="proPeriodLabel">ARS / mes</span>
          </div>
          <div style="font-size: 0.78rem; color: var(--cyan-bright); font-weight: 600; margin-top: -0.6rem; margin-bottom: 0.8rem;" data-i18n="plan_setup_sub">
            + $470.000 ARS ($300 USD) adelanto de software
          </div>"""

html = html.replace(pro_features_old, pro_features_new)

# Enterprise plan note
ent_old = """          <div class="plan-price-wrap">
            <span class="plan-amount" style="font-size: 2.1rem;">A Medida</span>
          </div>"""

ent_new = """          <div class="plan-price-wrap">
            <span class="plan-amount" style="font-size: 2.1rem;" data-i18n="ent_price">A Medida</span>
          </div>
          <div style="font-size: 0.78rem; color: var(--cyan-bright); font-weight: 600; margin-top: -0.6rem; margin-bottom: 0.8rem;" data-i18n="plan_setup_sub">
            + $470.000 ARS ($300 USD) adelanto de software
          </div>"""

html = html.replace(ent_old, ent_new)

# Save intermediate
with open("frontend/landing.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Updated landing HTML with B2B section and updated plan cards.")
