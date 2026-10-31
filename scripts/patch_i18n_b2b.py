import os

file_path = 'frontend/landing.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update ES I18N
old_es_b2b = '''        b2b_tag: "SOLUCIÓN B2B PARA EMPRESAS DE SEGURIDAD & MONITOREO",
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
        b2b_banner_btn: "Solicitar Alianza para Empresas",'''

new_es_b2b = '''        b2b_tag: "SOLUCIÓN B2B PARA EMPRESAS DE SEGURIDAD & MONITOREO",
        b2b_title: "Vendé Videovigilancia Forense con IA a tus Propios Clientes",
        b2b_desc: "Te proveemos la plataforma de software completa, tu propio panel máster multi-tenant y los servidores en la nube con IA pericial YOLOv11. Vos comercializás las cámaras e IA a tus clientes con tu propia marca o como partner oficial, con márgenes superiores al 500%.",
        b2b_opt1_title: "Plataforma Baddgroup Partner",
        b2b_opt1_desc: "Implementación del software donde vendés y ofrecés la IA respaldado por la plataforma Baddgroup Vision AI a tus abonados.",
        b2b_opt1_btn: "Solicitar Partner Baddgroup ($300 USD)",
        b2b_opt2_title: "Marca Blanca (Plataforma Propia)",
        b2b_opt2_desc: "Tu propia plataforma con tu marca para proveer los servicios de instalación e IA de forma independiente como empresa/negocio frente a tus clientes (sin mención de Baddgroup).",
        b2b_opt2_btn: "Lanzar con Marca Blanca ($500 USD)",
        b2b_monthly_title: "Estructura de Abono Mensual para la Empresa de Seguridad",
        b2b_monthly_desc: "Pagás un costo base mínimo de plataforma y escalás por bloques de cámaras a un costo ultrabajo, asegurando un margen neto superior al 500% en cada cliente.",
        b2b_banner_btn: "Solicitar Alianza y Demo para Empresas de Seguridad",'''

assert old_es_b2b in content, "old_es_b2b not found"
content = content.replace(old_es_b2b, new_es_b2b, 1)

# Update EN I18N
old_en_b2b = '''        b2b_tag: "B2B SOLUTION FOR SECURITY COMPANIES & ALARM STATIONS",
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
        b2b_banner_btn: "Request B2B Security Partnership",'''

new_en_b2b = '''        b2b_tag: "B2B SOLUTION FOR SECURITY COMPANIES & ALARM STATIONS",
        b2b_title: "Sell AI Forensic Video Surveillance to Your Own Clients",
        b2b_desc: "We provide the complete software platform, your dedicated multi-tenant master dashboard, and cloud servers running YOLOv11 forensic AI. You sell security cameras and AI to your clients under your own brand or as an official partner, with net margins over 500%.",
        b2b_opt1_title: "Baddgroup Partner Platform",
        b2b_opt1_desc: "Software implementation where you sell and offer AI backed by the Baddgroup Vision AI brand to your subscribers.",
        b2b_opt1_btn: "Apply for Partner ($300 USD)",
        b2b_opt2_title: "White-Label (Your Own Platform)",
        b2b_opt2_desc: "Your independent platform branded with your company logo, domain, and colors to provide installation and AI services autonomously as your own business (zero Baddgroup mention).",
        b2b_opt2_btn: "Launch with White-Label ($500 USD)",
        b2b_monthly_title: "Monthly SaaS Fee Structure for Security Companies",
        b2b_monthly_desc: "Pay a minimal base platform fee and scale in camera bundles at ultra-low cost, locking in net margins above 500% on every client.",
        b2b_banner_btn: "Request B2B Security Company Partnership",'''

assert old_en_b2b in content, "old_en_b2b not found"
content = content.replace(old_en_b2b, new_en_b2b, 1)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("I18N B2B keys updated successfully!")
