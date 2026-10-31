import re
from pathlib import Path

html_path = Path("frontend/index.html")
content = html_path.read_text(encoding="utf-8")

# Let's locate the entire block from :root[data-theme="dark"] down to the end of :root[data-theme="light"] { ... }
start_token = ':root[data-theme="dark"]'
end_token = '    :root[data-theme="light"] {'

idx_start = content.find(start_token)
idx_light = content.find(end_token)
if idx_start != -1 and idx_light != -1:
    # Find the closing brace of light theme
    idx_end = content.find('    }', idx_light) + 5
    print(f"Found root tokens range: {idx_start} to {idx_end}")
    
    unified_tokens = """:root, :root[data-theme="dark"], :root[data-theme="light"] {
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
    content = content[:idx_start] + unified_tokens + content[idx_end:]
    print("Tokens replaced successfully")
else:
    print("Root tokens not found:", idx_start, idx_light)

# Extra CSS rules to guarantee NO white bars, NO white arrow squares, NO unreadable text
css_rules = """
    /* =========================================================
       CYBER SOC OVERHAUL - BADDGROUP VISION AI
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
      padding: 0.95rem 1.2rem 0.95rem 3.1rem !important;
      padding-right: 165px !important;
      background: rgba(6, 9, 16, 0.85) !important;
      border: 1px solid rgba(255, 255, 255, 0.12) !important;
      border-radius: 12px !important;
      color: #ffffff !important;
      font-size: 0.95rem !important;
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
      font-size: 0.85rem !important;
      padding: 0.65rem 1.35rem !important;
      border: none !important;
      border-radius: 10px !important;
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
      padding: 0.42rem 0.95rem !important;
      border-radius: 9999px !important;
      font-size: 0.82rem !important;
      font-weight: 600 !important;
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
      font-weight: 700 !important;
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

if "/* CYBER SOC OVERHAUL - BADDGROUP VISION AI */" not in content:
    content = content.replace("</style>", css_rules + "\n  </style>")

# Update the empty state in renderEvents
old_empty = """          <div style="padding:2.5rem; text-align:center; width:100%; border:1px dashed var(--border-color); border-radius:10px; background:var(--bg-surface);">"""
new_empty = """          <div style="padding:3.2rem 2rem; text-align:center; width:100%; border:1px dashed rgba(255,255,255,0.14); border-radius:16px; background:rgba(13, 18, 30, 0.65); backdrop-filter:blur(16px); box-shadow:0 8px 30px rgba(0,0,0,0.5);">
            <div style="width:54px; height:54px; margin:0 auto 1.1rem; border-radius:50%; background:rgba(6,182,212,0.12); border:1px solid rgba(6,182,212,0.35); display:flex; align-items:center; justify-content:center; color:#00f2fe; box-shadow:0 0 20px rgba(6,182,212,0.2);">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"></rect><line x1="7" y1="2" x2="7" y2="22"></line><line x1="17" y1="2" x2="17" y2="22"></line><line x1="2" y1="12" x2="22" y2="12"></line><line x1="2" y1="7" x2="7" y2="7"></line><line x1="2" y1="17" x2="7" y2="17"></line><line x1="17" y1="17" x2="22" y2="17"></line><line x1="17" y1="7" x2="22" y2="7"></line></svg>
            </div>"""

if old_empty in content:
    content = content.replace(old_empty, new_empty)
    print("Empty state container updated")

# Update theme toggle function to always enforce Dark SOC
old_theme = """    function toggleTheme() {
      applyTheme(currentTheme === 'dark' ? 'light' : 'dark');
    }"""
new_theme = """    function toggleTheme() {
      applyTheme('dark');
      showToast("Modo de Centro de Monitoreo SOC 24/7 activo", "success");
    }"""
if old_theme in content:
    content = content.replace(old_theme, new_theme)
    print("Theme toggle updated to enforce dark")

# Force dark theme on init
content = content.replace("let currentTheme = localStorage.getItem('smartcam_theme') || 'dark';", "let currentTheme = 'dark'; localStorage.setItem('smartcam_theme', 'dark');")

html_path.write_text(content, encoding="utf-8")
print("frontend/index.html patched and written successfully.")
