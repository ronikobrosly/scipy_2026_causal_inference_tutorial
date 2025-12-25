.PHONY: setup run format lint

setup:
	uv sync

run:
	uv run marimo edit notebooks/01_introduction.py

format:
	uv run black .
	uv run ruff check --fix .

lint:
	uv run ruff check .