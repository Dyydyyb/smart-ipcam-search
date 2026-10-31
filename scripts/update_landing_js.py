with open("frontend/landing.html", "r", encoding="utf-8") as f:
    html = f.read()

# Let's locate PRICING_DATA and replace it
pricing_data_start = html.find('const PRICING_DATA = {')
pricing_data_end = html.find('const I18N = {')

new_pricing_data = """const PRICING_DATA = {
      ARS: {
        symbol: "$",
        code: "ARS",
        periodMonth: "ARS / mes",
        periodAnnual: "ARS / mes (anual)",
        starterMonth: "29.000",
        starterAnnual: "23.200",
        proMonth: "59.000",
        proAnnual: "47.200",
        calcBaseMonth: 10000,
        calcBaseAnnual: 8000,
        calcSoftwareSetup: 470000,
        calcInstallPerCam: 200000, // 5 cámaras = $1.000.000 ARS llave en mano
        formatPrice: (n) => `$${n.toLocaleString('es-AR')}`,
        calcDescHardware: (monthly, equip, setup, totalInitial, cams) => 
          `<div style="display:flex; flex-direction:column; gap:0.4rem; text-align:left; font-size:0.88rem; line-height:1.45;">
            <div>• Abono mensual con IA: <strong style="color:var(--cyan-bright);">$${monthly.toLocaleString('es-AR')} ARS/mes</strong></div>
            <div>• Adelanto por instalación de software: <strong style="color:#fff;">$${setup.toLocaleString('es-AR')} ARS</strong> (pago único)</div>
            <div>• Provisión de ${cams} cámaras 2K e instalación física: <strong style="color:#34d399;">$${equip.toLocaleString('es-AR')} ARS</strong> (pago único)</div>
            <div style="margin-top:0.35rem; padding-top:0.4rem; border-top:1px solid rgba(255,255,255,0.1); color:#fff; font-weight:700;">
              Total Inicial (Instalación + Cámaras + Software): $${totalInitial.toLocaleString('es-AR')} ARS
            </div>
          </div>`,
        calcDescSoftware: (monthly, setup, cams) => 
          `<div style="display:flex; flex-direction:column; gap:0.4rem; text-align:left; font-size:0.88rem; line-height:1.45;">
            <div>• Abono mensual con IA (${cams} cámaras): <strong style="color:var(--cyan-bright);">$${monthly.toLocaleString('es-AR')} ARS/mes</strong></div>
            <div>• Adelanto por instalación de software y alta P2P: <strong style="color:#fff;">$${setup.toLocaleString('es-AR')} ARS</strong> (pago único)</div>
            <div style="font-size:0.8rem; color:var(--text-muted);">Aprovechando tus cámaras existentes IP / RTSP sin compra de equipos nuevos.</div>
          </div>`
      },
      USD: {
        symbol: "$",
        code: "USD",
        periodMonth: "USD / mo",
        periodAnnual: "USD / mo (annual)",
        starterMonth: "19",
        starterAnnual: "15",
        proMonth: "39",
        proAnnual: "31",
        calcBaseMonth: 7,
        calcBaseAnnual: 5.5,
        calcSoftwareSetup: 300,
        calcInstallPerCam: 130, // 5 cameras = $650 USD turnkey
        formatPrice: (n) => `$${n.toLocaleString('en-US')} USD`,
        calcDescHardware: (monthly, equip, setup, totalInitial, cams) => 
          `<div style="display:flex; flex-direction:column; gap:0.4rem; text-align:left; font-size:0.88rem; line-height:1.45;">
            <div>• Monthly AI fee: <strong style="color:var(--cyan-bright);">$${monthly.toLocaleString('en-US')} USD/mo</strong></div>
            <div>• Software setup & onboarding fee: <strong style="color:#fff;">$${setup.toLocaleString('en-US')} USD</strong> (one-time)</div>
            <div>• ${cams} 2K cameras provision & turnkey installation: <strong style="color:#34d399;">$${equip.toLocaleString('en-US')} USD</strong> (one-time)</div>
            <div style="margin-top:0.35rem; padding-top:0.4rem; border-top:1px solid rgba(255,255,255,0.1); color:#fff; font-weight:700;">
              Total Initial Investment (Hardware + Setup): $${totalInitial.toLocaleString('en-US')} USD
            </div>
          </div>`,
        calcDescSoftware: (monthly, setup, cams) => 
          `<div style="display:flex; flex-direction:column; gap:0.4rem; text-align:left; font-size:0.88rem; line-height:1.45;">
            <div>• Monthly AI fee (${cams} cameras): <strong style="color:var(--cyan-bright);">$${monthly.toLocaleString('en-US')} USD/mo</strong></div>
            <div>• Software installation & P2P cloud bridge: <strong style="color:#fff;">$${setup.toLocaleString('en-US')} USD</strong> (one-time)</div>
            <div style="font-size:0.8rem; color:var(--text-muted);">Using your existing cameras (SaaS Software Only). No new hardware purchase needed.</div>
          </div>`
      }
    };

    """

html = html[:pricing_data_start] + new_pricing_data + html[pricing_data_end:]

# 2. Update I18N to include new B2B and Pricing keys
i18n_start = html.find('const I18N = {')
i18n_end = html.find('// 1. Reloj en vivo para el OSD')

new_i18n = """const I18N = {
      es: {
        page_title: "Baddgroup Vision AI | Plataforma de Videovigilancia Inteligente y Búsqueda Forense con IA",
        nav_about: "¿De qué trata?",
        nav_hire: "Cómo Contratar",
        nav_b2b: "Empresas de Seguridad",
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

        b2b_tag: "SOLUCIÓN B2B PARA EMPRESAS DE SEGURIDAD & MONITOREO",
        b2b_title: "Potenciá tu Empresa de Seguridad con IA de Baddgroup",
        b2b_desc: "Te proveemos el software completo, tu propio panel máster multi-tenant, cuentas independientes para tus clientes e infraestructura en la nube. Vos vendés el servicio con tu marca a tus abonados y nosotros ponemos la inteligencia artificial pericial.",
        b2b_c1_title: "Tu Propio Panel Máster Multi-Tenant",
        b2b_c1_desc: "Centro de control administrativo total. Asigná cuentas a tus abonados, agregá cámaras remotas en segundos con su Safety Code y suspendé o reactivá servicios al instante.",
        b2b_c2_title: "Adelanto por Instalación de Software",
        b2b_c2_desc: "Configuración integral, despliegue del software y asignación de servidores dedicados por un adelanto inicial de $300 USD (~$470.000 ARS) pago único.",
        b2b_c3_title: "Abono Base + Escala por Cámara Vendida",
        b2b_c3_desc: "Precio base de plataforma de $95.000 ARS/mes ($60 USD/mo) + solo $4.500 ARS/cámara ($3 USD/cámara). Revendé a tus clientes con más de un 200% de margen.",
        b2b_c4_title: "Búsqueda Forense y Alertas en tu Central",
        b2b_c4_desc: "Tus operadores no pierden horas mirando pantallas inactivas. Detección YOLOv11 en milisegundos y búsqueda forense en lenguaje natural para esclarecer incidentes al instante.",
        b2b_banner_title: "¿Sos dueño de una empresa de seguridad o central de monitoreo?",
        b2b_banner_desc: "Solicitá una demostración corporativa y conocé nuestro plan mayorista para equipar a todos tus abonados con tecnología de videovigilancia con IA.",
        b2b_banner_btn: "Solicitar Alianza para Empresas",

        pricing_tag: "TRANSPARENCIA TOTAL",
        pricing_title: "Planes diseñados para cada escala",
        pricing_desc: "Elegí la cobertura ideal para tu hogar, comercio o empresa. Todos los planes incluyen detección en tiempo real con IA.",
        pricing_setup_notice: "Adelanto único por instalación y puesta en marcha de software: <strong>$300 USD (~$470.000 ARS)</strong>",
        plan_setup_sub: "+ $470.000 ARS ($300 USD) adelanto de software",
        ent_price: "A Medida",
        billing_monthly: "Facturación Mensual",
        billing_discount: "2 Meses Bonificados (-20%)",

        calc_tag: "SIMULADOR EN TIEMPO REAL",
        calc_title: "Calculá tu Presupuesto",
        calc_desc: "Deslizá la cantidad de cámaras y configurá si requerís instalación física para ver el valor estimado.",
        calc_cams_label: "Cantidad de Cámaras:",
        calc_install_check: "Incluir provisión de cámaras 2K e instalación física profesional llave en mano",
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
        nav_b2b: "Security Companies",
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

        b2b_tag: "B2B SOLUTION FOR SECURITY COMPANIES & ALARM STATIONS",
        b2b_title: "Empower Your Security Company with Baddgroup AI",
        b2b_desc: "We provide you with the complete software, your dedicated multi-tenant master panel, independent client accounts, and cloud infrastructure. You sell the service under your brand to your subscribers while we power the forensic AI.",
        b2b_c1_title: "Your Own Multi-Tenant Master Panel",
        b2b_c1_desc: "Total administrative control. Provision accounts for your subscribers, link remote cameras in seconds via Safety Code, and suspend or restore services instantly.",
        b2b_c2_title: "Software Installation & Setup Advance",
        b2b_c2_desc: "Comprehensive onboarding, software deployment, and dedicated server setup for a one-time initial fee of $300 USD (~$470.000 ARS).",
        b2b_c3_title: "Base Platform Fee + Scale per Camera Sold",
        b2b_c3_desc: "Base platform fee of $60 USD/mo ($95.000 ARS/mo) + only $3 USD/camera/mo ($4.500 ARS/camera). Resell to your clients with over 200% margin.",
        b2b_c4_title: "Forensic Search & Real-Time Alerts for Guards",
        b2b_c4_desc: "Operators no longer waste hours staring at idle screens. YOLOv11 detection in milliseconds and plain-language forensic queries solve events instantly.",
        b2b_banner_title: "Do you run a security company or monitoring center?",
        b2b_banner_desc: "Request an executive demo and discover our wholesale partner program to equip all your clients with AI video surveillance.",
        b2b_banner_btn: "Request B2B Security Partnership",

        pricing_tag: "TOTAL TRANSPARENCY",
        pricing_title: "Plans tailored for every scale",
        pricing_desc: "Choose the ideal coverage for your residence, store or enterprise. All plans include real-time YOLOv11 AI detection.",
        pricing_setup_notice: "One-time software installation & onboarding fee: <strong>$300 USD (~$470.000 ARS)</strong>",
        plan_setup_sub: "+ $300 USD software setup fee",
        ent_price: "Custom",
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

    """

html = html[:i18n_start] + new_i18n + html[i18n_end:]

# 3. Update updateCalculator() in JavaScript to use the new formula and display breakdown
calc_func_old = """    function updateCalculator() {
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
    }"""

calc_func_new = """    function updateCalculator() {
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

      totalEl.textContent = `${cfg.formatPrice(monthlyCost)} / mes`;

      const setupCost = cfg.calcSoftwareSetup;
      if (installCheck && installCheck.checked) {
        const equipTotal = cams * cfg.calcInstallPerCam; // 5 cámaras = $1.000.000 ARS
        const totalInitial = equipTotal + setupCost;
        descEl.innerHTML = cfg.calcDescHardware(monthlyCost, equipTotal, setupCost, totalInitial, cams);
      } else {
        descEl.innerHTML = cfg.calcDescSoftware(monthlyCost, setupCost, cams);
      }
    }"""

html = html.replace(calc_func_old, calc_func_new)

# Update slider default to 5 cameras
html = html.replace('value="4" oninput="updateCalculator()"', 'value="5" oninput="updateCalculator()"')
html = html.replace('<span class="badge-count" id="calcCamCountBadge">4 Cámaras</span>', '<span class="badge-count" id="calcCamCountBadge">5 Cámaras</span>')

with open("frontend/landing.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Updated landing JavaScript and calculator successfully.")
