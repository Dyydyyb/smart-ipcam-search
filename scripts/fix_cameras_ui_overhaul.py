import re
from pathlib import Path

html_path = Path("frontend/index.html")
content = html_path.read_text(encoding="utf-8")

# 1. UNIFY DESIGN TOKENS (DELETE BROKEN LIGHT MODE AND MAKE DARK SOC MASTER)
old_roots = re.search(r':root\[data-theme="dark"\]\s*\{.*?\}:root\[data-theme="light"\]\s*\{.*?\}', content, re.DOTALL)
if old_roots:
    unified_tokens = """/* =========================================================
       SISTEMA DE DISEÑO CYBERNETIC SAAS BADDGROUP VISION AI (DARK SOC MASTER)
       ========================================================= */
    :root, :root[data-theme="dark"], :root[data-theme="light"] {
      --bg-base: #05070e;
      --bg-surface: #0a0e17;
      --bg-card: rgba(13, 18, 30, 0.82);
      --bg-card-hover: rgba(20, 28, 48, 0.92);
      --border-color: rgba(255, 255, 255, 0.08);
      --border-subtle: rgba(255, 255, 255, 0.08);
      --border-accent: #00f2fe;
      --border-glow: rgba(0, 242, 254, 0.35);
      --border-cyan: rgba(6, 182, 212, 0.45);
      --accent-primary: #00f2fe;
      --accent-primary-hover: #38bdf8;
      --accent-secondary: #2563eb;
      --accent-secondary-hover: #1d4ed8;
      --accent-success: #10b981;
      --accent-danger: #ef4444;
      --cyan-bright: #00f2fe;
      --blue-electric: #3b82f6;
      --indigo-glow: #6366f1;
      --text-main: #f8fafc;
      --text-body: #94a3b8;
      --text-muted: #64748b;
      --badge-bg: rgba(6, 182, 212, 0.12);
      --badge-text: #00f2fe;
      --input-bg: rgba(6, 9, 16, 0.85);
      --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.5);
      --shadow-md: 0 8px 24px rgba(0, 0, 0, 0.6);
      --shadow-lg: 0 16px 48px -12px rgba(6, 182, 212, 0.2);
      --live-viewport-bg: #020408;
      --gradient-brand: linear-gradient(135deg, #00f2fe 0%, #3b82f6 50%, #6366f1 100%);
    }"""
    content = content[:old_roots.start()] + unified_tokens + content[old_roots.end():]
    print("✓ Unified design tokens replaced")
else:
    print("! Old roots not matched directly, checking...")

# 2. UPGRADE SPECIFIC CSS CLASSES FOR MAXIMUM COHESION AND SLEEK CONTOURS
css_patch = """
    /* =========================================================
       OVERHAUL DE ESTILOS DE ELEMENTOS CRÍTICOS (SIN FONDOS BLANCOS)
       ========================================================= */
    .live-hero-footer {
      padding: 0.75rem 1.4rem !important;
      background: rgba(10, 14, 23, 0.95) !important;
      border-top: 1px solid rgba(255, 255, 255, 0.08) !important;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.78rem !important;
      color: #94a3b8 !important;
      flex-wrap: wrap;
      gap: 0.5rem;
    }

    .search-card {
      background: rgba(13, 18, 30, 0.85) !important;
      backdrop-filter: blur(20px) !important;
      -webkit-backdrop-filter: blur(20px) !important;
      border: 1px solid rgba(0, 242, 254, 0.25) !important;
      border-radius: 20px !important;
      padding: 1.6rem 2rem !important;
      box-shadow: 0 20px 48px -10px rgba(0, 0, 0, 0.8), 0 0 20px rgba(6, 182, 212, 0.08) !important;
      display: flex;
      flex-direction: column;
      gap: 1.25rem;
      transition: all 0.25s ease;
    }

    .search-card:hover {
      border-color: rgba(0, 242, 254, 0.45) !important;
      box-shadow: 0 24px 60px rgba(0, 0, 0, 0.85), 0 0 30px rgba(6, 182, 212, 0.18) !important;
    }

    .search-title {
      color: #f8fafc !important;
    }

    .ai-camera-dropdown {
      width: 100%;
      background: rgba(13, 18, 30, 0.95) !important;
      border: 1px solid rgba(0, 242, 254, 0.35) !important;
      color: #f8fafc !important;
      padding: 0.55rem 0.95rem !important;
      border-radius: 8px !important;
      font-size: 0.88rem !important;
      font-weight: 600;
      outline: none;
      transition: border-color 0.15s ease, box-shadow 0.15s ease;
    }

    .ai-camera-dropdown:focus {
      border-color: #00f2fe !important;
      box-shadow: 0 0 16px rgba(0, 242, 254, 0.3) !important;
    }

    .ai-camera-dropdown option {
      background: #0a0e17 !important;
      color: #f8fafc !important;
    }

    .search-input {
      width: 100%;
      padding: 0.95rem 1.2rem 0.95rem 3.1rem;
      padding-right: 165px;
      background: rgba(6, 9, 16, 0.85) !important;
      border: 1px solid rgba(255, 255, 255, 0.12) !important;
      border-radius: 12px !important;
      color: #ffffff !important;
      font-size: 0.95rem;
      font-family: inherit;
      outline: none;
      box-shadow: 0 0 16px rgba(0, 0, 0, 0.5);
      transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }

    .search-input::placeholder {
      color: #64748b !important;
    }

    .search-input:focus {
      border-color: #00f2fe !important;
      box-shadow: 0 0 24px rgba(0, 242, 254, 0.35) !important;
    }

    .search-btn {
      position: absolute;
      right: 0.5rem;
      background: linear-gradient(135deg, #00f2fe 0%, #3b82f6 50%, #6366f1 100%) !important;
      color: #05070e !important;
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-weight: 800 !important;
      font-size: 0.85rem;
      padding: 0.65rem 1.35rem;
      border: none;
      border-radius: 10px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
      box-shadow: 0 0 18px rgba(6, 182, 212, 0.4);
      transition: all 0.2s ease;
    }

    .search-btn:hover {
      transform: translateY(-1px);
      box-shadow: 0 0 26px rgba(6, 182, 212, 0.6);
      filter: brightness(1.1);
    }

    .chip-label {
      font-size: 0.78rem;
      color: #94a3b8 !important;
      margin-right: 0.35rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    .chip {
      background: rgba(255, 255, 255, 0.05) !important;
      border: 1px solid rgba(255, 255, 255, 0.12) !important;
      color: #cbd5e1 !important;
      padding: 0.42rem 0.95rem;
      border-radius: 9999px;
      font-size: 0.82rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
    }

    .chip:hover {
      background: rgba(6, 182, 212, 0.15) !important;
      border-color: rgba(0, 242, 254, 0.4) !important;
      color: #ffffff !important;
      transform: translateY(-1px);
    }

    .chip.active {
      background: rgba(0, 242, 254, 0.18) !important;
      border-color: #00f2fe !important;
      color: #00f2fe !important;
      box-shadow: 0 0 16px rgba(0, 242, 254, 0.35);
      font-weight: 700;
    }

    .slider-title {
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 1.25rem !important;
      font-weight: 800 !important;
      color: #f8fafc !important;
      display: flex;
      align-items: center;
      gap: 0.6rem;
    }

    .slider-arrow-btn {
      width: 38px !important;
      height: 38px !important;
      border-radius: 50% !important;
      background: rgba(255, 255, 255, 0.06) !important;
      border: 1px solid rgba(255, 255, 255, 0.12) !important;
      color: #f8fafc !important;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.2s ease;
    }

    .slider-arrow-btn:hover {
      background: rgba(0, 242, 254, 0.15) !important;
      border-color: #00f2fe !important;
      color: #00f2fe !important;
      box-shadow: 0 0 14px rgba(0, 242, 254, 0.3);
      transform: scale(1.05);
    }

    .btn-action-primary {
      background: rgba(37, 99, 235, 0.2) !important;
      color: #93c5fd !important;
      border: 1px solid rgba(59, 130, 246, 0.45) !important;
      padding: 0.45rem 1rem !important;
      border-radius: 9999px !important;
      font-size: 0.8rem !important;
      font-weight: 700 !important;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
      transition: all 0.2s ease;
      box-shadow: 0 0 12px rgba(37, 99, 235, 0.25);
    }

    .btn-action-primary:hover {
      background: rgba(37, 99, 235, 0.35) !important;
      border-color: #60a5fa !important;
      color: #ffffff !important;
      transform: translateY(-1px);
      box-shadow: 0 0 18px rgba(37, 99, 235, 0.4);
    }

    .btn-action-danger-subtle {
      background: rgba(239, 68, 68, 0.1) !important;
      color: #fca5a5 !important;
      border: 1px solid rgba(239, 68, 68, 0.32) !important;
      padding: 0.45rem 1rem !important;
      border-radius: 9999px !important;
      font-size: 0.8rem !important;
      font-weight: 600 !important;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
      transition: all 0.2s ease;
    }

    .btn-action-danger-subtle:hover {
      background: rgba(239, 68, 68, 0.22) !important;
      border-color: #ef4444 !important;
      color: #ffffff !important;
      transform: translateY(-1px);
    }
"""

# Insert css_patch right before </style>
content = content.replace("</style>", css_patch + "\n  </style>")

# 3. FIX THE "Cámara a Analizar:" ROW IN THE SEARCH CARD MARKUP
old_selector_row = re.search(r'<div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:0.75rem; background:rgba\(6,9,16,0.65\); border:1px solid rgba\(255,255,255,0.08\); border-radius:12px; padding:0.65rem 1rem;">.*?</div>\s*</div>', content, re.DOTALL)
if old_selector_row:
    new_selector_row = """<div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:0.75rem; background:rgba(6,9,16,0.75); border:1px solid rgba(255,255,255,0.1); border-radius:12px; padding:0.75rem 1.15rem;">
        <div style="display:flex; align-items:center; gap:0.55rem; font-size:0.86rem; font-weight:700; color:#f8fafc;">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--cyan-bright)" stroke-width="2.5"><path d="M23 7l-7 5 7 5V7z"></path><rect x="1" y="5" width="15" height="14" rx="2" ry="2"></rect></svg>
          <span>Cámara a Analizar:</span>
        </div>
        <div style="flex:1; max-width:480px;">
          <select id="aiCameraSelect" class="ai-camera-dropdown" onchange="onAICameraSelectChange(this.value)" style="border-radius:8px; padding:0.55rem 0.95rem; font-size:0.86rem;">
            <option value="" disabled selected>Elige una cámara en específico para consultar con IA...</option>
          </select>
        </div>
        <div style="font-size:0.76rem; color:var(--cyan-bright); font-weight:700; display:flex; align-items:center; gap:0.4rem; background:rgba(6,182,212,0.1); border:1px solid rgba(6,182,212,0.25); padding:0.35rem 0.75rem; border-radius:9999px;">
          <span style="display:inline-block; width:6px; height:6px; border-radius:50%; background:var(--cyan-bright); box-shadow:0 0 8px var(--cyan-bright);"></span>
          <span>Análisis Pericial Focalizado</span>
        </div>
      </div>"""
    content = content[:old_selector_row.start()] + new_selector_row + content[old_selector_row.end():]
    print("✓ Camera selector row markup updated")

# 4. FIX EMPTY STATE IN renderEvents
old_empty_state = re.search(r'container\.innerHTML = `\s*<div style="padding:2\.5rem; text-align:center;.*?<\/div>\s*`;', content, re.DOTALL)
if old_empty_state:
    new_empty_state = """container.innerHTML = `
          <div style="padding:3.2rem 2rem; text-align:center; width:100%; border:1px dashed rgba(255,255,255,0.14); border-radius:16px; background:rgba(13, 18, 30, 0.65); backdrop-filter:blur(16px); box-shadow:0 8px 30px rgba(0,0,0,0.5);">
            <div style="width:54px; height:54px; margin:0 auto 1.1rem; border-radius:50%; background:rgba(6,182,212,0.12); border:1px solid rgba(6,182,212,0.35); display:flex; align-items:center; justify-content:center; color:#00f2fe; box-shadow:0 0 20px rgba(6,182,212,0.2);">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"></rect><line x1="7" y1="2" x2="7" y2="22"></line><line x1="17" y1="2" x2="17" y2="22"></line><line x1="2" y1="12" x2="22" y2="12"></line><line x1="2" y1="7" x2="7" y2="7"></line><line x1="2" y1="17" x2="7" y2="17"></line><line x1="17" y1="17" x2="22" y2="17"></line><line x1="17" y1="7" x2="22" y2="7"></line></svg>
            </div>
            <p style="font-size:1.1rem; font-weight:700; color:#f8fafc; font-family:'Plus Jakarta Sans', sans-serif;">
              ${isSpecific ? 'No se encontraron grabaciones correspondientes a esta consulta' : 'Aún no hay grabaciones registradas en este período'}
            </p>
            <p style="font-size:0.86rem; color:#94a3b8; margin-top:0.4rem; max-width:540px; margin-left:auto; margin-right:auto; line-height:1.55;">
              ${isSpecific ? 'El motor pericial analizó las grabaciones de la cámara sin encontrar coincidencias para el criterio indicado.' : 'El sistema de detección inteligente YOLOv11 está activo y monitoreando 24/7. Cualquier movimiento o persona detectada se indexará automáticamente.'}
            </p>
            ${isSpecific ? '<button class="btn-play-clip" style="margin-top:1.25rem; font-size:0.82rem; padding:0.5rem 1.25rem;" onclick="resetSearch()">✕ Ver todas las grabaciones</button>' : ''}
          </div>
        `;"""
    content = content[:old_empty_state.start()] + new_empty_state + content[old_empty_state.end():]
    print("✓ Empty state template updated to Cyber SOC card")

# 5. FIX THEME SWITCHER LOGIC (ALWAYS ENFORCE DARK)
old_theme_func = re.search(r'function applyTheme\(theme\)\s*\{.*?function toggleTheme\(\)\s*\{.*?\}', content, re.DOTALL)
if old_theme_func:
    new_theme_func = """function applyTheme(theme) {
      currentTheme = 'dark';
      document.documentElement.setAttribute('data-theme', 'dark');
      localStorage.setItem('smartcam_theme', 'dark');
      const sunIcon = document.getElementById('themeIconSun');
      const moonIcon = document.getElementById('themeIconMoon');
      const text = document.getElementById('themeText');
      if (sunIcon) sunIcon.style.display = 'none';
      if (moonIcon) moonIcon.style.display = 'inline-block';
      if (text) text.innerText = 'SOC 24/7 Modo Noche';
    }

    function toggleTheme() {
      applyTheme('dark');
      showToast("Modo de Centro de Monitoreo SOC 24/7 activo", "success");
    }"""
    content = content[:old_theme_func.start()] + new_theme_func + content[old_theme_func.end():]
    print("✓ Theme logic updated to always lock to Dark SOC")

html_path.write_text(content, encoding="utf-8")
print("Finished patching frontend/index.html")
