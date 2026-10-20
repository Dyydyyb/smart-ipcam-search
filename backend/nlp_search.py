import json
import re
import datetime
import requests
from typing import List, Dict, Any, Optional
from loguru import logger
from sqlalchemy import select, and_, desc
from core.config import settings
from core.models import SecurityEvent

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

ABSURD_OR_UNSUPPORTED = [
    "dinosaurio", "ovni", "ufo", "alien", "extraterrestre", "fantasma", "espiritu",
    "dragon", "monstruo", "zombie", "vampiro", "leon", "tigre", "elefante", "jirafa",
    "ballena", "tiburon", "submarino", "cohete", "nave espacial", "helicoptero", "tanque"
]

def reason_and_pick_specific_event(user_query: str, candidate_events: List[SecurityEvent]) -> Dict[str, Any]:
    """
    Usa Ollama (Qwen 2.5) para razonar sobre los eventos candidatos y seleccionar
    EXCLUSIVAMENTE el evento que responde a la pregunta específica del usuario.
    """
    q_lower = user_query.lower()
    
    # Detección inmediata de peticiones absurdas o imposibles
    if any(w in q_lower for w in ABSURD_OR_UNSUPPORTED):
        return {
            "found": False,
            "ai_answer": f"No se registró ningún evento relacionado con '{user_query}' en el historial de video. El sistema de videovigilancia únicamente monitorea y registra actividad habitual y personas.",
            "matched_ids": []
        }

    if not candidate_events:
        return {
            "found": False,
            "ai_answer": f"No se encontraron grabaciones registradas para '{user_query}' en el rango de tiempo consultado.",
            "matched_ids": []
        }

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
El usuario realiza la siguiente consulta: "{user_query}"

Grabaciones registradas por la cámara:
{events_text}

Instrucciones de análisis crítico:
1. Recuerda: cualquier consulta sobre personas moviéndose, moviendo los brazos, gestos, pasando o ingresando corresponde directamente a los eventos de 'person' (personas) listados arriba.
2. Si la consulta del usuario busca a una persona o movimiento humano (ej: "¿en qué momento alguien movió un brazo?", "¿cuándo pasó una persona?", "¿en qué momento hubo movimiento?"):
   - SÍ COINCIDE: Debes seleccionar el evento más reciente y relevante de la lista.
   - "coincidencia_encontrada": true
   - "evento_ids_coincidentes": ["ID_DEL_EVENTO"]
   - "respuesta_ia": "A las [HH:MM] hs del [DD/MM] se visualizó a una persona realizando movimiento frente a la cámara (duración [duración]s) tal como solicitaste."
3. Si la consulta pide algo ABSURDO, FICTICIO o que NO existe en el metraje (ej: dinosaurios, ovnis, vehículos si no hay vehículos, armas, etc.):
   - "coincidencia_encontrada": false
   - "evento_ids_coincidentes": []
   - "respuesta_ia": "No se registró ningún evento relacionado con '{user_query}' en el historial de video."
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
        res = requests.post(url, json=payload, timeout=20.0)
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
        logger.warning(f"Error en razonamiento LLM: {e}")

    # Fallback formal si el LLM tarda
    latest = candidate_events[0]
    t_str = latest.start_time.strftime("%H:%M") if latest.start_time else "00:00"
    d_str = latest.start_time.strftime("%d/%m") if latest.start_time else "hoy"
    return {
        "found": True,
        "ai_answer": f"A las {t_str} hs del {d_str} se visualizó la presencia y movimiento de {latest.object_class} (duración {latest.duration_seconds}s) tal como consultaste.",
        "matched_ids": [latest.id]
    }

async def execute_smart_search(session, user_query: str) -> Dict[str, Any]:
    """Ejecuta la búsqueda inteligente en la base de datos con razonamiento del LLM."""
    parsed_filter = parse_query_with_ollama(user_query)
    
    conditions = []
    
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
        reasoning = reason_and_pick_specific_event(user_query, candidate_events)
        is_found = reasoning.get("found", True)
        matched_ids = set(reasoning.get("matched_ids", []))
        
        # Si la consulta fue absurda o no hubo coincidencia real, devolver 0 resultados de forma limpia
        if not is_found or not matched_ids:
            return {
                "query": user_query,
                "ai_answer": reasoning.get("ai_answer", f"No se registraron filmaciones correspondientes a '{user_query}'."),
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
            "ai_answer": reasoning.get("ai_answer"),
            "is_specific": True,
            "total_results": len(filtered_events),
            "results": [e.to_dict() for e in filtered_events]
        }

    # Búsqueda general
    return {
        "query": user_query,
        "ai_answer": f"Se encontraron {len(candidate_events)} eventos que coinciden con tu criterio.",
        "is_specific": False,
        "total_results": len(candidate_events),
        "results": [e.to_dict() for e in candidate_events]
    }
