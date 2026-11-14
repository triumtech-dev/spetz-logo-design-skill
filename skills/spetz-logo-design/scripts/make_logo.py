#!/usr/bin/env python3
"""מחולל לוגו (SVG ו-PNG אופציונלי) מתוך שם עסק, סמל, צבעים ופונט. ספריית התקן בלבד."""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from render import FONTS, Spec, build_all  # noqa: E402
from symbols import SYMBOLS, suggest  # noqa: E402

STYLES = ("circle", "square", "rounded")


def valid_color(value):
    if not re.fullmatch(r"#[0-9a-fA-F]{6}", value):
        raise argparse.ArgumentTypeError("צבע חייב להיות בפורמט #RRGGBB")
    return value


def build(spec, out_dir):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    files = build_all(spec)
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


def write_preview(out_dir, names):
    cells = "".join(f'<figure><img src="{n}" alt="{n}"><figcaption>{n}</figcaption></figure>'
                    for n in names)
    html = ('<!doctype html><meta charset="utf-8"><title>Logo preview</title>'
            '<style>body{font-family:sans-serif;display:flex;flex-wrap:wrap;gap:24px;padding:24px}'
            'figure{margin:0;padding:16px;border:1px solid #ccc;background:#fff}'
            'img{max-width:420px;max-height:220px;display:block}'
            'figcaption{font-size:12px;color:#555;margin-top:8px}</style>' + cells)
    (Path(out_dir) / "preview.html").write_text(html, encoding="utf-8")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--name", help="שם העסק")
    p.add_argument("--tagline", default="", help="שורת משנה (אופציונלי)")
    p.add_argument("--symbol", default="monogram",
                   help="שם סמל מהספרייה (ראו --list-symbols) או monogram (אות פותחת)")
    p.add_argument("--color", type=valid_color, default="#2563eb", help="צבע ראשי #RRGGBB")
    p.add_argument("--accent", type=valid_color, default="#f59e0b", help="צבע משני #RRGGBB")
    p.add_argument("--style", choices=STYLES, default="rounded", help="צורת מונוגרמה")
    p.add_argument("--font", choices=sorted(FONTS), default="assistant")
    p.add_argument("--out", help="תיקיית פלט")
    p.add_argument("--png", action="store_true", help="להפיק גם PNG (דורש Chrome או Edge)")
    p.add_argument("--preview", action="store_true", help="ליצור preview.html להשוואה")
    p.add_argument("--list-symbols", action="store_true", help="להציג את הסמלים הזמינים")
    p.add_argument("--suggest", metavar="TEXT", help="הצעת סמלים, צבעים ופונט לפי תיאור התחום")
    a = p.parse_args(argv)

    if a.list_symbols:
        print("\n".join(sorted(SYMBOLS)))
        return 0
    if a.suggest is not None:
        found = suggest(a.suggest)
        if not found:
            print("לא נמצאה התאמה. נסו מילה כללית יותר או בחרו סמל ידנית.")
            return 0
        for f in found:
            print(f"סמלים: {', '.join(f['symbols'])} | צבע: {f['color']} | משני: {f['accent']} "
                  f"| פונט: {f['font']} | סגנון: {f['style']}")
        return 0
    if not a.name or not a.name.strip():
        p.error("חובה --name לא ריק")
    if not a.out:
        p.error("חובה --out")
    if a.symbol != "monogram" and a.symbol not in SYMBOLS:
        p.error(f"סמל לא מוכר: {a.symbol}. ראו --list-symbols")

    spec = Spec(a.name, a.tagline, a.symbol, a.style, a.color, a.accent, a.font)
    names = build(spec, a.out)
    shown = list(names)
    if a.png:
        shown += render_png(a.out, names)
    if a.preview:
        write_preview(a.out, [n for n in shown if n.endswith(".png")] or names)
        shown.append("preview.html")
    print("\n".join(shown))
    return 0


if __name__ == "__main__":
    sys.exit(main())
