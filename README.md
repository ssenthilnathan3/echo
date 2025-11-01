# Echo
Echo is not a workflow engine for humans; it’s an execution layer for AI agents.
You declare what tools exist, how they can be used, and how their side effects are handled.
Echo ensures those tools are orchestrated deterministically — so your AI can act safely, reproducibly, and autonomously.

## Overview

Echo provides a lightweight, declarative alternative to complex orchestration platforms like Airflow or Temporal. It consists of:

- **Control Plane**: FastAPI-based REST API for job management
- **Workers**: Distributed Python workers for workflow execution  
- **Plugin System**: Extensible tool plugins for different step types
- **Infrastructure**: Redis for queuing, Postgres for persistence

## Quick Start

### Development Setup

1. Install dependencies:
```bash
poetry install
```

2. Set up pre-commit hooks:
```bash
poetry run pre-commit install
```

3. Start infrastructure services:
```bash
docker-compose up -d postgres redis
```

4. Run database migrations:
```bash
poetry run alembic upgrade head
```

5. Start the control plane:
```bash
poetry run uvicorn app.control_plane.main:app --reload
```

6. Start a worker:
```bash
poetry run python -m app.worker.main
```

## Project Structure

```
specops/
├── control_plane/     # FastAPI REST API
├── worker/           # Job execution workers
├── common/           # Shared utilities and models
└── tests/            # Test suite
```

## Development

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=specops

# Run only unit tests
poetry run pytest -m unit

# Run only integration tests  
poetry run pytest -m integration
```

### Code Quality

```bash
# Format code
poetry run black .

# Lint code
poetry run ruff check .

# Type checking
poetry run mypy .

# Run all pre-commit hooks
poetry run pre-commit run --all-files
```

## License

MIT License
