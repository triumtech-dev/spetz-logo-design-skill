#!/usr/bin/env python3
"""בדיקות עשן: מחולל הלוגו, היעדר ספריית מותגים והיעדר מציינים לא מוחלפים."""
import os
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "skills" / "spetz-logo-design" / "scripts" / "make_logo.py"
EXPECTED = {"horizontal.svg", "stacked.svg", "wordmark.svg",
            "horizontal-on-dark.svg", "mono-black.svg"}
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


with tempfile.TemporaryDirectory() as tmp:
    r = run("--name", "קפה הדר", "--color", "#c2410c", "--style", "circle", "--out", tmp)
    check(r.returncode == 0, "המחולל נכשל: " + r.stderr)
    produced = {p.name for p in Path(tmp).glob("*.svg")}
    check(produced == EXPECTED, f"קבצי פלט שגויים: {sorted(produced)}")
    for p in Path(tmp).glob("*.svg"):
        try:
            ET.parse(p)
        except ET.ParseError as e:
            check(False, f"{p.name} אינו XML תקין: {e}")
    check("קפה הדר" in (Path(tmp) / "wordmark.svg").read_text(encoding="utf-8"), "השם חסר ב-SVG")
    check("<script" not in (Path(tmp) / "horizontal.svg").read_text(encoding="utf-8"), "נמצא script ב-SVG")

    sys.path.insert(0, str(SCRIPT.parent))
    import make_logo
    if make_logo.find_chrome():
        png_out = Path(tmp) / "png"
        pr = run("--name", "בדיקה", "--out", str(png_out), "--png")
        pngs = list(png_out.glob("*.png"))
        check(pr.returncode == 0 and len(pngs) == 5, f"PNG לא נוצרו ({len(pngs)}/5)")
        check(all(p.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n" for p in pngs), "קובץ PNG לא תקין")
    else:
        print("PNG checks skipped: no Chrome/Edge")

    inj = run("--name", '<script>x</script>&"', "--out", tmp)
    check(inj.returncode == 0 and "<script>" not in
          (Path(tmp) / "horizontal.svg").read_text(encoding="utf-8"), "שם עם תווים מסוכנים לא עבר escape")

check(run("--name", "א", "--color", "red", "--out", "x").returncode != 0, "צבע שגוי התקבל")
check(run("--name", "  ", "--out", "x").returncode != 0, "שם ריק התקבל")
check(not (ROOT / "skills" / "spetz-logo-design" / "assets" / "library" / "svg").exists(),
      "קיימת ספריית לוגואים של מותגים")

for f in ROOT.rglob("*"):
    if f.is_file() and ".git" not in f.parts and f.name != "smoke_test.py":
        try:
            text = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for tok in BAD_TOKENS:
            check(tok not in text, f"{tok} נמצא ב-{f.relative_to(ROOT)}")

if failures:
    print(f"{len(failures)} checks failed")
    sys.exit(1)
print("all checks passed")
