PYTHON ?= $(shell \
	if command -v python3.11 >/dev/null 2>&1; then command -v python3.11; \
	elif command -v python3.12 >/dev/null 2>&1; then command -v python3.12; \
	elif [ -x "$(HOME)/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3" ]; then \
		printf "%s" "$(HOME)/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"; \
	else command -v python3; fi)

.PHONY: install test lint

install:
	$(PYTHON) -m pip install -e ".[dev]"

test:
	$(PYTHON) -m pytest

lint:
	$(PYTHON) -m ruff check .
