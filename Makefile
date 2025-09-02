lint:
	@clear
	@echo "Running ruff on src"
	@ruff check --fix src/ || true
	@echo "Running ruff on tests"
	@ruff check --fix tests/ || true

mypy:
	@clear
	@echo "Running mypy on src"
	@poetry run mypy src/ || true
	@echo "Running mypy on tests"
	@poetry run mypy tests/ || true

format:
	@clear
	@echo "Running ruff format on src"
	@ruff format src/ || true
	@echo "Running ruff format on tests"
	@ruff format tests/ || true

format-diff:
	@clear
	@echo "Running ruff format on src"
	@ruff format --diff src/ || true
	@echo "Running ruff format on tests"
	@ruff format --diff tests/ || true