import re
from pathlib import Path

html_path = Path("frontend/index.html")
content = html_path.read_text(encoding="utf-8")

# 1. NEW CLEAN HEADER WITH 3 BALANCED ZONES
new_header = """  <!-- HEADER - SOC CYBER COMMAND CENTER -->
  <header>
    <a href="#" class="brand-logo" aria-label="BADDGROUP - Inicio">
      <div class="brand-logo-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100%" height="100%">
          <polygon points="50,4 92,26 92,74 50,96 8,74 8,26" fill="#1e293b" stroke="#3b82f6" stroke-width="2.5"/>
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

    <!-- CÁPSULA CENTRAL: CONTROL RÁPIDO DE CÁMARAS Y ESTADO -->
    <div class="header-center-capsule">
      <!-- SELECTOR DE CÁMARA ACTIVA -->
      <div class="camera-selector-box" title="Filtrar eventos por cámara">
        <svg class="v-icon" viewBox="0 0 24 24" style="color:var(--cyan-bright);"><path d="M17 10.5V7c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h12c.55 0 1-.45 1-1v-3.5l4 4v-11l-4 4z"/></svg>
        <select id="cameraSelect" class="camera-select-dropdown" onchange="onCameraSelectChange(this.value)">
          <option value="" disabled selected>Cargando cámaras...</option>
        </select>
      </div>

      <!-- BOTÓN GESTOR DE CÁMARAS -->
      <button class="btn-action" onclick="openCameraModal()" title="Gestor de Cámaras & Distribución en Producción">
        <svg class="v-icon" viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/></svg>
        <span>Cámaras (<span id="camerasCountHeader">1</span>)</span>
      </button>

      <!-- INDICADOR EN VIVO -->
      <div class="status-badge" style="border:none; background:transparent; padding:0.25rem 0.5rem;">
        <span class="status-indicator-dot"></span>
        <span id="cameraOnlineStatusText" style="font-weight:600;">Cámara En Vivo</span>
      </div>

      <!-- RESOLUCIÓN & FPS -->
      <div class="status-badge" id="cameraResBadge" style="font-family:monospace; font-size:0.74rem;">640x480 (15 FPS)</div>
    </div>

    <!-- ACCIONES DE USUARIO Y NAVEGACIÓN -->
    <div class="header-right">
      <!-- ACCESO CRM & FACTURACIÓN -->
      <a href="/crm" class="btn-header-crm" id="headerCrmLink" title="Panel de Administración CRM, Clientes & Facturación">
        <svg class="v-icon" viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 3c1.93 0 3.5 1.57 3.5 3.5S13.93 13 12 13s-3.5-1.57-3.5-3.5S10.07 6 12 6zm7 13H5v-.23c0-.62.28-1.2.76-1.58C7.47 15.82 9.64 15 12 15s4.53.82 6.24 2.19c.48.38.76.97.76 1.58V19z"/></svg>
        <span>CRM</span>
      </a>

      <!-- ACCESO A PRESENTACIÓN -->
      <a href="/" class="btn-action" title="Presentación Institucional & Planes" style="text-decoration:none;">
        <svg class="v-icon" viewBox="0 0 24 24"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>
        <span>Presentación</span>
      </a>

      <!-- BADGE USUARIO -->
      <div id="userBadgeHeader" class="status-badge" style="display:none; align-items:center; gap:0.4rem;">
        <svg class="v-icon" viewBox="0 0 24 24" style="width:14px;height:14px;fill:currentColor;"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>
        <span id="userNameHeader" style="font-weight:700;">Usuario</span>
      </div>

      <!-- BOTÓN SALIR -->
      <button id="logoutBtnHeader" class="btn-action" onclick="logoutSession()" title="Cerrar Sesión">
        <svg class="v-icon" viewBox="0 0 24 24" style="width:14px;height:14px;fill:currentColor;"><path d="M10.09 15.59L11.5 17l5-5-5-5-1.41 1.41L12.67 11H3v2h9.67l-2.58 2.59zM19 3H5c-1.11 0-2 .9-2 2v4h2V5h14v14H5v-4H3v4c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2z"/></svg>
        <span>Salir</span>
      </button>

      <!-- BADGE DE ESTADO SOC 24/7 -->
      <div class="status-badge" style="background:rgba(6,182,212,0.1); border-color:rgba(6,182,212,0.3); color:#00f2fe; gap:0.4rem; padding:0.4rem 0.85rem;" title="Centro de Operaciones de Seguridad Baddgroup Activo 24/7">
        <span class="status-indicator-dot" style="background:#00f2fe; box-shadow:0 0 8px #00f2fe;"></span>
        <span style="font-weight:700; font-size:0.75rem; letter-spacing:0.05em;">SOC 24/7</span>
      </div>
    </div>
  </header>"""

# Replace existing header
header_match = re.search(r'<header>.*?</header>', content, re.DOTALL)
if header_match:
    content = content[:header_match.start()] + new_header + content[header_match.end():]
    print("Header replaced successfully with 3-zone capsule layout")

# Extra CSS rules to refine everything
refined_css = """
    /* =========================================================
       REFINED HEADER & CAPSULE LAYOUT
       ========================================================= */
    header {
      background: rgba(6, 9, 16, 0.92) !important;
      backdrop-filter: blur(20px) !important;
      -webkit-backdrop-filter: blur(20px) !important;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
      position: sticky;
      top: 0;
      z-index: 50;
      padding: 0.75rem 2rem !important;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 1.5rem;
      box-shadow: 0 4px 24px rgba(0, 0, 0, 0.7) !important;
    }

    .header-center-capsule {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      background: rgba(13, 18, 30, 0.78);
      border: 1px solid rgba(255, 255, 255, 0.1);
      padding: 0.3rem 0.65rem;
      border-radius: 9999px;
      backdrop-filter: blur(14px);
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
    }

    @media (max-width: 1240px) {
      .header-center-capsule {
        display: none;
      }
    }

    .camera-selector-box {
      background: rgba(6, 9, 16, 0.6) !important;
      border: 1px solid rgba(255, 255, 255, 0.08) !important;
      border-radius: 9999px !important;
      color: #f8fafc !important;
      padding: 0.28rem 0.75rem !important;
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
    }

    .camera-select-dropdown {
      background: transparent !important;
      color: #f8fafc !important;
      font-weight: 600;
      font-size: 0.8rem;
      border: none !important;
      outline: none !important;
      cursor: pointer;
    }

    .camera-select-dropdown option {
      background: #0a0e17 !important;
      color: #f8fafc !important;
    }

    header .btn-action {
      background: rgba(255, 255, 255, 0.05) !important;
      border: 1px solid rgba(255, 255, 255, 0.1) !important;
      border-radius: 9999px !important;
      color: #f8fafc !important;
      padding: 0.38rem 0.85rem !important;
      font-size: 0.8rem !important;
      font-weight: 600 !important;
      transition: all 0.2s ease !important;
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
    }

    header .btn-action:hover {
      background: rgba(6, 182, 212, 0.15) !important;
      border-color: #00f2fe !important;
      color: #fff !important;
      box-shadow: 0 0 14px rgba(6, 182, 212, 0.3) !important;
    }

    header .status-badge {
      background: rgba(6, 182, 212, 0.08) !important;
      border: 1px solid rgba(6, 182, 212, 0.25) !important;
      color: #f8fafc !important;
      border-radius: 9999px !important;
      padding: 0.38rem 0.85rem !important;
      font-size: 0.76rem !important;
      font-weight: 600 !important;
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
    }

    #userBadgeHeader {
      background: rgba(37, 99, 235, 0.15) !important;
      border: 1px solid rgba(59, 130, 246, 0.4) !important;
      color: #93c5fd !important;
      border-radius: 9999px !important;
      padding: 0.38rem 0.85rem !important;
    }

    #logoutBtnHeader {
      background: rgba(239, 68, 68, 0.08) !important;
      border: 1px solid rgba(239, 68, 68, 0.3) !important;
      color: #fca5a5 !important;
      border-radius: 9999px !important;
      padding: 0.38rem 0.85rem !important;
    }

    #logoutBtnHeader:hover {
      background: rgba(239, 68, 68, 0.2) !important;
      border-color: #ef4444 !important;
      color: #ffffff !important;
    }
"""

if "/* REFINED HEADER & CAPSULE LAYOUT */" not in content:
    content = content.replace("</style>", refined_css + "\n  </style>")

html_path.write_text(content, encoding="utf-8")
print("All redesign updates applied to frontend/index.html")
