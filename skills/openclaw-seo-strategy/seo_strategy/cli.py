from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .analyzer import DEFAULT_CONTEXT, InputError, build_report, fetch_url, parse_page
from .formatter import to_json, to_markdown


def _read_input(args: argparse.Namespace) -> tuple[str, str | None, str]:
    if args.url:
        return fetch_url(args.url), args.url, "url"

    if args.input_file:
        path = Path(args.input_file)
        if not path.exists():
            raise InputError(f"El archivo no existe: {path}")
        return path.read_text(encoding="utf-8"), None, "file"

    if args.text:
        return args.text, None, "text"

    if not sys.stdin.isatty():
        return sys.stdin.read(), None, "stdin"

    raise InputError("Debes indicar --url, --input-file, --text o pasar contenido por stdin.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="openclaw-seo-strategy",
        description="Auditoría SEO estratégica v1 para servicios inmobiliarios.",
    )
    parser.add_argument("--url", help="URL a analizar")
    parser.add_argument("--input-file", help="Archivo HTML o TXT a analizar")
    parser.add_argument("--text", help="Texto/HTML inline")
    parser.add_argument("--brand", default=DEFAULT_CONTEXT["brand"])
    parser.add_argument("--location", default=DEFAULT_CONTEXT["location"])
    parser.add_argument("--output", choices=["markdown", "json"], default="markdown")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        content, source_url, source_type = _read_input(args)
        page = parse_page(content, source=source_type, url=source_url)
        context = {"brand": args.brand, "location": args.location}
        report = build_report(page, context)
    except InputError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # noqa: BLE001
        print(f"[ERROR] Fallo inesperado durante el análisis: {exc}", file=sys.stderr)
        return 1

    if args.output == "json":
        print(to_json(report))
    else:
        print(to_markdown(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
