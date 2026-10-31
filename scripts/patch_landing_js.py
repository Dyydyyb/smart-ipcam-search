import os

file_path = 'frontend/landing.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Locate the beginning of <script> and update state + PRICING_DATA + Dolar Blue logic
old_script_start = '''  <script>
    // ==========================================================================
    // ESTADO GLOBAL: IDIOMA, MONEDA, FACTURACIÓN Y AUTENTICACIÓN
    // ==========================================================================
    let currentLang = localStorage.getItem("baddgroup_lang") || "es";
    let currentCurrency = localStorage.getItem("baddgroup_currency") || "ARS";
    let currentBilling = "monthly";

    // Diccionario de Precios y Cotizador por Moneda
    const PRICING_DATA = {'''

new_script_start = '''  <script>
    // ==========================================================================
    // ESTADO GLOBAL: IDIOMA, MONEDA, FACTURACIÓN, DÓLAR BLUE Y AUTENTICACIÓN
    // ==========================================================================
    let currentLang = localStorage.getItem("baddgroup_lang") || "es";
    let currentCurrency = localStorage.getItem("baddgroup_currency") || "ARS";
    let currentBilling = "monthly";
    let liveDolarBlue = parseInt(localStorage.getItem("baddgroup_dolar_rate"), 10) || 1565;
    let dolarBlueUpdatedAt = "";

    // Diccionario de Precios y Cotizador Dinámico por Moneda
    const PRICING_DATA = {'''

assert old_script_start in content, "old_script_start not found"
content = content.replace(old_script_start, new_script_start, 1)

# Locate PRICING_DATA block and replace with dynamic rate-aware PRICING_DATA
old_pricing_block = '''    // Diccionario de Precios y Cotizador Dinámico por Moneda
    const PRICING_DATA = {
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
    };'''

new_pricing_block = '''    // Diccionario de Precios y Cotizador Dinámico por Moneda
    function getPricingConfig(curr) {
      const isARS = (curr || currentCurrency) === 'ARS';
      const setupCostARS = Math.round(300 * liveDolarBlue);
      const setupCostUSD = 300;
      const installPerCamARS = 200000; // 5 cámaras = $1.000.000 ARS llave en mano
      const installPerCamUSD = Math.round(200000 / liveDolarBlue);

      if (isARS) {
        return {
          symbol: "$",
          code: "ARS",
          periodMonth: "ARS / mes",
          periodAnnual: "ARS / mes (anual)",
          starterMonth: "29.000",
          starterAnnual: "23.200",
          proMonth: "59.000",
          proAnnual: "47.200",
          calcSoftwareSetup: setupCostARS,
          calcInstallPerCam: installPerCamARS,
          formatPrice: (n) => `$${Math.round(n).toLocaleString('es-AR')}`,
          calcDescHardware: (monthly, equip, setup, totalInitial, cams) => 
            `<div style="display:flex; flex-direction:column; gap:0.4rem; text-align:left; font-size:0.88rem; line-height:1.45;">
              <div>• Abono mensual con IA: <strong style="color:var(--cyan-bright);">$${monthly.toLocaleString('es-AR')} ARS/mes</strong></div>
              <div>• Adelanto por instalación de software: <strong style="color:#fff;">$${setup.toLocaleString('es-AR')} ARS</strong> ($300 USD)</div>
              <div>• Provisión de ${cams} cámaras 2K e instalación física: <strong style="color:#34d399;">$${equip.toLocaleString('es-AR')} ARS</strong> (pago único)</div>
              <div style="margin-top:0.35rem; padding-top:0.4rem; border-top:1px solid rgba(255,255,255,0.1); color:#fff; font-weight:700;">
                Total Inicial (Instalación + Cámaras + Software): $${totalInitial.toLocaleString('es-AR')} ARS
              </div>
            </div>`,
          calcDescSoftware: (monthly, setup, cams) => 
            `<div style="display:flex; flex-direction:column; gap:0.4rem; text-align:left; font-size:0.88rem; line-height:1.45;">
              <div>• Abono mensual con IA (${cams} cámaras): <strong style="color:var(--cyan-bright);">$${monthly.toLocaleString('es-AR')} ARS/mes</strong></div>
              <div>• Adelanto por instalación de software y alta P2P: <strong style="color:#fff;">$${setup.toLocaleString('es-AR')} ARS</strong> ($300 USD)</div>
              <div style="font-size:0.8rem; color:var(--text-muted);">Aprovechando tus cámaras existentes IP / RTSP sin compra de equipos nuevos.</div>
            </div>`
        };
      } else {
        return {
          symbol: "$",
          code: "USD",
          periodMonth: "USD / mo",
          periodAnnual: "USD / mo (annual)",
          starterMonth: "19",
          starterAnnual: "15",
          proMonth: "39",
          proAnnual: "31",
          calcSoftwareSetup: setupCostUSD,
          calcInstallPerCam: installPerCamUSD,
          formatPrice: (n) => `$${Math.round(n).toLocaleString('en-US')} USD`,
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
        };
      }
    }'''

assert old_pricing_block in content, "old_pricing_block not found"
content = content.replace(old_pricing_block, new_pricing_block, 1)

# Update getMonthlyCalculatorCost function and updateCalculator
old_calculator_func = '''    // 5. Calculadora Dinámica de Presupuesto
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

      totalEl.textContent = `${cfg.formatPrice(monthlyCost)} / mes`;

      const setupCost = cfg.calcSoftwareSetup;
      if (installCheck && installCheck.checked) {
        const equipTotal = cams * cfg.calcInstallPerCam; // 5 cámaras = $1.000.000 ARS
        const totalInitial = equipTotal + setupCost;
        descEl.innerHTML = cfg.calcDescHardware(monthlyCost, equipTotal, setupCost, totalInitial, cams);
      } else {
        descEl.innerHTML = cfg.calcDescSoftware(monthlyCost, setupCost, cams);
      }
    }'''

new_calculator_func = '''    // Función armónica para calcular la cuota mensual de la calculadora (alineada con los Planes)
    function getCameraMonthlyRate(cams, isAnnual, currency) {
      if (currency === 'ARS') {
        if (cams === 1) return isAnnual ? 19900 : 24900;
        if (cams === 2) return isAnnual ? 23200 : 29000; // Plan Starter exacto ($29.000 ARS)
        if (cams === 3) return isAnnual ? 33600 : 42000;
        if (cams === 4) return isAnnual ? 40800 : 51000;
        if (cams === 5) return isAnnual ? 47200 : 59000; // Plan Pro exacto ($59.000 ARS)
        if (cams === 6) return isAnnual ? 53600 : 67000;
        // 7 a 24 cámaras: base Plan Pro (5 cámaras) + adicional por cámara con descuentos por volumen
        const base = isAnnual ? 47200 : 59000;
        let extra = isAnnual ? 6800 : 8500;
        if (cams >= 18) extra = isAnnual ? 5200 : 6500;
        else if (cams >= 12) extra = isAnnual ? 6000 : 7500;
        return base + (cams - 5) * extra;
      } else {
        // USD
        if (cams === 1) return isAnnual ? 13 : 16;
        if (cams === 2) return isAnnual ? 15 : 19; // Plan Starter exacto ($19 USD)
        if (cams === 3) return isAnnual ? 22 : 28;
        if (cams === 4) return isAnnual ? 27 : 34;
        if (cams === 5) return isAnnual ? 31 : 39; // Plan Pro exacto ($39 USD)
        if (cams === 6) return isAnnual ? 35 : 44;
        const base = isAnnual ? 31 : 39;
        let extra = isAnnual ? 4.5 : 5.5;
        if (cams >= 18) extra = isAnnual ? 3.4 : 4.2;
        else if (cams >= 12) extra = isAnnual ? 3.9 : 4.8;
        return Math.round(base + (cams - 5) * extra);
      }
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

      const cfg = getPricingConfig(currentCurrency);
      const isAnnual = currentBilling === 'annual';
      const monthlyCost = getCameraMonthlyRate(cams, isAnnual, currentCurrency);

      const periodSuffix = currentLang === 'en' ? (isAnnual ? ' / mo (annual)' : ' / mo') : (isAnnual ? ' / mes (anual)' : ' / mes');
      totalEl.textContent = `${cfg.formatPrice(monthlyCost)}${periodSuffix}`;

      const setupCost = cfg.calcSoftwareSetup;
      if (installCheck && installCheck.checked) {
        const equipTotal = cams * cfg.calcInstallPerCam; // 5 cámaras = $1.000.000 ARS
        const totalInitial = equipTotal + setupCost;
        descEl.innerHTML = cfg.calcDescHardware(monthlyCost, equipTotal, setupCost, totalInitial, cams);
      } else {
        descEl.innerHTML = cfg.calcDescSoftware(monthlyCost, setupCost, cams);
      }
    }'''

assert old_calculator_func in content, "old_calculator_func not found"
content = content.replace(old_calculator_func, new_calculator_func, 1)

# Update updateBillingPeriodUI to use getPricingConfig
old_billing_func = '''    function updateBillingPeriodUI() {
      const cfg = PRICING_DATA[currentCurrency] || PRICING_DATA.ARS;
      const pStarter = document.getElementById('priceStarter');'''

new_billing_func = '''    function updateBillingPeriodUI() {
      const cfg = getPricingConfig(currentCurrency);
      const pStarter = document.getElementById('priceStarter');'''

assert old_billing_func in content, "old_billing_func not found"
content = content.replace(old_billing_func, new_billing_func, 1)

# Add real-time Dólar Blue fetching and live conversion logic
dolar_fetch_code = '''
    // ==========================================================================
    // INTEGRACIÓN API DÓLAR BLUE EN TIEMPO REAL (DOLARAPI + FALLBACK PROXY)
    // ==========================================================================
    async function fetchLiveDolarBlue() {
      try {
        const res = await fetch('https://dolarapi.com/v1/dolares/blue', { mode: 'cors' });
        if (res.ok) {
          const data = await res.json();
          if (data && data.venta) {
            applyDolarBlueRate(data.venta, data.fechaActualizacion);
            return;
          }
        }
      } catch (e) {
        console.warn("Direct DolarApi error, attempting backend proxy...", e);
      }

      try {
        const res = await fetch('/api/dolar-blue');
        if (res.ok) {
          const data = await res.json();
          if (data && data.venta) {
            applyDolarBlueRate(data.venta, data.fechaActualizacion);
            return;
          }
        }
      } catch (e) {
        console.warn("Backend Dolar Blue proxy error, using cached rate", e);
      }
    }

    function applyDolarBlueRate(rate, fecha) {
      if (!rate || isNaN(rate)) return;
      liveDolarBlue = Math.round(rate);
      dolarBlueUpdatedAt = fecha || "";
      localStorage.setItem("baddgroup_dolar_rate", liveDolarBlue);

      // Actualizar indicadores visuales de tasa
      const formattedRate = `$${liveDolarBlue.toLocaleString('es-AR')}`;
      const headerRateEl = document.getElementById('headerDolarRate');
      const mobileRateEl = document.getElementById('mobileDolarRate');
      const pricingRateEl = document.getElementById('pricingDolarRate');
      if (headerRateEl) headerRateEl.textContent = formattedRate;
      if (mobileRateEl) mobileRateEl.textContent = formattedRate;
      if (pricingRateEl) pricingRateEl.textContent = `${formattedRate} ARS`;

      // Actualizar precios dinámicos vinculados al dólar
      updateDolarDependentPrices();
    }

    function updateDolarDependentPrices() {
      const setupARS = Math.round(300 * liveDolarBlue);
      const b2bPartnerARS = Math.round(300 * liveDolarBlue);
      const b2bWhiteARS = Math.round(500 * liveDolarBlue);
      const b2bBaseMonthlyARS = Math.round(15 * liveDolarBlue);
      const b2bPer30CamsARS = Math.round(50 * liveDolarBlue);

      const setupNoticeARSEl = document.getElementById('setupNoticeARS');
      if (setupNoticeARSEl) setupNoticeARSEl.textContent = `~$${setupARS.toLocaleString('es-AR')} ARS`;

      document.querySelectorAll('.dyn-setup-ars').forEach(el => {
        el.textContent = `~$${setupARS.toLocaleString('es-AR')} ARS`;
      });

      const partnerArsEl = document.getElementById('b2bPartnerArs');
      const whiteArsEl = document.getElementById('b2bWhiteArs');
      const baseMonthlyArsEl = document.getElementById('b2bBaseMonthlyArs');
      const per30CamsArsEl = document.getElementById('b2bPer30CamsArs');

      if (partnerArsEl) partnerArsEl.textContent = `(~$${b2bPartnerARS.toLocaleString('es-AR')} ARS)`;
      if (whiteArsEl) whiteArsEl.textContent = `(~$${b2bWhiteARS.toLocaleString('es-AR')} ARS)`;
      if (baseMonthlyArsEl) baseMonthlyArsEl.textContent = `(~$${b2bBaseMonthlyARS.toLocaleString('es-AR')} ARS/mes)`;
      if (per30CamsArsEl) per30CamsArsEl.textContent = `(~$${b2bPer30CamsARS.toLocaleString('es-AR')} cada 30 cámaras)`;

      updateBillingPeriodUI();
      updateCalculator();
    }

    // Inicializar Dólar Blue en tiempo real
    fetchLiveDolarBlue();
    setInterval(fetchLiveDolarBlue, 300000); // Actualizar cada 5 minutos
'''

# Insert dolar_fetch_code before window.addEventListener('DOMContentLoaded') or at end of script
dom_listener = "    // Inicialización al cargar la página"
assert dom_listener in content, "dom_listener not found"
content = content.replace(dom_listener, dolar_fetch_code + "\n" + dom_listener, 1)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Step 2 (JavaScript dynamic pricing, calculator & live dolar blue) updated successfully!")
