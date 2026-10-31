import os

file_path = 'frontend/landing.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add CSS for live-dolar-header-pill, live-pulse-dot, b2b styles
css_marker = '    /* SEGMENTED SWITCHER PILLS (CURRENCY & LANGUAGE) */'
css_to_add = '''    /* LIVE DOLAR BLUE BADGE & PULSE */
    .live-dolar-header-pill {
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      background: rgba(16, 185, 129, 0.08);
      border: 1px solid rgba(16, 185, 129, 0.28);
      border-radius: 9999px;
      padding: 0.32rem 0.65rem;
      font-size: 0.74rem;
      color: #34d399;
      white-space: nowrap;
      transition: all 0.2s ease;
    }
    .live-dolar-header-pill strong {
      color: #fff;
    }
    .live-pulse-dot {
      width: 6px;
      height: 6px;
      background: #10b981;
      border-radius: 50%;
      box-shadow: 0 0 8px #10b981;
      animation: pulse-dot 2s infinite;
      display: inline-block;
    }

    /* SEGMENTED SWITCHER PILLS (CURRENCY & LANGUAGE) */'''

assert css_marker in content, "css_marker not found"
content = content.replace(css_marker, css_to_add, 1)

# 2. Add header live dolar badge in nav-controls-suite
old_header_switchers = '''        <!-- Currency & Language Switchers (Desktop) -->
        <div class="desktop-switchers" style="display: flex; align-items: center; gap: 0.5rem;">
          <!-- Currency Switcher Pill -->
          <div class="segmented-pill" title="Cambiar moneda / Change currency">
            <button type="button" class="segmented-btn active" id="currBtnARS" onclick="setCurrency('ARS')">ARS</button>
            <button type="button" class="segmented-btn" id="currBtnUSD" onclick="setCurrency('USD')">USD</button>
          </div>

          <!-- Language Switcher Pill -->'''

new_header_switchers = '''        <!-- Currency & Language Switchers (Desktop) -->
        <div class="desktop-switchers" style="display: flex; align-items: center; gap: 0.5rem;">
          <!-- Currency Switcher Pill -->
          <div class="segmented-pill" title="Cambiar moneda / Change currency">
            <button type="button" class="segmented-btn active" id="currBtnARS" onclick="setCurrency('ARS')">ARS</button>
            <button type="button" class="segmented-btn" id="currBtnUSD" onclick="setCurrency('USD')">USD</button>
          </div>

          <!-- Live Dolar Blue Badge -->
          <div class="live-dolar-header-pill" id="headerDolarBadge" title="Cotización oficial en tiempo real Dólar Blue (DolarApi)">
            <span class="live-pulse-dot"></span>
            <span>Blue: <strong id="headerDolarRate">$1.565</strong></span>
          </div>

          <!-- Language Switcher Pill -->'''

assert old_header_switchers in content, "old_header_switchers not found"
content = content.replace(old_header_switchers, new_header_switchers, 1)

# 3. Add mobile live dolar badge in mobileDrawer
old_mobile_switchers = '''        <div class="mobile-switchers-group">
          <!-- Mobile Currency Switcher -->
          <div class="segmented-pill">
            <button type="button" class="segmented-btn active" id="currBtnARSMobile" onclick="setCurrency('ARS')">ARS</button>
            <button type="button" class="segmented-btn" id="currBtnUSDMobile" onclick="setCurrency('USD')">USD</button>
          </div>
          <!-- Mobile Language Switcher -->'''

new_mobile_switchers = '''        <div class="mobile-switchers-group">
          <!-- Mobile Currency Switcher -->
          <div class="segmented-pill">
            <button type="button" class="segmented-btn active" id="currBtnARSMobile" onclick="setCurrency('ARS')">ARS</button>
            <button type="button" class="segmented-btn" id="currBtnUSDMobile" onclick="setCurrency('USD')">USD</button>
          </div>
          <div class="live-dolar-header-pill" id="mobileDolarBadge">
            <span class="live-pulse-dot"></span>
            <span>Blue: <strong id="mobileDolarRate">$1.565</strong></span>
          </div>
          <!-- Mobile Language Switcher -->'''

assert old_mobile_switchers in content, "old_mobile_switchers not found"
content = content.replace(old_mobile_switchers, new_mobile_switchers, 1)

# 4. Replace B2B Section (#empresas-seguridad)
old_b2b_start = '  <section class="section-security-companies" id="empresas-seguridad"'
old_b2b_end = '  <section class="section-pricing" id="planes">'

idx_start = content.find(old_b2b_start)
idx_end = content.find(old_b2b_end)
assert idx_start != -1 and idx_end != -1, "B2B section boundaries not found"

new_b2b_section = '''  <section class="section-security-companies" id="empresas-seguridad" style="padding: 6rem 0; position: relative; border-top: 1px solid var(--border-subtle); border-bottom: 1px solid var(--border-subtle); background: radial-gradient(circle at 50% 30%, rgba(37, 99, 235, 0.08) 0%, transparent 70%);">
    <div class="container">
      <div class="section-header" style="text-align: center; max-width: 860px; margin: 0 auto 3.5rem;">
        <span class="section-tag" style="background: rgba(37, 99, 235, 0.15); border-color: rgba(37, 99, 235, 0.4); color: #60a5fa;" data-i18n="b2b_tag">SOLUCIÓN B2B PARA EMPRESAS DE SEGURIDAD & MONITOREO</span>
        <h2 class="section-title" style="font-size: 2.6rem; margin: 0.8rem 0;" data-i18n="b2b_title">Vendé Videovigilancia Forense con IA a tus Propios Clientes</h2>
        <p class="section-desc" style="font-size: 1.05rem; line-height: 1.6; color: var(--text-muted);" data-i18n="b2b_desc">
          Te proveemos la plataforma de software completa, tu propio panel máster multi-tenant y los servidores en la nube con IA pericial YOLOv11. Vos comercializás las cámaras e IA a tus clientes con tu propia marca o como partner oficial, con márgenes superiores al 500%.
        </p>
      </div>

      <!-- LAS 2 MODALIDADES DE IMPLEMENTACIÓN (SETUP INICIAL) -->
      <div class="b2b-setup-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1.75rem; margin-bottom: 2.5rem;">
        
        <!-- Opción 1: Implementación Partner Baddgroup -->
        <div class="b2b-tier-card" style="background: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: 20px; padding: 2.2rem 2rem; display: flex; flex-direction: column; justify-content: space-between; box-shadow: var(--shadow-card); transition: var(--transition-smooth);">
          <div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
              <span class="b2b-tier-badge badge-partner" style="background: rgba(37, 99, 235, 0.15); border: 1px solid rgba(37, 99, 235, 0.4); color: #60a5fa; padding: 0.3rem 0.8rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase;">CO-BRANDING • INICIO RÁPIDO</span>
            </div>
            <h3 style="font-size: 1.5rem; font-weight: 800; color: #fff; margin-bottom: 0.5rem;" data-i18n="b2b_opt1_title">Plataforma Baddgroup Partner</h3>
            <p style="font-size: 0.92rem; color: var(--text-muted); line-height: 1.5;" data-i18n="b2b_opt1_desc">
              Implementación del software donde vendés y ofrecés la IA respaldado por la plataforma Baddgroup Vision AI a tus abonados.
            </p>

            <div style="margin: 1.25rem 0; padding: 1.2rem; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px;">
              <div style="font-size: 0.78rem; text-transform: uppercase; color: var(--text-dim); font-weight: 700; letter-spacing: 0.05em;">Inversión Única de Implementación</div>
              <div style="display: flex; align-items: baseline; gap: 0.6rem; margin-top: 0.3rem;">
                <span style="font-size: 2.4rem; font-weight: 800; color: #fff; font-family: 'Plus Jakarta Sans', sans-serif;">$300 USD</span>
                <span id="b2bPartnerArs" style="font-size: 0.95rem; color: var(--cyan-bright); font-weight: 700;">(~$470.000 ARS)</span>
              </div>
              <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.2rem;">Pago único por despliegue de software, aprovisionamiento de servidor y capacitación técnica.</div>
            </div>

            <ul class="plan-features-list" style="margin-bottom: 1.5rem;">
              <li class="plan-feature-item">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
                <span><strong>Panel Máster Multi-Tenant:</strong> Administrá a todos tus clientes</span>
              </li>
              <li class="plan-feature-item">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
                <span>Cuentas independientes y aisladas para tus abonados</span>
              </li>
              <li class="plan-feature-item">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
                <span>Conexión de cámaras en 30 seg con Safety Code P2P</span>
              </li>
              <li class="plan-feature-item">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
                <span>Búsqueda forense con IA y detección de personas/autos</span>
              </li>
              <li class="plan-feature-item">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
                <span>Respaldo y soporte técnico pericial Baddgroup</span>
              </li>
            </ul>
          </div>

          <button class="btn btn-secondary" onclick="openContactModal('Implementación B2B Partner Baddgroup ($300 USD)')" style="width: 100%; justify-content: center;">
            <span data-i18n="b2b_opt1_btn">Solicitar Partner Baddgroup ($300 USD)</span>
          </button>
        </div>

        <!-- Opción 2: Marca Blanca / Plataforma Propia (White-Label) -->
        <div class="b2b-tier-card" style="background: linear-gradient(180deg, rgba(13, 25, 48, 0.95) 0%, rgba(8, 14, 26, 0.95) 100%); border: 1px solid rgba(6, 182, 212, 0.5); border-radius: 20px; padding: 2.2rem 2rem; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 0 35px rgba(6, 182, 212, 0.15); transition: var(--transition-smooth);">
          <div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
              <span class="b2b-tier-badge badge-whitelabel" style="background: rgba(6, 182, 212, 0.18); border: 1px solid rgba(6, 182, 212, 0.45); color: var(--cyan-bright); padding: 0.3rem 0.8rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; box-shadow: 0 0 12px rgba(6, 182, 212, 0.3);">MÁXIMA AUTONOMÍA • TU PROPIA EMPRESA</span>
            </div>
            <h3 style="font-size: 1.5rem; font-weight: 800; color: #fff; margin-bottom: 0.5rem;" data-i18n="b2b_opt2_title">Marca Blanca (Plataforma Propia)</h3>
            <p style="font-size: 0.92rem; color: var(--text-muted); line-height: 1.5;" data-i18n="b2b_opt2_desc">
              Tu propia plataforma con tu marca para proveer los servicios de instalación e IA de forma independiente como empresa/negocio frente a tus clientes (sin mención de Baddgroup).
            </p>

            <div style="margin: 1.25rem 0; padding: 1.2rem; background: rgba(6, 182, 212, 0.08); border: 1px solid rgba(6, 182, 212, 0.28); border-radius: 14px;">
              <div style="font-size: 0.78rem; text-transform: uppercase; color: var(--cyan-bright); font-weight: 700; letter-spacing: 0.05em;">Inversión Única Marca Blanca</div>
              <div style="display: flex; align-items: baseline; gap: 0.6rem; margin-top: 0.3rem;">
                <span style="font-size: 2.4rem; font-weight: 800; color: #fff; font-family: 'Plus Jakarta Sans', sans-serif;">$500 USD</span>
                <span id="b2bWhiteArs" style="font-size: 0.95rem; color: var(--cyan-bright); font-weight: 700;">(~$780.000 ARS)</span>
              </div>
              <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.2rem;">Pago único: Software personalizado con tu logo, paleta corporativa y dominio propio.</div>
            </div>

            <ul class="plan-features-list" style="margin-bottom: 1.5rem;">
              <li class="plan-feature-item">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
                <span><strong>100% tu Marca:</strong> Tu logo, nombre, favicon y colores</span>
              </li>
              <li class="plan-feature-item">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
                <span><strong>Dominio Propio:</strong> <code>seguridad.tuempresa.com</code></span>
              </li>
              <li class="plan-feature-item">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
                <span><strong>Cero mención de Baddgroup:</strong> Todo pertenece a tu negocio</span>
              </li>
              <li class="plan-feature-item">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
                <span><strong>Fijá tus propios precios:</strong> 100% de margen de ganancia</span>
              </li>
              <li class="plan-feature-item">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
                <span>Portal de clientes y reportes con la identidad de tu empresa</span>
              </li>
            </ul>
          </div>

          <button class="btn btn-primary" onclick="openContactModal('Implementación B2B Marca Blanca Propia ($500 USD)')" style="width: 100%; justify-content: center;">
            <span data-i18n="b2b_opt2_btn">Lanzar con Marca Blanca ($500 USD)</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
          </button>
        </div>

      </div>

      <!-- ESTRUCTURA DE ABONO MENSUAL SAAS Y MARGEN DE GANANCIA -->
      <div style="background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(13, 18, 30, 0.95) 100%); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 20px; padding: 2.2rem 2.2rem; margin-bottom: 2.5rem; box-shadow: 0 16px 40px rgba(0,0,0,0.5);">
        <div style="text-align: center; max-width: 780px; margin: 0 auto 2rem;">
          <span style="font-size: 0.8rem; font-weight: 800; color: #34d399; letter-spacing: 0.1em; text-transform: uppercase;">ABONO MENSUAL SAAS RECURRENTE • MÁXIMA ESCALABILIDAD</span>
          <h3 style="font-size: 1.8rem; font-weight: 800; color: #fff; margin: 0.4rem 0;" data-i18n="b2b_monthly_title">Estructura de Abono Mensual para la Empresa de Seguridad</h3>
          <p style="font-size: 0.95rem; color: var(--text-muted); line-height: 1.5;" data-i18n="b2b_monthly_desc">
            Pagás un costo base mínimo de plataforma y escalás por bloques de cámaras a un costo ultrabajo, asegurando un margen neto superior al 500% en cada cliente.
          </p>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1.5rem; margin-bottom: 1.75rem;">
          <!-- Bloque Base -->
          <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 1.5rem;">
            <div style="font-size: 0.78rem; font-weight: 700; color: #60a5fa; text-transform: uppercase;">1. Abono Base Mensual</div>
            <div style="font-size: 2.1rem; font-weight: 800; color: #fff; margin: 0.3rem 0;">$15 USD <span style="font-size: 0.9rem; font-weight: 500; color: var(--text-muted);">/ mes</span></div>
            <div id="b2bBaseMonthlyArs" style="font-size: 0.85rem; color: var(--cyan-bright); font-weight: 600; margin-bottom: 0.5rem;">(~$23.500 ARS/mes)</div>
            <p style="font-size: 0.86rem; color: var(--text-muted); line-height: 1.45;">Mantiene activo tu servidor en la nube, panel máster, backups automáticos y actualizaciones del motor de IA.</p>
          </div>

          <!-- Bloque Escala -->
          <div style="background: rgba(16, 185, 129, 0.05); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 14px; padding: 1.5rem;">
            <div style="font-size: 0.78rem; font-weight: 700; color: #34d399; text-transform: uppercase;">2. Escala de Cámaras con IA</div>
            <div style="font-size: 2.1rem; font-weight: 800; color: #fff; margin: 0.3rem 0;">+$50 USD <span style="font-size: 0.9rem; font-weight: 500; color: var(--text-muted);">/ 30 cámaras</span></div>
            <div id="b2bPer30CamsArs" style="font-size: 0.85rem; color: #34d399; font-weight: 600; margin-bottom: 0.5rem;">(~$78.000 ARS cada 30 cámaras)</div>
            <p style="font-size: 0.86rem; color: var(--text-muted); line-height: 1.45;">¡Cuesta solo <strong>$1.67 USD por cámara al mes</strong> para tu empresa! Vos le cobrás a tus abonados entre $10 y $25 USD por cámara.</p>
          </div>

          <!-- Proyección de Ganancia -->
          <div style="background: linear-gradient(135deg, rgba(6, 182, 212, 0.1) 0%, rgba(37, 99, 235, 0.12) 100%); border: 1px solid rgba(6, 182, 212, 0.35); border-radius: 14px; padding: 1.5rem;">
            <div style="font-size: 0.78rem; font-weight: 700; color: var(--cyan-bright); text-transform: uppercase;">3. Ejemplo de Rentabilidad Real</div>
            <div style="font-size: 1.15rem; font-weight: 800; color: #fff; margin: 0.3rem 0;">Con 30 Cámaras Vendidas:</div>
            <ul style="font-size: 0.84rem; color: var(--text-muted); line-height: 1.5; list-style: none; padding: 0; margin: 0.5rem 0 0;">
              <li>• Tu costo con nosotros: <strong style="color:#fff;">$65 USD/mes</strong> ($15 + $50)</li>
              <li>• Facturación a tus clientes: <strong style="color:#34d399;">$450 USD/mes</strong> ($15/cam)</li>
              <li style="margin-top: 0.35rem; padding-top: 0.35rem; border-top: 1px solid rgba(255,255,255,0.1); color: #fff; font-weight: 700;">
                Tu Ganancia Neta: <span style="color: var(--cyan-bright); font-size: 1rem;">+$385 USD/mes (+590% margen)</span>
              </li>
            </ul>
          </div>
        </div>

        <div style="text-align: center;">
          <button class="btn btn-primary" onclick="openContactModal('Alianza B2B Empresas de Seguridad')" style="padding: 0.9rem 2rem;">
            <span data-i18n="b2b_banner_btn">Solicitar Alianza y Demo para Empresas de Seguridad</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
          </button>
        </div>
      </div>

    </div>
  </section>

'''

content = content[:idx_start] + new_b2b_section + content[idx_end:]

# 5. Update pricing setup notice to include live dolar blue ticker
old_notice = '''        <div class="pricing-setup-notice" style="margin-top: 1.25rem; display: inline-flex; align-items: center; gap: 0.6rem; background: rgba(6, 182, 212, 0.08); border: 1px solid rgba(6, 182, 212, 0.3); border-radius: 9999px; padding: 0.5rem 1.25rem; font-size: 0.85rem; color: #e2e8f0;">
          <span style="color: var(--cyan-bright); font-weight: 700;">💡 Onboarding & Activación:</span>
          <span data-i18n="pricing_setup_notice">Adelanto único por instalación y puesta en marcha de software: <strong>$300 USD (~$470.000 ARS)</strong></span>
        </div>'''

new_notice = '''        <div class="pricing-setup-notice" style="margin-top: 1.25rem; display: inline-flex; align-items: center; gap: 0.75rem; background: rgba(6, 182, 212, 0.08); border: 1px solid rgba(6, 182, 212, 0.3); border-radius: 9999px; padding: 0.5rem 1.25rem; font-size: 0.85rem; color: #e2e8f0; flex-wrap: wrap; justify-content: center;">
          <span style="color: var(--cyan-bright); font-weight: 700;">💡 Onboarding & Activación:</span>
          <span>Adelanto único por instalación de software: <strong>$300 USD (<span id="setupNoticeARS">~$470.000 ARS</span>)</strong></span>
          <span style="color: rgba(255,255,255,0.2);">|</span>
          <span class="dolar-live-indicator" style="display: inline-flex; align-items: center; gap: 0.35rem; color: #34d399; font-size: 0.82rem;">
            <span class="live-pulse-dot"></span> Dólar Blue: <strong id="pricingDolarRate">$1.565 ARS</strong> (En vivo)
          </span>
        </div>'''

assert old_notice in content, "old_notice not found"
content = content.replace(old_notice, new_notice, 1)

# 6. Update plan cards setup subtext to use span for live ARS update
old_starter_sub = '''          <div style="font-size: 0.78rem; color: var(--cyan-bright); font-weight: 600; margin-top: -0.6rem; margin-bottom: 0.8rem;" data-i18n="plan_setup_sub">
            + $470.000 ARS ($300 USD) adelanto de software
          </div>'''

new_starter_sub = '''          <div style="font-size: 0.78rem; color: var(--cyan-bright); font-weight: 600; margin-top: -0.6rem; margin-bottom: 0.8rem;" class="dyn-setup-badge">
            + $300 USD (<span class="dyn-setup-ars">~$470.000 ARS</span>) adelanto de software
          </div>'''

# Replace in Starter, Pro, Enterprise
content = content.replace(old_starter_sub, new_starter_sub)

# Write back intermediate check
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Step 1 (HTML markup) updated successfully!")
