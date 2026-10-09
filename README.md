# Biomedical API Toolkit

An English-language agent skill for finding biomedical literature, verifying citations, and obtaining public research and teaching data through APIs with free access options.

**New here?** Read the [beginner guide in English](docs/getting-started.md) or [hướng dẫn tiếng Việt](docs/getting-started.vi.md). Both explain the toolkit's purpose, installation, first task, example prompts, outputs and common errors.

**14 API entries · 3 implementation tracks · Python standard library only**

The skill includes PubMed, Europe PMC, MeSH, Crossref, OpenAlex, Semantic Scholar, Unpaywall, ClinicalTrials.gov, World Bank, openFDA, RxNorm, medRxiv, bioRxiv, and ChEMBL. Free access may have rate limits, require registration, or be a limited free tier; this is not a promise of unlimited free service.

## What can you do with it?

| Your task | How the toolkit helps | Example result |
|---|---|---|
| Find literature for a biomedical question | Guides an AI agent through terminology, database searches and source recording | Candidate article table with identifiers and a reproducible search strategy |
| Check references supplied by AI | Guides comparison of DOI, title, authors, year and journal | Matched, mismatched, ambiguous or unresolved reference table |
| Prepare real data for a lesson or scoped study | Helps select and query public data sources and preserve provenance | Raw extract plus a documented table, if you ask the agent to prepare one |

The repository contains instructions for an AI agent, a source catalog and a small Python request helper. It is not a standalone website or a complete automated review application. The helper retrieves data; an agent or researcher still performs the requested verification and analysis.

## Choose how to start

**Use an AI agent:** install the skill in a compatible client, then describe your task. You do not need to write Python yourself. Live retrieval requires the client's network and execution tools; Python is needed if it runs the included helper.

**Use Python directly:** download the repository and run the helper in a terminal. This returns source data and request details, not a finished literature review or analysis. You do not need an AI client for this route.

## Install as a Codex skill

You can ask Codex's installer:

```text
Use $skill-installer to install the skill from
https://github.com/vuduykien-netizen/biomedical-api-toolkit.
The skill is at the repository root.
```

For manual installation with Git, the current [official local skill guide](https://learn.chatgpt.com/docs/build-skills) lists `~/.agents/skills` as the user location. Use the directory supported by your installed client; some setups use `~/.codex/skills` or a customized `CODEX_HOME/skills`. Keep one installation and do not overwrite an existing folder.

macOS / Linux:

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/vuduykien-netizen/biomedical-api-toolkit.git ~/.agents/skills/biomedical-api-toolkit
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.agents\skills" | Out-Null
git clone https://github.com/vuduykien-netizen/biomedical-api-toolkit.git "$env:USERPROFILE\.agents\skills\biomedical-api-toolkit"
```

Reload skills or start a new session if your client has not discovered the skill yet. Other skill-capable clients can use this folder if they support the `SKILL.md` format; installation locations are client-specific.

No Git installed? The [beginner guide](docs/getting-started.md) also covers downloading a ZIP and placing the skill folder manually.

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

Requires Python 3.10+; no third-party packages are needed for the helper. Run these commands **from the toolkit folder**, which contains `SKILL.md` and `scripts/`. Check `python --version`; if your installation uses `python3` or `py`, replace `python` accordingly.

```bash
python scripts/fetch_api.py pubmed --demo --dry-run
python scripts/fetch_api.py pubmed --demo --output results/pubmed.json
python scripts/fetch_api.py clinicaltrials --path studies --param query.cond=diabetes --param pageSize=2
python scripts/fetch_api.py crossref --path works --param "query.bibliographic=systematic review" --param rows=2
```

The helper makes one read-only GET request with up to two retries for transient errors. It does not exhaust pagination, synthesize findings, verify clinical claims, or implement the three full applications. Read [API setup and examples](references/api-catalog.md) before querying at scale. `--output` refuses to replace an existing file.

Free biomedical API access is separate from any subscription or usage costs of your AI client. You can start with small PubMed, MeSH, Crossref, ClinicalTrials.gov or World Bank examples without configuring a key. See the catalog before using an account with metered usage.

## Contents

- [SKILL.md](SKILL.md): skill entry point and evidence boundaries.
- [Beginner guide](docs/getting-started.md) / [Tiếng Việt](docs/getting-started.vi.md): purpose, setup, examples, outputs and troubleshooting.
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
