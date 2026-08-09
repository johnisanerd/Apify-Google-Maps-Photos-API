"""
Google Maps Photos API: A Quick Start Example
See more at: https://apify.com/johnvc/google-maps-photos-api?fpr=9n7kx3
Input schema: https://apify.com/johnvc/google-maps-photos-api/input-schema?fpr=9n7kx3

This script shows how to call the Google Maps Photos API on Apify from Python
and read its structured JSON output: one row per photo, with the full-size image
URL, a thumbnail, its position in the place's gallery, and a stable photo ID you
can de-duplicate on across runs.

It searches by name, so you do not need a place identifier to get started. The
run is kept small so your first call stays cheap.

Get your free Apify API key at: https://apify.com?fpr=9n7kx3
"""

import os

from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

# Initialize the Apify client with your API token (read from .env)
client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

# Build the Actor input.
# Searching by name is the simplest way in. One search plus one place keeps the
# first run inexpensive; raise maxPlacesPerSearch for a whole neighbourhood.
run_input = {
    "searchTerm": "Mozart's Coffee Roasters, Austin TX",
    "maxPlacesPerSearch": 1,
    "maxPhotosPerPlace": 20,   # photos arrive in blocks of 20
    "hl": "en",
}

# Run the Actor and wait for it to finish
run = client.actor("johnvc/google-maps-photos-api").call(run_input=run_input)

# Read structured results from the run's default dataset.
# apify-client 3.x returns a typed Run object, so use the attribute (not run["defaultDatasetId"]).
items = list(client.dataset(run.default_dataset_id).iterate_items())

photos = [i for i in items if i.get("result_type") == "photo"]
summaries = [i for i in items if i.get("result_type") == "place_summary"]
errors = [i for i in items if i.get("result_type") == "error"]

print(f"{len(photos)} photo(s) across {len(summaries)} place(s)\n")

for p in photos[:5]:
    print(f"  #{p['position']:>2}  {p.get('place_title', p['data_id'])}")
    print(f"       full size : {p['image'][:78]}")
    print(f"       thumbnail : {p['thumbnail'][:78]}")
    print(f"       photo id  : {p.get('photo_id')}")

# The per-place summary row is how you discover a venue's own gallery sections.
# Feed one of these IDs back in as categoryId to pull just that section.
for s in summaries:
    cats = s.get("place_categories") or []
    print(f"\n{s.get('place_title', s['data_id'])}: "
          f"{s['photos_returned']} photo(s), {len(cats)} gallery category(ies)")
    for c in cats[:8]:
        print(f"    {c['id']:<28} {c['title']}")

for e in errors:
    print(f"\n[{e['error_type']}] {e['error_message']}")

# --- Other things you can do -------------------------------------------------
#
# Filter to one gallery section. The universal categories work on any place;
# menu, food_and_drink, and vibe exist on food and drink venues:
#
#   {"searchTerm": "...", "photoCategory": "street_view"}
#   {"searchTerm": "...", "photoCategory": "menu"}
#
# Sweep a whole area in one run:
#
#   {"searchTerm": "coffee shops in Austin, TX", "maxPlacesPerSearch": 10}
#
# Skip the search charge entirely by passing a Google Maps URL, or an identifier
# you already have from the Google Maps Places API:
#
#   {"placeUrls": ["https://www.google.com/maps/place/..."]}
#   {"dataIds": ["0x8644b5554461664d:0xbc4ff333ec9ad1ad"]}
