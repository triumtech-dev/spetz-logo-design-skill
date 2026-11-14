<div dir="rtl">

# Logo Design Skill

סקיל חינמי לעיצוב לוגו לעסק, בעברית. שירות מטעם Trium Technology.

הסקיל מנהל ראיון קצר על העסק, עוזר לבחור כיוון ויזואלי ומפיק קבצי SVG נקיים (ו-PNG כשמותקן Chrome): לוגו אופקי, מוערם, מילולי, גרסה לרקע כהה וגרסה בשחור בלבד.

## התקנה

הורידו את [spetz-logo-design.zip](https://github.com/triumtech-dev/spetz-logo-design-skill/releases/latest/download/spetz-logo-design.zip) ופרסו אותה לתיקיית הסקילים של Claude (`~/.claude/skills/`). לאחר מכן בקשו מ-Claude: "תעצב לי לוגו לעסק".

## הרצה ישירה של המחולל

דרושה רק Python 3.9 ומעלה, בלי חבילות נוספות.

```bash
python skills/spetz-logo-design/scripts/make_logo.py --name "שם העסק" --color "#2563eb" --style rounded --out out
```

סגנונות: `circle`, `square`, `rounded`. הצבע בפורמט `#RRGGBB`. הוספת `--png` מייצרת גם קבצי PNG, בתנאי ש-Chrome או Edge מותקנים.

## מגבלות

- הפלט הוא נקודת פתיחה ולא תחליף למעצב מקצועי.
- לפני שימוש מסחרי יש לבדוק זמינות שם וסימן מסחרי.
- הסקיל לא כולל ולא מפיץ לוגואים של מותגים.

## רישיון

הקוד ברישיון [MIT](LICENSE). השם והסימנים של Trium Technology שמורים, ראו [NOTICE](NOTICE).

</div>

## English

A free Hebrew-first skill for designing a business logo, a service by Trium Technology. It interviews you about the business, helps pick a direction, and generates clean SVG files (plus PNG when Chrome or Edge is installed): horizontal, stacked, wordmark, dark-background and single-color versions. Python 3.9+ standard library only. Code is MIT licensed; the Trium Technology name and marks are reserved (see NOTICE). It does not include third-party brand logos.

```bash
python skills/spetz-logo-design/scripts/make_logo.py --name "My Business" --color "#2563eb" --out out --png
```
