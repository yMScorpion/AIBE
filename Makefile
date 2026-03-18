.PHONY: setup install lint format typecheck test up down migrate launch clean

setup:
	pip install uv
	uv pip install --system -e ".[dev,security,ml]"
	pre-commit install
	cp -n env.example .env 2>/dev/null || true
	@echo "Setup complete. Edit .env with your keys."

install:
	uv pip install --system -e ".[dev,security,ml]"

lint:
	ruff check aibe/ tests/
	black --check aibe/ tests/

format:
	ruff check --fix aibe/ tests/
	black aibe/ tests/

typecheck:
	mypy aibe/ --config-file mypy.ini

test:
	pytest tests/unit/ -x -q --cov=aibe --cov-report=term-missing

test-all:
	pytest tests/ -x -q --cov=aibe --cov-report=term-missing

up:
	docker compose up -d

down:
	docker compose down

migrate:
	alembic upgrade head

launch:
	python -m aibe.core.orchestrator.launch

security-scan:
	bandit -r aibe/ -c pyproject.toml
	ruff check aibe/ --select S

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/ .coverage coverage.xml
