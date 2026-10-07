#!/usr/bin/env python3
"""Drug, device, and food recall reports as structured JSON. Python, Node.js and cURL clients for the FDA Recalls API Scraper on Apify, pay per result.

Command-line client for the themineworks/fda-recalls-scraper actor on Apify: runs it, waits for it
to finish and saves every result as JSON and CSV. Flags map 1:1 to the actor's input.
Free Apify account and API token: https://console.apify.com/sign-up
Docs and pricing: https://themineworks.com/actors/fda-recalls-scraper/
"""
import argparse, csv, json, os, sys
from apify_client import ApifyClient

ACTOR = "themineworks/fda-recalls-scraper"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--token", default=os.environ.get("APIFY_TOKEN"), help="Apify API token (or set APIFY_TOKEN)")
    ap.add_argument("--out", default="results", help="Output basename, writes .json and .csv")
    ap.add_argument("--product-type", help="Which FDA enforcement dataset to search")
    ap.add_argument("--search-term", help="Free-text term matched against the product description (for example metformin, infant…")
    ap.add_argument("--recalling-firm", help="Filter to recalls by firms whose name matches this text (for example Pfizer)")
    ap.add_argument("--classification", help="FDA hazard class")
    ap.add_argument("--status", help="Current status of the recall")
    ap.add_argument("--state", help="Two-letter US state code of the recalling firm (for example CA, NY)")
    ap.add_argument("--date-from", help="Earliest recall report date, for example '2023-01-01'")
    ap.add_argument("--date-to", help="Latest recall report date, for example '2023-12-31'")
    ap.add_argument("--max-results", type=int, help="Maximum number of recall records to return, newest first")
    a = ap.parse_args()
    if not a.token:
        sys.exit("Provide --token or set APIFY_TOKEN. Free token: https://console.apify.com/sign-up")

    run_input = {}
    if a.product_type is not None: run_input["productType"] = a.product_type
    if a.search_term is not None: run_input["searchTerm"] = a.search_term
    if a.recalling_firm is not None: run_input["recallingFirm"] = a.recalling_firm
    if a.classification is not None: run_input["classification"] = a.classification
    if a.status is not None: run_input["status"] = a.status
    if a.state is not None: run_input["state"] = a.state
    if a.date_from is not None: run_input["dateFrom"] = a.date_from
    if a.date_to is not None: run_input["dateTo"] = a.date_to
    if a.max_results is not None: run_input["maxResults"] = a.max_results

    client = ApifyClient(a.token)
    print(f"Running {ACTOR} ...")
    run = client.actor(ACTOR).call(run_input=run_input)
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    with open(a.out + ".json", "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    keys = []
    for it in items:
        keys += [k for k in it if k not in keys]
    if items:
        with open(a.out + ".csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
            w.writeheader()
            for it in items:
                w.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v for k, v in it.items()})
    print(f"Done: {len(items)} results saved to {a.out}.json and {a.out}.csv")


if __name__ == "__main__":
    main()
