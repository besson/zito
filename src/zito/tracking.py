"""Thin wrapper so run scripts don't hardcode one tracking backend.

Usage:
    from zito.tracking import start_run

    with start_run(run_name="extract-baseline", config={"model": "qwen2.5-3b"}) as run:
        run.log({"f1": 0.71})

Set ZITO_TRACKER=wandb|mlflow|none in .env. Defaults to "none" so the
scaffold runs with zero external accounts until you're ready to wire one up.
"""

from __future__ import annotations

import os
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any


@dataclass
class _NullRun:
    def log(self, metrics: dict[str, Any]) -> None:
        print(f"[tracking:none] {metrics}")


@dataclass
class _WandbRun:
    run: Any

    def log(self, metrics: dict[str, Any]) -> None:
        self.run.log(metrics)


@dataclass
class _MlflowRun:
    def log(self, metrics: dict[str, Any]) -> None:
        import mlflow

        mlflow.log_metrics(metrics)


@contextmanager
def start_run(run_name: str, config: dict[str, Any] | None = None):
    backend = os.getenv("ZITO_TRACKER", "none").lower()
    config = config or {}

    if backend == "wandb":
        import wandb

        run = wandb.init(
            project=os.getenv("WANDB_PROJECT", "zito-listingiq"),
            name=run_name,
            config=config,
        )
        try:
            yield _WandbRun(run=run)
        finally:
            run.finish()

    elif backend == "mlflow":
        import mlflow

        mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "sqlite:///mlflow.db"))
        mlflow.set_experiment(os.getenv("MLFLOW_EXPERIMENT_NAME", "zito-listingiq"))
        with mlflow.start_run(run_name=run_name):
            mlflow.log_params(config)
            yield _MlflowRun()

    else:
        yield _NullRun()
