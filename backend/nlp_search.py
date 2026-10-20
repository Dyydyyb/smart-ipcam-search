import json
import re
import datetime
import requests
from typing import List, Dict, Any, Optional
from loguru import logger
from sqlalchemy import select, and_, desc
from core.config import settings
from core.models import SecurityEvent

SYSTEM_PROMPT = """Eres el motor de búsqueda inteligente de un sistema de videovigilancia.
Tu función es convertir la consulta en lenguaje natural del usuario en un objeto JSON con los filtros de búsqueda.

Las clases de objetos válidas son:
['person', 'car', 'truck', 'bus', 'motorcycle', 'bicycle', 'dog', 'cat', 'backpack', 'tv', 'cell phone', 'laptop']

Reglas:
1. Traduce términos en español a las clases válidas (ej: "gente", "hombre", "mujer", "chico" -> "person"; "auto", "coche", "vehiculo" -> ["car", "truck", "motorcycle"]).
2. Si el usuario menciona "última hora", "últimos 30 minutos", "hoy", etc., calcula 'hours_back'. Si no menciona tiempo, usa null.
3. Responde ÚNICAMENTE con el objeto JSON válido, sin texto adicional ni explicaciones.

Ejemplo de salida esperada:
{
  "classes": ["person"],
  "hours_back": 2.0,
  "min_duration": 0,
  "summary": "Personas detectadas en las últimas 2 horas"
}
"""

def parse_query_with_ollama(user_query: str) -> Dict[str, Any]:
    """Envía la consulta del usuario a Ollama (Qwen 2.5) y extrae los filtros estructurados."""
    try:
        url = f"{settings.OLLAMA_HOST}/api/generate"
        payload = {
            "model": settings.OLLAMA_MODEL,
            "prompt": f"{SYSTEM_PROMPT}\nConsulta del usuario: \"{user_query}\"\nJSON:",
            "stream": False,
            "format": "json"
        }
        res = requests.post(url, json=payload, timeout=12.0)
        if res.status_code == 200:
            data = res.json()
            raw_response = data.get("response", "{}")
            parsed = json.loads(raw_response)
            logger.info(f"Filtro interpretado por Ollama: {parsed}")
            return parsed
    except Exception as e:
        logger.warning(f"Ollama no respondió a tiempo o error de parsing: {e}. Usando fallback heurístico.")

    # Fallback heurístico si Ollama tarda o no está disponible
    return fallback_heuristic_parser(user_query)

def fallback_heuristic_parser(query: str) -> Dict[str, Any]:
    """Analizador por patrones regex como respaldo seguro e instantáneo."""
    q = query.lower()
    classes = []
    
    if any(w in q for w in ["persona", "gente", "alguien", "hombre", "mujer", "chico", "chica", "ladron", "sujeto", "brazo", "mano", "movio", "movió", "cuerpo", "gesto"]):
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
        "summary": f"Filtro de búsqueda para: {query}"
    }

async def execute_smart_search(session, user_query: str) -> Dict[str, Any]:
    """Ejecuta la búsqueda inteligente en la base de datos."""
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

    stmt = select(SecurityEvent).order_by(desc(SecurityEvent.start_time)).limit(50)
    if conditions:
        stmt = stmt.where(and_(*conditions))

    result = await session.execute(stmt)
    events = result.scalars().all()

    return {
        "query": user_query,
        "interpreted_filter": parsed_filter,
        "total_results": len(events),
        "results": [e.to_dict() for e in events]
    }
