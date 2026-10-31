import os
import re

# Read current landing.html
with open("frontend/landing.html", "r", encoding="utf-8") as f:
    orig = f.read()

# Let's inspect CSS insertion point
# We will replace the header CSS (.site-header, .nav-wrapper, .brand-*, .nav-links, .nav-actions)
# and add .nav-capsule, .segmented-pill, .segmented-btn, .mobile-menu-btn, .mobile-drawer, etc.

NEW_HEADER_CSS = """
    /* ==========================================================================
       HEADER & NAVEGACIÓN SAAS PREMIUM (FLOATING CAPSULE & SUITE)
       ========================================================================== */
    header.site-header {
      position: sticky;
      top: 0;
      z-index: 100;
      background: rgba(6, 9, 16, 0.88);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      transition: var(--transition-smooth);
    }

    .nav-wrapper {
      display: flex;
      align-items: center;
      justify-content: space-between;
      height: 74px;
      gap: 1rem;
    }

    /* ZONA 1: BRAND LOGO */
    .brand-logo {
      display: flex;
      align-items: center;
      gap: 12px;
      text-decoration: none;
      flex-shrink: 0;
    }

    .brand-icon-wrap {
      width: 40px;
      height: 40px;
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
      filter: drop-shadow(0 0 10px rgba(6, 182, 212, 0.45));
    }

    .brand-text {
      display: flex;
      flex-direction: column;
    }

    .brand-name {
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 1.22rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      color: #fff;
      line-height: 1.1;
    }

    .brand-tagline {
      font-size: 0.65rem;
      font-weight: 700;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--cyan-bright);
    }

    /* ZONA 2: CENTER CAPSULE PILL NAV */
    .nav-capsule-wrapper {
      display: flex;
      align-items: center;
      justify-content: center;
      flex: 1;
    }

    .nav-capsule {
      display: flex;
      align-items: center;
      gap: 0.25rem;
      background: rgba(13, 18, 30, 0.72);
      border: 1px solid rgba(255, 255, 255, 0.1);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border-radius: 9999px;
      padding: 0.3rem 0.55rem;
      box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.4), inset 0 1px 1px rgba(255, 255, 255, 0.08);
      list-style: none;
    }

    .nav-capsule li a {
      color: var(--text-muted);
      text-decoration: none;
      font-size: 0.88rem;
      font-weight: 500;
      padding: 0.42rem 0.82rem;
      border-radius: 9999px;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      display: inline-block;
      white-space: nowrap;
    }

    .nav-capsule li a:hover {
      color: #00f2fe;
      background: rgba(6, 182, 212, 0.1);
      box-shadow: 0 0 14px rgba(6, 182, 212, 0.25);
    }

    /* ZONA 3: CONTROLS SUITE & CTA */
    .nav-controls-suite {
      display: flex;
      align-items: center;
      gap: 0.65rem;
      flex-shrink: 0;
    }

    /* SEGMENTED SWITCHER PILLS (CURRENCY & LANGUAGE) */
    .segmented-pill {
      display: inline-flex;
      align-items: center;
      background: rgba(15, 23, 42, 0.75);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 9999px;
      padding: 3px;
      gap: 2px;
      backdrop-filter: blur(12px);
    }

    .segmented-btn {
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-family: inherit;
      font-size: 0.74rem;
      font-weight: 700;
      letter-spacing: 0.05em;
      padding: 0.32rem 0.62rem;
      border-radius: 9999px;
      cursor: pointer;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      line-height: 1;
    }

    .segmented-btn:hover {
      color: #f8fafc;
    }

    .segmented-btn.active {
      background: var(--gradient-brand);
      color: #060911;
      font-weight: 800;
      box-shadow: 0 0 14px rgba(6, 182, 212, 0.4);
    }

    /* ACTION BUTTONS */
    .btn-nav-demo {
      display: inline-flex;
      align-items: center;
      padding: 0.5rem 0.95rem;
      border-radius: 9999px;
      font-size: 0.85rem;
      font-weight: 600;
      text-decoration: none;
      color: #cbd5e1;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.12);
      transition: var(--transition-smooth);
      white-space: nowrap;
    }

    .btn-nav-demo:hover {
      color: #fff;
      background: rgba(255, 255, 255, 0.12);
      border-color: rgba(255, 255, 255, 0.28);
      transform: translateY(-1px);
    }

    .btn-nav-portal {
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
      padding: 0.52rem 1.15rem;
      border-radius: 9999px;
      font-size: 0.86rem;
      font-weight: 700;
      text-decoration: none;
      background: var(--gradient-brand);
      color: #060911;
      box-shadow: 0 0 20px rgba(6, 182, 212, 0.35);
      border: none;
      cursor: pointer;
      transition: var(--transition-smooth);
      white-space: nowrap;
    }

    .btn-nav-portal:hover {
      transform: translateY(-2px);
      box-shadow: 0 0 30px rgba(6, 182, 212, 0.6);
      filter: brightness(1.1);
    }

    /* HAMBURGER BUTTON (MOBILE / TABLET) */
    .mobile-menu-btn {
      display: none;
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid rgba(255, 255, 255, 0.15);
      color: #f8fafc;
      width: 42px;
      height: 42px;
      border-radius: 12px;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.2s ease;
      flex-shrink: 0;
    }

    .mobile-menu-btn:hover {
      border-color: var(--cyan-bright);
      box-shadow: 0 0 16px rgba(6, 182, 212, 0.35);
    }

    /* MOBILE SLIDE-DOWN DRAWER */
    .mobile-drawer {
      display: none;
      position: absolute;
      top: 100%;
      left: 0;
      width: 100%;
      background: rgba(6, 9, 16, 0.98);
      backdrop-filter: blur(24px);
      -webkit-backdrop-filter: blur(24px);
      border-bottom: 1px solid rgba(255, 255, 255, 0.12);
      box-shadow: 0 24px 48px rgba(0, 0, 0, 0.85);
      padding: 1.5rem 1.5rem 2rem;
      flex-direction: column;
      gap: 1.25rem;
      animation: drawerSlideDown 0.28s cubic-bezier(0.16, 1, 0.3, 1) forwards;
      z-index: 999;
    }

    @keyframes drawerSlideDown {
      from { opacity: 0; transform: translateY(-12px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .mobile-drawer.open {
      display: flex;
    }

    .mobile-nav-links {
      display: flex;
      flex-direction: column;
      gap: 0.45rem;
      list-style: none;
    }

    .mobile-nav-links a {
      color: #e2e8f0;
      text-decoration: none;
      font-size: 1.05rem;
      font-weight: 600;
      padding: 0.8rem 1.1rem;
      border-radius: 12px;
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.05);
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .mobile-nav-links a:hover {
      color: #00f2fe;
      border-color: rgba(6, 182, 212, 0.3);
      background: rgba(6, 182, 212, 0.08);
    }

    .mobile-controls-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
      padding-top: 0.8rem;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      flex-wrap: wrap;
    }

    .mobile-switchers-group {
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }

    .mobile-portal-btn {
      width: 100%;
      text-align: center;
      padding: 0.85rem;
      font-size: 1rem;
    }
"""

print("CSS template prepared.")
