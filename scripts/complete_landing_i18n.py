import re

with open("frontend/landing.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update Hero section CTAs and data-i18n
hero_old = """        <div class="hero-cta-group">
          <a href="#planes" class="btn btn-primary" style="padding: 0.95rem 2rem; font-size: 1rem;">
            <span>Contratar Planes</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <line x1="7" y1="17" x2="17" y2="7"></line>
              <polyline points="7 7 17 7 17 17"></polyline>
            </svg>
          </a>

          <a href="/cameras" class="btn btn-secondary" style="padding: 0.95rem 1.8rem; font-size: 1rem;">
            <span>Ingresar a Gestión de Cámaras</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
              <line x1="8" y1="21" x2="16" y2="21"></line>
              <line x1="12" y1="17" x2="12" y2="21"></line>
            </svg>
          </a>
        </div>"""

hero_new = """        <div class="hero-cta-group">
          <a href="#planes" class="btn btn-primary" style="padding: 0.95rem 2rem; font-size: 1rem;">
            <span data-i18n="hero_cta_hire">Contratar Planes</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <line x1="7" y1="17" x2="17" y2="7"></line>
              <polyline points="7 7 17 7 17 17"></polyline>
            </svg>
          </a>

          <a href="/login?redirect=/cameras" id="heroPortalBtn" class="btn btn-secondary" style="padding: 0.95rem 1.8rem; font-size: 1rem;">
            <span data-i18n="hero_cta_portal">Ingresar a Gestión de Cámaras</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
              <line x1="8" y1="21" x2="16" y2="21"></line>
              <line x1="12" y1="17" x2="12" y2="21"></line>
            </svg>
          </a>
        </div>"""

if hero_old in html:
    html = html.replace(hero_old, hero_new)
    print("Replaced hero CTA successfully.")
else:
    print("WARNING: hero_old not found exactly.")

# 2. Update Active Portal Banner CTA
portal_old = """          <div class="portal-banner-actions">
            <a href="/cameras" class="btn btn-primary" style="padding: 0.9rem 1.8rem;">
              <span>Ingresar a Gestión de Cámaras</span>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="7" y1="17" x2="17" y2="7"></line><polyline points="7 7 17 7 17 17"></polyline></svg>
            </a>

            <a href="/crm" class="btn btn-secondary" style="padding: 0.9rem 1.6rem;">
              <span>Panel CRM Administradores</span>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
            </a>
          </div>"""

portal_new = """          <div class="portal-banner-actions">
            <a href="/login?redirect=/cameras" id="bannerPortalBtn" class="btn btn-primary" style="padding: 0.9rem 1.8rem;">
              <span data-i18n="portal_cta_cams">Ingresar a Gestión de Cámaras</span>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="7" y1="17" x2="17" y2="7"></line><polyline points="7 7 17 7 17 17"></polyline></svg>
            </a>

            <a href="/login?redirect=/crm" id="bannerCrmBtn" class="btn btn-secondary" style="padding: 0.9rem 1.6rem;">
              <span data-i18n="portal_cta_crm">Panel CRM Administradores</span>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
            </a>
          </div>"""

if portal_old in html:
    html = html.replace(portal_old, portal_new)
    print("Replaced portal banner CTA successfully.")
else:
    print("WARNING: portal_old not found exactly.")

# 3. Update Pricing Cards for Currency
pricing_starter_old = """          <div class="plan-price-wrap">
            <span class="plan-currency">$</span>
            <span class="plan-amount" id="priceStarter">14.900</span>
            <span class="plan-period">ARS / mes</span>
          </div>"""

pricing_starter_new = """          <div class="plan-price-wrap">
            <span class="plan-currency" id="starterCurrSymbol">$</span>
            <span class="plan-amount" id="priceStarter">14.900</span>
            <span class="plan-period" id="starterPeriodLabel">ARS / mes</span>
          </div>"""

pricing_pro_old = """          <div class="plan-price-wrap">
            <span class="plan-currency">$</span>
            <span class="plan-amount" id="pricePro">29.900</span>
            <span class="plan-period">ARS / mes</span>
          </div>"""

pricing_pro_new = """          <div class="plan-price-wrap">
            <span class="plan-currency" id="proCurrSymbol">$</span>
            <span class="plan-amount" id="pricePro">29.900</span>
            <span class="plan-period" id="proPeriodLabel">ARS / mes</span>
          </div>"""

if pricing_starter_old in html and pricing_pro_old in html:
    html = html.replace(pricing_starter_old, pricing_starter_new)
    html = html.replace(pricing_pro_old, pricing_pro_new)
    print("Replaced pricing cards currency wrappers successfully.")
else:
    print("WARNING: pricing old blocks not found.")

# Save intermediate
with open("frontend/landing.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Step 2 completed.")
