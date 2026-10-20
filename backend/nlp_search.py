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

def reason_and_pick_specific_event(user_query: str, candidate_events: List[SecurityEvent]) -> Dict[str, Any]:
    """
    Usa Ollama (Qwen 2.5) para razonar sobre los eventos candidatos y seleccionar
    EXCLUSIVAMENTE el evento que responde a la pregunta específica del usuario.
    """
    if not candidate_events:
        return {
            "ai_answer": "No se encontraron grabaciones coincidentes en el historial.",
            "matched_ids": []
        }

    # Construir resumen de eventos para el LLM
    events_summary = []
    for idx, e in enumerate(candidate_events[:15], 1):
        t_str = e.start_time.strftime("%H:%M:%S") if e.start_time else "desconocida"
        events_summary.append(
            f"- Evento #{idx} [ID: {e.id}]: Clase: {e.object_class}, Hora: {t_str}, Duración: {e.duration_seconds}s, Confianza: {int(e.confidence * 100)}%"
        )
    events_text = "\n".join(events_summary)

    prompt = f"""Eres el cerebro analista de seguridad de un sistema de cámaras IP inteligentes.
El usuario realiza la siguiente consulta: "{user_query}"

Aquí tienes los eventos grabados recientemente por la cámara:
{events_text}

Instrucciones estrictas:
1. Responde a la pregunta del usuario con una frase clara y concisa indicando la HORA EXACTA y DURACIÓN del evento más relevante.
2. Si el usuario pregunta por un momento o evento específico (ej: "¿En qué momento alguien movió un brazo?", "¿Cuándo pasó el auto?"), selecciona ÚNICAMENTE el ID del evento que mejor responde a su pregunta (NO selecciones todos).
3. Responde únicamente en formato JSON válido con las claves: "respuesta_ia" y "evento_ids_coincidentes".

Ejemplo de salida JSON:
{{
  "respuesta_ia": "Se detectó el movimiento a las 05:05:18 con una duración de 3.7 segundos.",
  "evento_ids_coincidentes": ["{candidate_events[0].id}"]
}}
"""

    try:
        url = f"{settings.OLLAMA_HOST}/api/generate"
        payload = {
            "model": settings.OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }
        res = requests.post(url, json=payload, timeout=12.0)
        if res.status_code == 200:
            data = res.json()
            parsed = json.loads(data.get("response", "{}"))
            answer = parsed.get("respuesta_ia")
            matched = parsed.get("evento_ids_coincidentes", [])
            if answer and matched:
                return {
                    "ai_answer": answer,
                    "matched_ids": matched
                }
    except Exception as e:
        logger.warning(f"Error en razonamiento LLM: {e}")

    # Fallback si el LLM falla: tomar el evento más reciente relevante
    latest = candidate_events[0]
    t_str = latest.start_time.strftime("%H:%M:%S") if latest.start_time else ""
    return {
        "ai_answer": f"Se detectó el evento más relevante a las {t_str} con una duración de {latest.duration_seconds}s.",
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

    # Filtro de tiempo
    hours_back = parsed_filter.get("hours_back")
    if hours_back and isinstance(hours_back, (int, float)):
        since_time = datetime.datetime.utcnow() - datetime.timedelta(hours=float(hours_back))
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
        "mostrame", "busca", "buscá", "ver", "en que"
    ]
    is_specific_query = any(w in q_lower for w in specific_keywords) or len(q_lower.split()) >= 3

    if is_specific_query and candidate_events:
        reasoning = reason_and_pick_specific_event(user_query, candidate_events)
        matched_ids = set(reasoning.get("matched_ids", []))
        
        # Filtrar para mostrar EXCLUSIVAMENTE el evento que responde a la consulta
        filtered_events = [e for e in candidate_events if e.id in matched_ids]
        if not filtered_events:
            filtered_events = candidate_events[:1]  # El más relevante
        else:
            filtered_events = filtered_events[:1]  # Únicamente 1 evento exacto

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
