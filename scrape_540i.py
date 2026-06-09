"""Scrape BMW 540i (2019-2020) listings from autoscout24.ch via Playwright.

autoscout24.ch is behind Akamai Bot Manager (plain HTTP -> 403) and has no public
JSON API. But its server-rendered pages embed the listing data in the Next.js RSC
"flight" stream (self.__next_f.push([1,"..."]) chunks). We drive a real headless
Chromium to get past the bot-wall, grab the page HTML, reconstruct that flight
payload, and brace-match the individual listing objects (clean, structured data).

Search slug discovered by probing: /de/s/mo-540/mk-bmw  (model 540, make BMW).
"mo-540" returns 540i + 540d; we keep only 540i (petrol).

Run with:
    uv run --with playwright playwright install chromium   # one time
    uv run --with playwright python scrape_540i.py
"""

import csv
import json
import re
import sys
import time

from playwright.sync_api import sync_playwright

BASE = "https://www.autoscout24.ch"
SEARCH = (
    BASE + "/de/s/mo-540/mk-bmw"
    "?vehtyp=10&firstRegistrationYearFrom=2019&firstRegistrationYearTo=2020"
    "&sort=price&desc=0&page={page}"
)
UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)


def flight_text(html):
    """Reconstruct the decoded RSC flight payload from the page HTML."""
    chunks = re.findall(r'self\.__next_f\.push\(\[1,(".*?")\]\)', html, re.S)
    parts = []
    for c in chunks:
        try:
            parts.append(json.loads(c))
        except json.JSONDecodeError:
            pass
    return "".join(parts)


def listing_objects(s):
    """Yield JSON substrings of objects that hold exactly one listing."""
    out = []
    stack = []
    in_str = esc = False
    for i, ch in enumerate(s):
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
        else:
            if ch == '"':
                in_str = True
            elif ch == "{":
                stack.append(i)
            elif ch == "}" and stack:
                start = stack.pop()
                obj = s[start:i + 1]
                if (obj.count('"versionFullName":') == 1
                        and '"mileage":' in obj and '"price":' in obj):
                    out.append(obj)
    return out


def slugify(text):
    t = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return re.sub(r"-+", "-", t)


def parse_page(html):
    listings = {}
    for obj in listing_objects(flight_text(html)):
        try:
            d = json.loads(obj)
        except json.JSONDecodeError:
            continue
        if d.get("make", {}).get("key") != "bmw":
            continue
        version = str(d.get("versionFullName", ""))
        if not version.startswith("540i"):      # 540i petrol only (skip 540d)
            continue
        reg = d.get("firstRegistrationDate") or ""
        year = d.get("firstRegistrationYear") or (int(reg[:4]) if reg[:4].isdigit() else None)
        if year not in (2019, 2020):            # drop sponsored slots outside range
            continue
        lid = d.get("id")
        listings[lid] = {
            "id": lid,
            "version": version,
            "price_chf": d.get("price"),
            "km": d.get("mileage"),
            "year": year,
            "reg_date": reg[:10] if reg else "",
            "power_ps": d.get("horsePower"),
            "fuel": d.get("fuelType"),
            "drivetrain": "xDrive" if "xdrive" in version.lower() else "Hinterrad",
            "body": "Touring (Kombi)" if "touring" in version.lower() else "Limousine",
            "trim": ("Luxury Line" if "luxury" in version.lower()
                     else "M Sport" if "m sport" in version.lower()
                     or "m-sport" in version.lower() else ""),
            "accident": d.get("hadAccident"),
            "zip": d.get("seller", {}).get("zipCode") or "",
            "city": d.get("seller", {}).get("city") or "",
            "url": f"{BASE}/de/d/bmw-{slugify(version)}-{lid}",
        }
    return listings


def main():
    rows = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(
            user_agent=UA, viewport={"width": 1440, "height": 900}, locale="de-CH"
        )
        page = ctx.new_page()
        for page_num in range(1, 11):
            page.goto(SEARCH.format(page=page_num), wait_until="domcontentloaded",
                      timeout=60000)
            time.sleep(4)
            found = parse_page(page.content())
            new = sum(1 for k in found if k not in rows)
            rows.update(found)
            print(f"[page {page_num}] {len(found)} x 540i, {new} new "
                  f"(total {len(rows)})", file=sys.stderr)
            if new == 0:
                break
            time.sleep(2)
        browser.close()

    out = sorted(rows.values(), key=lambda r: r["price_chf"] or 0)
    fields = ["id", "version", "price_chf", "km", "year", "reg_date", "power_ps",
              "fuel", "drivetrain", "body", "trim", "accident", "zip", "city", "url"]
    with open("autoscout_540i.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(out)
    print(f"\nWrote {len(out)} BMW 540i listings to autoscout_540i.csv\n")
    for r in out:
        print(f"  CHF {r['price_chf']:>7,} | {r['km']:>7,} km | {r['year']} | "
              f"{r['body']:15} | {r['trim'] or '-':11} | {r['city']}")


if __name__ == "__main__":
    main()
