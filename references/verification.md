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
- All 12 offline helper tests passed: search syntax encoding, query/header credential handling, response-echo redaction (including lowercase percent escapes), missing required contact handling, API-relative paths, credential-parameter rejection, bounded retries, sanitized HTTP errors, non-JSON preservation, and preventing output replacement.
- Local Markdown links were checked after all referenced files were created.

## Independent forward test

A separate agent used the completed skill to distinguish a synthetic wrong-DOI citation from an unresolved reference, and to prepare a small Vietnam life-expectancy teaching extract for 2010–2023. The helper retrieved 14 annual observations with query, definition, timestamp and transformation provenance. An initial transient World Bank network failure was resolved by one bounded retry.

The review identified an encoded credential-echo redaction gap; it was corrected and independently rechecked with synthetic credentials before release. No remaining actionable helper defect was reported. Dataset-specific reuse terms were not independently reconfirmed in the forward test because the indicator portal timed out; any dataset redistribution still requires its applicable license check. Test artifacts and raw datasets are not bundled in this repository.

## Practical limits

A single successful probe does not establish completeness, pagination correctness, billing guarantees, uptime or scientific validity. The helper performs one request with bounded retries; downstream applications must inspect provider-level messages and implement requested screening, pagination, normalization or analysis. Future changes should update this record with date, request scope and failures.
