#!/usr/bin/env python3
"""מחולל כיווני לוגו בסיסיים (SVG) מתוך שם עסק, צבע וסגנון. ספריית התקן בלבד."""
import argparse
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape

FONT = "Assistant, 'Segoe UI', Arial, sans-serif"
STYLES = ("circle", "square", "rounded")


def valid_color(value):
    if not re.fullmatch(r"#[0-9a-fA-F]{6}", value):
        raise argparse.ArgumentTypeError("צבע חייב להיות בפורמט #RRGGBB")
    return value


def mark(style, color, glyph, glyph_color, cx, cy, size):
    r = size / 2
    if style == "circle":
        shape = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}"/>'
    elif style == "square":
        shape = f'<rect x="{cx - r}" y="{cy - r}" width="{size}" height="{size}" fill="{color}"/>'
    else:
        shape = (f'<rect x="{cx - r}" y="{cy - r}" width="{size}" height="{size}" '
                 f'rx="{size * 0.22}" fill="{color}"/>')
    text = (f'<text x="{cx}" y="{cy + size * 0.18}" font-family="{FONT}" font-weight="700" '
            f'font-size="{size * 0.56}" text-anchor="middle" fill="{glyph_color}">{escape(glyph)}</text>')
    return shape + text


def svg(width, height, body, bg=None, label=""):
    rect = f'<rect width="{width}" height="{height}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" role="img" aria-label="{escape(label)}">'
            f'{rect}{body}</svg>\n')


def horizontal(name, style, fg, mark_fill, glyph_fill, bg):
    glyph = name.strip()[0]
    m = mark(style, mark_fill, glyph, glyph_fill, 90, 90, 120)
    t = (f'<text x="170" y="108" font-family="{FONT}" font-weight="700" font-size="64" '
         f'direction="rtl" fill="{fg}">{escape(name)}</text>')
    width = 200 + 40 * len(name)
    return svg(width, 180, m + t, bg, name)


def stacked(name, style, fg, mark_fill, glyph_fill, bg):
    glyph = name.strip()[0]
    width = max(360, 60 + 36 * len(name))
    m = mark(style, mark_fill, glyph, glyph_fill, width / 2, 100, 130)
    t = (f'<text x="{width / 2}" y="250" font-family="{FONT}" font-weight="700" font-size="60" '
         f'text-anchor="middle" direction="rtl" fill="{fg}">{escape(name)}</text>')
    return svg(width, 300, m + t, bg, name)


def wordmark(name, fg, bg):
    width = 80 + 44 * len(name)
    t = (f'<text x="{width / 2}" y="105" font-family="{FONT}" font-weight="800" font-size="72" '
         f'text-anchor="middle" direction="rtl" fill="{fg}">{escape(name)}</text>')
    return svg(width, 160, t, bg, name)


def build(name, style, color, out_dir):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    dark, light = "#111827", "#ffffff"
    files = {
        "horizontal.svg": horizontal(name, style, dark, color, light, None),
        "stacked.svg": stacked(name, style, dark, color, light, None),
        "wordmark.svg": wordmark(name, color, None),
        "horizontal-on-dark.svg": horizontal(name, style, light, light, dark, dark),
        "mono-black.svg": horizontal(name, style, "#000000", "#000000", light, None),
    }
    for fname, content in files.items():
        (out / fname).write_text(content, encoding="utf-8")
    return sorted(files)


def find_chrome():
    import os
    import shutil
    for name in ("chrome", "google-chrome", "chromium", "msedge"):
        found = shutil.which(name)
        if found:
            return found
    for base in (os.environ.get("PROGRAMFILES"), os.environ.get("PROGRAMFILES(X86)")):
        if not base:
            continue
        for rel in (r"Google\Chrome\Application\chrome.exe", r"Microsoft\Edge\Application\msedge.exe"):
            path = Path(base) / rel
            if path.exists():
                return str(path)
    mac = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    return mac if Path(mac).exists() else None


def render_png(out_dir, names):
    import subprocess
    chrome = find_chrome()
    if not chrome:
        print("PNG דולג: Chrome או Edge לא נמצאו", file=sys.stderr)
        return []
    made = []
    for fname in names:
        svg_path = Path(out_dir).resolve() / fname
        m = re.search(r'width="(\d+)" height="(\d+)"', svg_path.read_text(encoding="utf-8"))
        w, h = (int(m.group(1)), int(m.group(2))) if m else (400, 200)
        png = svg_path.with_suffix(".png")
        subprocess.run([chrome, "--headless", "--disable-gpu", "--hide-scrollbars",
                        "--default-background-color=00000000", f"--window-size={w},{h}",
                        f"--screenshot={png}", svg_path.as_uri()],
                       capture_output=True, timeout=60)
        if png.exists():
            made.append(png.name)
    return made


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--name", required=True, help="שם העסק")
    p.add_argument("--color", type=valid_color, default="#2563eb", help="צבע ראשי #RRGGBB")
    p.add_argument("--style", choices=STYLES, default="rounded")
    p.add_argument("--out", required=True, help="תיקיית פלט")
    p.add_argument("--png", action="store_true", help="להפיק גם PNG (דורש Chrome או Edge)")
    a = p.parse_args(argv)
    if not a.name.strip():
        p.error("השם ריק")
    names = build(a.name.strip(), a.style, a.color, a.out)
    for f in names:
        print(f)
    if a.png:
        for f in render_png(a.out, names):
            print(f)
    return 0


if __name__ == "__main__":
    sys.exit(main())
