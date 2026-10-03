"""Render the public theoretical paper from its Markdown source.

Requires Python Markdown and a local Chrome/Chromium executable. Run from any
directory with ``python papers/render_pdf.py``.
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

import markdown


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "ARTICULO_TEORETICO_METODOLOGICO.md"
OUTPUT = HERE / "ARTICULO_TEORETICO_METODOLOGICO.pdf"
BASE = "https://github.com/SairaAsua/movimiento-armonico-investigacion/blob/main/papers/"

CSS = """
@page { size: A4; margin: 5mm 19mm 5mm 19mm; }
body { font-family: Georgia, "Noto Serif", serif; font-size: 9.1pt;
       line-height: 1.0; color: #172d35; }
h1, h2, h3 { font-family: Arial, sans-serif; color: #173f4b;
             line-height: 1.18; break-after: avoid; }
h1 { font-size: 21pt; margin: 0 0 20pt; }
h2 { font-size: 14pt; margin: 11pt 0 6pt; }
h3 { font-size: 11.8pt; margin: 9pt 0 5pt; }
p { margin: 0 0 3.5pt; orphans: 3; widows: 3; }
a { color: #126379; text-decoration: none; }
strong { color: #143946; }
code { font-family: "DejaVu Sans Mono", monospace; font-size: 9pt;
       overflow-wrap: anywhere; }
pre { background: #edf4f4; padding: 8pt; white-space: pre-wrap;
      break-inside: avoid; }
table { border-collapse: collapse; width: 100%; font-size: 8.8pt;
        margin: 8pt 0 12pt; }
th, td { border: 1px solid #b6c8c9; padding: 5pt; vertical-align: top; }
th { background: #e4eeee; }
tr { break-inside: avoid; }
ul, ol { padding-left: 17pt; margin: 5pt 0 10pt; }
li { margin: 0 0 4pt; }
ol li { font-size: 7.5pt; line-height: 0.90; margin-bottom: 0; break-inside: avoid; }
ol li p { margin: 0; }
blockquote { border-left: 3px solid #6ca5a5; padding-left: 10pt;
             color: #425b62; }
hr { border: 0; border-top: 1px solid #a5c1c2; margin: 18pt 0; }
"""


def main() -> None:
    browser = shutil.which("google-chrome") or shutil.which("chromium")
    if browser is None:
        raise SystemExit("Chrome/Chromium is required to render the paper PDF")

    body = markdown.markdown(
        SOURCE.read_text(encoding="utf-8"),
        extensions=["tables", "fenced_code", "sane_lists"],
    )
    html = (
        '<!doctype html><html lang="es"><head><meta charset="utf-8">'
        f'<base href="{BASE}">'
        '<title>Geometría del movimiento</title>'
        f"<style>{CSS}</style></head><body>{body}</body></html>"
    )
    with tempfile.TemporaryDirectory(prefix="paper-render-") as temporary:
        page = Path(temporary) / "paper.html"
        page.write_text(html, encoding="utf-8")
        subprocess.run(
            [
                browser,
                "--headless",
                "--no-sandbox",
                "--disable-gpu",
                "--no-pdf-header-footer",
                f"--print-to-pdf={OUTPUT}",
                page.as_uri(),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
    print(OUTPUT)


if __name__ == "__main__":
    main()
