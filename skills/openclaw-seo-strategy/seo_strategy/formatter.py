from __future__ import annotations

import json
from dataclasses import asdict

from .models import SeoReport


def to_json(report: SeoReport) -> str:
    return json.dumps(asdict(report), ensure_ascii=False, indent=2)


def to_markdown(report: SeoReport) -> str:
    lines = [
        "# Informe SEO Estratégico (v1)",
        "",
        "## Resumen ejecutivo",
        f"- {report.executive_summary}",
        "",
        "## Keyword principal sugerida",
        f"- {report.suggested_primary_keyword}",
        "",
        "## Keywords secundarias",
    ]
    lines += [f"- {kw}" for kw in report.secondary_keywords]
    lines += [
        "",
        "## Intención de búsqueda",
        f"- {report.search_intent}",
        "",
        "## Problemas detectados",
    ]

    for issue in report.detected_issues:
        lines += [
            f"- **[{issue.severity.upper()}] {issue.finding}**",
            f"  - Impacto: {issue.impact}",
            f"  - Acción: {issue.recommendation}",
        ]

    lines += ["", "## Oportunidades"]
    lines += [f"- {item}" for item in report.opportunities]

    lines += ["", "## Estructura de páginas recomendada"]
    lines += [f"- {item}" for item in report.page_structure]

    lines += ["", "## Propuesta de titles y metadescripciones"]
    for item in report.title_meta_proposals:
        lines += [
            f"- **{item['page']}**",
            f"  - Title: {item['title']}",
            f"  - Meta: {item['meta']}",
        ]

    lines += ["", "## Propuesta de headings"]
    for item in report.heading_proposals:
        lines += [f"- **{item['page']}**"]
        lines += [f"  - H1: {h}" for h in item["h1"]]
        lines += [f"  - H2: {h}" for h in item["h2"]]

    lines += ["", "## Mejoras de copy y conversión"]
    lines += [f"- {item}" for item in report.copy_improvements]

    lines += ["", "## Plan de contenidos inicial"]
    lines += [f"- {item}" for item in report.content_roadmap]

    lines += ["", "## Plan de acción priorizado"]
    lines += [f"- {item}" for item in report.prioritized_action_plan]

    lines += ["", "## Keywords por servicio (clusters)"]
    for plan in report.keyword_plans_by_service:
        lines += [
            f"- **{plan.service}**",
            f"  - Keyword principal: {plan.primary}",
            f"  - Cluster: {plan.cluster}",
            f"  - Intención: {plan.search_intent}",
        ]
        lines += [f"  - Secundaria: {kw}" for kw in plan.secondary]

    return "\n".join(lines)
