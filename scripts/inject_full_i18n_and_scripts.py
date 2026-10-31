import re
import json

with open("frontend/landing.html", "r", encoding="utf-8") as f:
    html = f.read()

# Let's verify and inject data-i18n tags on the various sections of HTML:

# 1. Hero Title & Subtitle
html = html.replace(
    '<span class="dot"></span>\n          <span>Plataforma de Videovigilancia Inteligente • Algoritmos YOLOv11 & Visión Forense</span>',
    '<span class="dot"></span>\n          <span data-i18n="hero_badge">Plataforma de Videovigilancia Inteligente • Algoritmos YOLOv11 & Visión Forense</span>'
)

html = html.replace(
    'De Cámaras Pasivas a <br>\n          <span class="gradient-text">Seguridad Inteligente en Tiempo Real.</span>',
    '<span data-i18n="hero_title_p1">De Cámaras Pasivas a</span> <br>\n          <span class="gradient-text" data-i18n="hero_title_p2">Seguridad Inteligente en Tiempo Real.</span>'
)

html = html.replace(
    '<p class="hero-subtitle">\n          Explicá el valor. Llevá al usuario a probarlo. Monitoreo preventivo 24/7 con detección de personas, \n          vehículos y conductas en milisegundos, búsqueda forense en lenguaje natural y compatibilidad \n          con cualquier cámara IP sin cambiar tu equipamiento.\n        </p>',
    '<p class="hero-subtitle" data-i18n="hero_subtitle">\n          Explicá el valor. Llevá al usuario a probarlo. Monitoreo preventivo 24/7 con detección de personas, \n          vehículos y conductas en milisegundos, búsqueda forense en lenguaje natural y compatibilidad \n          con cualquier cámara IP sin cambiar tu equipamiento.\n        </p>'
)

# 2. Hero Trust Strip
html = html.replace(
    'Compatible con Dahua, Hikvision, IMOU y RTSP',
    '<span data-i18n="hero_trust_compat">Compatible con Dahua, Hikvision, IMOU y RTSP</span>'
)
html = html.replace(
    'Conexión en 1 minuto vía Safety Code',
    '<span data-i18n="hero_trust_safety">Conexión en 1 minuto vía Safety Code</span>'
)
html = html.replace(
    'Servidores Cloud DonWeb con Latencia &lt; 15ms',
    '<span data-i18n="hero_trust_cloud">Servidores Cloud DonWeb con Latencia &lt; 15ms</span>'
)

# 3. Mockup Topbar & Metrics
html = html.replace(
    '<span>Cámara 1: Entrada Principal [Safety Code: BG-SEC-01]</span>',
    '<span data-i18n="mockup_cam_title">Cámara 1: Entrada Principal [Canal P2P Encriptado]</span>'
)
html = html.replace(
    '<span>STREAM EN VIVO • 15 FPS</span>',
    '<span data-i18n="mockup_live_stream">STREAM EN VIVO • 15 FPS</span>'
)
html = html.replace(
    '<span>YOLOv11 TRACKING ACTIVO</span>',
    '<span data-i18n="mockup_yolo_active">YOLOv11 TRACKING ACTIVO</span>'
)

# Metrics labels & deltas
html = html.replace(
    '<div class="metric-label">Cámaras Conectadas</div>',
    '<div class="metric-label" data-i18n="m1_label">Cámaras Conectadas</div>'
)
html = html.replace(
    '<span>4 Activas</span>',
    '<span data-i18n="m1_val">4 Activas</span>'
)
html = html.replace(
    '<div class="metric-label">Eventos Analizados Hoy</div>',
    '<div class="metric-label" data-i18n="m2_label">Eventos Analizados Hoy</div>'
)
html = html.replace(
    '<span class="metric-delta">0 Falsos Positivos</span>',
    '<span class="metric-delta" data-i18n="m2_delta">0 Falsos Positivos</span>'
)
html = html.replace(
    '<div class="metric-label">Velocidad Búsqueda Forense</div>',
    '<div class="metric-label" data-i18n="m3_label">Velocidad Búsqueda Forense</div>'
)
html = html.replace(
    '<span class="metric-delta">Lenguaje Natural</span>',
    '<span class="metric-delta" data-i18n="m3_delta">Lenguaje Natural</span>'
)
html = html.replace(
    '<div class="metric-label">Consumo de Red & CPU</div>',
    '<div class="metric-label" data-i18n="m4_label">Consumo de Red & CPU</div>'
)

# AI Panel
html = html.replace(
    '<span>Búsqueda Forense con IA en Tiempo Real</span>',
    '<span data-i18n="ai_search_title">Búsqueda Forense con IA en Tiempo Real</span>'
)
html = html.replace(
    '<button class="btn btn-primary" style="padding: 0.35rem 0.85rem; font-size: 0.74rem;" onclick="runDemoSearch()">Buscar</button>',
    '<button class="btn btn-primary" style="padding: 0.35rem 0.85rem; font-size: 0.74rem;" onclick="runDemoSearch()" data-i18n="ai_search_btn">Buscar</button>'
)
html = html.replace(
    '<span style="font-size: 0.72rem; color: var(--text-dim); font-weight: 600;">PROBÁ ESTAS CONSULTAS EN VIVO:</span>',
    '<span style="font-size: 0.72rem; color: var(--text-dim); font-weight: 600;" data-i18n="ai_chips_title">PROBÁ ESTAS CONSULTAS EN VIVO:</span>'
)

# Section ¿De qué trata?
html = html.replace(
    '<span class="section-tag">EL VALOR REAL PARA TU CLIENTE</span>',
    '<span class="section-tag" data-i18n="comp_tag">EL VALOR REAL PARA TU CLIENTE</span>'
)
html = html.replace(
    '<h2 class="section-title">¿Por qué cambiar el paradigma de la seguridad?</h2>',
    '<h2 class="section-title" data-i18n="comp_title">¿Por qué cambiar el paradigma de la seguridad?</h2>'
)
html = html.replace(
    '<p class="section-desc">\n          Las cámaras tradicionales solo sirven para ver qué pasó después del robo. Baddgroup Vision AI \n          convierte tu sistema en un detector proactivo con análisis en milisegundos y búsqueda forense inmediata.\n        </p>',
    '<p class="section-desc" data-i18n="comp_desc">\n          Las cámaras tradicionales solo sirven para ver qué pasó después del robo. Baddgroup Vision AI \n          convierte tu sistema en un detector proactivo con análisis en milisegundos y búsqueda forense inmediata.\n        </p>'
)

html = html.replace(
    '<div class="comparison-title">Cámaras Tradicionales (El Pasado)</div>',
    '<div class="comparison-title" data-i18n="trad_title">Cámaras Tradicionales (El Pasado)</div>'
)
html = html.replace(
    '<div style="font-size: 0.78rem; color: #ef4444; font-weight: 600;">GRABACIÓN CIEGA Y PASIVA</div>',
    '<div style="font-size: 0.78rem; color: #ef4444; font-weight: 600;" data-i18n="trad_badge">GRABACIÓN CIEGA Y PASIVA</div>'
)

html = html.replace(
    '<div class="comparison-title">Baddgroup Vision AI (La Nueva Era)</div>',
    '<div class="comparison-title" data-i18n="badd_title">Baddgroup Vision AI (La Nueva Era)</div>'
)
html = html.replace(
    '<div style="font-size: 0.78rem; color: var(--cyan-bright); font-weight: 700;">INTELIGENCIA ARTIFICIAL EN TIEMPO REAL</div>',
    '<div style="font-size: 0.78rem; color: var(--cyan-bright); font-weight: 700;" data-i18n="badd_badge">INTELIGENCIA ARTIFICIAL EN TIEMPO REAL</div>'
)

# Section Cómo Contratar
html = html.replace(
    '<span class="section-tag">DOS MODALIDADES A TU MEDIDA</span>',
    '<span class="section-tag" data-i18n="hire_tag">DOS MODALIDADES A TU MEDIDA</span>'
)
html = html.replace(
    '<h2 class="section-title">Elegí cómo comenzar con Baddgroup</h2>',
    '<h2 class="section-title" data-i18n="hire_title">Elegí cómo comenzar con Baddgroup</h2>'
)
html = html.replace(
    '<p class="section-desc">\n          Ya sea que tengas cámaras existentes instaladas o necesites un proyecto integral desde cero, \n          Baddgroup tiene la solución adecuada para tu empresa o residencia.\n        </p>',
    '<p class="section-desc" data-i18n="hire_desc">\n          Ya sea que tengas cámaras existentes instaladas o necesites un proyecto integral desde cero, \n          Baddgroup tiene la solución adecuada para tu empresa o residencia.\n        </p>'
)

# Section Planes y Precios
html = html.replace(
    '<span class="section-tag">TRANSPARENCIA TOTAL</span>',
    '<span class="section-tag" data-i18n="pricing_tag">TRANSPARENCIA TOTAL</span>'
)
html = html.replace(
    '<h2 class="section-title">Planes diseñados para cada escala</h2>',
    '<h2 class="section-title" data-i18n="pricing_title">Planes diseñados para cada escala</h2>'
)
html = html.replace(
    '<p class="section-desc">\n          Elegí la cobertura ideal para tu hogar, comercio o empresa. Todos los planes incluyen detección en tiempo real con IA.\n        </p>',
    '<p class="section-desc" data-i18n="pricing_desc">\n          Elegí la cobertura ideal para tu hogar, comercio o empresa. Todos los planes incluyen detección en tiempo real con IA.\n        </p>'
)

html = html.replace(
    '<span class="billing-label active" id="labelMonthly" onclick="setBillingPeriod(\'monthly\')">Facturación Mensual</span>',
    '<span class="billing-label active" id="labelMonthly" onclick="setBillingPeriod(\'monthly\')" data-i18n="billing_monthly">Facturación Mensual</span>'
)
html = html.replace(
    '<span class="discount-badge">2 Meses Bonificados (-20%)</span>',
    '<span class="discount-badge" id="discountBadgeText" data-i18n="billing_discount">2 Meses Bonificados (-20%)</span>'
)

# Section Calculadora
html = html.replace(
    '<span class="section-tag">SIMULADOR EN TIEMPO REAL</span>',
    '<span class="section-tag" data-i18n="calc_tag">SIMULADOR EN TIEMPO REAL</span>'
)
html = html.replace(
    '<h2 style="font-size: 2rem; font-weight: 800; margin-bottom: 0.75rem;">Calculá tu Presupuesto</h2>',
    '<h2 style="font-size: 2rem; font-weight: 800; margin-bottom: 0.75rem;" data-i18n="calc_title">Calculá tu Presupuesto</h2>'
)
html = html.replace(
    '<p style="font-size: 0.95rem; color: var(--text-muted); line-height: 1.5;">\n            Deslizá la cantidad de cámaras y configurá si requerís instalación física para ver el valor estimado.\n          </p>',
    '<p style="font-size: 0.95rem; color: var(--text-muted); line-height: 1.5;" data-i18n="calc_desc">\n            Deslizá la cantidad de cámaras y configurá si requerís instalación física para ver el valor estimado.\n          </p>'
)
html = html.replace(
    '<span>Cantidad de Cámaras:</span>',
    '<span data-i18n="calc_cams_label">Cantidad de Cámaras:</span>'
)
html = html.replace(
    '<span>Incluir provisión de cámaras 2K e instalación física profesional</span>',
    '<span data-i18n="calc_install_check">Incluir provisión de cámaras 2K e instalación física profesional</span>'
)
html = html.replace(
    '<div class="quote-title">Abono Mensual Estimado</div>',
    '<div class="quote-title" data-i18n="calc_quote_title">Abono Mensual Estimado</div>'
)
html = html.replace(
    '<span>Pedir Cotización Formal</span>',
    '<span data-i18n="calc_quote_cta">Pedir Cotización Formal</span>'
)

# Section Portal Banner
html = html.replace(
    '<span class="dot"></span>\n            <span>PORTAL DE MONITOREO ACTIVO</span>',
    '<span class="dot"></span>\n            <span data-i18n="portal_tag">PORTAL DE MONITOREO ACTIVO</span>'
)
html = html.replace(
    '<h2 class="portal-banner-title">¿Ya sos cliente o querés probar la plataforma?</h2>',
    '<h2 class="portal-banner-title" data-i18n="portal_title">¿Ya sos cliente o querés probar la plataforma?</h2>'
)
html = html.replace(
    '<p class="portal-banner-desc">\n            Accedé ahora al panel centralizado de Baddgroup. Visualizá tus cámaras en tiempo real, \n            configurá nuevos códigos Safety Code de cámaras y utilizá el buscador con IA.\n          </p>',
    '<p class="portal-banner-desc" data-i18n="portal_desc">\n            Accedé ahora al panel centralizado de Baddgroup. Visualizá tus cámaras en tiempo real, \n            configurá nuevos códigos Safety Code de cámaras y utilizá el buscador con IA.\n          </p>'
)
html = html.replace(
    '<span>Autenticación Segura JWT • Cifrado de Punta a Punta • Base de Datos Supabase</span>',
    '<span data-i18n="portal_badge_security">Autenticación Segura JWT • Cifrado de Punta a Punta • Base de Datos Supabase</span>'
)

# Section FAQ
html = html.replace(
    '<span class="section-tag">DUDAS RESUELTAS</span>',
    '<span class="section-tag" data-i18n="faq_tag">DUDAS RESUELTAS</span>'
)
html = html.replace(
    '<h2 class="section-title">Preguntas Frecuentes</h2>',
    '<h2 class="section-title" data-i18n="faq_title">Preguntas Frecuentes</h2>'
)
html = html.replace(
    '<p class="section-desc">Todo lo que necesitás saber antes de dar el salto a Baddgroup Vision AI.</p>',
    '<p class="section-desc" data-i18n="faq_desc">Todo lo que necesitás saber antes de dar el salto a Baddgroup Vision AI.</p>'
)

# Footer link
html = html.replace(
    '<a href="/login" style="color: var(--cyan-bright); text-decoration: none; font-weight: 600;">Ingreso a Gestión de Cámaras</a>',
    '<a href="/login?redirect=/cameras" id="footerPortalBtn" style="color: var(--cyan-bright); text-decoration: none; font-weight: 600;" data-i18n="footer_portal_link">Ingreso a Gestión de Cámaras</a>'
)

# Now, let's prepare the comprehensive <script> section:
script_start = html.find('<script>')
if script_start != -1:
    before_script = html[:script_start]
else:
    raise Exception("Could not find <script> tag")

new_script = """<script>
    // ==========================================================================
    // ESTADO GLOBAL: IDIOMA, MONEDA, FACTURACIÓN Y AUTENTICACIÓN
    // ==========================================================================
    let currentLang = localStorage.getItem("baddgroup_lang") || "es";
    let currentCurrency = localStorage.getItem("baddgroup_currency") || "ARS";
    let currentBilling = "monthly";

    // Diccionario de Precios y Cotizador por Moneda
    const PRICING_DATA = {
      ARS: {
        symbol: "$",
        code: "ARS",
        periodMonth: "ARS / mes",
        periodAnnual: "ARS / mes (anual)",
        starterMonth: "14.900",
        starterAnnual: "11.900",
        proMonth: "29.900",
        proAnnual: "23.900",
        calcBaseMonth: 7500,
        calcBaseAnnual: 6200,
        calcInstallPerCam: 65000,
        formatPrice: (n) => `$${n.toLocaleString('es-AR')}`,
        calcDescHardware: (monthly, equip) => `Abono mensual con IA: <strong>$${monthly.toLocaleString('es-AR')} ARS</strong><br>+ Instalación y provisión llave en mano: <strong>$${equip.toLocaleString('es-AR')} ARS</strong> (pago único)`,
        calcDescSoftware: () => `Aprovechando tus cámaras actuales (Solo Software SaaS). Incluye detección continua con IA y 30 días de grabaciones.`
      },
      USD: {
        symbol: "$",
        code: "USD",
        periodMonth: "USD / mo",
        periodAnnual: "USD / mo (annual)",
        starterMonth: "15",
        starterAnnual: "12",
        proMonth: "29",
        proAnnual: "24",
        calcBaseMonth: 8,
        calcBaseAnnual: 6,
        calcInstallPerCam: 65,
        formatPrice: (n) => `$${n.toLocaleString('en-US')} USD`,
        calcDescHardware: (monthly, equip) => `Monthly AI fee: <strong>$${monthly.toLocaleString('en-US')} USD</strong><br>+ Turnkey hardware & installation: <strong>$${equip.toLocaleString('en-US')} USD</strong> (one-time fee)`,
        calcDescSoftware: () => `Using your existing IP cameras (SaaS Software Only). Includes continuous AI detection and 30-day cloud recordings.`
      }
    };

    // Diccionario de Traducción Internacional (Español como principal, Inglés alternable)
    const I18N = {
      es: {
        page_title: "Baddgroup Vision AI | Plataforma de Videovigilancia Inteligente y Búsqueda Forense con IA",
        nav_about: "¿De qué trata?",
        nav_hire: "Cómo Contratar",
        nav_pricing: "Planes & Precios",
        nav_calculator: "Cotizador",
        nav_faq: "Preguntas",
        nav_demo: "Ver Demo",
        nav_client_login: "Acceso Clientes",
        nav_my_cameras: "Mis Cámaras",
        nav_crm_panel: "Panel CRM (Admin)",

        hero_badge: "Plataforma de Videovigilancia Inteligente • Algoritmos YOLOv11 & Visión Forense",
        hero_title_p1: "De Cámaras Pasivas a",
        hero_title_p2: "Seguridad Inteligente en Tiempo Real.",
        hero_subtitle: "Explicá el valor. Llevá al usuario a probarlo. Monitoreo preventivo 24/7 con detección de personas, vehículos y conductas en milisegundos, búsqueda forense en lenguaje natural y compatibilidad con cualquier cámara IP sin cambiar tu equipamiento.",
        hero_cta_hire: "Contratar Planes",
        hero_cta_portal: "Ingresar a Gestión de Cámaras",
        hero_trust_compat: "Compatible con Dahua, Hikvision, IMOU y RTSP",
        hero_trust_safety: "Conexión en 1 minuto vía Safety Code",
        hero_trust_cloud: "Servidores Cloud DonWeb con Latencia < 15ms",

        mockup_cam_title: "Cámara 1: Entrada Principal [Canal P2P Encriptado]",
        mockup_live_stream: "STREAM EN VIVO • 15 FPS",
        mockup_yolo_active: "YOLOv11 TRACKING ACTIVO",
        m1_label: "Cámaras Conectadas",
        m1_val: "4 Activas",
        m2_label: "Eventos Analizados Hoy",
        m2_delta: "0 Falsos Positivos",
        m3_label: "Velocidad Búsqueda Forense",
        m3_delta: "Lenguaje Natural",
        m4_label: "Consumo de Red & CPU",
        ai_search_title: "Búsqueda Forense con IA en Tiempo Real",
        ai_search_btn: "Buscar",
        ai_chips_title: "PROBÁ ESTAS CONSULTAS EN VIVO:",

        comp_tag: "EL VALOR REAL PARA TU CLIENTE",
        comp_title: "¿Por qué cambiar el paradigma de la seguridad?",
        comp_desc: "Las cámaras tradicionales solo sirven para ver qué pasó después del robo. Baddgroup Vision AI convierte tu sistema en un detector proactivo con análisis en milisegundos y búsqueda forense inmediata.",
        trad_title: "Cámaras Tradicionales (El Pasado)",
        trad_badge: "GRABACIÓN CIEGA Y PASIVA",
        badd_title: "Baddgroup Vision AI (La Nueva Era)",
        badd_badge: "INTELIGENCIA ARTIFICIAL EN TIEMPO REAL",

        hire_tag: "DOS MODALIDADES A TU MEDIDA",
        hire_title: "Elegí cómo comenzar con Baddgroup",
        hire_desc: "Ya sea que tengas cámaras existentes instaladas o necesites un proyecto integral desde cero, Baddgroup tiene la solución adecuada para tu empresa o residencia.",

        pricing_tag: "TRANSPARENCIA TOTAL",
        pricing_title: "Planes diseñados para cada escala",
        pricing_desc: "Elegí la cobertura ideal para tu hogar, comercio o empresa. Todos los planes incluyen detección en tiempo real con IA.",
        billing_monthly: "Facturación Mensual",
        billing_discount: "2 Meses Bonificados (-20%)",

        calc_tag: "SIMULADOR EN TIEMPO REAL",
        calc_title: "Calculá tu Presupuesto",
        calc_desc: "Deslizá la cantidad de cámaras y configurá si requerís instalación física para ver el valor estimado.",
        calc_cams_label: "Cantidad de Cámaras:",
        calc_install_check: "Incluir provisión de cámaras 2K e instalación física profesional",
        calc_quote_title: "Abono Mensual Estimado",
        calc_quote_cta: "Pedir Cotización Formal",

        portal_tag: "PORTAL DE MONITOREO ACTIVO",
        portal_title: "¿Ya sos cliente o querés probar la plataforma?",
        portal_desc: "Accedé ahora al panel centralizado de Baddgroup. Visualizá tus cámaras en tiempo real, configurá nuevos códigos Safety Code de cámaras y utilizá el buscador con IA.",
        portal_cta_cams: "Ingresar a Gestión de Cámaras",
        portal_cta_crm: "Panel CRM Administradores",
        portal_badge_security: "Autenticación Segura JWT • Cifrado de Punta a Punta • Base de Datos Supabase",

        faq_tag: "DUDAS RESUELTAS",
        faq_title: "Preguntas Frecuentes",
        faq_desc: "Todo lo que necesitás saber antes de dar el salto a Baddgroup Vision AI.",
        footer_portal_link: "Ingreso a Gestión de Cámaras"
      },
      en: {
        page_title: "Baddgroup Vision AI | Intelligent Video Surveillance & Forensic AI Search Platform",
        nav_about: "What is it?",
        nav_hire: "How to Hire",
        nav_pricing: "Plans & Pricing",
        nav_calculator: "Calculator",
        nav_faq: "FAQ",
        nav_demo: "Watch Demo",
        nav_client_login: "Client Access",
        nav_my_cameras: "My Cameras",
        nav_crm_panel: "CRM Panel (Admin)",

        hero_badge: "Intelligent Video Surveillance Platform • YOLOv11 & Forensic Vision AI",
        hero_title_p1: "From Passive Cameras to",
        hero_title_p2: "Real-Time Intelligent Security.",
        hero_subtitle: "Proactive 24/7 surveillance with millisecond detection of persons, vehicles, and behaviors, conversational forensic search, and universal compatibility with any IP camera without replacing equipment.",
        hero_cta_hire: "Explore Plans",
        hero_cta_portal: "Access Cameras Portal",
        hero_trust_compat: "Compatible with Dahua, Hikvision, IMOU & RTSP",
        hero_trust_safety: "1-minute setup via Safety Code",
        hero_trust_cloud: "DonWeb Cloud Servers with < 15ms Latency",

        mockup_cam_title: "Camera 1: Main Entrance [Encrypted P2P Channel]",
        mockup_live_stream: "LIVE STREAM • 15 FPS",
        mockup_yolo_active: "YOLOv11 TRACKING ACTIVE",
        m1_label: "Connected Cameras",
        m1_val: "4 Active",
        m2_label: "Events Analyzed Today",
        m2_delta: "0 False Positives",
        m3_label: "Forensic Search Speed",
        m3_delta: "Natural Language",
        m4_label: "Network & CPU Load",
        ai_search_title: "Real-Time AI Forensic Search",
        ai_search_btn: "Search",
        ai_chips_title: "TRY THESE LIVE PROMPTS:",

        comp_tag: "REAL VALUE FOR YOUR SECURITY",
        comp_title: "Why change the security paradigm?",
        comp_desc: "Traditional cameras only help see what happened after a crime. Baddgroup Vision AI turns your system into a proactive detector with millisecond analysis and instant forensic search.",
        trad_title: "Traditional Cameras (The Past)",
        trad_badge: "BLIND & PASSIVE RECORDING",
        badd_title: "Baddgroup Vision AI (The New Era)",
        badd_badge: "REAL-TIME ARTIFICIAL INTELLIGENCE",

        hire_tag: "TWO TAILORED OPTIONS",
        hire_title: "Choose how to start with Baddgroup",
        hire_desc: "Whether you already have cameras installed or need a complete turnkey project from scratch, Baddgroup has the right solution for your home or enterprise.",

        pricing_tag: "TOTAL TRANSPARENCY",
        pricing_title: "Plans tailored for every scale",
        pricing_desc: "Choose the ideal coverage for your residence, store or enterprise. All plans include real-time YOLOv11 AI detection.",
        billing_monthly: "Monthly Billing",
        billing_discount: "2 Months Free (-20%)",

        calc_tag: "REAL-TIME ESTIMATOR",
        calc_title: "Estimate Your Budget",
        calc_desc: "Slide camera count and select if you need professional installation to see the estimated investment.",
        calc_cams_label: "Camera Count:",
        calc_install_check: "Include 2K cameras & professional turnkey installation",
        calc_quote_title: "Estimated Monthly Fee",
        calc_quote_cta: "Request Official Quote",

        portal_tag: "ACTIVE MONITORING PORTAL",
        portal_title: "Already a client or ready to test the platform?",
        portal_desc: "Access the centralized Baddgroup dashboard. View your cameras live, configure cameras securely and experience real-time forensic search.",
        portal_cta_cams: "Access Cameras Portal",
        portal_cta_crm: "Admin CRM Panel",
        portal_badge_security: "Secure JWT Authentication • End-to-End Encryption • Supabase Cloud Database",

        faq_tag: "FREQUENTLY ASKED",
        faq_title: "Frequently Asked Questions",
        faq_desc: "Everything you need to know before stepping up to Baddgroup Vision AI.",
        footer_portal_link: "Access Cameras Portal"
      }
    };

    // 1. Reloj en vivo para el OSD
    function updateClock() {
      const now = new Date();
      const pad = (n) => String(n).padStart(2, '0');
      const y = now.getFullYear();
      const m = pad(now.getMonth() + 1);
      const d = pad(now.getDate());
      const h = pad(now.getHours());
      const min = pad(now.getMinutes());
      const s = pad(now.getSeconds());
      const clockEl = document.getElementById('liveOsdClock');
      if (clockEl) {
        clockEl.textContent = `${y}-${m}-${d} ${h}:${min}:${s}`;
      }
    }
    setInterval(updateClock, 1000);
    updateClock();

    // 2. Control de Idioma (ES / EN)
    function setLanguage(lang) {
      currentLang = (lang === 'en') ? 'en' : 'es';
      localStorage.setItem("baddgroup_lang", currentLang);
      document.documentElement.lang = currentLang;

      // Actualizar botones de switchers
      document.querySelectorAll('#langBtnES, #langBtnESMobile').forEach(el => el.classList.toggle('active', currentLang === 'es'));
      document.querySelectorAll('#langBtnEN, #langBtnENMobile').forEach(el => el.classList.toggle('active', currentLang === 'en'));

      // Reemplazar textos con data-i18n
      const dict = I18N[currentLang] || I18N.es;
      document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (dict[key]) {
          el.textContent = dict[key];
        }
      });

      if (dict.page_title) {
        document.title = dict.page_title;
      }

      // Actualizar textos dinámicos dependientes
      updateNavAuthStatus();
      updateBillingPeriodUI();
      updateCalculator();
    }

    // 3. Control de Moneda (ARS / USD)
    function setCurrency(curr) {
      currentCurrency = (curr === 'USD') ? 'USD' : 'ARS';
      localStorage.setItem("baddgroup_currency", currentCurrency);

      // Actualizar botones
      document.querySelectorAll('#currBtnARS, #currBtnARSMobile').forEach(el => el.classList.toggle('active', currentCurrency === 'ARS'));
      document.querySelectorAll('#currBtnUSD, #currBtnUSDMobile').forEach(el => el.classList.toggle('active', currentCurrency === 'USD'));

      // Actualizar tarjetas de planes
      updateBillingPeriodUI();
      updateCalculator();
    }

    // 4. Selector Mensual / Anual
    function toggleBillingPeriod() {
      setBillingPeriod(currentBilling === 'monthly' ? 'annual' : 'monthly');
    }

    function setBillingPeriod(period) {
      currentBilling = period;
      const toggle = document.getElementById('billingToggle');
      const lMonthly = document.getElementById('labelMonthly');
      const lAnnual = document.getElementById('labelAnnual');

      if (period === 'annual') {
        if (toggle) toggle.classList.add('annual');
        if (lAnnual) lAnnual.classList.add('active');
        if (lMonthly) lMonthly.classList.remove('active');
      } else {
        if (toggle) toggle.classList.remove('annual');
        if (lMonthly) lMonthly.classList.add('active');
        if (lAnnual) lAnnual.classList.remove('active');
      }
      updateBillingPeriodUI();
      updateCalculator();
    }

    function updateBillingPeriodUI() {
      const cfg = PRICING_DATA[currentCurrency] || PRICING_DATA.ARS;
      const pStarter = document.getElementById('priceStarter');
      const pPro = document.getElementById('pricePro');
      const sLabel = document.getElementById('starterPeriodLabel');
      const pLabel = document.getElementById('proPeriodLabel');
      const sSym = document.getElementById('starterCurrSymbol');
      const pSym = document.getElementById('proCurrSymbol');

      if (sSym) sSym.textContent = cfg.symbol;
      if (pSym) pSym.textContent = cfg.symbol;

      const isAnnual = currentBilling === 'annual';
      if (pStarter) pStarter.textContent = isAnnual ? cfg.starterAnnual : cfg.starterMonth;
      if (pPro) pPro.textContent = isAnnual ? cfg.proAnnual : cfg.proMonth;

      const label = isAnnual ? cfg.periodAnnual : cfg.periodMonth;
      if (sLabel) sLabel.textContent = label;
      if (pLabel) pLabel.textContent = label;
    }

    // 5. Calculadora Dinámica de Presupuesto
    function updateCalculator() {
      const slider = document.getElementById('camRangeSlider');
      const badge = document.getElementById('calcCamCountBadge');
      const totalEl = document.getElementById('calcMonthlyTotal');
      const descEl = document.getElementById('calcInstallDesc');
      const installCheck = document.getElementById('calcIncludeInstall');
      if (!slider || !badge || !totalEl || !descEl) return;

      const cams = parseInt(slider.value, 10);
      const camWord = currentLang === 'en' 
        ? (cams === 1 ? 'Camera' : 'Cameras')
        : (cams === 1 ? 'Cámara' : 'Cámaras');
      badge.textContent = `${cams} ${camWord}`;

      const cfg = PRICING_DATA[currentCurrency] || PRICING_DATA.ARS;
      const basePerCam = currentBilling === 'annual' ? cfg.calcBaseAnnual : cfg.calcBaseMonth;
      let monthlyCost = Math.round(cams * basePerCam);

      if (cams >= 8) {
        monthlyCost = Math.round(monthlyCost * 0.85); // 15% Descuento por volumen
      }

      totalEl.textContent = cfg.formatPrice(monthlyCost);

      if (installCheck && installCheck.checked) {
        const equipTotal = cams * cfg.calcInstallPerCam;
        descEl.innerHTML = cfg.calcDescHardware(monthlyCost, equipTotal);
      } else {
        descEl.innerHTML = cfg.calcDescSoftware();
      }
    }

    function requestCalculatedQuote() {
      const cams = document.getElementById('camRangeSlider').value;
      const install = document.getElementById('calcIncludeInstall').checked;
      const text = currentLang === 'en'
        ? `Hello Baddgroup, I want to request a quote for ${cams} cameras (${install ? 'including new 2K cameras & installation' : 'software SaaS only for existing cameras'}) in ${currentBilling} billing (${currentCurrency}).`
        : `Hola Baddgroup, quiero solicitar presupuesto para ${cams} cámaras (${install ? 'con instalación y cámaras nuevas' : 'solo software para cámaras existentes'}) en plan ${currentBilling} (${currentCurrency}).`;
      window.open(`https://wa.me/5491169957772?text=${encodeURIComponent(text)}`, '_blank');
    }

    // 6. Verificación de Autenticación y Adaptación de Botones (Gating a Cámaras)
    function updateNavAuthStatus() {
      try {
        const token = localStorage.getItem("baddgroup_auth_token");
        const userRaw = localStorage.getItem("baddgroup_user");
        const user = (token && userRaw) ? JSON.parse(userRaw) : null;

        const navBtns = [
          document.getElementById("dynamicPortalBtn"),
          document.getElementById("dynamicPortalBtnMobile")
        ];
        const heroBtn = document.getElementById("heroPortalBtn");
        const bannerBtn = document.getElementById("bannerPortalBtn");
        const footerBtn = document.getElementById("footerPortalBtn");

        const dict = I18N[currentLang] || I18N.es;

        if (user && user.role === "admin") {
          navBtns.forEach(btn => {
            if (btn) {
              btn.href = "/crm";
              btn.innerHTML = `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg><span>${dict.nav_crm_panel}</span>`;
            }
          });
          if (heroBtn) {
            heroBtn.href = "/cameras";
            heroBtn.querySelector("span").textContent = dict.nav_my_cameras;
          }
          if (bannerBtn) {
            bannerBtn.href = "/cameras";
            bannerBtn.querySelector("span").textContent = dict.nav_my_cameras;
          }
          if (footerBtn) {
            footerBtn.href = "/cameras";
            footerBtn.textContent = dict.nav_my_cameras;
          }
        } else if (user) {
          // Cliente Autenticado -> va directo a sus cámaras
          const label = `${dict.nav_my_cameras} (${user.username || 'Cliente'})`;
          navBtns.forEach(btn => {
            if (btn) {
              btn.href = "/cameras";
              btn.innerHTML = `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M23 7l-7 5 7 5V7z"></path><rect x="1" y="5" width="15" height="14" rx="2" ry="2"></rect></svg><span>${label}</span>`;
            }
          });
          if (heroBtn) {
            heroBtn.href = "/cameras";
            heroBtn.querySelector("span").textContent = dict.nav_my_cameras;
          }
          if (bannerBtn) {
            bannerBtn.href = "/cameras";
            bannerBtn.querySelector("span").textContent = dict.nav_my_cameras;
          }
          if (footerBtn) {
            footerBtn.href = "/cameras";
            footerBtn.textContent = dict.nav_my_cameras;
          }
        } else {
          // No Autenticado -> Siempre primero al Login
          navBtns.forEach(btn => {
            if (btn) {
              btn.href = "/login?redirect=/cameras";
              btn.innerHTML = `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg><span>${dict.nav_client_login}</span>`;
            }
          });
          if (heroBtn) {
            heroBtn.href = "/login?redirect=/cameras";
            heroBtn.querySelector("span").textContent = dict.hero_cta_portal;
          }
          if (bannerBtn) {
            bannerBtn.href = "/login?redirect=/cameras";
            bannerBtn.querySelector("span").textContent = dict.portal_cta_cams;
          }
          if (footerBtn) {
            footerBtn.href = "/login?redirect=/cameras";
            footerBtn.textContent = dict.footer_portal_link;
          }
        }
      } catch (e) {
        console.warn("Auth check error:", e);
      }
    }

    // 7. Menú Hamburguesa Mobile
    function toggleMobileMenu() {
      const drawer = document.getElementById("mobileDrawer");
      if (drawer) drawer.classList.toggle("open");
    }

    function closeMobileMenu() {
      const drawer = document.getElementById("mobileDrawer");
      if (drawer) drawer.classList.remove("open");
    }

    // 8. Canvas de Ondas Neurales
    const canvas = document.getElementById('neural-canvas');
    if (canvas) {
      const ctx = canvas.getContext('2d');
      let width = canvas.width = window.innerWidth;
      let height = canvas.height = window.innerHeight;

      window.addEventListener('resize', () => {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
      });

      const particles = [];
      const particleCount = Math.min(width > 768 ? 45 : 20, 50);

      for (let i = 0; i < particleCount; i++) {
        particles.push({
          x: Math.random() * width,
          y: Math.random() * height,
          vx: (Math.random() - 0.5) * 0.4,
          vy: (Math.random() - 0.5) * 0.4,
          radius: Math.random() * 2 + 1
        });
      }

      function animateCanvas() {
        ctx.clearRect(0, 0, width, height);
        ctx.fillStyle = "rgba(6, 182, 212, 0.5)";
        ctx.strokeStyle = "rgba(6, 182, 212, 0.08)";

        for (let i = 0; i < particles.length; i++) {
          const p = particles[i];
          p.x += p.vx;
          p.y += p.vy;

          if (p.x < 0) p.x = width;
          if (p.x > width) p.x = 0;
          if (p.y < 0) p.y = height;
          if (p.y > height) p.y = 0;

          ctx.beginPath();
          ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
          ctx.fill();

          for (let j = i + 1; j < particles.length; j++) {
            const p2 = particles[j];
            const dx = p.x - p2.x;
            const dy = p.y - p2.y;
            const dist = Math.sqrt(dx * dx + dy * dy);

            if (dist < 130) {
              ctx.beginPath();
              ctx.moveTo(p.x, p.y);
              ctx.lineTo(p2.x, p2.y);
              ctx.stroke();
            }
          }
        }
        requestAnimationFrame(animateCanvas);
      }
      animateCanvas();
    }

    // 9. Demo Forense con IA
    function setDemoQuery(query) {
      const input = document.getElementById('demoQueryInput');
      if (input) {
        input.value = query;
        runDemoSearch();
      }
    }

    function runDemoSearch() {
      const input = document.getElementById('demoQueryInput');
      const resBox = document.getElementById('demoResultBox');
      if (!input || !resBox) return;

      const isEn = currentLang === 'en';
      resBox.innerHTML = `<span style="color: var(--cyan-bright);">${isEn ? 'Processing forensic metadata with YOLOv11 on Cloud Server...' : 'Procesando metadatos periciales con YOLOv11 en servidor Cloud...'}</span>`;

      setTimeout(() => {
        const q = input.value.toLowerCase();
        if (q.includes("brazo") || q.includes("brazos") || q.includes("arm") || q.includes("arms")) {
          resBox.innerHTML = isEn
            ? `<span class="highlight">Exact Forensic Match:</span> "At <strong>10:14:25 am</strong> a <strong>person moving arms</strong> was detected in Camera Main Entrance (duration 1.8s, conf 0.94). 2K Clip available."`
            : `<span class="highlight">Coincidencia Forense Exacta:</span> "A las <strong>10:14:25 hs</strong> se visualizó en Cámara Entrada a una <strong>persona realizando movimiento corporal y de brazos</strong> frente a la cámara (duración 1.8s, conf 0.94). Clip 2K disponible."`;
        } else if (q.includes("negro") || q.includes("oscura") || q.includes("dark") || q.includes("black")) {
          resBox.innerHTML = isEn
            ? `<span class="highlight">Exact Forensic Match:</span> "At <strong>09:48:12 am</strong> a person in <strong>dark / black clothing</strong> passed through lateral access (duration 3.2s). Forensic thumbnail ready."`
            : `<span class="highlight">Coincidencia Forense Exacta:</span> "A las <strong>09:48:12 hs</strong> se registró el paso de un sujeto con <strong>ropa oscura / negra</strong> en acceso lateral (duración 3.2s). Miniatura pericial generada."`;
        } else if (q.includes("auto") || q.includes("vehiculo") || q.includes("car") || q.includes("vehicle")) {
          resBox.innerHTML = isEn
            ? `<span class="highlight">Exact Forensic Match:</span> "At <strong>08:30:19 am</strong> a <strong>vehicle (car)</strong> entered driveway (duration 9.8s). Plate and trajectory saved."`
            : `<span class="highlight">Coincidencia Forense Exacta:</span> "A las <strong>08:30:19 hs</strong> ingresó un <strong>vehículo (car)</strong> a la dársena de ingreso (duración 9.8s). Patente y trayectoria guardadas."`;
        } else {
          resBox.innerHTML = isEn
            ? `<span class="highlight">Exact Forensic Match:</span> "Event detected at <strong>10:14 am</strong> matching your query: human presence and motion verified."`
            : `<span class="highlight">Coincidencia Forense Exacta:</span> "Evento detectado a las <strong>10:14 hs</strong> correspondiente a tu consulta: presencia humana y movimiento verificado."`;
        }
      }, 500);
    }

    // 10. FAQ Acordeón
    function toggleFaq(element) {
      element.classList.toggle('open');
    }

    // 11. Modal de Contacto
    function openContactModal(planName) {
      const modal = document.getElementById('contactModal');
      const select = document.getElementById('formServiceSelect');
      const sub = document.getElementById('modalPlanSubtitle');

      if (planName) {
        if (sub) sub.textContent = currentLang === 'en' 
          ? `Interest in: ${planName}. We will contact you immediately.`
          : `Interés en: ${planName}. Te contactaremos de inmediato.`;
        if (select) {
          for (let opt of select.options) {
            if (opt.text.toLowerCase().includes(planName.toLowerCase())) {
              opt.selected = true;
              break;
            }
          }
        }
      }
      if (modal) modal.classList.add('active');
    }

    function closeContactModal() {
      const modal = document.getElementById('contactModal');
      if (modal) modal.classList.remove('active');
    }

    function openDemoViewer(e) {
      if (e) e.preventDefault();
      const el = document.getElementById('demo');
      if (el) el.scrollIntoView({ behavior: 'smooth' });
    }

    function handleFormSubmit(e) {
      e.preventDefault();
      const name = document.getElementById('formName').value;
      const phone = document.getElementById('formPhone').value;
      const company = document.getElementById('formCompany').value;
      const service = document.getElementById('formServiceSelect').value;
      const notes = document.getElementById('formNotes').value;

      const msg = `Hola Baddgroup! Mi nombre es ${name}${company ? ' de ' + company : ''}. Me interesa contratar ${service} (Moneda: ${currentCurrency}). Mi WhatsApp es ${phone}. Nota: ${notes || 'Quiero más información.'}`;
      window.open(`https://wa.me/5491169957772?text=${encodeURIComponent(msg)}`, '_blank');
      closeContactModal();
    }

    // Inicialización al cargar la página
    document.addEventListener("DOMContentLoaded", () => {
      // 1. Inicializar idioma guardado (o default es)
      setLanguage(currentLang);

      // 2. Inicializar moneda guardada (o default ARS)
      setCurrency(currentCurrency);

      // 3. Inicializar estado de autenticación en navbar y botones
      updateNavAuthStatus();
    });
  </script>
</body>
</html>
"""

html = before_script + new_script

with open("frontend/landing.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Landing page complete i18n, currency switcher, and auth logic injected successfully!")
