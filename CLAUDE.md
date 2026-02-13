# Wisconsin Adventure Cards

A 50-card Wisconsin couples adventure deck. Each physical card (3x5 in) shows a location name,
metadata badges, and a QR code. Scanning the QR reveals the full adventure on a GitHub Pages site.

## Build & Deploy

```bash
pip install segno
python build.py
git init
git add -A
git commit -m "Initial build"
git remote add origin git@github.com:aliamrabdalla/wisconsin-adventures.git
git branch -M main
git push -u origin main
```

Enable GitHub Pages: repo Settings > Pages > Source: Deploy from branch > main / root.

## URLs (permanent — QR codes depend on these)

- Site: `https://aliamrabdalla.github.io/wisconsin-adventures/`
- Cards: `https://aliamrabdalla.github.io/wisconsin-adventures/cards/WI-XXX/`
- Repo SSH: `git@github.com:aliamrabdalla/wisconsin-adventures.git`

## Repo Structure (after build)

```
wisconsin-adventures/
  index.html              # Homepage grid of all 50 cards
  build.py                # Build script (generates everything)
  CLAUDE.md
  .gitignore
  assets/
    style.css             # Generated global stylesheet
  cards/
    WI-001/index.html     # Card reveal pages (x50)
    ...
    WI-050/index.html
  data/
    cards.json            # Source of truth
  qr/
    WI-001.svg            # QR images (x50 SVG + x50 PNG)
    WI-001.png
    ...
  print/
    cards.html            # Print-ready layout (4 cards per letter sheet)
```

## Design System

### Colors

| Name       | Hex       | Usage                    |
|------------|-----------|--------------------------|
| Forest     | #2D5016   | Headings, primary accent |
| Lake       | #1B4965   | Badges, links            |
| Amber      | #C4952A   | Highlights, list markers |
| Cream      | #FAF8F5   | Page background          |
| Charcoal   | #1A1A1A   | Body text                |
| Light Gray | #E8E4DF   | Borders, dividers        |

### Typography

System stack only: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif.
No web fonts.

### Metadata Vocabulary (exact allowed values)

| Field    | Allowed Values                                              |
|----------|-------------------------------------------------------------|
| Cost     | $0-$15, $15-$40, $40-$100, $100-$300                       |
| Time     | DAY, NIGHT, EITHER                                          |
| Duration | 1-2H, 2-4H, HALF DAY, FULL DAY                             |
| Setting  | INDOOR, OUTDOOR, BOTH                                       |
| Effort   | CHILL, MODERATE, ACTIVE                                     |
| Season   | WINTER, SPRING, SUMMER, FALL, ANY, or range like SPR-FALL   |

## Data Schema

Source file: `data/cards.json` (array of 50 objects).

```json
{
  "id": "WI-001",
  "location_title": "APPLETON, WI",
  "cost": "$15-$40",
  "time_of_day": "EITHER",
  "duration": "1-2H",
  "setting": "INDOOR",
  "effort": "ACTIVE",
  "season": "ANY",
  "reveal_title": "HEAD TO THE BREAKING POINT LLC RAGE ROOM",
  "bonus": "Bring your own music to jam out to!",
  "summary_blurb": "One sentence description.",
  "steps": ["Step 1", "Step 2", "Step 3"],
  "links": [{"label": "Map", "url": "https://..."}, {"label": "Website", "url": "https://..."}],
  "notes": ["Note 1", "Note 2"]
}
```

`bonus` and `summary_blurb` may be `null`.

## Physical Cards

- Size: 3 x 5 inches, vertical orientation
- Print: 4 per letter sheet (8.5 x 11), dashed cut lines
- Layout (top to bottom): location title, QR code (1.75 in square), card ID, 2x3 badge grid
- Badge order row 1: COST | TIME | DURATION; row 2: SETTING | EFFORT | SEASON

### Printing

1. Run `python build.py` (generates `print/cards.html`)
2. Open `print/cards.html` in a browser
3. Print: no margins, 100% scale, background graphics ON, letter paper
4. Cut along dashed lines
5. 13 sheets for all 50 cards

## Build Script

`build.py` reads `data/cards.json` and generates the entire site. All HTML/CSS templates are
embedded in the script. Only dependency: `segno` (pure Python QR library, no Pillow needed).

It generates:
- `assets/style.css`
- `cards/WI-XXX/index.html` (50 card reveal pages)
- `index.html` (homepage directory)
- `qr/WI-XXX.svg` + `qr/WI-XXX.png` (50 QR code images)
- `print/cards.html` (print-ready card sheets)

## Verification (do this before printing permanent QR codes)

- Scan 5-10 QR codes from a test print to confirm they resolve
- Check all card page URLs load correctly
- Verify external links (map, website) work
- Confirm prices and hours are current (data sourced ~early 2025, verify before use)

## How to Update

- **One card**: edit its entry in `data/cards.json`, re-run `python build.py`
- **All pages**: re-run `python build.py` (idempotent, overwrites generated files)
- **Add cards**: append entries with sequential IDs (WI-051+), re-run build
- **QR codes are permanent**: URLs never change; page content can change freely
