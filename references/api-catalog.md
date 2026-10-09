# Public biomedical research API catalog

Reviewed **2026-10-10**. Prices, access rules, limits and endpoints can change. Consult the linked official docs before building or scaling an integration. Public metadata access does not imply unlimited requests or unrestricted reuse of underlying content.

## Provider selection

| Provider ID | Best use | Free access / authentication | Interpretation limits |
|---|---|---|---|
| `pubmed` | Biomedical citations, search, abstracts when present | Free; 3 requests/second per IP without key, 10 by default with free NCBI key | Not all full text; copyright can apply to abstracts; large retrievals need documented batch/history methods |
| `europepmc` | Life-science search, abstracts, publication metadata and full-text links | Public web service; no key in example | Full-text availability and reuse license vary; includes preprints |
| `mesh` | Controlled vocabulary, entry terms, hierarchy | Open lookup and RDF/SPARQL APIs | Does not translate a research question into a validated search automatically |
| `crossref` | DOI and bibliographic metadata, deposited updates | Free public API, no signup; optional contact email for polite requests | Not all DOI agencies; metadata completeness varies; a missing update is not proof of no retraction |
| `openalex` | Scholarly discovery, works, authors, topics, grouped counts | **Limited free tier**; casual keyless access; free account/key currently has $1/day usage budget | API serving is metered; check account allowance and avoid paid fallback; counts are index-specific |
| `semanticscholar` | Papers, authors, references and citations | Public unauthenticated requests exist; free API key recommended; limits depend on endpoint/access | Keyless pool can throttle; citation counts are not study quality |
| `unpaywall` | DOI open-access status and locations | Free DOI API; contact email parameter required; docs specify up to 100,000 calls/day | Some DOIs have no open location; licenses differ; search endpoint retired 2026-09-18 |
| `clinicaltrials` | Study registrations, designs, status and submitted results | Public v2 API; no key in tested request | Registry coverage is not all research; registration is not proof of efficacy |
| `worldbank` | Public country/indicator time series | Public v2 API, no key required | Record indicator definitions, revisions and missingness; country associations are ecological |
| `openfda` | Labels, recalls, devices, adverse-event reports | Free key; docs list 1,000/day keyless, 120,000/day with key and 240/minute; keyless probe succeeded | Auth page also says key required: verify current behavior, prefer free key for regular use; FAERS is not incidence/causation data |
| `rxnorm` | Drug identifiers and vocabulary normalization | Most functions need no license; proprietary sources need UMLS conditions; optional UMLS key | US terminology coverage; interaction features discontinued 2024-01-02 |
| `medrxiv` | Medical preprint metadata, versions and publication links | Public details API, no key in tested example; no quota confirmed here | Label preprints; check current publication/review status and per-item license |
| `biorxiv` | Biological preprint metadata and versions | Public details API; no quota confirmed here | Preclinical findings do not establish clinical effectiveness |
| `chembl` | Compounds, targets, assays and bioactivity | Public REST web services | Preserve assay context, units, relation operators and activity type; not clinical evidence |

## Official documentation

- PubMed: [NCBI E-utilities overview](https://www.ncbi.nlm.nih.gov/books/NBK25497/), [key and usage guidance](https://eutilities.github.io/site/API_Key/usageandkey/).
- Europe PMC: [REST service](https://europepmc.org/RestfulWebService), [official help](https://europepmc.org/help).
- MeSH: [RDF, lookup and API](https://id.nlm.nih.gov/mesh/), [NLM overview](https://www.nlm.nih.gov/mesh/meshhome.html).
- Crossref: [REST API](https://www.crossref.org/documentation/retrieve-metadata/rest-api/), [official GitHub documentation](https://github.com/Crossref/rest-api-doc).
- OpenAlex: [API](https://help.openalex.org/api/), [authentication](https://help.openalex.org/api/authentication/), [pricing](https://help.openalex.org/access/pricing/).
- Semantic Scholar: [Academic Graph API](https://api.semanticscholar.org/api-docs/), [official tutorial](https://webflow.semanticscholar.org/product/api/tutorial).
- Unpaywall: [REST API](https://unpaywall.org/api), [response schema](https://unpaywall.org/data-format).
- ClinicalTrials.gov: [v2 documentation](https://clinicaltrials.gov/data-api/about-api), [NLM introduction](https://www.nlm.nih.gov/pubs/techbull/ma24/ma24_clinicaltrials_api.html).
- World Bank: [Indicators API](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392), [query structure](https://datahelpdesk.worldbank.org/knowledgebase/articles/898581), [indicator metadata](https://datahelpdesk.worldbank.org/knowledgebase/articles/898599-indicator-api-queries).
- openFDA: [authentication and quotas](https://open.fda.gov/apis/authentication/), [FAERS interpretation](https://open.fda.gov/apis/drug/event/).
- RxNorm: [functions and licensing](https://www.lhncbc.nlm.nih.gov/RxNav/APIs/RxNormAPIs.html), [RxNav FAQs](https://lhncbc-portal.lhcaws-prod-pub.nlm.nih.gov/RxNav/information/FAQs.html).
- medRxiv / bioRxiv: [details API](https://api.medrxiv.org/details/medrxiv/help), [bioRxiv API](https://api.biorxiv.org/).
- ChEMBL: [official web-service documentation](https://github.com/chembl/GLaDOS-docs/blob/master/web-services/chembl-data-web-services.md), [EMBL-EBI training](https://www.ebi.ac.uk/training/online/courses/embl-ebi-programmatically/chembl-programmatically/).

## Run a small request

From the skill directory, `python scripts/fetch_api.py PROVIDER --demo` uses the tiny query in `registry.json`. Add `--dry-run` to inspect the redacted URL without network access. No real credentials are bundled.

Examples of useful endpoint variations:

```bash
# PubMed search, then metadata/abstract retrieval for returned PMID values
python scripts/fetch_api.py pubmed --path esearch.fcgi --param db=pubmed --param 'term=diabetes[MeSH Terms]' --param retmax=5 --param retmode=json
python scripts/fetch_api.py pubmed --path efetch.fcgi --param db=pubmed --param id=30866872 --param retmode=xml

# MeSH terminology and bibliographic candidates (results need manual appraisal)
python scripts/fetch_api.py mesh --path lookup/descriptor --param label=diabetes --param match=contains --param limit=5
python scripts/fetch_api.py crossref --path works --param 'query.bibliographic=systematic review diabetes' --param rows=5
python scripts/fetch_api.py crossref --path works/10.1038/nature12373

# Literature search and citation graph
python scripts/fetch_api.py europepmc --path search --param query=diabetes --param pageSize=5 --param format=json --param resultType=core
python scripts/fetch_api.py openalex --path works --param search=diabetes --param per_page=5
python scripts/fetch_api.py semanticscholar --path paper/DOI:10.1038/nature12373 --param fields=title,year,authors,externalIds

# Open-access lookup (requires UNPAYWALL_EMAIL in the environment)
python scripts/fetch_api.py unpaywall --path 10.1038/nature12373

# Registered studies and a country time series
python scripts/fetch_api.py clinicaltrials --path studies --param query.cond=diabetes --param pageSize=5 --param format=json
python scripts/fetch_api.py worldbank --path country/VNM/indicator/SP.DYN.LE00.IN --param date=2010:2023 --param format=json --param per_page=50

# Drug data and preprint metadata
python scripts/fetch_api.py openfda --path drug/label.json --param 'search=openfda.generic_name:metformin' --param limit=1
python scripts/fetch_api.py rxnorm --path rxcui.json --param name=metformin
python scripts/fetch_api.py medrxiv --path details/medrxiv/2026-10-01/2026-10-02/0/json
python scripts/fetch_api.py biorxiv --path details/biorxiv/2026-10-01/2026-10-02/0/json
python scripts/fetch_api.py chembl --path molecule/CHEMBL25.json
```

Shell quoting differs by environment. Quote an entire `key=value` argument when it contains spaces or shell-special characters. `--path` takes an API-relative path, not a URL; put query arguments in repeated `--param` options. Endpoint examples are not a promise that any particular article remains available.

## Credentials

Set credentials only when needed in your local environment. The helper recognizes:

| Environment variable | Provider | Sent as |
|---|---|---|
| `NCBI_API_KEY` | PubMed | `api_key` query parameter |
| `CROSSREF_MAILTO` | Crossref | optional `mailto` query parameter |
| `OPENALEX_API_KEY` | OpenAlex | `api_key` query parameter |
| `S2_API_KEY` | Semantic Scholar | `x-api-key` header |
| `UNPAYWALL_EMAIL` | Unpaywall | required `email` query parameter |
| `OPENFDA_API_KEY` | openFDA | `api_key` query parameter |
| `UMLS_API_KEY` | RxNav | `Authorization: Bearer` header |

The contact email is transmitted to the provider when its variable is configured. Do not use someone else's email or fabricate a contact to bypass this requirement. Never place real credentials in command-line arguments, committed files, examples or issues. The helper rejects credential/contact query parameters supplied through `--param`, redacts configured secrets from returned string content, and does not print authentication headers. Redacted provenance cannot reconstruct credentials; provide them again locally to repeat a request.

No endpoint automatically activates a paid plan. However, existing metered accounts can consume their configured budget: check your OpenAlex account before using a key. This helper does not inspect provider billing or enforce a free daily budget.

## Response handling and scale

The helper supports JSON and preserves non-JSON responses as text (for example PubMed XML). HTTP success is not necessarily application success: inspect provider errors/messages, counts and required fields inside the body. Persist provider pagination cursors if retrieving more pages; do not claim a full dataset from one helper call.

The helper bounds retries and request size. It does not impose provider-specific request pacing across runs. For automation, use the current published rate policy, batching, caching and a task-appropriate maximum page/record budget. Stop at exhausted free quota or sustained throttling rather than silently upgrading.

## Deferred source

WHO is valuable, but its [legacy notice](https://www.who.int/data/gho/legacy) states that old GHO interfaces have been retired or scheduled for deprecation. The old API is deliberately excluded from the executable registry until a current replacement endpoint and schema are verified. Do not copy legacy WHO endpoints from a public API list into a new integration without checking this migration.
