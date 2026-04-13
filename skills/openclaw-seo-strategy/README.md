# OpenClaw SEO Strategy Skill (v1)

Skill ligera para auditoría SEO estratégica enfocada en negocio, útil incluso sin datos de tráfico ni Search Console.

## Enfoque de negocio incluido por defecto

- Marca: **ARFA Studios**
- Vertical: servicios visuales para inmobiliaria
- Zona principal: **Tarragona y alrededores**

## Estructura

- `SKILL.md`: instrucciones de activación y uso en OpenClaw.
- `bin/openclaw-seo-strategy`: wrapper CLI.
- `seo_strategy/`: motor modular (parseo, análisis, formateo).
- `requirements.txt`: sin dependencias externas en v1.

## Instalación

Desde la raíz del workspace:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r skills/openclaw-seo-strategy/requirements.txt
```

## Uso rápido

### 1) Analizar por URL

```bash
skills/openclaw-seo-strategy/bin/openclaw-seo-strategy \
  --url https://arfastudios.com \
  --output markdown
```

### 2) Analizar HTML/TXT local

```bash
skills/openclaw-seo-strategy/bin/openclaw-seo-strategy \
  --input-file ./home.html \
  --location Tarragona
```

### 3) Analizar texto inline

```bash
skills/openclaw-seo-strategy/bin/openclaw-seo-strategy \
  --text "<html><title>Inicio</title><h1>Servicios visuales</h1></html>"
```

### 4) Salida JSON para automatizar

```bash
skills/openclaw-seo-strategy/bin/openclaw-seo-strategy \
  --url https://arfastudios.com \
  --output json
```

## Errores manejados

- URL no accesible
- Archivo inexistente
- Falta de input (`--url`, `--input-file`, `--text` o `stdin`)
- Fallo inesperado de análisis (mensaje explícito)

## Inputs opcionales recomendados para mejores recomendaciones

- Servicios prioritarios (orden de negocio)
- Localidades secundarias objetivo (Reus, Salou, etc.)
- Tipo de cliente prioritario (inmobiliaria vs. vacacional)
- Oferta comercial principal (pack, plazo, garantía)

## Limitaciones v1

- No reemplaza una investigación de mercado completa.
- No hace crawling multi-sitio ni análisis técnico profundo.
- No usa APIs externas de competencia o volumen de búsqueda.
- Propuestas basadas en heurísticas estratégicas + estructura visible de la página.
