from __future__ import annotations

import re
from html.parser import HTMLParser
from typing import Dict, List, Optional
from urllib.error import URLError
from urllib.request import Request, urlopen

from .models import Issue, KeywordPlan, PageData, SeoReport

DEFAULT_CONTEXT = {
    "brand": "ARFA Studios",
    "location": "Tarragona",
    "services": [
        "fotografía inmobiliaria",
        "vídeo inmobiliario",
        "dron inmobiliario",
        "tour virtual 360",
        "contenido para venta y alquiler vacacional",
        "contenido para portales inmobiliarios",
    ],
    "audiences": [
        "inmobiliarias",
        "agentes inmobiliarios",
        "promotoras",
        "propietarios de viviendas premium",
        "gestores de alquiler vacacional y Airbnb",
    ],
}


class InputError(ValueError):
    pass


class SimpleHTMLExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._current_tag = ""
        self.title = ""
        self.h1: List[str] = []
        self.h2: List[str] = []
        self.text_parts: List[str] = []
        self.meta_description = ""

    def handle_starttag(self, tag: str, attrs: List[tuple[str, str | None]]) -> None:
        self._current_tag = tag.lower()
        if self._current_tag == "meta":
            attrs_dict = {k.lower(): (v or "") for k, v in attrs}
            if attrs_dict.get("name", "").lower() == "description":
                self.meta_description = attrs_dict.get("content", "").strip()

    def handle_data(self, data: str) -> None:
        text = data.strip()
        if not text:
            return
        self.text_parts.append(text)
        if self._current_tag == "title":
            self.title = f"{self.title} {text}".strip()
        elif self._current_tag == "h1":
            self.h1.append(text)
        elif self._current_tag == "h2":
            self.h2.append(text)


def fetch_url(url: str, timeout: int = 15) -> str:
    try:
        request = Request(url, headers={"User-Agent": "OpenClaw-SEO-Strategy/1.0"})
        with urlopen(request, timeout=timeout) as response:
            return response.read().decode("utf-8", errors="ignore")
    except URLError as exc:
        raise InputError(f"No se pudo descargar la URL '{url}': {exc}") from exc


def parse_page(content: str, source: str, url: Optional[str] = None) -> PageData:
    parser = SimpleHTMLExtractor()
    parser.feed(content)

    text = " ".join(parser.text_parts)
    cta_candidates = re.findall(
        r"\b(contacta|solicita|reserva(?:r)?|llama|pide|empieza|descubre|agenda)\b[^.\n]*",
        text,
        flags=re.I,
    )
    ctas = [c if isinstance(c, str) else str(c) for c in cta_candidates][:8]

    return PageData(
        source=source,
        url=url,
        raw_text=text,
        title=parser.title,
        meta_description=parser.meta_description,
        h1=parser.h1,
        h2=parser.h2,
        ctas=ctas,
    )


def _contains_any(text: str, words: List[str]) -> bool:
    lower = text.lower()
    return any(w.lower() in lower for w in words)


def _build_keyword_plans(location: str) -> List[KeywordPlan]:
    return [
        KeywordPlan(
            service="Fotografía inmobiliaria",
            primary=f"fotografía inmobiliaria {location.lower()}",
            secondary=[
                f"fotógrafo de pisos en {location.lower()}",
                "fotos profesionales para inmobiliaria",
                "fotografía para venta de viviendas",
            ],
            search_intent="Transaccional local",
            cluster="captación de inmuebles",
        ),
        KeywordPlan(
            service="Vídeo inmobiliario",
            primary=f"vídeo inmobiliario {location.lower()}",
            secondary=[
                "video tour de vivienda",
                "vídeo para anunciar piso",
                f"productora inmobiliaria {location.lower()}",
            ],
            search_intent="Transaccional local",
            cluster="contenido visual para venta",
        ),
        KeywordPlan(
            service="Tour virtual 360",
            primary=f"tour virtual 360 inmobiliario {location.lower()}",
            secondary=[
                "visita virtual vivienda",
                "tour 360 para inmobiliarias",
                "recorrido virtual piso",
            ],
            search_intent="Comparativa + contratación",
            cluster="experiencia inmersiva",
        ),
        KeywordPlan(
            service="Dron inmobiliario",
            primary=f"dron inmobiliario {location.lower()}",
            secondary=[
                "fotografía aérea de viviendas",
                "vídeo con dron para promociones",
                "servicio dron para inmobiliaria",
            ],
            search_intent="Transaccional local",
            cluster="diferenciación visual premium",
        ),
    ]


def build_report(page: PageData, context: Dict[str, object]) -> SeoReport:
    location = str(context.get("location") or DEFAULT_CONTEXT["location"])
    brand = str(context.get("brand") or DEFAULT_CONTEXT["brand"])

    issues: List[Issue] = []
    text_lower = page.raw_text.lower()

    if not page.title or len(page.title) < 35:
        issues.append(Issue("weak_title", "alta", "Title inexistente o demasiado genérico/corto.", "Reduce CTR y relevancia para términos de servicio + localidad.", f"Usa formato: 'Servicio principal | {location} | {brand}' con 50-60 caracteres."))
    if not page.meta_description or len(page.meta_description) < 90:
        issues.append(Issue("weak_meta", "media", "Metadescripción ausente o sin propuesta de valor concreta.", "Menor capacidad de atraer clic cualificado.", "Redactar una meta de 130-155 caracteres con beneficio + prueba + CTA."))
    if len(page.h1) != 1:
        issues.append(Issue("h1_structure", "alta", f"Se detectaron {len(page.h1)} H1; debería haber uno enfocado en intención principal.", "Ambigüedad de foco semántico de la página.", "Definir 1 H1 centrado en servicio + ciudad + resultado para cliente."))
    if not _contains_any(page.raw_text, [location, "tarragona", "reus", "salou", "costa daurada"]):
        issues.append(Issue("missing_local_focus", "alta", "No hay señales locales suficientes en el copy visible.", "Difícil competir en búsquedas geolocalizadas de alta intención.", "Integrar localidad objetivo en hero, bloques de servicios, casos y FAQ."))
    if not _contains_any(text_lower, ["inmobiliaria", "vivienda", "piso", "alquiler", "airbnb"]):
        issues.append(Issue("weak_market_fit", "alta", "El copy no refleja claramente el sector inmobiliario objetivo.", "Menor match con intención del cliente y peores señales semánticas.", "Aterrizar mensajes por segmento: inmobiliaria, promotoras, alquiler vacacional."))
    if len(page.ctas) < 2:
        issues.append(Issue("weak_cta", "media", "Pocos CTAs accionables o demasiado genéricos.", "Caída de conversión en leads cualificados.", "Definir CTA principal ('Solicitar presupuesto en 24h') y secundarios por servicio."))

    keyword_plans = _build_keyword_plans(location)
    page_structure = [
        "Home (posicionamiento global + enlaces a servicios + prueba social local)",
        f"/fotografia-inmobiliaria-{location.lower()}",
        f"/video-inmobiliario-{location.lower()}",
        f"/tour-virtual-360-inmobiliario-{location.lower()}",
        f"/dron-inmobiliario-{location.lower()}",
        f"/contenido-airbnb-alquiler-vacacional-{location.lower()}",
        f"/portales-inmobiliarios-contenido-{location.lower()}",
        f"/casos-exito-inmobiliaria-{location.lower()}",
        f"/contacto-servicios-visuales-inmobiliarios-{location.lower()}",
    ]
    title_meta_proposals = [
        {"page": f"Fotografía inmobiliaria {location}", "title": f"Fotografía inmobiliaria en {location} | {brand}", "meta": f"Fotos inmobiliarias profesionales en {location}. Acelera venta o alquiler con imágenes optimizadas para portales y RRSS. Pide presupuesto."},
        {"page": f"Tour virtual 360 {location}", "title": f"Tour virtual 360 inmobiliario en {location} | {brand}", "meta": f"Visitas virtuales 360 para viviendas en {location}. Mejora la cualificación de visitas y destaca frente a otras agencias. Solicita demo."},
    ]
    heading_proposals = [{"page": "Home", "h1": [f"Contenido visual inmobiliario en {location} que acelera ventas y alquileres"], "h2": ["Servicios para inmobiliarias, agentes y promotoras", f"Cómo ayudamos a captar más compradores en {location}", "Casos reales y resultados", "Solicita propuesta en 24 horas"]}]
    copy_improvements = [
        "Abrir la home con promesa medible: 'Publica inmuebles con mejor presentación en 48h'.",
        "Separar claramente cada servicio con bloque: problema -> solución visual -> entregable -> CTA.",
        f"Añadir prueba local: menciones de zonas (ej. {location}, Reus, Salou) y mini casos con resultado.",
        "Incluir objeciones frecuentes (precio, tiempos, derechos de uso) en FAQ comercial.",
    ]
    content_roadmap = [
        f"Semana 1: crear landing de fotografía inmobiliaria + FAQ local ({location}).",
        "Semana 2: publicar landing de tour virtual 360 con comparativa vs visita presencial.",
        "Semana 3: caso de éxito (antes/después) con métricas de tiempo de cierre o leads.",
        "Semana 4: guía para propietarios Airbnb sobre contenido visual que mejora reservas.",
    ]
    prioritized_action_plan = [
        "P1 (impacto alto): redefinir propuesta de valor de la home con enfoque inmobiliario y local.",
        "P1 (impacto alto): crear páginas separadas por servicio para evitar mezcla de intenciones.",
        "P1 (impacto alto): implementar titles/H1 orientados a 'servicio + Tarragona'.",
        "P2: reforzar CTAs con oferta concreta (presupuesto 24h, demo 360, pack captación).",
        "P2: activar bloque de prueba social/casos por segmento de cliente.",
        "P3: ejecutar calendario de contenidos de 4 semanas y medir leads por página.",
    ]

    return SeoReport(
        executive_summary="La página analizada necesita clarificar la propuesta de valor SEO-comercial, separar servicios por intención de búsqueda y reforzar foco local. La prioridad es pasar de una home genérica a una arquitectura por servicios orientada a conversión para inmobiliarias y alquiler vacacional.",
        suggested_primary_keyword=keyword_plans[0].primary,
        secondary_keywords=keyword_plans[0].secondary,
        search_intent=keyword_plans[0].search_intent,
        detected_issues=issues,
        opportunities=["Posicionarse en long-tail local de baja competencia por servicio.", "Captar leads más cualificados con landings dedicadas por segmento.", "Aumentar CTR con titles orientados a resultado comercial y ubicación."],
        page_structure=page_structure,
        title_meta_proposals=title_meta_proposals,
        heading_proposals=heading_proposals,
        copy_improvements=copy_improvements,
        content_roadmap=content_roadmap,
        prioritized_action_plan=prioritized_action_plan,
        keyword_plans_by_service=keyword_plans,
    )
