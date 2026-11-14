"""בניית קבצי SVG של לוגו: פריסות, סמל או מונוגרמה, ווריאנטים."""
from xml.sax.saxutils import escape

from symbols import SYMBOLS, symbol_paths

FONTS = {
    "assistant": "Assistant, 'Segoe UI', Arial, sans-serif",
    "heebo": "Heebo, 'Segoe UI', Arial, sans-serif",
    "rubik": "Rubik, 'Segoe UI', Arial, sans-serif",
    "frank": "'Frank Ruhl Libre', 'David Libre', 'Times New Roman', serif",
}
INK = "#111827"
WHITE = "#ffffff"
MUTED = "#6b7280"


def is_rtl(text):
    return any("֐" <= c <= "׿" for c in text)


def text_width(text, size):
    """הערכת רוחב טקסט בפיקסלים (קירוב, ללא מדידת פונט אמיתית)."""
    total = 0.0
    for c in text:
        if c == " ":
            total += 0.28
        elif c.isupper():
            total += 0.72
        elif c.isdigit():
            total += 0.56
        elif "֐" <= c <= "׿":
            total += 0.52
        else:
            total += 0.58
    return total * size


def icon(kind, style, color, glyph_color, x, y, size, name, stroke=6):
    """מצייר סמל (שם מהספרייה) או מונוגרמה בתיבה size x size שפינתה (x, y)."""
    if kind in SYMBOLS:
        d = " ".join(f'<path d="{p}"/>' for p in symbol_paths(kind))
        return (f'<g transform="translate({x:.1f} {y:.1f}) scale({size / 100:.4f})" fill="none" '
                f'stroke="{color}" stroke-width="{stroke}" stroke-linecap="round" '
                f'stroke-linejoin="round">{d}</g>')
    r = size / 2
    cx, cy = x + r, y + r
    if style == "circle":
        shape = f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{color}"/>'
    elif style == "square":
        shape = f'<rect x="{x:.1f}" y="{y:.1f}" width="{size}" height="{size}" fill="{color}"/>'
    else:
        shape = (f'<rect x="{x:.1f}" y="{y:.1f}" width="{size}" height="{size}" '
                 f'rx="{size * 0.22:.1f}" fill="{color}"/>')
    glyph = escape(name.strip()[0])
    return shape + (f'<text x="{cx:.1f}" y="{cy + size * 0.19:.1f}" font-weight="700" '
                    f'font-size="{size * 0.56:.1f}" text-anchor="middle" fill="{glyph_color}">{glyph}</text>')


def svg(width, height, body, font, bg=None, label=""):
    rect = f'<rect width="{width:.0f}" height="{height:.0f}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.0f} {height:.0f}" '
            f'width="{width:.0f}" height="{height:.0f}" font-family="{font}" role="img" '
            f'aria-label="{escape(label)}">{rect}{body}</svg>\n')


class Spec:
    def __init__(self, name, tagline, kind, style, color, accent, font):
        self.name = name.strip()
        self.tagline = (tagline or "").strip()
        self.kind = kind
        self.style = style
        self.color = color
        self.accent = accent
        self.font = FONTS[font]
        self.rtl = is_rtl(self.name)


def _texts(spec, name_fill, tag_fill, x, cy, anchor, size=64, tag_size=26):
    """בלוק שם ושורת משנה ממורכז אנכית סביב cy."""
    gap = 14 if spec.tagline else 0
    h = size * 0.78 + ((gap + tag_size * 0.8) if spec.tagline else 0)
    top = cy - h / 2
    out = (f'<text x="{x:.1f}" y="{top + size * 0.78:.1f}" font-weight="700" font-size="{size}" '
           f'text-anchor="{anchor}" fill="{name_fill}">{escape(spec.name)}</text>')
    if spec.tagline:
        out += (f'<text x="{x:.1f}" y="{top + size * 0.78 + gap + tag_size * 0.8:.1f}" '
                f'font-size="{tag_size}" text-anchor="{anchor}" fill="{tag_fill}">'
                f'{escape(spec.tagline)}</text>')
    return out


def horizontal(spec, fg, icon_color, glyph_color, tag_fill, bg=None):
    pad, s, gap = 30, 120, 28
    w_text = max(text_width(spec.name, 64), text_width(spec.tagline, 26))
    width = 2 * pad + s + gap + w_text
    height = 2 * pad + s
    if spec.rtl:
        ix = width - pad - s
        tx, anchor = ix - gap, "end"
    else:
        ix = pad
        tx, anchor = pad + s + gap, "start"
    body = icon(spec.kind, spec.style, icon_color, glyph_color, ix, pad, s, spec.name)
    body += _texts(spec, fg, tag_fill, tx, height / 2, anchor)
    return svg(width, height, body, spec.font, bg, spec.name)


def stacked(spec, fg, icon_color, glyph_color, tag_fill, bg=None):
    pad, s = 36, 130
    w_text = max(text_width(spec.name, 60), text_width(spec.tagline, 24))
    width = max(s + 2 * pad, w_text + 2 * pad)
    body = icon(spec.kind, spec.style, icon_color, glyph_color, (width - s) / 2, pad, s, spec.name)
    body += _texts(spec, fg, tag_fill, width / 2, pad + s + 30 + (78 if spec.tagline else 40) / 2,
                   "middle", size=60, tag_size=24)
    height = pad + s + 30 + (78 if spec.tagline else 48) + pad / 2
    return svg(width, height, body, spec.font, bg, spec.name)


def wordmark(spec, fg, bar_color, tag_fill, bg=None):
    pad = 40
    w_text = max(text_width(spec.name, 72), text_width(spec.tagline, 26))
    width = w_text + 2 * pad
    height = 150 + (46 if spec.tagline else 0)
    body = (f'<text x="{width / 2:.1f}" y="{pad + 56}" font-weight="800" font-size="72" '
            f'text-anchor="middle" fill="{fg}">{escape(spec.name)}</text>')
    bar_w = min(w_text * 0.5, 180)
    body += (f'<rect x="{(width - bar_w) / 2:.1f}" y="{pad + 78}" width="{bar_w:.1f}" height="6" '
             f'rx="3" fill="{bar_color}"/>')
    if spec.tagline:
        body += (f'<text x="{width / 2:.1f}" y="{pad + 122}" font-size="26" text-anchor="middle" '
                 f'fill="{tag_fill}">{escape(spec.tagline)}</text>')
    return svg(width, height, body, spec.font, bg, spec.name)


def icon_only(spec, icon_color, glyph_color, bg=None):
    s = 200
    body = icon(spec.kind, spec.style, icon_color, glyph_color, 40, 40, 120, spec.name)
    return svg(s, s, body, spec.font, bg, spec.name)


def app_icon(spec):
    """אייקון אפליקציה 512x512 עם רקע צבע ראשי וסמל לבן."""
    s = 512
    bg = f'<rect width="{s}" height="{s}" rx="112" fill="{spec.color}"/>'
    if spec.kind in SYMBOLS:
        body = icon(spec.kind, spec.style, WHITE, WHITE, 136, 136, 240, spec.name, stroke=7)
    else:
        glyph = escape(spec.name.strip()[0])
        body = (f'<text x="{s / 2}" y="{s / 2 + 90}" font-weight="700" font-size="280" '
                f'text-anchor="middle" fill="{WHITE}">{glyph}</text>')
    return svg(s, s, bg + body, spec.font, None, spec.name)


def build_all(spec):
    """מחזיר מילון שם קובץ -> תוכן SVG."""
    return {
        "horizontal.svg": horizontal(spec, INK, spec.color, WHITE, MUTED),
        "stacked.svg": stacked(spec, INK, spec.color, WHITE, MUTED),
        "wordmark.svg": wordmark(spec, spec.color, spec.accent, MUTED),
        "icon.svg": icon_only(spec, spec.color, WHITE),
        "app-icon.svg": app_icon(spec),
        "horizontal-on-dark.svg": horizontal(spec, WHITE, WHITE, INK, "#d1d5db", INK),
        "mono-black.svg": horizontal(spec, "#000000", "#000000", WHITE, "#000000"),
        "mono-white.svg": horizontal(spec, WHITE, WHITE, "#000000", WHITE),
    }
