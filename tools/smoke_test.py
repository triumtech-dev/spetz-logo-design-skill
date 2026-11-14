#!/usr/bin/env python3
"""בדיקות עשן: מחולל הלוגו, ספריית הסמלים, היעדר ספריית מותגים והיעדר מציינים לא מוחלפים."""
import os
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "skills" / "spetz-logo-design" / "scripts"
SCRIPT = SCRIPTS / "make_logo.py"
EXPECTED = {"horizontal.svg", "stacked.svg", "wordmark.svg", "icon.svg", "app-icon.svg",
            "horizontal-on-dark.svg", "mono-black.svg", "mono-white.svg"}
BAD_TOKENS = ("{{SPETZ_URL}}", "{{REPO}}", "botmanishma/spetz-logo-design-skill")
failures = []


def check(cond, msg):
    if not cond:
        failures.append(msg)
        print("FAIL:", msg)


def run(*args):
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    return subprocess.run([sys.executable, "-I", str(SCRIPT), *args], env=env,
                          capture_output=True, text=True, encoding="utf-8", errors="replace")


def read(path):
    return Path(path).read_text(encoding="utf-8")


sys.path.insert(0, str(SCRIPTS))
import make_logo  # noqa: E402
from symbols import INDUSTRIES, SYMBOLS, suggest  # noqa: E402

# ספריית הסמלים: כל סמל חייב להפיק SVG תקין, וכל הצעה חייבת להצביע לסמל קיים
for sym in SYMBOLS:
    with tempfile.TemporaryDirectory() as t:
        r = run("--name", "Acme", "--symbol", sym, "--out", t)
        check(r.returncode == 0, f"הסמל {sym} נכשל: {r.stderr}")
        try:
            ET.parse(Path(t) / "icon.svg")
        except ET.ParseError as e:
            check(False, f"icon.svg של {sym} לא תקין: {e}")
for _, syms, palette, font, style in INDUSTRIES:
    check(all(s in SYMBOLS for s in syms), f"הצעה מצביעה לסמל לא קיים: {syms}")
    check(all(re.fullmatch(r"#[0-9a-f]{6}", c) for c in palette), f"צבע לא תקין: {palette}")
check(suggest("עורך דין")[0]["symbols"][0] == "scales", "הצעה לעורך דין שגויה")
check(suggest("zzzz") == [], "הצעה לא אמורה להתאים לטקסט אקראי")

with tempfile.TemporaryDirectory() as tmp:
    r = run("--name", "קפה הדר", "--tagline", "קפה מיוחד", "--symbol", "coffee",
            "--color", "#c2410c", "--font", "rubik", "--out", tmp, "--preview")
    check(r.returncode == 0, "המחולל נכשל: " + r.stderr)
    produced = {p.name for p in Path(tmp).glob("*.svg")}
    check(produced == EXPECTED, f"קבצי פלט שגויים: {sorted(produced)}")
    for p in Path(tmp).glob("*.svg"):
        try:
            ET.parse(p)
        except ET.ParseError as e:
            check(False, f"{p.name} אינו XML תקין: {e}")
    text = read(Path(tmp) / "horizontal.svg")
    check("קפה הדר" in text and "קפה מיוחד" in text, "שם או שורת משנה חסרים ב-SVG")
    check('text-anchor="end"' in text, "בעברית הטקסט אמור להיות מיושר לימין הסמל")
    check((Path(tmp) / "preview.html").exists(), "preview.html לא נוצר")

    run("--name", "Acme", "--out", tmp + "/l")
    ltr = read(Path(tmp) / "l" / "horizontal.svg")
    check('text-anchor="start"' in ltr, "בלטינית הטקסט אמור להיות משמאל לסמל")

    if make_logo.find_chrome():
        png_out = Path(tmp) / "png"
        pr = run("--name", "בדיקה", "--symbol", "star", "--out", str(png_out), "--png")
        pngs = list(png_out.glob("*.png"))
        check(pr.returncode == 0 and len(pngs) == len(EXPECTED), f"PNG לא נוצרו ({len(pngs)})")
        check(all(p.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n" for p in pngs), "קובץ PNG לא תקין")
    else:
        print("PNG checks skipped: no Chrome/Edge")

    inj = run("--name", '<script>x</script>&"', "--tagline", "<b>", "--out", tmp + "/i")
    inj_text = read(Path(tmp) / "i" / "horizontal.svg")
    check(inj.returncode == 0 and "<script>" not in inj_text and "<b>" not in inj_text,
          "קלט עם תווים מסוכנים לא עבר escape")

check(run("--name", "א", "--color", "red", "--out", "x").returncode != 0, "צבע שגוי התקבל")
check(run("--name", "  ", "--out", "x").returncode != 0, "שם ריק התקבל")
check(run("--name", "א", "--symbol", "nope", "--out", "x").returncode != 0, "סמל לא מוכר התקבל")
check(run("--list-symbols").stdout.split() == sorted(SYMBOLS), "--list-symbols שגוי")
check(not (ROOT / "skills" / "spetz-logo-design" / "assets" / "library" / "svg").exists(),
      "קיימת ספריית לוגואים של מותגים")

for f in ROOT.rglob("*"):
    if f.is_file() and ".git" not in f.parts and "__pycache__" not in f.parts and f.name != "smoke_test.py":
        try:
            content = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for tok in BAD_TOKENS:
            check(tok not in content, f"{tok} נמצא ב-{f.relative_to(ROOT)}")
        check(len(content.splitlines()) <= 450 or f.suffix not in (".py",),
              f"קובץ ארוך מדי: {f.relative_to(ROOT)}")

if failures:
    print(f"{len(failures)} checks failed")
    sys.exit(1)
print("all checks passed")
