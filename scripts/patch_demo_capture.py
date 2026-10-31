import os

file_path = 'frontend/landing.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_block = '''            <!-- Simulated Live Camera Viewport -->
            <div class="mockup-camera-viewport">
              <!-- Background Camera SVG Grid Scene -->
              <svg class="simulated-stream-bg" viewBox="0 0 640 360" xmlns="http://www.w3.org/2000/svg">
                <defs>
                  <linearGradient id="wallGrad" x1="0" y1="0" x2="1" y2="1">
                    <stop offset="0%" stop-color="#141c2e"/>
                    <stop offset="100%" stop-color="#0a0f1d"/>
                  </linearGradient>
                </defs>
                <rect width="640" height="360" fill="url(#wallGrad)"/>
                <!-- Floor grid lines -->
                <path d="M 0 360 L 240 200 L 400 200 L 640 360" fill="none" stroke="#1f2d48" stroke-width="1.5"/>
                <line x1="320" y1="200" x2="320" y2="360" stroke="#1f2d48" stroke-width="1"/>
                <line x1="160" y1="280" x2="480" y2="280" stroke="#1f2d48" stroke-width="0.8"/>
                <!-- Doorway outline -->
                <rect x="270" y="90" width="100" height="150" fill="#090d18" stroke="#253554" stroke-width="2"/>
                <!-- Person silhouette walking -->
                <circle cx="340" cy="140" r="14" fill="#64748b"/>
                <path d="M 328 158 Q 340 156 352 158 L 350 210 L 330 210 Z" fill="#475569"/>
                <line x1="335" y1="210" x2="328" y2="260" stroke="#334155" stroke-width="6" stroke-linecap="round"/>
                <line x1="345" y1="210" x2="352" y2="258" stroke="#334155" stroke-width="6" stroke-linecap="round"/>
                <line x1="328" y1="168" x2="315" y2="200" stroke="#475569" stroke-width="4.5" stroke-linecap="round"/>
                <line x1="352" y1="168" x2="368" y2="195" stroke="#475569" stroke-width="4.5" stroke-linecap="round"/>
              </svg>

              <!-- Dynamic AI Bounding Box Overlay -->
              <div class="ai-bounding-overlay">
                <div class="bbox-simulated">
                  <div class="bbox-tag">#19 person 0.94 • Movimiento</div>
                </div>
              </div>

              <!-- Camera OSD overlay -->
              <div class="cam-osd-top">
                <span>CAM 01: ENTRADA COMERCIO</span>
                <span id="liveOsdClock">2026-10-31 10:14:52</span>
              </div>

              <div class="cam-osd-bottom">
                <span>RTSP PROXY • BUFFER PRE-ROLL 3.0s</span>
                <span style="color: #00f2fe; font-weight: 600;">BADDGROUP VISION AI</span>
              </div>
            </div>'''

new_block = '''            <!-- Captura Real de la Plataforma de Monitoreo & Filtros de Búsqueda -->
            <div class="mockup-camera-viewport" style="background: #050811; border: 1px solid rgba(6, 182, 212, 0.4); box-shadow: 0 12px 35px rgba(0,0,0,0.7), 0 0 25px rgba(6, 182, 212, 0.12); position: relative; overflow: hidden; border-radius: 14px; aspect-ratio: 16/9; display: flex; align-items: center; justify-content: center;">
              <img src="/static/platform_demo_capture.jpg" alt="Captura Real de la Plataforma Baddgroup Vision AI - Monitoreo de Cámaras y Filtros de Búsqueda" style="width: 100%; height: 100%; object-fit: cover; display: block; border-radius: 13px; transition: transform 0.35s ease;">
              <div style="position: absolute; top: 12px; left: 12px; background: rgba(6, 9, 16, 0.88); backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px); border: 1px solid rgba(0, 242, 254, 0.45); padding: 0.35rem 0.85rem; border-radius: 9999px; font-size: 0.74rem; font-weight: 700; color: #fff; display: flex; align-items: center; gap: 0.45rem; box-shadow: 0 4px 18px rgba(0,0,0,0.6); pointer-events: none;">
                <span class="live-pulse-dot"></span>
                <span>PLATAFORMA ACTIVA • MULTI-CÁMARA & FILTROS DE BÚSQUEDA</span>
              </div>
            </div>'''

assert old_block in content, "old_block not found"
content = content.replace(old_block, new_block, 1)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Demo section successfully updated with real platform capture!")
