# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

We create classified ads (*Inserate*) for selling **used cars (Occasionen)** on the
Swiss (CH) market. For each car the user supplies photos and general info; the
assistant reviews them and writes a ready-to-publish ad in **Swiss Standard German**.

## Workflow

1. User puts the car photos into `photos/` (HEIC format) and provides general info.
2. Convert + merge the HEIC photos into a single PDF (`car_photos.pdf`) for review.
3. Review the photos against the supplied info; note anything worth highlighting
   (condition, equipment, visible wear).
4. Draft the ad text in Swiss Standard German.
5. Iterate with the user.

## Photos: HEIC → single PDF

Photos arrive as `.HEIC`, which is awkward to view directly, so convert and merge
them into one PDF first. Preferred approach (Python):

```python
from PIL import Image
import pillow_heif, glob

pillow_heif.register_heif_opener()
imgs = [Image.open(p).convert("RGB") for p in sorted(glob.glob("photos/*.HEIC"))]
imgs[0].save("car_photos.pdf", save_all=True, append_images=imgs[1:])
```

Install once: `pip install pillow pillow-heif`.
Alternatives if needed: `heif-convert`, or ImageMagick (`magick photos/*.heic car_photos.pdf`)
when the HEIC delegate is installed.

## Language rules — Swiss Standard German (strict)

- **No ß, ever.** Always write **ss** — *Strasse, weiss, Fussraum, grösser, Schliessanlage*.
- **Use the Perfekt, not the Präteritum**, for anything in the past —
  *"Das Fahrzeug ist gepflegt worden"*, *"Wir haben es regelmässig gewartet"*
  (not *"pflegten" / "warteten"*).
- Swiss vocabulary / Helvetisms where natural — *Occasion* for a used car, etc.
- Currency: **CHF** with the apostrophe thousands separator and `.–` for whole francs,
  e.g. **CHF 12'500.–**.
- Tone: clear, factual, trustworthy — the norm for CH car listings.

## General info to collect for each car

Marke/Modell · Jahrgang (Inverkehrsetzung) · Kilometerstand · Treibstoff · Getriebe ·
Leistung (PS/kW) · Farbe · Anzahl Türen/Plätze · MFK-Status (geprüft / ungeprüft, Datum) ·
Service-/Garantie-Infos · Ausstattung · Zustand/Mängel · Preis · Standort · Kontakt.

## Output

- `car_photos.pdf` — merged photos for review.
- The finished ad text in German, ready to paste into the listing platform.

## Notes

- Target platform, fixed fields, preferred ad structure, and example ads will be added
  here as the project develops.
