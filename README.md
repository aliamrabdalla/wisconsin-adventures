# Wisconsin Adventure Cards

A 50-card couples adventure deck for Wisconsin. Each physical card shows a location name, metadata badges, and a QR code. Scanning the QR opens a themed reveal page with the full adventure details, steps, links, and notes.

**Live site:** https://aliamrabdalla.github.io/wisconsin-adventures/

## What's in the box

| Output | Description |
|--------|-------------|
| `index.html` | Homepage grid of all 50 cards with badges |
| `cards/WI-XXX/index.html` | Individual reveal pages (50 total) |
| `qr/WI-XXX.svg` and `.png` | QR code images for each card (print-ready) |
| `print/cards.html` | Print layout — 4 cards per letter sheet, 13 pages |
| `data/cards.json` | Source of truth for all card data |
| `build.py` | Build script that generates everything from `cards.json` |

## Next steps

### 1. Enable GitHub Pages

Once the repo is pushed, go to:

**Settings > Pages > Source: Deploy from branch > `main` / `/ (root)` > Save**

Wait 1-2 minutes, then visit https://aliamrabdalla.github.io/wisconsin-adventures/

### 2. Verify the content

Before printing permanent QR codes:

- [ ] Browse the live site and read through all 50 adventures
- [ ] Check that prices, hours, and offerings are still current (data sourced ~early 2025)
- [ ] Click all Map and Website links to make sure they resolve
- [ ] Scan 5-10 QR codes from a test print to confirm they load the right pages

### 3. Print the physical cards

1. Open `print/cards.html` in your browser (Chrome recommended)
2. Press `Ctrl+P` to open the print dialog
3. Set paper to **Letter (8.5 x 11 in)**
4. Set margins to **None**
5. Set scale to **100%**
6. Enable **Background graphics** (needed for the green accent bar)
7. Print on cardstock
8. Cut along the solid green borders — 4 cards per sheet, 13 sheets total

Each card is 3 x 5 inches (vertical) with: green banner header with location title, QR code in center, and a 2x3 badge grid with Font Awesome icons at the bottom.

**Note:** The print page loads [Font Awesome](https://fontawesome.com/) from a CDN for badge icons, so you need an internet connection when opening `print/cards.html`.

### 4. Edit an adventure

All card data lives in `data/cards.json`. To change one:

1. Edit the entry in `cards.json`
2. Run `python build.py`
3. Commit and push

The QR codes never change — they point to permanent URLs. Only the page content updates.

### 5. Add new cards

Append entries to `cards.json` with sequential IDs (`WI-051`, `WI-052`, ...) and re-run the build. Existing QR codes remain valid.

## How it works

```
data/cards.json  -->  build.py  -->  cards/WI-XXX/index.html  (50 reveal pages)
                                     index.html                (homepage)
                                     qr/WI-XXX.svg + .png     (100 QR images)
                                     print/cards.html          (print sheets)
                                     assets/style.css          (stylesheet)
```

`build.py` reads the JSON, generates all HTML from embedded templates, and creates QR codes using the `segno` library. No other dependencies.

## Card metadata

Each card has six badge fields displayed on both the physical card and the reveal page:

| Field | Values |
|-------|--------|
| Cost | `$0-$15`, `$15-$40`, `$40-$100`, `$100-$300` |
| Time | `DAY`, `NIGHT`, `EITHER` |
| Duration | `1-2H`, `2-4H`, `HALF DAY`, `FULL DAY` |
| Setting | `INDOOR`, `OUTDOOR`, `BOTH` |
| Effort | `CHILL`, `MODERATE`, `ACTIVE` |
| Season | `WINTER`, `SPRING`, `SUMMER`, `FALL`, `ANY`, or range like `SPR-FALL` |

## Requirements

- Python 3.8+
- `segno` (`pip install segno`) — pure Python, no other dependencies
