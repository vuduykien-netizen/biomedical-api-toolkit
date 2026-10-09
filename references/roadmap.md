# Gradual implementation roadmap

These are three implementation directions, preserved independently of any channel, client, or institution. The API helper is a foundation; none of these complete applications is claimed to exist yet.

## Track 1 — Literature discovery assistant

**Purpose:** turn a research question into a traceable candidate literature set.

**Suggested providers:** MeSH → PubMed and Europe PMC → optional Semantic Scholar/OpenAlex exploration → Unpaywall open-access lookup.

**First deliverable:** an exported table of title, authors, year, publication type, DOI, PMID/PMCID, source, abstract availability and full-text location, plus exact search strategies and retrieval timestamps.

**Build gradually:**

1. Record a question and generate inspectable terminology and database-specific queries.
2. Retrieve a bounded candidate set and deduplicate by identifiers.
3. Add open-access links and user-defined screening fields.
4. Only when requested, extend to saved searches or periodic update checks.

**Acceptance:** searches can be repeated; retrieval and deduplication counts are reconciled; missing abstracts and full text remain explicit; a candidate set is not described as a completed systematic review.

## Track 2 — AI-generated citation verifier

**Purpose:** check bibliographic identity and identify mismatched or unresolved references.

**Suggested providers:** Crossref + PubMed; Europe PMC and OpenAlex/Semantic Scholar for secondary resolution.

**First deliverable:** a table containing the supplied reference, matched record, identifiers, differences, verification method and status.

**Build gradually:**

1. Parse a small list of references without guessing missing identifiers.
2. Resolve supplied DOI/PMID directly; otherwise search bibliographic fields.
3. Compare title, authors, year and journal and expose ambiguous candidates.
4. Add review of linked correction/retraction information when available.
5. Support a user-reviewed corrected bibliography export.

**Acceptance:** malformed and valid-but-mismatched DOIs receive different explanations; no-match is unresolved; identity checks are separated from claim verification and study-quality appraisal.

## Track 3 — Real datasets for research-methods teaching

**Purpose:** create small reproducible teaching datasets or scoped research extracts.

**Suggested providers:** World Bank for country time series; ClinicalTrials.gov for study registrations; openFDA for pharmacovigilance; RxNorm for drug coding; ChEMBL for bioactivity; medRxiv/bioRxiv for preprint metadata.

**First deliverable:** a raw extract, documented transformation, analysis-ready table, data dictionary and provenance manifest. Keep the example small and non-identifying.

**Build gradually:**

1. Choose a research question and unit of analysis before fetching.
2. Preserve units, dates, source definitions, missing values and stable IDs.
3. Demonstrate cleaning, descriptive statistics and one suitable visualization.
4. Expand to inferential analysis only after defining the design and assumptions.

**Acceptance:** the transformation can be rerun; counts and exclusions reconcile; ecological and reporting biases are explained; simulated values are never presented as observed API data.

## Suggested rollout

Start with **Track 2**, then **Track 1**, then **Track 3**. This order delivers an inspectable citation-checking result before taking on multi-database discovery and dataset interpretation. Users may choose another order based on their goals. No deployment, monitoring or publication is scheduled by this roadmap.
