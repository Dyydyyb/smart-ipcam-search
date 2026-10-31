import re

with open("frontend/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Fix default theme to 'dark'
html = html.replace(
    "let currentTheme = localStorage.getItem('smartcam_theme') || 'light';",
    "let currentTheme = localStorage.getItem('smartcam_theme') || 'dark';"
)

# 2. Update CSS for search-card and header to make it ultra-premium cyber SaaS
search_css_old = """    /* SECTION 2: BUSCADOR CON IA */
    .search-card {
      background: var(--bg-card);
      backdrop-filter: blur(16px);
      border: 1px solid var(--border-color);
      border-radius: 18px;
      padding: 1.5rem 1.8rem;
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.7), 0 0 0 1px rgba(6, 182, 212, 0.1);
      display: flex;
      flex-direction: column;
      gap: 1.15rem;
      transition: all 0.25s ease;
    }

    .search-card:hover {
      border-color: rgba(6, 182, 212, 0.35);
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8), 0 0 25px rgba(6, 182, 212, 0.15);
    }"""

search_css_new = """    /* SECTION 2: BUSCADOR CON IA (CYBER COMMAND BAR) */
    .search-card {
      background: rgba(13, 18, 30, 0.88) !important;
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid rgba(6, 182, 212, 0.32) !important;
      border-radius: 20px;
      padding: 1.6rem 2rem;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8), 0 0 25px rgba(6, 182, 212, 0.12);
      display: flex;
      flex-direction: column;
      gap: 1.25rem;
      transition: all 0.25s ease;
    }

    .search-card:hover {
      border-color: rgba(0, 242, 254, 0.5) !important;
      box-shadow: 0 24px 60px rgba(0, 0, 0, 0.85), 0 0 32px rgba(6, 182, 212, 0.22);
    }"""

html = html.replace(search_css_old, search_css_new)

# 3. Update CSS for ai-search-cam-selector-box to eliminate the ugly clunky look
ai_cam_box_old = """    .ai-search-cam-selector-box {
      background: rgba(6, 9, 16, 0.75);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 12px;
      padding: 0.95rem 1.2rem;
      display: flex;
      flex-direction: column;
      gap: 0.6rem;
      transition: all 0.2s ease;
    }"""

ai_cam_box_new = """    .ai-search-cam-selector-box {
      background: rgba(6, 9, 16, 0.6);
      border: 1px solid rgba(255, 255, 255, 0.07);
      border-radius: 14px;
      padding: 0.85rem 1.2rem;
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
      transition: all 0.2s ease;
    }"""

html = html.replace(ai_cam_box_old, ai_cam_box_new)

# 4. Enhance the live hero card and header CSS
header_css_old = """    header.site-header {
      background: var(--bg-surface);
      border-bottom: 1px solid var(--border-color);
      padding: 0.85rem 2rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: sticky;
      top: 0;
      z-index: 50;
      backdrop-filter: blur(16px);
      box-shadow: var(--shadow-sm);
      transition: background-color 0.2s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }"""

header_css_new = """    header.site-header {
      background: rgba(6, 9, 16, 0.92);
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      padding: 0.75rem 2rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: sticky;
      top: 0;
      z-index: 100;
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.8);
      transition: var(--transition-smooth);
    }

    .header-center-capsule {
      display: flex;
      align-items: center;
      gap: 0.45rem;
      background: rgba(13, 18, 30, 0.75);
      border: 1px solid rgba(255, 255, 255, 0.1);
      backdrop-filter: blur(16px);
      border-radius: 9999px;
      padding: 0.3rem 0.65rem;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
    }"""

html = html.replace(header_css_old, header_css_new)

# 5. Update HTML Header in frontend/index.html
header_html_old = """  <!-- SITE HEADER -->
  <header class="site-header">
    <a href="/" class="brand-container" style="text-decoration:none;" title="Volver a la Presentación">
      <div class="brand-logo-wrap">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100%" height="100%">
          <polygon points="50,4 92,26 92,74 50,96 8,74 8,26" fill="#1e293b" stroke="#00f2fe" stroke-width="2.5"/>
          <path d="M28 24 H48 C54.5 24 59 28 59 33.5 C59 37.5 56.5 41 52.5 42.5 C57.5 44 61 48 61 53.5 C61 60 55.5 64 48 64 H28 V24 Z" 
                fill="none" stroke="#2563eb" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>
          <path d="M28 44 H48" stroke="#2563eb" stroke-width="4.5" stroke-linecap="round"/>
          <path d="M72 40 V62 C72 68 66 73 58 73 H46" 
                fill="none" stroke="#059669" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M58 58 H72" stroke="#059669" stroke-width="4" stroke-linecap="round"/>
        </svg>
      </div>
      <div class="brand-text">
        <span class="brand-name">BADDGROUP</span>
        <span class="brand-title">VISION AI &bull; PLATAFORMA DE SEGURIDAD</span>
      </div>
    </a>

    <div class="header-right">
      <!-- SELECTOR DE CÁMARA ACTIVA -->
      <div class="camera-selector-box" title="Filtrar eventos por cámara">
        <svg class="v-icon" viewBox="0 0 24 24"><path d="M17 10.5V7c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h12c.55 0 1-.45 1-1v-3.5l4 4v-11l-4 4z"/></svg>
        <select id="cameraSelect" class="camera-select-dropdown" onchange="onCameraSelectChange(this.value)">
          <option value="" disabled selected>Cargando cámaras...</option>
        </select>
      </div>

      <!-- BOTÓN GESTOR DE CÁMARAS Y DISTRIBUCIÓN -->
      <button class="btn-action" onclick="openCameraModal()" title="Gestor de Cámaras & Distribución en Producción">
        <svg class="v-icon" viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/></svg>
        <span>Cámaras (<span id="camerasCountHeader">1</span>)</span>
      </button>

      <div class="status-badge">
        <span class="status-indicator-dot"></span>
        <span id="cameraOnlineStatusText">Cámara En Vivo</span>
      </div>
      <div class="status-badge" id="cameraResBadge">640x480 (15 FPS)</div>
      <!-- ACCESO CRM & FACTURACIÓN -->
      <a href="/crm" class="btn-header-crm" id="headerCrmLink" title="Panel de Administración CRM, Clientes & Facturación">
        <svg class="v-icon" viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 3c1.93 0 3.5 1.57 3.5 3.5S13.93 13 12 13s-3.5-1.57-3.5-3.5S10.07 6 12 6zm7 13H5v-.23c0-.62.28-1.2.76-1.58C7.47 15.82 9.64 15 12 15s4.53.82 6.24 2.19c.48.38.76.97.76 1.58V19z"/></svg>
        <span>CRM & Cobranzas</span>
      </a>

      <!-- ACCESO A PRESENTACIÓN -->
      <a href="/" class="btn-action" title="Presentación Institucional & Planes" style="text-decoration:none;">
        <svg class="v-icon" viewBox="0 0 24 24"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>
        <span>Presentación</span>
      </a>

      <!-- BADGE USUARIO Y LOGOUT -->
      <div id="userBadgeHeader" class="status-badge" style="display:none; align-items:center; gap:0.4rem; background:#18233c; border:1px solid #2563eb; color:#93c5fd;">
        <svg class="v-icon" viewBox="0 0 24 24" style="width:14px;height:14px;fill:currentColor;"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>
        <span id="userNameHeader" style="font-weight:700;">Usuario</span>
      </div>

      <button id="logoutBtnHeader" class="btn-action" onclick="logoutSession()" title="Cerrar Sesión" style="border-color:rgba(239, 68, 68, 0.4); color:#f87171;">
        <svg class="v-icon" viewBox="0 0 24 24" style="width:14px;height:14px;fill:currentColor;"><path d="M10.09 15.59L11.5 17l5-5-5-5-1.41 1.41L12.67 11H3v2h9.67l-2.58 2.59zM19 3H5c-1.11 0-2 .9-2 2v4h2V5h14v14H5v-4H3v4c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2z"/></svg>
        <span>Salir</span>
      </button>

      <!-- BOTON DE MODO CLARO / OSCURO (CON SVG) -->
      <button id="themeToggleBtn" class="theme-toggle-btn" onclick="toggleTheme()" aria-label="Cambiar tema">
        <svg id="themeIconSun" class="v-icon" style="display:none;" viewBox="0 0 24 24"><circle cx="12" cy="12" r="5"/><path d="M12 1v2m0 18v2M4.22 4.22l1.42 1.42m12.72 12.72l1.42 1.42M1 12h2m18 0h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
        <svg id="themeIconMoon" class="v-icon" viewBox="0 0 24 24"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
        <span id="themeText">Modo Oscuro</span>
      </button>
    </div>
  </header>"""

header_html_new = """  <!-- SITE HEADER CYBERNETIC SAAS -->
  <header class="site-header">
    <a href="/" class="brand-container" style="text-decoration:none;" title="Volver a la Presentación">
      <div class="brand-logo-wrap" style="width:38px; height:38px; filter:drop-shadow(0 0 8px rgba(6,182,212,0.4));">
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
        <span class="brand-name" style="font-family:'Plus Jakarta Sans',sans-serif; font-size:1.15rem; font-weight:800; letter-spacing:-0.02em; color:#fff;">BADDGROUP</span>
        <span class="brand-title" style="font-size:0.65rem; font-weight:700; letter-spacing:0.1em; color:var(--cyan-bright); text-transform:uppercase;">VISION AI &bull; PLATAFORMA DE SEGURIDAD</span>
      </div>
    </a>

    <!-- CAPSULE DE NAVEGACIÓN Y CONTROL DE CÁMARAS (CENTRO) -->
    <div class="header-center-capsule">
      <!-- SELECTOR DE CÁMARA ACTIVA -->
      <div class="camera-selector-box" title="Filtrar eventos por cámara" style="background:transparent; border:none; padding:0;">
        <svg class="v-icon" viewBox="0 0 24 24" style="color:var(--cyan-bright); width:15px; height:15px;"><path d="M17 10.5V7c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h12c.55 0 1-.45 1-1v-3.5l4 4v-11l-4 4z"/></svg>
        <select id="cameraSelect" class="camera-select-dropdown" onchange="onCameraSelectChange(this.value)" style="border-radius:9999px; background:rgba(6,9,16,0.85); font-size:0.82rem; padding:0.35rem 0.75rem;">
          <option value="" disabled selected>Cargando cámaras...</option>
        </select>
      </div>

      <!-- BOTÓN GESTOR DE CÁMARAS -->
      <button class="btn-action" onclick="openCameraModal()" title="Gestor de Cámaras & Distribución en Producción" style="border-radius:9999px; font-size:0.8rem; padding:0.35rem 0.8rem;">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
        <span>Cámaras (<span id="camerasCountHeader">1</span>)</span>
      </button>

      <div class="status-badge" style="border-radius:9999px; font-size:0.75rem; padding:0.32rem 0.75rem; background:rgba(16,185,129,0.12); border-color:rgba(16,185,129,0.3); color:#34d399;">
        <span class="status-indicator-dot" style="background:#10b981; box-shadow:0 0 8px #10b981;"></span>
        <span id="cameraOnlineStatusText">En Vivo</span>
      </div>
      <div class="status-badge" id="cameraResBadge" style="border-radius:9999px; font-size:0.75rem; padding:0.32rem 0.65rem;">640x480 (15 FPS)</div>
    </div>

    <!-- SUITE DERECHA: USUARIO, PRESENTACIÓN, CRM Y SALIR -->
    <div class="header-right" style="display:flex; align-items:center; gap:0.6rem;">
      <!-- BADGE USUARIO LOGUEADO -->
      <div id="userBadgeHeader" class="status-badge" style="display:none; align-items:center; gap:0.45rem; background:rgba(37,99,235,0.15); border:1px solid rgba(37,99,235,0.4); color:#93c5fd; border-radius:9999px; padding:0.38rem 0.85rem; font-size:0.82rem;">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
        <span id="userNameHeader" style="font-weight:700;">Usuario</span>
      </div>

      <!-- ACCESO CRM & FACTURACIÓN (SOLO ADMINS) -->
      <a href="/crm" class="btn-header-crm" id="headerCrmLink" title="Panel de Administración CRM, Clientes & Facturación" style="border-radius:9999px; padding:0.4rem 0.85rem; font-size:0.8rem; text-decoration:none;">
        <svg class="v-icon" viewBox="0 0 24 24" style="width:14px;height:14px;"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 3c1.93 0 3.5 1.57 3.5 3.5S13.93 13 12 13s-3.5-1.57-3.5-3.5S10.07 6 12 6zm7 13H5v-.23c0-.62.28-1.2.76-1.58C7.47 15.82 9.64 15 12 15s4.53.82 6.24 2.19c.48.38.76.97.76 1.58V19z"/></svg>
        <span>CRM</span>
      </a>

      <!-- ACCESO A PRESENTACIÓN -->
      <a href="/" class="btn-action" title="Presentación Institucional & Planes" style="text-decoration:none; border-radius:9999px; font-size:0.8rem; padding:0.4rem 0.85rem;">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
        <span>Presentación</span>
      </a>

      <!-- BOTON CERRAR SESIÓN -->
      <button id="logoutBtnHeader" class="btn-action" onclick="logoutSession()" title="Cerrar Sesión" style="border-radius:9999px; border-color:rgba(239, 68, 68, 0.4); color:#f87171; font-size:0.8rem; padding:0.4rem 0.85rem;">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>
        <span>Salir</span>
      </button>

      <!-- BOTON DE TEMA -->
      <button id="themeToggleBtn" class="theme-toggle-btn" onclick="toggleTheme()" aria-label="Cambiar tema" style="border-radius:9999px; width:34px; height:34px; padding:0; display:flex; align-items:center; justify-content:center;">
        <svg id="themeIconSun" class="v-icon" style="display:none; width:15px; height:15px;" viewBox="0 0 24 24"><circle cx="12" cy="12" r="5"/><path d="M12 1v2m0 18v2M4.22 4.22l1.42 1.42m12.72 12.72l1.42 1.42M1 12h2m18 0h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
        <svg id="themeIconMoon" class="v-icon" style="width:15px; height:15px;" viewBox="0 0 24 24"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
        <span id="themeText" style="display:none;">Modo Oscuro</span>
      </button>
    </div>
  </header>"""

html = html.replace(header_html_old, header_html_new)

# 6. Update Search Card HTML to make it a sleek cyber command bar
search_html_old = """    <!-- 2. BÚSQUEDA INTELIGENTE EN LENGUAJE NATURAL -->
    <section class="search-card">
      <div class="search-title-wrap">
        <div class="search-title">
          <svg class="v-icon-lg" viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
          <span>Búsqueda de Eventos en Lenguaje Natural con IA</span>
        </div>
        <div class="status-badge" id="aiEngineBadge" style="font-size:0.75rem;">
          Motor IA: Gemini 1.5 Flash (Visión Multimodal)
        </div>
      </div>

      <!-- SELECTOR OBLIGATORIO DE CÁMARA PARA BÚSQUEDA IA -->
      <div class="ai-search-cam-selector-box">
        <div class="ai-search-cam-label-row">
          <div class="ai-search-cam-title">
            <svg class="v-icon" viewBox="0 0 24 24"><path d="M17 10.5V7c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h12c.55 0 1-.45 1-1v-3.5l4 4v-11l-4 4z"/></svg>
            <span>Selecciona la Cámara a Analizar con IA:</span>
          </div>
          <span class="required-badge">Obligatorio</span>
        </div>
        <select id="aiCameraSelect" class="ai-camera-dropdown" onchange="onAICameraSelectChange(this.value)">
          <option value="" disabled selected>Elige una cámara en específico para consultar con IA...</option>
        </select>
        <div class="ai-search-cam-rule">
          <svg class="v-icon-sm" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/></svg>
          <span>Para garantizar precisión pericial y evitar confusiones entre zonas, la IA analiza una cámara específica a la vez.</span>
        </div>
      </div>

      <form id="searchForm" class="search-input-box" onsubmit="handleSearch(event)">
        <span class="search-input-icon">
          <svg class="v-icon" viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
        </span>
        <input 
          id="searchInput" 
          type="text" 
          class="search-input" 
          placeholder="Escribe tu consulta: 'en que momento alguien movio un brazo', 'cuando paso un auto', 'personas de la ultima hora'..." 
          autocomplete="off"
        >
        <button type="submit" class="search-btn">
          <svg class="v-icon" viewBox="0 0 24 24"><path d="M5 13h11.86l-5.43 5.43 1.42 1.42L21.14 12l-8.29-8.29-1.42 1.42L16.86 11H5v2z"/></svg>
          <span>Buscar con IA</span>
        </button>
      </form>"""

search_html_new = """    <!-- 2. BÚSQUEDA INTELIGENTE EN LENGUAJE NATURAL (CYBER COMMAND BAR) -->
    <section class="search-card">
      <div class="search-title-wrap">
        <div class="search-title" style="display:flex; align-items:center; gap:0.65rem;">
          <div style="width:36px; height:36px; border-radius:10px; background:rgba(6,182,212,0.15); border:1px solid rgba(6,182,212,0.4); display:flex; align-items:center; justify-content:center; color:var(--cyan-bright); box-shadow:0 0 15px rgba(6,182,212,0.25);">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
          </div>
          <div>
            <div style="font-size:1.18rem; font-weight:800; color:#fff; letter-spacing:-0.02em;">Búsqueda Forense con Inteligencia Artificial</div>
            <div style="font-size:0.75rem; color:var(--text-muted);">Consultá filmaciones históricas en lenguaje natural (ej: "¿en qué momento alguien movió un brazo?")</div>
          </div>
        </div>
        <div class="status-badge" id="aiEngineBadge" style="font-size:0.75rem; border-radius:9999px; padding:0.35rem 0.85rem; background:rgba(37,99,235,0.15); border-color:rgba(37,99,235,0.4); color:#93c5fd;">
          YOLOv11 &bull; Gemini 1.5 Flash Multimodal
        </div>
      </div>

      <!-- SELECTOR INTEGRADO Y ELEGANTE DE CÁMARA PARA BÚSQUEDA IA -->
      <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:0.75rem; background:rgba(6,9,16,0.65); border:1px solid rgba(255,255,255,0.08); border-radius:12px; padding:0.65rem 1rem;">
        <div style="display:flex; align-items:center; gap:0.55rem; font-size:0.85rem; font-weight:700; color:var(--text-main);">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="var(--cyan-bright)" stroke-width="2.5"><path d="M23 7l-7 5 7 5V7z"></path><rect x="1" y="5" width="15" height="14" rx="2" ry="2"></rect></svg>
          <span>Cámara a Analizar:</span>
        </div>
        <div style="flex:1; max-width:480px;">
          <select id="aiCameraSelect" class="ai-camera-dropdown" onchange="onAICameraSelectChange(this.value)" style="border-radius:8px; padding:0.5rem 0.85rem; font-size:0.85rem;">
            <option value="" disabled selected>Elige una cámara en específico para consultar con IA...</option>
          </select>
        </div>
        <div style="font-size:0.75rem; color:var(--cyan-bright); font-weight:600; display:flex; align-items:center; gap:0.35rem;">
          <span style="display:inline-block; width:6px; height:6px; border-radius:50%; background:var(--cyan-bright); box-shadow:0 0 6px var(--cyan-bright);"></span>
          <span>Análisis Pericial Focalizado</span>
        </div>
      </div>

      <form id="searchForm" class="search-input-box" onsubmit="handleSearch(event)">
        <span class="search-input-icon">
          <svg class="v-icon" viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
        </span>
        <input 
          id="searchInput" 
          type="text" 
          class="search-input" 
          placeholder="Escribe tu consulta: 'en que momento alguien movio un brazo', 'cuando paso un auto', 'personas de la ultima hora'..." 
          autocomplete="off"
        >
        <button type="submit" class="search-btn" style="background:var(--gradient-brand); color:#060911; font-weight:700; border-radius:10px; box-shadow:0 0 16px rgba(6,182,212,0.4);">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
          <span>Buscar con IA</span>
        </button>
      </form>"""

html = html.replace(search_html_old, search_html_new)

with open("frontend/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Overhauled cameras UI in frontend/index.html successfully.")
