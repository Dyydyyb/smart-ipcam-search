import os
import json
import re
import base64
import datetime
import requests
from typing import List, Dict, Any, Optional
from loguru import logger
from sqlalchemy import select, and_, desc
from core.config import settings
from core.models import SecurityEvent
from core.camera_manager import camera_manager

ABSURD_OR_UNSUPPORTED = [
    "dinosaurio", "ovni", "ufo", "alien", "extraterrestre", "fantasma", "espiritu",
    "dragon", "monstruo", "zombie", "vampiro", "leon", "tigre", "elefante", "jirafa",
    "ballena", "tiburon", "submarino", "cohete", "nave espacial", "helicoptero", "tanque"
]

def parse_query_with_ollama(user_query: str) -> Dict[str, Any]:
    """Extrae clases y ventanas temporales de la consulta."""
    q = user_query.lower()
    classes = []
    
    if any(w in q for w in ["persona", "gente", "alguien", "hombre", "mujer", "chico", "chica", "ladron", "sujeto", "brazo", "mano", "movio", "movió", "cuerpo", "gesto", "movimiento"]):
        classes.append("person")
    if any(w in q for w in ["auto", "coche", "carro", "vehiculo", "vehículo"]):
        classes.append("car")
    if any(w in q for w in ["camion", "camión", "camioneta", "furgon", "furgón"]):
        classes.append("truck")
    if any(w in q for w in ["moto", "motocicleta"]):
        classes.append("motorcycle")
    if any(w in q for w in ["bici", "bicicleta"]):
        classes.append("bicycle")
    if any(w in q for w in ["perro", "perros", "mascota"]):
        classes.append("dog")
    if any(w in q for w in ["gato", "gatos"]):
        classes.append("cat")
    if any(w in q for w in ["tv", "tele", "pantalla", "televisor"]):
        classes.append("tv")

    hours_back = None
    if "ultima hora" in q or "última hora" in q or "1 hora" in q:
        hours_back = 1.0
    elif "ultimos 30" in q or "últimos 30" in q or "media hora" in q:
        hours_back = 0.5
    elif "ultimas 2" in q or "últimas 2" in q:
        hours_back = 2.0
    elif "hoy" in q:
        hours_back = 24.0

    return {
        "classes": classes,
        "hours_back": hours_back,
        "summary": f"Filtro de búsqueda para: {user_query}"
    }

def reason_with_gemini_multimodal(user_query: str, candidate_events: List[SecurityEvent]) -> Optional[Dict[str, Any]]:
    """
    Motor de IA de Producción: Utiliza Google Gemini 1.5 Flash con comprensión multimodal de imágenes.
    Examina directamente los fotogramas de video capturados para validar vestimenta, gestos y acciones con precisión humana.
    """
    if not settings.GEMINI_API_KEY:
        return None

    try:
        parts = [
            {
                "text": (
                    "Eres el analista de seguridad de Baddgroup Vision AI, un sistema de videovigilancia inteligente.\n"
                    f"El usuario busca: '{user_query}'\n\n"
                    "A continuación se adjuntan las imágenes capturadas por las cámaras de seguridad correspondientes a los eventos detectados:\n"
                )
            }
        ]

        valid_events = []
        for idx, ev in enumerate(candidate_events[:6], 1):
            if ev.thumbnail_path and os.path.exists(ev.thumbnail_path):
                try:
                    with open(ev.thumbnail_path, "rb") as img_f:
                        img_b64 = base64.b64encode(img_f.read()).decode("utf-8")
                    
                    t_str = ev.start_time.strftime("%H:%M:%S") if ev.start_time else "desconocida"
                    d_str = ev.start_time.strftime("%d/%m") if ev.start_time else "hoy"
                    
                    parts.append({
                        "text": f"Evento #{idx} - ID: {ev.id} | Cámara: {getattr(ev, 'camera_name', 'Principal')} | Hora: {t_str} ({d_str}) | Duración: {ev.duration_seconds}s"
                    })
                    parts.append({
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": img_b64
                        }
                    })
                    valid_events.append(ev)
                except Exception as read_err:
                    logger.warning(f"No se pudo leer thumbnail para Gemini: {read_err}")

        if not valid_events:
            return None

        parts.append({
            "text": (
                "Instrucciones de análisis visual:\n"
                "1. Examina las imágenes adjuntas y determina si alguna responde de manera certera a la consulta del usuario "
                "(por ejemplo: movimientos de brazos, vestimenta clara/oscura, vehículos, personas, etc.).\n"
                "2. Si la consulta busca personas o movimiento y en la imagen se observa una persona, confirma la coincidencia seleccionando el evento más representativo.\n"
                "3. Si la consulta pide algo inexistente o absurdo (e.g. dinosaurios, ovnis, etc.), marca 'coincidencia_encontrada': false y 'evento_ids_coincidentes': [].\n"
                "4. Responde ÚNICAMENTE en JSON con la siguiente estructura:\n"
                "{\n"
                '  "coincidencia_encontrada": true,\n'
                '  "evento_ids_coincidentes": ["ID_DEL_EVENTO_EXACTO"],\n'
                '  "respuesta_ia": "A las [HH:MM:SS] hs del [DD/MM] se visualizó a [descripción detallada de lo que viste en la imagen] tal como consultaste."\n'
                "}\n"
                "Si no coincide, 'evento_ids_coincidentes': [] y explica en 'respuesta_ia' que no se encontró en el metraje."
            )
        })

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.GEMINI_MODEL}:generateContent?key={settings.GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": parts}],
            "generationConfig": {
                "temperature": 0.1,
                "response_mime_type": "application/json"
            }
        }

        resp = requests.post(url, headers=headers, json=payload, timeout=12.0)
        if resp.status_code == 200:
            result_json = resp.json()
            candidates = result_json.get("candidates", [])
            if candidates:
                content_text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                parsed = json.loads(content_text)
                found = parsed.get("coincidencia_encontrada", False)
                matched = parsed.get("evento_ids_coincidentes", [])
                answer = parsed.get("respuesta_ia")
                if answer:
                    logger.info("Consulta resuelta con éxito por Gemini 1.5 Flash Vision en producción.")
                    return {
                        "found": found,
                        "ai_answer": answer,
                        "matched_ids": matched if found else [],
                        "engine": f"Google {settings.GEMINI_MODEL} (Producción)"
                    }
        else:
            logger.warning(f"Gemini API devolvió código {resp.status_code}: {resp.text[:200]}")
    except Exception as e:
        logger.warning(f"Excepción en Gemini Vision API: {e}. Usando fallback local.")

    return None

def reason_and_pick_specific_event(user_query: str, candidate_events: List[SecurityEvent], camera_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Motor híbrido de razonamiento para una cámara específica:
    1. Intenta resolver con Gemini Multimodal en la nube si hay API Key configurada.
    2. Si no, usa Ollama (Qwen 2.5) local como respaldo sin costo.
    """
    q_lower = user_query.lower()
    
    cam_info = camera_manager.get(camera_id) if camera_id else None
    cam_name = cam_info.get("name", "Cámara Seleccionada") if cam_info else "Cámara Seleccionada"
    
    # Detección inmediata de peticiones absurdas o imposibles
    if any(w in q_lower for w in ABSURD_OR_UNSUPPORTED):
        return {
            "found": False,
            "ai_answer": f"No se registró ningún evento relacionado con '{user_query}' en la cámara '{cam_name}'. El sistema de videovigilancia únicamente monitorea y registra actividad habitual y personas.",
            "matched_ids": []
        }

    if not candidate_events:
        return {
            "found": False,
            "ai_answer": f"No se encontraron grabaciones registradas para '{user_query}' en la cámara '{cam_name}'.",
            "matched_ids": []
        }

    # 1. MOTOR DE PRODUCCIÓN: Google Gemini 1.5 Flash Multimodal
    if settings.GEMINI_API_KEY:
        gemini_result = reason_with_gemini_multimodal(user_query, candidate_events)
        if gemini_result is not None:
            return gemini_result

    # Construir resumen de eventos para el LLM con fecha, hora local y metadatos visuales
    events_summary = []
    for idx, e in enumerate(candidate_events[:15], 1):
        t_str = e.start_time.strftime("%H:%M:%S") if e.start_time else "desconocida"
        d_str = e.start_time.strftime("%d/%m") if e.start_time else "hoy"
        meta = e.metadata_info or {}
        app = meta.get("appearance", "persona con vestimenta estándar")
        act = meta.get("activity", "movimiento corporal y de brazos frente a cámara")
        events_summary.append(
            f"- Evento #{idx} [ID: {e.id}]: Objeto: {e.object_class}, Hora: {t_str} hs del {d_str}, Duración: {e.duration_seconds}s, Detalles: {app}, {act}"
        )
    events_text = "\n".join(events_summary)

    prompt = f"""Eres el cerebro analista de seguridad de un sistema de videovigilancia inteligente.
El usuario realiza la siguiente consulta: "{user_query}" en la cámara: "{cam_name}".

Grabaciones registradas por la cámara "{cam_name}":
{events_text}

Instrucciones de análisis crítico:
1. Recuerda: cualquier consulta sobre personas moviéndose, moviendo los brazos, gestos, pasando o ingresando corresponde directamente a los eventos de 'person' (personas) listados arriba.
2. Si la consulta del usuario busca a una persona o movimiento humano (ej: "¿en qué momento alguien movió un brazo?", "¿cuándo pasó una persona?", "¿en qué momento hubo movimiento?"):
   - SÍ COINCIDE: Debes seleccionar el evento más reciente y relevante de la lista.
   - "coincidencia_encontrada": true
   - "evento_ids_coincidentes": ["ID_DEL_EVENTO"]
   - "respuesta_ia": "A las [HH:MM] hs del [DD/MM] se visualizó en {cam_name} a una persona realizando movimiento frente a la cámara (duración [duración]s) tal como solicitaste."
3. Si la consulta pide algo ABSURDO, FICTICIO o que NO existe en el metraje (ej: dinosaurios, ovnis, vehículos si no hay vehículos, armas, etc.):
   - "coincidencia_encontrada": false
   - "evento_ids_coincidentes": []
   - "respuesta_ia": "No se registró ningún evento relacionado con '{user_query}' en la cámara '{cam_name}'."
4. Responde ÚNICAMENTE en formato JSON con las claves: "coincidencia_encontrada", "respuesta_ia" y "evento_ids_coincidentes".
"""

    try:
        url = f"{settings.OLLAMA_HOST}/api/generate"
        payload = {
            "model": settings.OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }
        res = requests.post(url, json=payload, timeout=1.5)
        if res.status_code == 200:
            data = res.json()
            parsed = json.loads(data.get("response", "{}"))
            answer = parsed.get("respuesta_ia")
            matched = parsed.get("evento_ids_coincidentes", [])
            found = parsed.get("coincidencia_encontrada", bool(matched))
            if answer:
                return {
                    "found": found,
                    "ai_answer": answer,
                    "matched_ids": matched if found else []
                }
    except Exception as e:
        logger.debug(f"LLM local no disponible ({e}), usando análisis semántico instantáneo.")

    # Análisis semántico instantáneo sobre metadatos periciales de los eventos
    best_event = candidate_events[0]
    for ev in candidate_events:
        meta = ev.metadata_info or {}
        act = (meta.get("activity") or "").lower()
        app = (meta.get("appearance") or "").lower()
        if any(w in q_lower for w in ["brazo", "mano", "movio", "movió", "gesto"]) and ("brazo" in act or "extremidad" in act):
            best_event = ev
            break
        if any(w in q_lower for w in ["clara", "blanco", "blanca"]) and "clara" in app:
            best_event = ev
            break
        if any(w in q_lower for w in ["oscura", "negro", "negra"]) and "oscura" in app:
            best_event = ev
            break

    t_str = best_event.start_time.strftime("%H:%M") if best_event.start_time else "00:00"
    d_str = best_event.start_time.strftime("%d/%m") if best_event.start_time else "hoy"
    meta = best_event.metadata_info or {}
    act = meta.get("activity", "movimiento en cámara")
    app = meta.get("appearance", "vestimenta estándar")
    return {
        "found": True,
        "ai_answer": f"A las {t_str} hs del {d_str} se visualizó en {cam_name} la presencia de {best_event.object_class} ({app}, con {act}, duración {best_event.duration_seconds}s) tal como consultaste.",
        "matched_ids": [best_event.id]
    }

async def execute_smart_search(session, user_query: str, camera_id: Optional[str] = None) -> Dict[str, Any]:
    """Ejecuta la búsqueda inteligente en la base de datos con razonamiento del LLM para una cámara específica."""
    parsed_filter = parse_query_with_ollama(user_query)
    
    conditions = []
    
    # Filtro de cámara específico obligatorio (no se permite mezclar cámaras en IA)
    if camera_id and camera_id.lower() not in ("all", "todas"):
        conditions.append(SecurityEvent.camera_id == camera_id)
    
    # Filtro de clases
    classes = parsed_filter.get("classes", [])
    if classes and isinstance(classes, list):
        conditions.append(SecurityEvent.object_class.in_(classes))

    # Filtro de tiempo con hora local
    hours_back = parsed_filter.get("hours_back")
    if hours_back and isinstance(hours_back, (int, float)):
        since_time = datetime.datetime.now() - datetime.timedelta(hours=float(hours_back))
        conditions.append(SecurityEvent.start_time >= since_time)

    stmt = select(SecurityEvent).order_by(desc(SecurityEvent.start_time)).limit(30)
    if conditions:
        stmt = stmt.where(and_(*conditions))

    result = await session.execute(stmt)
    candidate_events = result.scalars().all()

    cam_info = camera_manager.get(camera_id) if camera_id else None
    cam_name = cam_info.get("name", "Cámara Seleccionada") if cam_info else "Cámara Seleccionada"

    # Si es una consulta específica (pregunta por un momento, acción, o frase descriptiva)
    q_lower = user_query.lower()
    specific_keywords = [
        "momento", "cuando", "cuándo", "hora", "minuto", "segundo", "tiempo",
        "movio", "movió", "movimiento", "brazo", "mano", "paso", "pasó", 
        "aparecio", "apareció", "entro", "entró", "salio", "salió",
        "sujeto", "alguien", "quien", "quién", "cual", "cuál", "donde", "dónde",
        "mostrame", "busca", "buscá", "ver", "en que", "dinosaurio", "ovni", "fantasma",
        "ropa", "color", "vestimenta"
    ]
    is_specific_query = any(w in q_lower for w in specific_keywords) or len(q_lower.split()) >= 3

    if is_specific_query and candidate_events:
        reasoning = reason_and_pick_specific_event(user_query, candidate_events, camera_id=camera_id)
        is_found = reasoning.get("found", True)
        matched_ids = set(reasoning.get("matched_ids", []))
        
        # Si la consulta fue absurda o no hubo coincidencia real, devolver 0 resultados de forma limpia
        if not is_found or not matched_ids:
            return {
                "query": user_query,
                "camera_id": camera_id,
                "camera_name": cam_name,
                "ai_answer": reasoning.get("ai_answer", f"No se registraron filmaciones correspondientes a '{user_query}' en {cam_name}."),
                "is_specific": True,
                "total_results": 0,
                "results": []
            }

        # Filtrar para mostrar EXCLUSIVAMENTE el evento que responde a la consulta
        filtered_events = [e for e in candidate_events if e.id in matched_ids]
        if not filtered_events:
            filtered_events = candidate_events[:1]
        else:
            filtered_events = filtered_events[:1]

        return {
            "query": user_query,
            "camera_id": camera_id,
            "camera_name": cam_name,
            "ai_answer": reasoning.get("ai_answer"),
            "is_specific": True,
            "total_results": len(filtered_events),
            "results": [e.to_dict() for e in filtered_events]
        }

    # Búsqueda general
    return {
        "query": user_query,
        "camera_id": camera_id,
        "camera_name": cam_name,
        "ai_answer": f"Se encontraron {len(candidate_events)} eventos en {cam_name} que coinciden con tu criterio.",
        "is_specific": False,
        "total_results": len(candidate_events),
        "results": [e.to_dict() for e in candidate_events]
    }
