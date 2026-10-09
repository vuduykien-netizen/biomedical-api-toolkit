# Verification record

Date: **2026-10-10**. This is a dated snapshot, not a continuous service monitor.

## Scope

Reviewed official provider documentation linked in [api-catalog.md](api-catalog.md). Ran one small GET request per available provider using the registry's demo, without account credentials. Inspected expected response fields rather than relying on HTTP status alone. No raw adverse-event reports, contact emails, keys or private research data are committed.

| Entry | Result | Response check |
|---|---|---|
| PubMed | HTTP 200 | ESearch returned a PMID list |
| Europe PMC | HTTP 200 | Search returned publication records |
| MeSH | HTTP 200 | Lookup returned descriptor records |
| Crossref | HTTP 200 | Works search returned bibliographic records |
| OpenAlex | HTTP 200 | Keyless works search returned scholarly records |
| Semantic Scholar | HTTP 429 | Shared keyless access was throttled; not a successful data probe |
| Unpaywall | Not requested | Required contact email was not configured; no substitute email was invented |
| ClinicalTrials.gov | HTTP 200 | Studies endpoint returned a registered study |
| World Bank | HTTP 200 | Country/indicator endpoint returned a Vietnam time-series record |
| openFDA | HTTP 200 | Drug-event endpoint returned a report |
| RxNorm | HTTP 200 | Metformin lookup returned an RxCUI |
| medRxiv | HTTP 200 | Details returned status `ok` and manuscript metadata |
| bioRxiv | HTTP 200 | Details returned status `ok` and manuscript metadata |
| ChEMBL | HTTP 200 | Compound lookup returned CHEMBL25 |

**12 successful data probes, 1 throttled provider, 1 not requested.** Documentation for free access and limits was checked separately. The Unpaywall DOI endpoint is cataloged from official documentation, not a live authenticated/contact-bearing probe. Documentation pages may block automated readers even when their public API works.

## Local checks

- Skill creator structural validation passed.
- Offline helper tests passed: search syntax encoding, query/header credential handling, response-echo redaction, missing required contact handling, API-relative paths, credential-parameter rejection, bounded retries, sanitized HTTP errors, non-JSON preservation, and preventing output replacement.
- Local Markdown links were checked after all referenced files were created.

## Practical limits

A single successful probe does not establish completeness, pagination correctness, billing guarantees, uptime or scientific validity. The helper performs one request with bounded retries; downstream applications must inspect provider-level messages and implement requested screening, pagination, normalization or analysis. Future changes should update this record with date, request scope and failures.
