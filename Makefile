.PHONY: install install-ml lint format test hooks clean tracking-up

# base install (fast, no torch/transformers)
install:
	uv sync
	uv run pre-commit install

# pull in the heavy ML deps (torch/transformers/peft/bitsandbytes) when you hit Week 2
install-ml:
	uv sync --extra ml --extra tracking --extra retrieval

lint:
	uv run ruff check .

format:
	uv run ruff format .
	uv run ruff check --fix .

test:
	uv run pytest -q

hooks:
	uv run pre-commit run --all-files

# local MLflow UI backed by a sqlite file, no server setup required
tracking-up:
	uv run mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .ruff_cache .pytest_cache
