#!/usr/bin/env python3
"""Add one approved review and rebuild the pages."""
import argparse, json, pathlib, datetime, importlib.util

ROOT = pathlib.Path(__file__).resolve().parent.parent
ap = argparse.ArgumentParser()
ap.add_argument("--name", required=True, help='e.g. "Jane D." (first name and last initial)')
ap.add_argument("--type", default="Client", help="Buyer, Seller, Investor...")
ap.add_argument("--place", default="", help='e.g. "Lancaster County"')
ap.add_argument("--rating", type=int, required=True, choices=[1, 2, 3, 4, 5])
ap.add_argument("--text", required=True)
ap.add_argument("--date", default=datetime.date.today().isoformat())
a = ap.parse_args()

path = ROOT / "data" / "reviews.json"
data = json.loads(path.read_text(encoding="utf-8"))
data.append({"name": a.name, "type": a.type, "place": a.place, "rating": a.rating, "text": a.text, "date": a.date})
path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

spec = importlib.util.spec_from_file_location("build_reviews", ROOT / "scripts" / "build-reviews.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); mod.build()
