#!/usr/bin/env python3
"""Renders data/reviews.json into plain HTML inside reviews.html and index.html, so reviews are
crawlable by Google (no JavaScript needed). Run after editing data/reviews.json:

    python3 scripts/build-reviews.py

Add a review the easy way:

    python3 scripts/add-review.py --name "Jane D." --type Buyer --place "Lancaster County" --rating 5 --text "..." 
"""
import json, html, re, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
# Set this to the "Ask for reviews" link from the Google Business Profile once it exists.
GOOGLE_REVIEW_URL = ""


def month_year(d):
    try:
        return datetime.date.fromisoformat(d).strftime("%b %Y")
    except Exception:
        return ""


def card(r):
    n = max(1, min(5, int(r.get("rating", 5))))
    meta = " &middot; ".join(html.escape(x) for x in [r.get("type", ""), r.get("place", ""), month_year(r.get("date", ""))] if x)
    text = html.escape(r["text"].strip()).replace("\n", "<br>")
    return (
        '<article class="review-card">'
        f'<div class="stars" role="img" aria-label="{n} out of 5 stars">{"&#9733;" * n}<span class="off">{"&#9733;" * (5 - n)}</span></div>'
        f"<blockquote>&ldquo;{text}&rdquo;</blockquote>"
        f'<footer><strong>{html.escape(r["name"])}</strong><span>{meta}</span></footer>'
        "</article>"
    )


def replace_block(page, name, content):
    pat = re.compile(rf"(<!-- REVIEWS:{name}:START -->).*?(<!-- REVIEWS:{name}:END -->)", re.S)
    assert pat.search(page), f"marker {name} missing"
    return pat.sub(lambda m: m.group(1) + "\n" + content + "\n" + m.group(2), page)


def build():
    reviews = json.loads((ROOT / "data" / "reviews.json").read_text(encoding="utf-8"))
    reviews.sort(key=lambda r: (r.get("date", ""), r.get("rating", 0)), reverse=True)

    if reviews:
        cards = "\n".join(card(r) for r in reviews)
        summary = ""
        if len(reviews) >= 5:
            avg = sum(r["rating"] for r in reviews) / len(reviews)
            summary = f'<p class="review-summary"><strong>{avg:.1f} out of 5</strong> from {len(reviews)} client reviews</p>'
        listing = (f'<div class="review-grid">\n{cards}\n</div>\n{summary}\n'
                   '<p class="review-note">Reviews are shared by past clients with their permission.</p>')
    else:
        listing = ('<p class="review-empty">No reviews have been published here yet. If we have worked together, '
                   "we would be grateful if you shared how it went using the form below.</p>")

    google = (f'<a class="btn btn-line" href="{html.escape(GOOGLE_REVIEW_URL)}" target="_blank" rel="noopener">Review us on Google</a>'
              if GOOGLE_REVIEW_URL else "")

    top = sorted(reviews, key=lambda r: (r.get("rating", 0), r.get("date", "")), reverse=True)[:3]
    home = ""
    if top:
        home = ('<section class="section-pad">\n    <div class="wrap">\n'
                '      <div class="section-head"><span class="kicker">Client reviews</span><h2>What our clients say.</h2></div>\n'
                f'      <div class="review-grid">\n{chr(10).join(card(r) for r in top)}\n      </div>\n'
                '      <a href="reviews.html" class="btn btn-line" style="margin-top:32px">Read all reviews</a>\n'
                "    </div>\n  </section>")

    p = ROOT / "reviews.html"
    page = p.read_text(encoding="utf-8")
    page = replace_block(page, "LIST", listing)
    page = replace_block(page, "GOOGLE", google)
    p.write_text(page, encoding="utf-8")

    p = ROOT / "index.html"
    page = p.read_text(encoding="utf-8")
    page = replace_block(page, "HOME", home)
    p.write_text(page, encoding="utf-8")
    print(f"Built {len(reviews)} review(s). Homepage section: {'shown' if home else 'hidden (no reviews yet)'}.")


if __name__ == "__main__":
    build()
