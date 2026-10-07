# FDA Recalls API Scraper: Drug, Device & Food Enforcement

Search FDA drug, device, and food recall and enforcement reports as clean structured JSON. Filter by product type, classification, status, firm, state, and date. Empty results are never charged.

**Run it on Apify:** [apify.com/themineworks/fda-recalls-scraper](https://apify.com/themineworks/fda-recalls-scraper)
**Docs, FAQ and pricing:** [themineworks.com/actors/fda-recalls-scraper](https://themineworks.com/actors/fda-recalls-scraper/)

**Price:** From $0.60 per 1,000 recalls on Apify's higher plans ($1.00 on the free plan), plus a $0.005 start fee per run. Failed and empty results are never charged.

## What it returns

* Drug, device, food, and biologics recalls
* Class I, II, III classification included
* Firm name and distribution pattern data
* Filter by date range and product type
* Empty results are never charged

## Quick start

You need a free [Apify account](https://console.apify.com/sign-up) and its API token (Settings, API & Integrations).

### Python

```bash
pip install apify-client
```

```python
from apify_client import ApifyClient

client = ApifyClient("YOUR_APIFY_TOKEN")
run = client.actor("themineworks/fda-recalls-scraper").call(run_input={
    "productType": "drug",
    "searchTerm": "metformin",
    "recallingFirm": "Pfizer",
    "classification": "Class I"
})

for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)
```

### Node.js

```bash
npm install apify-client
```

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: 'YOUR_APIFY_TOKEN' });
const run = await client.actor('themineworks/fda-recalls-scraper').call({
    "productType": "drug",
    "searchTerm": "metformin",
    "recallingFirm": "Pfizer",
    "classification": "Class I"
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

### cURL

One request that runs the actor and returns the results in the response (for runs under 5 minutes):

```bash
curl -X POST "https://api.apify.com/v2/acts/themineworks~fda-recalls-scraper/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"productType": "drug", "searchTerm": "metformin", "recallingFirm": "Pfizer", "classification": "Class I"}'
```

### Command line

This repo includes ready-made clients that save results to JSON and CSV:

```bash
python3 fda_recalls_api_scraper.py --token YOUR_APIFY_TOKEN --product-type "drug" --search-term "metformin" --recalling-firm "Pfizer" --classification "Class I"
node fda_recalls_api_scraper.mjs --token YOUR_APIFY_TOKEN --product-type "drug" --search-term "metformin" --recalling-firm "Pfizer" --classification "Class I"
```

## Input

| Field | Type | Default | Description |
|---|---|---|---|
| `productType` | string | `"drug"` | Which FDA enforcement dataset to search |
| `searchTerm` | string |  | Free-text term matched against the product description (for example metformin, infant formula, insulin pump) |
| `recallingFirm` | string |  | Filter to recalls by firms whose name matches this text (for example Pfizer) |
| `classification` | string | `""` | FDA hazard class |
| `status` | string | `""` | Current status of the recall |
| `state` | string |  | Two-letter US state code of the recalling firm (for example CA, NY) |
| `dateFrom` | string |  | Earliest recall report date, for example "2023-01-01" |
| `dateTo` | string |  | Latest recall report date, for example "2023-12-31" |
| `maxResults` | integer | `100` | Maximum number of recall records to return, newest first |

## Output

One row per result, as JSON, CSV, Excel or through the API.

| Field | Type | Description |
|---|---|---|
| `recall_number` | string | FDA recall number |
| `product_type` | string | Product type (drug, device, food) |
| `classification` | string | Recall classification (Class I, II, III) |
| `status` | string | Recall status (Ongoing, Terminated, etc.) |
| `recalling_firm` | string | Name of the recalling firm |
| `product_description` | string | Description of the recalled product |
| `reason_for_recall` | string | Reason for the recall |
| `distribution_pattern` | string | Geographic distribution of the product |
| `product_quantity` | string | Quantity of product recalled |
| `voluntary_mandated` | string | Whether the recall was voluntary or mandated |
| `initial_firm_notification` | string | Method of initial firm notification |
| `city` | string | City of the recalling firm |
| `state` | string | State of the recalling firm |
| `country` | string | Country of the recalling firm |
| `report_date` | string | Date the recall was reported |
| `recall_initiation_date` | string | Date the recall was initiated |
| `center_classification_date` | string | Date the center classified the recall |
| `code_info` | string | Lot/batch/serial code information |
| `event_id` | string | FDA event identifier |
| `brand_name` | string | Brand name from openFDA data |
| `generic_name` | string | Generic name from openFDA data |
| `manufacturer_name` | string | Manufacturer name from openFDA data |
| `scraped_at` | string | Timestamp when the record was scraped |

## Use it from an AI agent

The actor works as a tool in Claude, Cursor or any MCP client through Apify's MCP server:

```
https://mcp.apify.com/?tools=themineworks/fda-recalls-scraper
```

## FAQ

### What types of FDA recalls can I track?

Drug recalls (Class I, II, III enforcement actions), medical device recalls, and food safety enforcement records. All three are available via the openFDA API.

### How current is the FDA recall data?

The FDA updates recall data weekly. The scraper pulls from the openFDA API which reflects the most recent weekly batch.

### What fields does each recall record include?

Recall number, recalling firm, reason for recall, product description, quantity affected, distribution pattern, classification (Class I/II/III), status, and voluntary/mandatory flag.

### Is there a free FDA API?

Yes. openFDA provides free API access with a limit of 240 requests per minute without a key. A free API key raises this to 1,000 per minute for bulk pulls.

### What does Class I recall mean?

Class I is the most serious: products likely to cause serious health consequences or death. Class II is potentially harmful. Class III is unlikely to cause harm but violates FDA regulations.

### How much does the FDA Recalls API Scraper cost?

From $0.60 per 1,000 recalls on Apify's higher plans ($1.00 on the free plan), plus a $0.005 start fee per run. Failed and empty results are never charged. You can cap what a single run may spend with the maximum cost setting on Apify.

### Can I export the results to CSV or Excel?

Yes. Every run saves to an Apify dataset you can download as JSON, CSV, Excel or XML, or read through the API. The Python and Node clients in this repo also write the results to local files.

### Can I run it on a schedule?

Yes. Save your input as a task on Apify and attach a schedule, or call the API from your own cron job. Scheduled runs are billed the same way as manual ones.

## Related scrapers

* [India Gov Data](https://themineworks.com/actors/india-data-gov-scraper/): Trade, prices, and thousands of datasets from data.gov.in
* [CourtListener Scraper](https://themineworks.com/actors/courtlistener-court-records/): US court opinions, dockets, and case law as structured JSON
* [Socrata Open Data](https://themineworks.com/actors/socrata-open-data/): Any government data portal: CDC, HHS, NYC, Texas, and hundreds more

Part of [The Mine Works](https://themineworks.com/): 151 pay-per-result scrapers with no login and no browser setup on your side.

## License

MIT © The Mine Works
