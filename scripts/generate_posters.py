#!/usr/bin/env python3
"""
Generate event posters from the Orion Band template.

Reads src/assets/events.json and creates posters for events without a poster_id
(missing key or null). Output: posters/poster_{date}.png at the repo root.

Date formatting matches src/utils/date.js (Czech weekday + date).
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = Path(__file__).resolve().parents[1]
EVENTS_PATH = REPO_ROOT / "src/assets/events.json"
TEMPLATE_PATH = REPO_ROOT / "src/assets/orion_band_plakat_template.jpg"
OUTPUT_DIR = REPO_ROOT / "posters"
FONT_PATH = Path(__file__).resolve().parent / "fonts/CourierPrime-Regular.ttf"

# Layout tuned to match src/assets/poster_2025-06-13.png (1024×1550).
FONT_SIZE = 40
LINE1_Y = 1369
LINE2_Y = 1454
TEXT_COLOR = "#FFFFFF"

CZECH_WEEKDAYS = (
    "pondělí",
    "úterý",
    "středa",
    "čtvrtek",
    "pátek",
    "sobota",
    "neděle",
)
CZECH_MONTHS = (
    "",
    "ledna",
    "února",
    "března",
    "dubna",
    "května",
    "června",
    "července",
    "srpna",
    "září",
    "října",
    "listopadu",
    "prosince",
)


def format_date(date_str: str) -> str:
    """Match src/utils/date.js Intl.DateTimeFormat('cs-CZ', ...) output."""
    year, month, day = map(int, date_str.split("-"))
    event_date = date(year, month, day)
    weekday = CZECH_WEEKDAYS[event_date.weekday()].capitalize()
    return f"{weekday} {day}. {CZECH_MONTHS[month]} {year}"


def needs_poster(event: dict) -> bool:
    return event.get("poster_id") is None


def load_font() -> ImageFont.FreeTypeFont:
    candidates = [
        FONT_PATH,
        Path("/System/Library/Fonts/Supplemental/Courier New.ttf"),
        Path("/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"),
    ]
    for path in candidates:
        if path.is_file():
            return ImageFont.truetype(str(path), FONT_SIZE)
    raise FileNotFoundError(
        "No suitable monospace font found. Expected bundled font at "
        f"{FONT_PATH}"
    )


def render_poster(event: dict, template: Image.Image, font: ImageFont.FreeTypeFont) -> Image.Image:
    line1 = f"{format_date(event['date'])} od {event['time']}"
    line2 = event["location"]

    poster = template.copy()
    draw = ImageDraw.Draw(poster)
    center_x = poster.width // 2
    draw.text((center_x, LINE1_Y), line1, font=font, fill=TEXT_COLOR, anchor="mm")
    draw.text((center_x, LINE2_Y), line2, font=font, fill=TEXT_COLOR, anchor="mm")
    return poster


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Orion Band event posters.")
    parser.add_argument(
        "--date",
        help="Generate poster only for this event date (YYYY-MM-DD).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing poster files.",
    )
    args = parser.parse_args()

    if not EVENTS_PATH.is_file():
        print(f"Events file not found: {EVENTS_PATH}", file=sys.stderr)
        return 1
    if not TEMPLATE_PATH.is_file():
        print(f"Template not found: {TEMPLATE_PATH}", file=sys.stderr)
        return 1

    events = json.loads(EVENTS_PATH.read_text(encoding="utf-8"))
    pending = [event for event in events if needs_poster(event)]

    if args.date:
        pending = [event for event in pending if event["date"] == args.date]
        if not pending:
            print(f"No event without poster_id found for date {args.date}.", file=sys.stderr)
            return 1

    if not pending:
        print("No events without poster_id found.")
        return 0

    OUTPUT_DIR.mkdir(exist_ok=True)
    template = Image.open(TEMPLATE_PATH).convert("RGBA")
    font = load_font()

    created = 0
    for event in pending:
        output_path = OUTPUT_DIR / f"poster_{event['date']}.png"
        if output_path.exists() and not args.force:
            print(f"Skipping {output_path.name} (already exists, use --force to overwrite)")
            continue

        poster = render_poster(event, template, font)
        poster.save(output_path, "PNG")
        print(f"Created {output_path.relative_to(REPO_ROOT)}")
        created += 1

    print(f"Done. Generated {created} poster(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
