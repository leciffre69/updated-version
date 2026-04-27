# Llangynidr Graveyard — Interactive Map

An interactive web map of the graveyard at **St Catwg's Church, Cwmddu, Lower Llangynidr**.  
Click any plot number on the original scanned diagram to see the occupant's full name, birth/death dates and inscription. Search by name or plot number.

---

## Quick Start

**Double-click `start.bat`**

That's it. The server starts automatically and your browser opens at `http://localhost:8000`.

> Requires **Python 3.8+** installed and available in your PATH.

---

## Pages

| URL | Page | Purpose |
|-----|------|---------|
| `http://localhost:8000/` | Interactive Map | Public-facing graveyard map |
| `http://localhost:8000/admin` | Admin — Coordinate Mapper | Map plot numbers to image positions |

---

## File Structure

```
├── start.bat              ← Double-click to launch
├── server.py              ← Python web server (routes / and /admin)
├── index.html             ← Interactive map page
├── mapper.html            ← Admin coordinate mapping tool
├── sketch.png             ← Original scanned graveyard diagram (800×1800)
├── plot_coords.json       ← x/y position of each plot number on the image
├── graveyard_plots.json   ← All burial records grouped by plot number
├── data.xlsx              ← Source spreadsheet — edit this to update records
├── build_data.py          ← Rebuilds graveyard_plots.json from data.xlsx
└── img/
    ├── logo.png           ← Site logo / favicon
    ├── 1.png – 5.png      ← Background / UI images
```

---

## How to Use the Map

- **Click** any plot number on the image → right panel shows all occupants, dates and inscription
- **Search** by typing a surname, forename or plot number in the search box
- **Drag** to pan the map
- **Scroll** to zoom in/out (or use the toolbar buttons)
- **Fit** button resets the view

---

## Updating Burial Records

All data lives in **`data.xlsx`** (Sheet1). Column layout:

| Column | Field |
|--------|-------|
| A | Surname |
| B | Forename |
| C | Plot number |
| D | Date of birth |
| E | Date of death |
| F | Age |
| G | Memorial Notes / Epitaph |

Multiple people sharing a plot each get their own row with the same plot number.

After editing `data.xlsx`, run:

```
python build_data.py
```

Then refresh the browser. No restart needed.

---

## Admin — Coordinate Mapper

Open `http://localhost:8000/admin` to map or adjust plot positions.

1. Type a plot number in the input box (e.g. `42`, `327A`, `NK`)
2. Click that number's location on the image — a gold dot appears
3. The input auto-advances to the next number
4. Click **Export plot_coords.json** when done and save it to this folder
5. Refresh the map — new positions take effect immediately

**Keyboard shortcuts:**
- `Ctrl+Z` — undo last placement
- `Enter` — focus the plot number input

---

## Plot Number Format

| Format | Example | Meaning |
|--------|---------|---------|
| Integer | `1` – `369` | Standard numbered plots |
| Suffix A/B | `327A`, `327B` | Sub-plots sharing a stone |
| Special | `195A`, `195B`, `142A` | Additional sub-plots |
| Text | `NK` | Unknown / not mapped to a number |

---

## Requirements

- Python 3.8 or later
- `openpyxl` library (only needed to rebuild data from Excel)

```
pip install openpyxl
```

No other dependencies. Everything runs in the browser with no internet connection required.

---

## Stopping the Server

Press `Ctrl+C` in the console window, or simply close it.
