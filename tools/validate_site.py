from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


class SiteParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.elements: list[tuple[str, dict[str, str]]] = []
        self.text_by_tag: dict[str, list[str]] = {}
        self.open_tags: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {key: value or "" for key, value in attrs}
        self.elements.append((tag, attributes))
        self.open_tags.append(tag)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {key: value or "" for key, value in attrs}
        self.elements.append((tag, attributes))

    def handle_endtag(self, tag: str) -> None:
        if tag in self.open_tags:
            index = len(self.open_tags) - 1 - self.open_tags[::-1].index(tag)
            self.open_tags.pop(index)

    def handle_data(self, data: str) -> None:
        if self.open_tags:
            self.text_by_tag.setdefault(self.open_tags[-1], []).append(data)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    html_path = root / "index.html"
    css_path = root / "styles.css"
    js_path = root / "script.js"

    for path in (html_path, css_path, js_path):
        if not path.is_file():
            fail(errors, f"Falta el archivo requerido: {path}")

    if errors:
        return errors

    html = html_path.read_text(encoding="utf-8")
    css = css_path.read_text(encoding="utf-8")
    js = js_path.read_text(encoding="utf-8")
    parser = SiteParser()
    try:
        parser.feed(html)
        parser.close()
    except Exception as exc:  # pragma: no cover - HTMLParser errors vary by Python version.
        fail(errors, f"HTML no parseable: {exc}")

    tags = [tag for tag, _ in parser.elements]
    attributes_by_tag = [(tag, attrs) for tag, attrs in parser.elements]
    ids = {attrs["id"] for _, attrs in attributes_by_tag if attrs.get("id")}

    if "<!doctype html>" not in html.lower():
        fail(errors, "index.html debe declarar <!doctype html>.")
    if not re.search(r"<html\b[^>]*\blang=[\"']es[\"']", html, re.I):
        fail(errors, "El documento debe declarar lang=\"es\".")
    for required in ("header", "nav", "main", "footer"):
        if required not in tags:
            fail(errors, f"Falta el elemento semántico <{required}>.")

    if len(re.findall(r"<h1\b", html, re.I)) != 1:
        fail(errors, "Debe existir exactamente un h1.")
    heading_levels = [int(level) for level in re.findall(r"<h([1-6])\b", html, re.I)]
    for previous, current in zip(heading_levels, heading_levels[1:]):
        if current > previous + 1:
            fail(errors, f"Jerarquía de encabezados salta de h{previous} a h{current}.")

    if not re.search(r'<meta\b[^>]*name=["\']viewport["\']', html, re.I):
        fail(errors, "Falta meta viewport.")
    if not re.search(r'<title>\s*[^<]+\s*</title>', html, re.I):
        fail(errors, "Falta un title no vacío.")

    for tag, attrs in attributes_by_tag:
        if tag == "img" and not attrs.get("alt", "").strip():
            fail(errors, "Toda imagen debe tener un alt no vacío.")
        if tag == "button" and attrs.get("type") != "button":
            fail(errors, "Todo botón de interfaz debe declarar type=\"button\".")
        if tag == "a" and attrs.get("target") == "_blank":
            rel = set(attrs.get("rel", "").lower().split())
            if not {"noopener", "noreferrer"}.issubset(rel):
                fail(errors, f"Enlace _blank inseguro: {attrs.get('href', '<sin href>')}")
        if tag == "a" and attrs.get("href", "").startswith("http:"):
            fail(errors, f"Enlace externo no cifrado: {attrs['href']}")
        if tag == "button" and attrs.get("aria-controls") and attrs["aria-controls"] not in ids:
            fail(errors, f"aria-controls apunta a un id inexistente: {attrs['aria-controls']}")
        if tag == "button" and "aria-expanded" in attrs and attrs.get("aria-expanded") not in {"true", "false"}:
            fail(errors, "aria-expanded debe ser true o false.")

    for href in re.findall(r'<a\b[^>]*\bhref=["\']([^"\']+)', html, re.I):
        if href.startswith("#") and href[1:] not in ids:
            fail(errors, f"Enlace interno sin destino: {href}")
        if href.startswith("https://"):
            parsed = urlparse(href)
            if not parsed.netloc:
                fail(errors, f"URL externa inválida: {href}")

    for required_css in (":focus-visible", "@media (max-width: 760px)", "prefers-reduced-motion", "aspect-ratio"):
        if required_css not in css:
            fail(errors, f"styles.css no contiene la regla responsive/accesible esperada: {required_css}")

    forbidden = ("react", "vue", "angular", "jquery")
    if any(re.search(rf"\b{library}\b", js, re.I) for library in forbidden):
        fail(errors, "script.js contiene una dependencia/framework no permitido.")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida el sitio estático para CI.")
    parser.add_argument("root", type=Path, help="Carpeta que contiene index.html")
    args = parser.parse_args()
    errors = validate(args.root)
    if errors:
        print("VALIDACIÓN FALLIDA")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Validación estática OK: HTML semántico, ARIA, enlaces, imágenes, CSS responsive y JavaScript sin frameworks.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
