# zito — ListingIQ

Structured attribute extraction + relevance ranking for e-commerce listings.

**Pipeline, one line:** ingest → route (category) → extract (QLoRA sLLM, RAG-grounded
against a taxonomy KB, abstains when unsure) → rank (cross-encoder, ± attributes ablation)
→ serve → monitor.

**Datasets:**
- [MAVE](https://github.com/google-research-datasets/MAVE) — 3M span-level attribute labels, 1,257 categories, incl. negatives + zero-shot test set
- [ESCI](https://github.com/amazon-science/esci-data) — 130K queries, 2.6M query-product relevance judgments (E/S/C/I)

## Capability → component map

| Capability | Where it lives here |
|---|---|
| Dataset design/curation | MAVE join + silver→gold extraction set on ESCI text |
| Data augmentation & curation | Dedup, span checks, category balancing, negatives for abstention |
| LLM fine-tuning | QLoRA on a small open model for attribute extraction |
| Prompt engineering | Extraction prompts, abstention instructions, silver-labeling prompts |
| RAG | Taxonomy KB retrieval grounding extraction |
| Efficient inference | vLLM serving |
| Quantization / pruning / distillation | Optimization pass + Pareto report |
| HPO (Optuna / Ray Tune) | LoRA rank/α/LR sweep |
| Experiment tracking | W&B and/or MLflow, wired in from day one — see `src/zito/tracking.py` |
| Reproducibility | uv lockfile, config-driven runs, fixed seeds |
| Deployment + CI/CD | FastAPI + Docker + GitHub Actions |
| Monitoring + drift detection | Prometheus/Grafana + Evidently on real covariate shift (zero-shot categories, EN→ES/JA) |
| Ranking depth | ESCI cross-encoder + attribute-lift ablation |
| MLOps stack | Docker/K8s/MLflow/Prometheus (K8s optional/bonus) |

## Setup

Base install — no GPU, no ML libs, just enough to develop and run tests:

```bash
uv sync
uv run pre-commit install
```

Or via Makefile:

```bash
make install
```

When you hit the fine-tuning weeks, pull in torch/transformers/peft/bitsandbytes and the
tracking libs:

```bash
make install-ml
```

## Experiment tracking

Nothing is hardcoded to one backend. `src/zito/tracking.py` reads `ZITO_TRACKER` from
`.env` (`wandb`, `mlflow`, or unset/`none`):

```bash
cp .env.example .env
# then set ZITO_TRACKER=wandb and WANDB_API_KEY=... after `wandb login`,
# or ZITO_TRACKER=mlflow to log locally with zero external account
```

Local MLflow UI (SQLite-backed, no server to stand up):

```bash
make tracking-up   # serves at http://localhost:5000
```

## Common commands

```bash
make lint     # ruff check
make format   # ruff format + fix
make test     # pytest
make hooks    # run all pre-commit hooks against the whole repo
```

## Repo layout

```
src/zito/        # package code
tests/            # pytest
configs/          # run configs (model, LoRA, data) as the project grows
notebooks/        # exploration only — logic that survives moves into src/zito
data/             # raw/processed/external — gitignored, not committed
```

## Status

Scaffold only — Week 1 (data materialization) not yet started. See `configs/` for
run configuration as scripts land.
