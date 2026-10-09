# Workflow guidance

## Literature discovery

Use the user's question and design to identify concepts. For intervention questions, PICO may help; it is not compulsory for every study type. Use MeSH to propose controlled terms and entry terms, then add free-text variants. Inspect MeSH hierarchy and explosion decisions rather than blindly appending every descendant.

Translate strategies per database. Record date restrictions and publication-type filters explicitly. PubMed's coverage and search behavior differ from citation indexes; filters can exclude relevant or not-yet-indexed papers.

Fetch a small first page; inspect returned fields and query translation, then paginate if the requested scope calls for it. PubMed has ESearch retrieval constraints for large sets; use the documented history/batch mechanisms or appropriate exports instead of assuming arbitrary offsets retrieve every result. The included helper does not paginate or implement Entrez History for you.

Deduplicate using DOI, PMID, and PMCID where possible. Handle preprint versus published versions explicitly. Keep separate counts for retrieved records, unique records and screened records. Source link lists alone do not prove systematic-review completeness.

Recommended table columns: `provider`, `provider_id`, `doi`, `pmid`, `pmcid`, `title`, `authors`, `year`, `publication_type`, `abstract_available`, `full_text_url`, `retrieved_at_utc`, `screening_status`. Add fields only when the output requires them; preserve unavailable values as missing.

## Citation verification

Preserve the reference as supplied. Normalize DOI prefixes and whitespace without altering the suffix arbitrarily. Resolve known DOI/PMID first; search by title/author/year when identifiers are absent or contradictory. Crossref does not register all DOIs, so an absent Crossref record is not conclusive.

Compare multiple fields and expose alternatives. Year differences can reflect online-first versus issue dates, and journal names can have abbreviations. Do not hide meaningful inconsistencies behind a similarity score.

Use statuses that have an explanation:

- **matched:** identity fields align, with harmless formatting differences explained.
- **mismatched:** a supplied identifier resolves to a different record or important fields disagree.
- **ambiguous:** multiple plausible records need a human decision.
- **unresolved:** no adequate match was found in the searched sources.

Record the sources searched, exact query and retrieval time. Separate a verified bibliographic identity from whether the article supports a particular sentence. Claim verification requires relevant article content and context. A missing correction/retraction field is not proof that none exists; inspect authoritative publisher updates when that question matters.

## Registered studies and public datasets

Define the population, period, outcome and unit of analysis. For ClinicalTrials.gov, distinguish interventional studies from observational studies, registered enrollment from actual enrollment, registration status from results availability, and submission dates from study dates. Registry records can change; preserve the extraction date and update fields.

For World Bank time series, preserve indicator codes, country codes, units, source notes and data years. Filter for the intended years and missingness instead of assuming the first returned record is the latest usable observation. Avoid silently imputing missing data or converting missing values to zero.

For openFDA/FAERS, document reporting biases, duplicate/follow-up handling and suspect versus concomitant drug roles. Counts lack a treated-population denominator and cannot estimate incidence or establish causality. Use aggregate outputs for teaching rather than sharing individual report details unnecessarily.

For RxNorm, preserve RxCUI and mapping method; review ambiguous names and terminology coverage. For ChEMBL, preserve assay, target, units, relation operators and activity type; do not pool incompatible measurements without justification. For preprints, record version, date, license, and linked publication status; verify status again before describing an item as peer reviewed.

## Teaching and content adaptation

Select one practical learning objective and demonstrate it with inspectable source records. Keep source metadata and the substantive claim together. Distinguish API retrieval, analytical choices and scientific interpretation. Use only openly permitted text and media; an open-access location is not permission to republish every figure.

The user decides whether to create a lesson, code exercise, script, carousel or video. Research output does not itself authorize posting, sending messages or changing schedules.
