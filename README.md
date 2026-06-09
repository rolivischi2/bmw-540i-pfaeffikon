# BMW 540i xDrive · Verkauf

Verkaufsunterlagen und Landingpage für meinen **BMW 540i xDrive Luxury Line** (2019).

🔗 **Live-Seite:** https://site-wheat-rho-69.vercel.app

## Inhalt

| Pfad | Zweck |
|------|-------|
| `site/` | Statische Verkaufs-Landingpage (Dark Luxury, HTML/CSS/JS), deploybar auf Vercel |
| `site/assets/` | Web-optimierte Bilder (aus `pics/` generiert) |
| `pics/` | Originalfotos (Tageslicht-JPEGs + HEIC Ambiente-Aufnahmen) |
| `inserat.md` | Fertiger Inserat-Text (AutoScout24), Schweizer Hochdeutsch |
| `vergleich.md` | Marktpreis-Vergleich gegen andere 540i (2019–2020) in der CH |
| `build_assets.py` | HEIC → JPEG konvertieren + alle Bilder web-optimiert nach `site/assets/` |
| `scrape_540i.py` | Scraper für AutoScout24.ch (Playwright), vergleichbare 540i-Inserate |
| `analyze_540i.py` | Erzeugt `vergleich.md` aus den Scraper-Daten |

## Eckdaten

- BMW 540i xDrive Limousine (G30), 2019, ca. 90'600 km
- 340 PS (250 kW) Reihensechszylinder, ZF 8-Gang-Automat, xDrive
- Luxury Line · BMW Individual · Cashmere Silbermetallic
- Preis: CHF 34'900.– (Verhandlungsbasis) · Standort Pfäffikon SZ

## Entwicklung

Python-Skripte laufen über [uv](https://docs.astral.sh/uv/) (keine System-Python-Installation):

```bash
# Bilder aufbereiten
uv run --with pillow --with pillow-heif python build_assets.py

# Marktvergleich neu erheben
uv run --with playwright playwright install chromium   # einmalig
uv run --with playwright python scrape_540i.py
uv run python analyze_540i.py
```

Landingpage lokal ansehen: `site/index.html` im Browser öffnen.
Deploy: `vercel deploy --prod --cwd site`.
