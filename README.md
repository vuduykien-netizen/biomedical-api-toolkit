# Biomedical API Toolkit

An English-language agent skill for finding biomedical literature, verifying citations, and obtaining public research and teaching data through APIs with free access options.

**14 API entries · 3 implementation tracks · Python standard library only**

The skill includes PubMed, Europe PMC, MeSH, Crossref, OpenAlex, Semantic Scholar, Unpaywall, ClinicalTrials.gov, World Bank, openFDA, RxNorm, medRxiv, bioRxiv, and ChEMBL. Free access may have rate limits, require registration, or be a limited free tier; this is not a promise of unlimited free service.

## Install as a Codex skill

Clone into a new folder under your Codex skills directory. If `CODEX_HOME` is customized, use its `skills` directory instead. Do not overwrite an existing installation.

macOS / Linux:

```bash
git clone https://github.com/vuduykien-netizen/biomedical-api-toolkit.git ~/.codex/skills/biomedical-api-toolkit
```

Windows PowerShell:

```powershell
git clone https://github.com/vuduykien-netizen/biomedical-api-toolkit.git "$env:USERPROFILE\.codex\skills\biomedical-api-toolkit"
```

Reload skills or start a new session if your client has not discovered the skill yet. Other skill-capable clients can use this folder if they support the `SKILL.md` format; installation locations are client-specific.

## Example prompts

```text
Use $biomedical-api-toolkit to build and record a PubMed search strategy
for a biomedical research question, including MeSH terms and limitations.

Use $biomedical-api-toolkit to verify these references. Compare DOI,
title, authors, year, and journal, and distinguish mismatches from unresolved items.

Use $biomedical-api-toolkit to prepare a small teaching dataset of
Vietnam's life expectancy over time, preserving units, years, and source metadata.
```

## Try the API helper

Requires Python 3.10+; no third-party packages are needed for the helper.

```bash
python scripts/fetch_api.py pubmed --demo --dry-run
python scripts/fetch_api.py pubmed --demo --output results/pubmed.json
python scripts/fetch_api.py clinicaltrials --param query.cond=diabetes --param pageSize=2
python scripts/fetch_api.py crossref --path works --param query.bibliographic="systematic review" --param rows=2
```

The helper makes one read-only GET request with up to two retries for transient errors. It does not exhaust pagination, synthesize findings, verify clinical claims, or implement the three full applications. Read [API setup and examples](references/api-catalog.md) before querying at scale. `--output` refuses to replace an existing file.

## Contents

- [SKILL.md](SKILL.md): skill entry point and evidence boundaries.
- [API catalog](references/api-catalog.md): official docs, credentials, free access, examples and limits.
- [Workflow guidance](references/workflows.md): practical methods and outputs.
- [Implementation roadmap](references/roadmap.md): the three gradual implementation tracks.
- [Registry](references/registry.json): provider endpoints and small demo queries.
- [Fetch helper](scripts/fetch_api.py): bounded requests and provenance envelopes.
- [Local checks](tests/test_fetch_api.py): offline behavior checks.

Run offline checks with:

```bash
python -m unittest discover -s tests -v
```

## Verification and contributions

Initial catalog review: **2026-10-10**. The [verification record](references/verification.md) distinguishes successful live probes, documentation-only checks and access limitations. A successful probe establishes access for that request, not completeness or reliability of the entire service.

Contributions should link to official documentation, state free access and authentication requirements, record a verification date, include a small non-identifying query, and explain interpretation and reuse limits. Never include credentials or private research data. Keep this skill focused on research workflows rather than clinical advice or vendor promotion.

## License

MIT for this repository's original code and documentation. External API services, article text, figures, vocabularies and datasets retain their own terms and licenses. No affiliation or endorsement by the listed providers is implied.
