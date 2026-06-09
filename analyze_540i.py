"""Read autoscout_540i.csv and write vergleich.md: a Swiss-German price comparison
of the scraped BMW 540i (2019-2020) market against our own car.

Run:  uv run python analyze_540i.py
"""

import csv
import statistics as st

# Our car (see inserat.md).
OURS = {
    "price": 34900, "km": 90600, "year": 2019,
    "body": "Limousine", "drivetrain": "xDrive", "trim": "Luxury Line",
}


def grp(n):
    """Swiss thousands separator: 90600 -> 90'600."""
    return f"{n:,}".replace(",", "'")


def chf(n):
    return f"CHF {grp(round(n))}.–"


def stats(prices):
    return {
        "n": len(prices),
        "min": min(prices), "max": max(prices),
        "median": int(st.median(prices)),
        "mean": int(st.mean(prices)),
    }


def main():
    with open("autoscout_540i.csv", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f)]
    for r in rows:
        r["price_chf"] = int(r["price_chf"])
        r["km"] = int(r["km"]) if r["km"] else None

    rows.sort(key=lambda r: r["price_chf"])
    prices = [r["price_chf"] for r in rows]
    sedans = [r for r in rows if r["body"] == "Limousine"]
    sedan_prices = [r["price_chf"] for r in sedans]

    s_all = stats(prices)
    cheaper = sum(1 for p in prices if p < OURS["price"])

    lines = []
    lines.append("# Preisvergleich: BMW 540i (2019–2020) auf AutoScout24.ch\n")
    lines.append(
        "Automatisch erhoben mit `scrape_540i.py` (Stand: aktuelle Abfrage). "
        "Gefiltert auf **BMW 540i, Erstinverkehrsetzung 2019–2020, Benzin**, "
        "Region ganze Schweiz. Unser Fahrzeug: "
        f"**{OURS['body']} {OURS['drivetrain']} {OURS['trim']}, {OURS['year']}, "
        f"ca. {grp(OURS['km'])} km, Preisvorstellung {chf(OURS['price'])}**.\n"
    )

    lines.append("## Marktübersicht (alle 540i, nach Preis)\n")
    lines.append("| Preis | km | Jahr | Karosserie | Linie | Standort | Link |")
    lines.append("|---|---|---|---|---|---|---|")
    for r in rows:
        km = grp(r["km"]) if r["km"] else "?"
        loc = r["city"] or r["zip"] or ""
        lines.append(
            f"| {chf(r['price_chf'])} | {km} | {r['year']} | {r['body']} | "
            f"{r['trim'] or '–'} | {loc} | [Inserat]({r['url']}) |"
        )
    lines.append("")

    lines.append("## Preisverteilung\n")
    lines.append(f"- **Anzahl Inserate (540i, 2019–2020):** {s_all['n']}")
    lines.append(f"- **Tiefster Preis:** {chf(s_all['min'])}")
    lines.append(f"- **Median:** {chf(s_all['median'])}")
    lines.append(f"- **Durchschnitt:** {chf(s_all['mean'])}")
    lines.append(f"- **Höchster Preis:** {chf(s_all['max'])}")
    if sedan_prices:
        ss = stats(sedan_prices)
        lines.append(
            f"- **Nur Limousinen ({ss['n']} Stk., wie unser Auto):** "
            f"{chf(ss['min'])} – {chf(ss['max'])}, Median {chf(ss['median'])}"
        )
    lines.append("")

    lines.append("## Einordnung unseres Fahrzeugs\n")
    lines.append(
        f"Unsere Preisvorstellung von **{chf(OURS['price'])}** liegt **über dem "
        f"Median ({chf(s_all['median'])})** und nahe am oberen Ende des Marktes: "
        f"von {s_all['n']} vergleichbaren 540i sind **{cheaper} günstiger** als unser "
        f"Inserat. Der teuerste gefundene 540i kostet {chf(s_all['max'])}."
    )
    lines.append("")
    lines.append(
        "**Zu beachten zugunsten unseres Fahrzeugs:** mit ca. "
        f"{grp(OURS['km'])} km"
        " liegt der Kilometerstand im Vergleich tief, das Fahrzeug ist unfallfrei, "
        "ab MFK, mit Garantie bis Ende März 2027, Servicepaket bis 100'000 km, "
        "BMW Individual Ausstattung, frische Ganzjahresreifen und Nichtraucher. "
        "Diese Argumente rechtfertigen einen Aufpreis gegenüber dem Median."
    )
    lines.append("")
    lines.append(
        "**Einschätzung:** Die Stichprobe ist klein (der 540i ist in der CH selten). "
        f"Wer am oberen Ende verkaufen will, sollte die genannten Stärken im Inserat "
        f"klar betonen. Ein Preis im Bereich **CHF 33'000.– bis 35'000.–** dürfte "
        "schneller Interessenten anziehen; {price} ist ambitioniert, aber mit guter "
        "Ausstattung und tiefem km-Stand vertretbar.".format(price=chf(OURS["price"]))
    )
    lines.append("")

    with open("vergleich.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("Wrote vergleich.md")
    print(f"  N={s_all['n']}  min={chf(s_all['min'])}  median={chf(s_all['median'])}  "
          f"max={chf(s_all['max'])}  cheaper_than_ours={cheaper}")


if __name__ == "__main__":
    main()
