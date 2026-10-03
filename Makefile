.PHONY: setup doctor lint test video
setup: ; uv sync --extra dev && cp -n config/.env.example config/.env || true
doctor: ; uv run python -m bianca_studio.cli doctor
lint: ; uv run ruff check src tests
test: ; uv run pytest -q
video: ; uv run python -m bianca_studio.cli run --product $(PRODUCT)
