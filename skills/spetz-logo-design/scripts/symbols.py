"""ספריית סמלים גנריים מקוריים (קווים בלבד, ללא סמלי מותגים) והצעות לפי תחום."""
import math


def _ring(cx, cy, r1, r2, n, offset=0.0):
    parts = []
    for i in range(n):
        a = offset + 2 * math.pi * i / n
        parts.append(f"M{cx + r1 * math.cos(a):.1f} {cy + r1 * math.sin(a):.1f} "
                     f"L{cx + r2 * math.cos(a):.1f} {cy + r2 * math.sin(a):.1f}")
    return " ".join(parts)


def _star(cx, cy, ro, ri):
    pts = []
    for i in range(10):
        r = ro if i % 2 == 0 else ri
        a = -math.pi / 2 + i * math.pi / 5
        pts.append(f"{cx + r * math.cos(a):.1f} {cy + r * math.sin(a):.1f}")
    return "M" + " L".join(pts) + " Z"


# כל סמל: רשימת נתיבים בתיבה 100x100. כולם מצוירים בקו (stroke) עם fill="none".
SYMBOLS = {
    "scales": ["M50 18V82", "M30 84H70", "M18 30H82", "M18 30L8 58H28Z", "M82 30L72 58H92Z",
               "M8 58Q18 72 28 58", "M72 58Q82 72 92 58"],
    "shield": ["M50 12L82 24V50C82 70 68 84 50 90C32 84 18 70 18 50V24Z", "M36 50L47 61L66 38"],
    "book": ["M50 28C40 20 24 20 14 24V76C24 72 40 72 50 80C60 72 76 72 86 76V24C76 20 60 20 50 28Z",
             "M50 28V80"],
    "leaf": ["M20 80C20 40 45 18 82 18C82 55 60 82 20 80Z", "M20 80L58 42"],
    "gear": ["M50 24A26 26 0 1 1 49.9 24Z", "M50 40A10 10 0 1 1 49.9 40Z", _ring(50, 50, 26, 38, 8)],
    "house": ["M12 48L50 16L88 48", "M24 42V84H76V42", "M43 84V62H57V84"],
    "heart": ["M50 84C16 58 14 30 32 24C42 21 49 27 50 33C51 27 58 21 68 24C86 30 84 58 50 84Z"],
    "star": [_star(50, 52, 38, 16)],
    "bolt": ["M56 10L24 54H46L40 90L76 42H54Z"],
    "wave": ["M8 36Q21 20 34 36T60 36T92 36", "M8 54Q21 38 34 54T60 54T92 54", "M8 72Q21 56 34 72T60 72T92 72"],
    "mountain": ["M8 80L36 36L54 62L66 46L92 80Z"],
    "coffee": ["M20 38H66V58C66 72 56 82 43 82C30 82 20 72 20 58Z", "M66 44H74C84 44 84 64 72 64H66",
               "M34 16Q40 24 34 30", "M48 16Q54 24 48 30"],
    "camera": ["M14 30H86V80H14Z", "M50 42A14 14 0 1 1 49.9 42Z", "M36 30L42 18H58L64 30"],
    "code": ["M34 28L12 50L34 72", "M66 28L88 50L66 72", "M56 22L44 78"],
    "chat": ["M16 22H84V62H46L28 80V62H16Z"],
    "key": ["M30 34A16 16 0 1 1 29.9 34Z", "M46 50H88", "M74 50V62", "M84 50V60"],
    "check": ["M50 14A36 36 0 1 1 49.9 14Z", "M32 50L45 63L69 37"],
    "compass": ["M50 14A36 36 0 1 1 49.9 14Z", "M64 36L54 54L36 64L46 46Z"],
    "tree": ["M50 90V58", "M50 12C72 12 84 32 70 48C80 62 62 72 50 66C38 72 20 62 30 48C16 32 28 12 50 12Z"],
    "sun": ["M50 36A14 14 0 1 1 49.9 36Z", _ring(50, 50, 26, 40, 8)],
    "drop": ["M50 12C50 12 22 46 22 62C22 78 34 88 50 88C66 88 78 78 78 62C78 46 50 12 50 12Z"],
    "education": ["M50 20L92 40L50 60L8 40Z", "M26 52V68C38 78 62 78 74 68V52", "M92 40V62"],
    "chart": ["M18 84H86", "M26 84V54", "M44 84V36", "M62 84V62", "M80 84V24"],
    "health": ["M40 16H60V40H84V60H60V84H40V60H16V40H40Z"],
    "shop": ["M22 36H78L84 86H16Z", "M36 36V28C36 12 64 12 64 28V36"],
    "building": ["M24 86V14H76V86Z", "M36 28H44", "M56 28H64", "M36 44H44", "M56 44H64", "M44 86V68H56V86"],
    "people": ["M50 20A14 14 0 1 1 49.9 20Z", "M22 84C22 62 34 54 50 54C66 54 78 62 78 84Z"],
    "document": ["M24 10H60L78 28V90H24Z", "M60 10V28H78", "M36 46H66", "M36 60H66", "M36 74H54"],
}

# מילות מפתח (עברית ואנגלית) -> סמלים, פלטה (ראשי, משני), פונט וסגנון מומלצים
INDUSTRIES = [
    (("עורך דין", "משפט", "חוק", "legal", "law", "attorney"), ["scales", "document", "shield"],
     ("#1e3a5f", "#b8893a"), "frank", "square"),
    (("רפואה", "בריאות", "קליניקה", "טיפול", "health", "clinic", "medical"), ["health", "heart", "leaf"],
     ("#0f766e", "#99f6e4"), "assistant", "circle"),
    (("מזון", "קפה", "מסעדה", "קונדיטוריה", "coffee", "food", "restaurant", "cafe"),
     ["coffee", "leaf", "sun"], ("#9a3412", "#fbbf24"), "rubik", "rounded"),
    (("טכנולוגיה", "תוכנה", "אפליקציה", "סייבר", "tech", "software", "app", "cyber"),
     ["code", "bolt", "shield"], ("#2563eb", "#22d3ee"), "heebo", "rounded"),
    (("חינוך", "הוראה", "קורסים", "לימוד", "education", "school", "course"),
     ["education", "book", "star"], ("#7c3aed", "#fbbf24"), "rubik", "rounded"),
    (("נדלן", "דירות", "בנייה", "אדריכל", "real estate", "construction", "architect"),
     ["house", "building", "key"], ("#0f4c5c", "#e36414"), "heebo", "square"),
    (("פיננסים", "ייעוץ", "ביטוח", "השקעות", "חשבונאות", "finance", "consulting", "accounting"),
     ["chart", "shield", "people"], ("#14532d", "#ca8a04"), "heebo", "square"),
    (("צילום", "עיצוב", "אמנות", "סטודיו", "photo", "design", "studio", "art"),
     ["camera", "star", "wave"], ("#111827", "#f43f5e"), "assistant", "circle"),
    (("טבע", "אקולוגיה", "קיימות", "גינון", "nature", "eco", "garden"),
     ["leaf", "tree", "drop"], ("#166534", "#a3e635"), "assistant", "circle"),
    (("חנות", "מסחר", "אונליין", "shop", "store", "ecommerce"), ["shop", "star", "bolt"],
     ("#be185d", "#fbbf24"), "rubik", "rounded"),
    (("תקשורת", "שיווק", "קהילה", "marketing", "media", "community"), ["chat", "wave", "bolt"],
     ("#ea580c", "#1d4ed8"), "rubik", "rounded"),
    (("ספורט", "כושר", "יוגה", "sport", "fitness", "yoga"), ["bolt", "mountain", "heart"],
     ("#dc2626", "#111827"), "rubik", "square"),
]


def symbol_paths(name):
    return SYMBOLS[name]


def suggest(text):
    """מחזיר רשימת התאמות לפי מילות מפתח בטקסט חופשי."""
    low = text.lower()
    found = []
    for keys, syms, palette, font, style in INDUSTRIES:
        if any(k in low for k in keys):
            found.append({"symbols": syms, "color": palette[0], "accent": palette[1],
                          "font": font, "style": style})
    return found
