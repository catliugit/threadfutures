# Thread Futures

[![ci](https://github.com/catliugit/ThreadFutures/actions/workflows/ci.yml/badge.svg)](https://github.com/catliugit/ThreadFutures/actions/workflows/ci.yml)

**We find new homes for the clothes fashion brands can't sell.**

Thread Futures is a B2B resale service for fashion brands: we act as their sales team for stock they can't sell themselves (checking, finding buyers such as off-price retailers/resale platforms, contracts), and give them the money from each sale plus a record of which approved buyer took each lot, and what they declare happened next. We start with premium brands, for what their sample sale and archive didn't sell: new-with-tags stock, sold in small lots to trade buyers the brand approves by name. The brand keeps ownership of the stock until it is sold, buyers pay the brand directly, and the brand sees its net £ on every lot before it commits.

In the EU, large brands can no longer destroy unsold clothes and shoes they hold there, except on narrow documented grounds (since 19 July 2026; medium-sized firms from July 2030). Great Britain has no equivalent ban: for stock held in Great Britain, the case is money and discretion.

**Status:** Pre-launch and pre-revenue. An independent project Cathy Liu started in London in November 2026, in customer research with brands, warehouses and trade buyers. First pilots are planned for spring 2027. Until the 26 Feb 2027 decision we build nothing new: we use spreadsheets (the Google Sheet CRM, lot sheets, bid form and calculator), and scripts only when a real stock list or a real bid run needs them. No hosted app, no logins, no Stock Health index. **Go-to-market:** Brands are the buyer. We reach them directly and through their warehouses (3PLs); the brand's own 3PL does the physical work on every batch, and we test 3PL introductions in parallel.

**What this repository is:** earlier, exploratory technical work (models, data pipelines, regulation search, an API and CI). Parts 1–17 are earlier portfolio and skills work, not the product. The resale desk is PLANNED (designed, not built); its technical map is in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md). The offcut forecast (Part 1) and the purchase-order agent (Part 8) are earlier exploratory work for a previous idea (garment factories). The product is the service itself and the batch record (designed, not built; see docs/ARCHITECTURE.md), which would be built only if hand-run pilots show it is needed. Built with AI-assisted tooling, reviewed and tested by me.

- **How it works, per batch.** 1) The brand sends a stock list (no system access). 2) Its jobber gives a written bid: that's the floor. 3) We split the stock into small unbranded lots; the brand's own warehouse (3PL) does a carton check and one photo per style, on the brand's instructions. 4) Trade buyers the brand approves by name send written bids. 5) If the bids beat the floor by enough, the brand sells: buyers pay the brand, the 3PL releases the goods, and the brand gets a record of which buyer took each lot. Otherwise, no batch and nothing to pay. Anything no buyer takes can go to a charity or recycler the brand contracts directly, with the evidence logged; transport and warehouse work are arranged with and paid by the brand, at cost. Pricing: one fee per batch, only on the money buyers pay above the brand's written jobber bid (details: [investors page](https://threadfutures.com/investors.html)). *Status:* **planned, not built**; the first batches run by hand.
- **Stall-risk model (built, Part 4).** Scores a line from its first 12 weeks of sales. Runs on **real open retail data (UCI Online Retail II, a UK giftware wholesaler), not fashion and not a customer**. Earlier work, not the product.
- **Offcut Forecast (built, Part 1): SIMULATED, PARKED.** Earlier exploratory work for a previous idea (garment factories), not the product: estimates the kg of fabric a cutting run will leave over, trained on **simulated** cutting runs.

**Why not just use ChatGPT?** Much of the software in this repo (Parts 3, 4 and 7 especially) could be reproduced by a brand analyst with ChatGPT, Claude or Copilot, which is why software isn't what we sell. A chatbot can draft a template; it can't approve buyers, check goods, or get written bids from trade buyers on a real lot. **Why not just call TK Maxx?** For clean current stock, brands should. We are for the premium new-with-tags stock their sample sale and archive didn't sell.

Website: [threadfutures.com](https://threadfutures.com) · Building Thread Futures: Cathy Liu ([LinkedIn](https://www.linkedin.com/in/cathyqliu))

> **Honest scope.** This is an early-stage independent project, not a live product. The offcut forecast is trained on **simulated** cutting runs. The unsold-stock analytics run on **real open retail data** ([UCI Online Retail II](https://doi.org/10.24432/C5CG6D), a UK giftware wholesaler, CC BY 4.0), which is not fashion data and not a customer's. The service, the batch record and the buyer network are planned, not built. The regulation search covers ESPR articles only, on a 22-passage test set; Delegated Regulation (EU) 2026/296 and Implementing Regulation (EU) 2026/2 are not yet in the corpus. General information, not legal advice.

## Why

Since 19 July 2026, large companies may not destroy unsold clothing and footwear in the EU, and "destruction" includes recycling and energy recovery unless one of the exceptions in Delegated Regulation (EU) 2026/296 applies ([Regulation (EU) 2024/1781](https://eur-lex.europa.eu/eli/reg/2024/1781/oj), Articles 24–25). Medium-sized companies follow from July 2030. The donation exception needs goods offered for at least 8 weeks to at least three suitable social-economy entities in the EU (or on the brand's own website) and not accepted; UK charities don't count. Evidence must be kept 5 years and provided within 30 days of a request. The disclosure duty applies to large firms from the first full financial year after 18 July 2024; the mandatory standard format (Implementing Regulation (EU) 2026/2) applies from 2 March 2027, to the first full financial year after that date. Germany's fines (up to €100,000) apply from 1 Nov 2026.

Premium brands' filed accounts show heavy stock provisions and long days of stock; channels have narrowed (Afound and BULQ closed); and capital is flowing into the category (Ghost, smatch, eBay–Reskinned) [R]. The EU destruction ban is the expansion trigger for stock held in the EU. In the EU, large brands can no longer destroy unsold clothes and shoes they hold there, except on narrow documented grounds (since 19 July 2026; medium-sized firms from July 2030). Great Britain has no equivalent ban: for stock held in Great Britain, the case is money and discretion. The legal routes are narrow and need paperwork: sell, donate, or prove an exception before recycling.

## What's in the repository

| # | Part | What it does | Tools | Result |
|---|---|---|---|---|
| 1 | [Offcut forecasting](src/offcut) (*earlier work for a previous idea, not the product*) | P10/P50/P90 offcut forecast per cutting run; runs in the browser | Python, scikit-learn, pandas, JavaScript | **8.8%** mean error vs 20.3% for the 15% rule of thumb, 1,600 held-out *simulated* runs |
| 2 | [Analytics engineering](dbt) | Bronze (Parquet) → silver → gold models of 1.06m sales lines | dbt Core, DuckDB, SQL | **22** dbt data tests passing, including revenue reconciliation between layers |
| 3 | [Merchandising analytics](dbt/models/marts/mart_sku_health.sql) | Selling / slowing / stopped status, ABC/XYZ, velocity, markdown depth, return rate | SQL, dbt | **4,707** SKUs classified |
| 4 | [Stall-risk model](src/stock/train_stall.py) | From a line's first 12 weeks, predicts whether sales collapse in weeks 12–25 | scikit-learn, MLflow | ROC AUC **0.81** vs 0.60 for a "sales halved" rule on 423 later launches; top-20% precision 32% vs an 11% base rate |
| 5 | [Experimentation](src/stock/experiment.py) | Do markdowns help stock sell? How big must a routing pilot be? | statsmodels, SciPy | Stacked difference-in-differences (768 marked-down SKUs, 5 matched controls each). A placebo test found a pre-trend, so the +125% estimate is an upper bound. Pilot power analysis: **64** batches per arm |
| 6 | [Model monitoring](src/stock/monitor.py) | Accuracy, calibration and data drift per launch quarter | SciPy, pandas | Flagged over-prediction on 2011 Q2 launches (13.6% predicted vs 1.7% actual), an AUC alert for 2011 Q1 (0.65) and PSI drift. [Report](site/reports/monitoring.html) |
| 7 | [Regulation search](src/regsearch/search.py) | Finds the article of EU law that answers a question; checks citations | BM25, TF-IDF (scikit-learn), LLM API | Right article in the top 3 for **21 of 22** test questions (hit@1 73%, MRR 0.83) |
| 8 | [Purchase-order agent](src/offcut/agent.py) (*earlier work for a previous idea, not the product*) | Reads a messy order note, states assumptions, calls tested tools | LLM API with tool use | The model never does the arithmetic |
| 9 | [API](src/api/main.py) | Offcut forecast, stall risk and regulation search endpoints | FastAPI, Pydantic, Docker | **23** pytest tests; GitHub Actions runs them, builds the Docker image and calls the API on every push to main and every pull request (dbt tests run via `make dbt`, not in CI) |
| 18 | [Resale desk and batch record](docs/ARCHITECTURE.md#1-the-resale-desk-planned-technical-map) (**PLANNED: designed, not built**; replaces the old Part 18 design) | Modules M1–M10: stock-list intake, lots, written bids with valid-until dates (jobber floor, platform floor, observed ask, written indicative, firm written), the brand's approval of each buyer, release only after the brand confirms funds, a record to the first buyer of each lot plus each buyer's signed statement, and a batch report with net £ against the floor | Until GO: Google Sheet (`bids`, `lots`, `fees` tabs), lot sheets, bid form, Recovery Calculator, email. V1 after GO: Postgres and magic links | Not built. Nothing new is built before the 26 Feb 2027 GO / PIVOT / STOP decision; not before GO: a hosted app, logins, the Stock Health pipeline, the hash-chained ledger or any API. Effort estimates [E]: pilot toolkit 2–3 weeks; V1 6–9 weeks after GO |

Every number above (Parts 1 to 9) is produced by the code in this repo and saved under [`models/`](models).

### Things the checks caught

- **dbt tests** found 23 returns logged before an item's first recorded sale (stock sold before the data starts). The model now leaves weeks-since-launch empty for those rows.
- **The browser export** of the offcut model rounded split thresholds, but scikit-learn compares inputs as 32-bit floats. For edge inputs (e.g. a 1.57 m roll) the browser took a different branch. Thresholds are now exported at full precision and inputs cast with `Math.fround`, and a test checks the export matches scikit-learn.
- **The placebo test** showed marked-down lines were already gaining before the markdown, so the difference-in-differences estimate is reported as an upper bound, not a clean effect.
- **Monitoring** showed the stall model is well ranked but over-confident for spring launches heading into the Christmas season, which a seasonal feature or recalibration would need to fix.

## Documentation

- [Architecture](docs/ARCHITECTURE.md): how the parts fit together, and which are live, maybe later, parked or planned.
- Themed docs, one per group of parts. For each part: discipline, methodology, tools and status, the short part note, then the step-by-step guide (the code, every concept from scratch, results, what went wrong and how to run it). Parts 01 to 10 are built; 11 to 18 are planned, and none of 11 to 18 is scheduled during customer discovery (to early 2027).
  - [1. Data engineering](docs/1_data_engineering.md): Part 02 analytics engineering (dbt + DuckDB), Part 03 merchandising analytics
  - [2. Machine learning models](docs/2_ml_models.md): Part 01 offcut forecasting (earlier work for a previous idea, not the product), Part 04 stall-risk model
  - [3. Experiments and monitoring](docs/3_experiments_monitoring.md): Part 05 experimentation and causal analysis, Part 06 model monitoring
  - [4. AI tools](docs/4_ai_tools.md): Part 07 regulation search, Part 08 purchase-order agent (earlier work for a previous idea, not the product)
  - [5. Platform](docs/5_platform.md): Part 09 API service, Part 10 CI and Docker build
  - [6. Planned parts](docs/6_planned.md): Parts 11 to 18, including the Part 18 batch report prototype
- [Discipline and methodology by part](docs/ARCHITECTURE.md#discipline-and-methodology-by-part) and a [concept index](docs/ARCHITECTURE.md#concept-index).

## Run it

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

make offcuts      # simulate 8,000 cutting runs, train, evaluate
make stock        # download retail data, dbt build, stall model, experiment, monitoring, regulation search
                  # (the monitoring step rewrites site/reports/monitoring.html)
make test         # 23 tests
make site-export  # on purpose only: refresh site/model.js and site/data/*.js for the live website
make site-diff    # see what changed in site/ before committing
make api          # http://127.0.0.1:8000/docs
make mlflow-ui    # browse tracked runs
```

> **Note:** `site/` is published by Netlify whenever `main` changes. Only `make monitor` (part of `make stock`), `make site` and `make site-export` write into it; run `make site-diff` and review `git diff site/` before committing.

Docker (API only):

```bash
docker build -t threadfutures-api . && docker run -p 8000:8000 threadfutures-api
```

The purchase-order agent and generated regulation answers are optional and need an LLM API key: copy `.env.example` to `.env`, then `pip install -r requirements-llm.txt`.

## Layout

```
site/            static website (Netlify publishes this folder)
src/offcut/      offcut simulation, pipeline, quantile model, browser export, agent
src/stock/       retail ingest, stall-risk model, experiment, monitoring, site export
src/regsearch/   regulation retrieval, evaluation, cited answers
src/api/         FastAPI service
dbt/             dbt project (staging, intermediate, marts, semantic layer, tests)
data/            regulation text, evaluation questions, sample recyclers (raw data is downloaded)
models/          trained models and saved metrics
tests/           pytest suite
```

## Data and licences

- Retail data: Chen, D. (2012). *Online Retail II*. UCI Machine Learning Repository. https://doi.org/10.24432/C5CG6D (CC BY 4.0). Downloaded by `make retail`, not stored in the repo.
- Regulation text: Regulation (EU) 2024/1781, © European Union, https://eur-lex.europa.eu, reused under Commission Decision 2011/833/EU. General information, not legal advice.
- Offcut data is simulated from first principles and calibrated to published industry ranges.
- All rights reserved unless a LICENSE file says otherwise. UCI data CC BY 4.0; EUR-Lex text © European Union.

## Before publishing

Run `python3 scripts/claims_lint.py` (0 hits required) before any change to `site/` or this README goes live.

Updated Tue 24 Nov 2026.
