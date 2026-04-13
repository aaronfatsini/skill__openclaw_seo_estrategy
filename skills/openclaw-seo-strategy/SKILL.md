---
name: openclaw-seo-strategy
description: Genera una auditoría SEO estratégica accionable (sin Search Console) para webs de servicios, con foco en propuesta de valor, keywords por servicio/localidad, arquitectura, titles/meta, headings, copy y plan priorizado.
---

# OpenClaw SEO Strategy (v1)

Usa esta skill cuando el usuario quiera **mejorar estrategia SEO** aunque tenga poco o ningún tráfico orgánico.

## Qué cubre

- Auditoría estratégica on-page básica
- Propuesta de arquitectura SEO
- Keywords por servicio + localidad
- Propuesta de titles/meta/H1/H2
- Recomendaciones de copy y conversión
- Plan de contenidos inicial y plan de acción priorizado

## Qué no cubre (v1)

- Search Console
- Crawling complejo
- Backlinks masivos
- Integraciones/API pesadas

## Inputs soportados

1. URL (`--url`)
2. HTML/TXT en archivo (`--input-file`)
3. HTML/TXT inline (`--text` o `stdin`)

Opcionales:
- `--brand` (default: ARFA Studios)
- `--location` (default: Tarragona)
- `--output markdown|json`

## Ejecución

```bash
skills/openclaw-seo-strategy/bin/openclaw-seo-strategy --url https://arfastudios.com
```

```bash
skills/openclaw-seo-strategy/bin/openclaw-seo-strategy --input-file home.html --location Tarragona
```

## Flujo recomendado

1. Analizar home y páginas de servicio clave por separado.
2. Detectar gaps de propuesta de valor, foco local y estructura.
3. Aplicar primero acciones P1 (arquitectura + title/H1 + oferta/CTA).
4. Crear una página nueva de alto impacto según el plan priorizado.

## Formato de salida esperado

- Resumen ejecutivo
- Keyword principal y secundarias
- Intención de búsqueda
- Problemas detectados + impacto + acción
- Oportunidades
- Estructura recomendada de páginas
- Titles/meta sugeridos
- Headings sugeridos
- Mejoras de copy
- Plan de contenidos
- Plan de acción priorizado

## Ejemplos de prompts en OpenClaw

- “Analiza la home de arfastudios.com y dime cómo reestructurarla SEO.”
- “Dime qué página nueva debería crear primero y por qué.”
- “Propón mejores keywords para servicio de tour virtual 360 en Tarragona.”
- “Redáctame un title y una meta description para fotografía inmobiliaria Tarragona.”
