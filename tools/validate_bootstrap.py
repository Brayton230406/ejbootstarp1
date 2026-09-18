from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[str] = []
        self.elements: list[tuple[str, dict[str, str]]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.append(tag)
        self.elements.append((tag, {key: value or "" for key, value in attrs}))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.elements.append((tag, {key: value or "" for key, value in attrs}))


def validate_page(path: Path, offline: bool) -> list[str]:
    errors: list[str] = []
    html = path.read_text(encoding="utf-8")
    parser = PageParser()
    parser.feed(html)
    tags = parser.tags
    ids = {attrs.get("id") for _, attrs in parser.elements if attrs.get("id")}

    if "<!doctype html>" not in html.lower():
        errors.append("falta <!doctype html>")
    if not re.search(r'<html\b[^>]*\blang=["\']es["\']', html, re.I):
        errors.append('falta lang="es"')
    for required in ("header", "nav", "main", "footer"):
        if required not in tags:
            errors.append(f"falta <{required}>")
    if len(re.findall(r"<h1\b", html, re.I)) != 1:
        errors.append("debe existir exactamente un h1")

    for tag, attrs in parser.elements:
        if tag == "img" and not attrs.get("alt", "").strip():
            errors.append("imagen sin alt")
        if tag == "a" and attrs.get("target") == "_blank":
            rel = set(attrs.get("rel", "").lower().split())
            if not {"noopener", "noreferrer"}.issubset(rel):
                errors.append("enlace _blank sin noopener/noreferrer")
        if tag == "a" and attrs.get("href", "").startswith("http:"):
            errors.append("enlace externo inseguro con http")
        if tag == "a" and attrs.get("href", "").startswith("#") and attrs["href"][1:] not in ids:
            errors.append(f"ancla sin destino: {attrs['href']}")

    for ref in re.findall(r'(?:src|href)=["\']([^"\']+)', html, re.I):
        if ref.startswith("https://") and not urlparse(ref).netloc:
            errors.append(f"URL externa inválida: {ref}")
        if not re.match(r"^(?:https?:|#|mailto:|javascript:)", ref) and not (path.parent / ref).exists():
            errors.append(f"recurso local inexistente: {ref}")

    if offline and re.search(r"https?://", html, re.I):
        errors.append("la página offline contiene una dependencia remota")
    return errors


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "paginaCristianoRonaldo")
    pages = [(root / "bootstrap-online.html", False), (root / "bootstrap-offline.html", True)]
    all_errors: list[str] = []
    for path, offline in pages:
        if not path.is_file():
            all_errors.append(f"falta {path}")
            continue
        for error in validate_page(path, offline):
            all_errors.append(f"{path.name}: {error}")
    if all_errors:
        print("VALIDACIÓN BOOTSTRAP FALLIDA")
        print("\n".join(f"- {error}" for error in all_errors))
        return 1
    print("Validación Bootstrap OK: HTML5, semántica, accesibilidad básica, enlaces y recursos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
