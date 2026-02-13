#!/usr/bin/env python3
"""
Wisconsin Adventure Cards - Build Script

Generates the complete GitHub Pages site from data/cards.json.
All HTML/CSS templates are embedded in this script.

Usage:
    pip install segno
    python build.py
"""

import json
import os
import sys
import io
import base64
import html as html_mod

try:
    import segno
    HAS_SEGNO = True
except ImportError:
    HAS_SEGNO = False
    print("Warning: segno not installed. QR codes and print sheets will be skipped.")
    print("         Install with: pip install segno")

BASE_URL = "https://aliamrabdalla.github.io/wisconsin-adventures"


# ============================================================================
# Templates
# ============================================================================

STYLE_CSS = r"""
:root {
  --forest: #2D5016;
  --lake: #1B4965;
  --amber: #C4952A;
  --cream: #FAF8F5;
  --charcoal: #1A1A1A;
  --light-gray: #E8E4DF;
  --white: #FFFFFF;
}
*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  background: var(--cream);
  color: var(--charcoal);
  line-height: 1.6;
}
.page-wrap {
  max-width: 600px;
  margin: 0 auto;
  padding: 1.5rem 1rem;
}

/* ── Card Reveal Page ──────────────────────────── */

.card-header {
  text-align: center;
  padding-bottom: 1rem;
  border-bottom: 2px solid var(--forest);
}
.card-id {
  display: inline-block;
  font-size: 0.7rem;
  font-weight: 600;
  color: var(--lake);
  letter-spacing: 0.15em;
  text-transform: uppercase;
  border: 1px solid var(--lake);
  padding: 0.15rem 0.5rem;
  border-radius: 3px;
  margin-bottom: 0.5rem;
}
.location {
  font-size: 1.75rem;
  font-weight: 800;
  color: var(--forest);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin: 0.25rem 0 0;
}
.badges {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  justify-content: center;
  padding: 1rem 0;
}
.badge {
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--lake);
  background: var(--white);
  border: 1px solid var(--light-gray);
  border-radius: 3px;
  padding: 0.2rem 0.6rem;
}
.reveal {
  padding: 1.25rem 0;
  text-align: center;
  border-bottom: 1px solid var(--light-gray);
}
.reveal-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--charcoal);
  text-transform: uppercase;
  line-height: 1.4;
  letter-spacing: 0.03em;
}
.bonus {
  margin-top: 0.75rem;
  padding: 0.6rem 1rem;
  background: #fef9ee;
  border-left: 3px solid var(--amber);
  text-align: left;
  font-size: 0.9rem;
  border-radius: 0 4px 4px 0;
}
.bonus-label { font-weight: 700; color: var(--amber); }
.summary {
  margin-top: 0.5rem;
  font-style: italic;
  color: #555;
  font-size: 0.95rem;
}
.section {
  padding: 1.25rem 0;
  border-bottom: 1px solid var(--light-gray);
}
.section-title {
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--forest);
  margin-bottom: 0.6rem;
}
.section ul { list-style: none; padding: 0; }
.section ul li {
  padding: 0.25rem 0 0.25rem 1.2rem;
  position: relative;
  font-size: 0.95rem;
}
.section ul li::before {
  content: "\25B8";
  position: absolute;
  left: 0;
  color: var(--amber);
  font-size: 0.8rem;
}
.links { padding: 1.25rem 0; }
.links a {
  display: inline-block;
  margin: 0.25rem 0.4rem 0.25rem 0;
  padding: 0.5rem 1rem;
  background: var(--lake);
  color: var(--white);
  text-decoration: none;
  border-radius: 4px;
  font-size: 0.85rem;
  font-weight: 600;
  transition: background 0.15s;
}
.links a:hover, .links a:focus { background: var(--forest); }
.footer {
  padding: 1.5rem 0 0.5rem;
  text-align: center;
  font-size: 0.75rem;
  color: #999;
}
.footer a { color: #999; text-decoration: none; }
.footer a:hover { color: var(--forest); }

/* ── Index Page ────────────────────────────────── */

.index-header {
  text-align: center;
  padding: 2rem 0 1.5rem;
}
.index-header h1 {
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--forest);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}
.index-header p { color: #666; margin-top: 0.25rem; }
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
  padding: 1rem 0;
}
.grid-card {
  background: var(--white);
  border: 1px solid var(--light-gray);
  border-radius: 6px;
  padding: 1rem;
  text-decoration: none;
  color: inherit;
  transition: box-shadow 0.15s;
  display: block;
}
.grid-card:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.grid-card .gc-id {
  font-size: 0.65rem;
  font-weight: 600;
  color: var(--lake);
  letter-spacing: 0.1em;
}
.grid-card .gc-location {
  font-size: 1rem;
  font-weight: 700;
  color: var(--forest);
  text-transform: uppercase;
  margin: 0.25rem 0 0.5rem;
}
.grid-card .gc-badges { display: flex; flex-wrap: wrap; gap: 0.25rem; }
.grid-card .gc-badge {
  font-size: 0.6rem;
  font-weight: 600;
  color: var(--lake);
  background: var(--cream);
  border: 1px solid var(--light-gray);
  border-radius: 2px;
  padding: 0.1rem 0.4rem;
  text-transform: uppercase;
}
.grid-card .gc-reveal {
  display: inline-block;
  margin-top: 0.5rem;
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--amber);
}
""".lstrip()

CARD_PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>%%location_title%% - Wisconsin Adventure Cards</title>
  <link rel="stylesheet" href="../../assets/style.css">
</head>
<body>
  <div class="page-wrap">
    <header class="card-header">
      <span class="card-id">%%card_id%%</span>
      <h1 class="location">%%location_title%%</h1>
    </header>
    <div class="badges">
      <span class="badge">%%cost%%</span>
      <span class="badge">%%time_of_day%%</span>
      <span class="badge">%%duration%%</span>
      <span class="badge">%%setting%%</span>
      <span class="badge">%%effort%%</span>
      <span class="badge">%%season%%</span>
    </div>
    <section class="reveal">
      <h2 class="reveal-title">%%reveal_title%%</h2>
%%bonus_html%%
%%summary_html%%
    </section>
    <section class="section">
      <h3 class="section-title">What to Do</h3>
      <ul>
%%steps_html%%
      </ul>
    </section>
    <section class="section">
      <h3 class="section-title">Good to Know</h3>
      <ul>
%%notes_html%%
      </ul>
    </section>
    <div class="links">
      <h3 class="section-title">Links</h3>
%%links_html%%
    </div>
    <footer class="footer">
      <p>Details can change. Always verify hours, fees, and availability before you go.</p>
      <p><a href="../../index.html">Wisconsin Adventure Cards</a></p>
    </footer>
  </div>
</body>
</html>
"""

INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Wisconsin Adventure Cards</title>
  <link rel="stylesheet" href="assets/style.css">
</head>
<body>
  <div class="page-wrap" style="max-width: 960px;">
    <header class="index-header">
      <h1>Wisconsin Adventure Cards</h1>
      <p>50 adventures across the Badger State</p>
    </header>
    <div class="card-grid">
%%card_items%%
    </div>
    <footer class="footer">
      <p>Wisconsin Adventure Cards</p>
    </footer>
  </div>
</body>
</html>
"""

INDEX_CARD_TEMPLATE = """      <a href="%%card_url%%" class="grid-card">
        <span class="gc-id">%%card_id%%</span>
        <div class="gc-location">%%location_title%%</div>
        <div class="gc-badges">
          <span class="gc-badge">%%cost%%</span>
          <span class="gc-badge">%%time_of_day%%</span>
          <span class="gc-badge">%%duration%%</span>
          <span class="gc-badge">%%setting%%</span>
          <span class="gc-badge">%%effort%%</span>
          <span class="gc-badge">%%season%%</span>
        </div>
        <span class="gc-reveal">Reveal &rarr;</span>
      </a>"""

PRINT_PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Wisconsin Adventure Cards - Print</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  <style>
    @page { size: letter; margin: 0; }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }
    .p-page {
      width: 8.5in;
      height: 11in;
      display: grid;
      grid-template-columns: 3in 3in;
      grid-template-rows: 5in 5in;
      gap: 0.25in;
      padding: 0.375in 1.125in;
      page-break-after: always;
    }
    .p-page:last-child { page-break-after: auto; }
    .p-card {
      width: 3in;
      height: 5in;
      border: 1px solid #2D5016;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      overflow: hidden;
    }
    .p-empty { border: none; }
    .p-banner {
      width: 100%;
      background: #2D5016;
      color: #fff;
      padding: 0.22in 0.18in 0.2in;
      position: relative;
      flex-shrink: 0;
    }
    .p-id {
      position: absolute;
      top: 0.06in;
      right: 0.1in;
      font-size: 5pt;
      color: rgba(255,255,255,0.3);
      letter-spacing: 0.05em;
    }
    .p-location {
      font-size: 16pt;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      line-height: 1.15;
    }
    .p-qr {
      width: 2.1in;
      height: 2.1in;
      margin-top: 0.35in;
    }
    .p-qr img { width: 100%; height: 100%; image-rendering: pixelated; }
    .p-badges {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 0.06in;
      width: 100%;
      padding: 0 0.12in;
      margin-top: auto;
      margin-bottom: 0.15in;
    }
    .p-badge {
      font-size: 8.5pt;
      font-weight: 900;
      text-transform: uppercase;
      color: #1B4965;
      border: 0.75pt solid #bbb;
      border-radius: 3pt;
      padding: 4pt 2pt;
      text-align: center;
      white-space: nowrap;
      overflow: hidden;
      line-height: 1.3;
    }
    .p-icon {
      font-size: 10pt;
      display: block;
      margin-bottom: 1pt;
    }
  </style>
</head>
<body>
%%pages%%
</body>
</html>
"""

PRINT_CARD_TEMPLATE = """    <div class="p-card">
      <div class="p-banner">
        <span class="p-id">%%card_id%%</span>
        <div class="p-location">%%location_title%%</div>
      </div>
      <div class="p-qr"><img src="%%qr_src%%" alt="QR %%card_id%%"></div>
      <div class="p-badges">%%badges%%</div>
    </div>"""

GITIGNORE = """__pycache__/
*.pyc
.DS_Store
Thumbs.db
"""


# ============================================================================
# Helpers
# ============================================================================

def esc(text):
    """HTML-escape text content."""
    return html_mod.escape(str(text))


def write_file(path, content):
    """Write content to a file, creating directories as needed."""
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def render(template, replacements):
    """Replace %%key%% placeholders in template with values."""
    result = template
    for key, value in replacements.items():
        result = result.replace(f"%%{key}%%", str(value))
    return result


# ============================================================================
# Build functions
# ============================================================================

def load_cards():
    with open("data/cards.json", "r", encoding="utf-8") as f:
        return json.load(f)


def build_css():
    write_file("assets/style.css", STYLE_CSS)


def build_card_page(card):
    bonus_html = ""
    if card.get("bonus"):
        bonus_html = f'      <div class="bonus"><span class="bonus-label">Bonus: </span>{esc(card["bonus"])}</div>'

    summary_html = ""
    if card.get("summary_blurb"):
        summary_html = f'      <p class="summary">{esc(card["summary_blurb"])}</p>'

    steps_html = "\n".join(f"        <li>{esc(s)}</li>" for s in card["steps"])
    notes_html = "\n".join(f"        <li>{esc(n)}</li>" for n in card["notes"])
    links_html = "\n".join(
        f'      <a href="{esc(l["url"])}" target="_blank" rel="noopener">{esc(l["label"])}</a>'
        for l in card["links"]
    )

    page_html = render(CARD_PAGE_TEMPLATE, {
        "card_id": esc(card["id"]),
        "location_title": esc(card["location_title"]),
        "cost": esc(card["cost"]),
        "time_of_day": esc(card["time_of_day"]),
        "duration": esc(card["duration"]),
        "setting": esc(card["setting"]),
        "effort": esc(card["effort"]),
        "season": esc(card["season"]),
        "reveal_title": esc(card["reveal_title"]),
        "bonus_html": bonus_html,
        "summary_html": summary_html,
        "steps_html": steps_html,
        "notes_html": notes_html,
        "links_html": links_html,
    })

    write_file(f"cards/{card['id']}/index.html", page_html)


def build_qr(card):
    url = f"{BASE_URL}/cards/{card['id']}/"
    qr = segno.make(url)
    os.makedirs("qr", exist_ok=True)
    qr.save(f"qr/{card['id']}.svg", scale=10, border=2)
    qr.save(f"qr/{card['id']}.png", scale=25, border=2)


def get_qr_data_uri(url):
    qr = segno.make(url)
    buff = io.BytesIO()
    qr.save(buff, kind="png", scale=25, border=2)
    data = base64.b64encode(buff.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{data}"


def build_index(cards):
    card_items = []
    for card in cards:
        item = render(INDEX_CARD_TEMPLATE, {
            "card_id": esc(card["id"]),
            "location_title": esc(card["location_title"]),
            "cost": esc(card["cost"]),
            "time_of_day": esc(card["time_of_day"]),
            "duration": esc(card["duration"]),
            "setting": esc(card["setting"]),
            "effort": esc(card["effort"]),
            "season": esc(card["season"]),
            "card_url": f"cards/{card['id']}/index.html",
        })
        card_items.append(item)

    page_html = render(INDEX_TEMPLATE, {
        "card_items": "\n".join(card_items),
    })
    write_file("index.html", page_html)


BADGE_ICONS = {
    "cost":     {"_default": "fa-solid fa-dollar-sign"},
    "time":     {"DAY": "fa-solid fa-sun", "NIGHT": "fa-solid fa-moon", "EITHER": "fa-solid fa-clock"},
    "duration": {"_default": "fa-solid fa-hourglass-half"},
    "setting":  {"INDOOR": "fa-solid fa-house", "OUTDOOR": "fa-solid fa-mountain-sun", "BOTH": "fa-solid fa-door-open"},
    "effort":   {"CHILL": "fa-solid fa-couch", "MODERATE": "fa-solid fa-person-walking", "ACTIVE": "fa-solid fa-person-running"},
    "season":   {"WINTER": "fa-solid fa-snowflake", "SPRING": "fa-solid fa-seedling", "SUMMER": "fa-solid fa-sun",
                 "FALL": "fa-solid fa-leaf", "ANY": "fa-solid fa-calendar", "_default": "fa-solid fa-calendar"},
}

def badge_icon(category, value):
    cat = BADGE_ICONS.get(category, {})
    cls = cat.get(value, cat.get("_default", ""))
    if not cls:
        return ""
    return f'<i class="p-icon {cls}"></i>'


def build_print_sheets(cards):
    pages = [cards[i:i+4] for i in range(0, len(cards), 4)]
    all_pages = []

    for page_cards in pages:
        card_htmls = []
        for card in page_cards:
            url = f"{BASE_URL}/cards/{card['id']}/"
            qr_uri = get_qr_data_uri(url)

            badge_fields = [
                ("cost", card["cost"]),
                ("time", card["time_of_day"]),
                ("duration", card["duration"]),
                ("setting", card["setting"]),
                ("effort", card["effort"]),
                ("season", card["season"]),
            ]
            badge_html = "".join(
                f'<span class="p-badge">{badge_icon(cat, val)}{esc(val)}</span>'
                for cat, val in badge_fields
            )

            card_html = render(PRINT_CARD_TEMPLATE, {
                "location_title": esc(card["location_title"]),
                "qr_src": qr_uri,
                "card_id": esc(card["id"]),
                "badges": badge_html,
            })
            card_htmls.append(card_html)

        while len(card_htmls) < 4:
            card_htmls.append('    <div class="p-card p-empty"></div>')

        page_html = f'  <div class="p-page">\n{"".join(card_htmls)}\n  </div>'
        all_pages.append(page_html)

    full_html = render(PRINT_PAGE_TEMPLATE, {
        "pages": "\n".join(all_pages),
    })
    write_file("print/cards.html", full_html)


# ============================================================================
# Main
# ============================================================================

def main():
    print("Loading card data...")
    cards = load_cards()
    print(f"  Found {len(cards)} cards.")

    print("Writing stylesheet...")
    build_css()

    print("Generating card pages...")
    for card in cards:
        build_card_page(card)

    print("Generating index page...")
    build_index(cards)

    if HAS_SEGNO:
        print("Generating QR codes...")
        for card in cards:
            build_qr(card)

        print("Generating print sheets...")
        build_print_sheets(cards)
    else:
        print("Skipping QR codes and print sheets (segno not installed).")

    print("Writing .gitignore...")
    write_file(".gitignore", GITIGNORE)

    print()
    print("Done! Generated:")
    print(f"  {len(cards)} card pages     -> cards/WI-XXX/index.html")
    if HAS_SEGNO:
        print(f"  {len(cards)} QR SVGs + PNGs -> qr/")
        print(f"  1 print layout            -> print/cards.html")
    print(f"  1 index page              -> index.html")
    print(f"  1 stylesheet              -> assets/style.css")


if __name__ == "__main__":
    main()
