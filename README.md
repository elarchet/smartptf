# smartptf

This project now uses uv for dependency and environment management.

## Prerequisites

- Python 3.13
- uv installed on your machine

## Install Dependencies

From the project root, use one of these commands:

```bash
uv sync                              # Simple app execution
uv sync --dev                        # Development tools (tests, deptry, etc.)
uv sync --extra ai                  # DRL training dependencies
uv sync --all-extras --all-groups   # Everything
```

These commands create or update the local virtual environment in `.venv`.

## Run the Streamlit App

From the project root, run:

```bash
uv run streamlit run src/app.py
```

Streamlit should open automatically in your browser (typically at http://localhost:8501).

## AI Training and TensorBoard

To train the DRL model, make sure you installed AI dependencies first:

```bash
uv sync --extra ai
```

Training logs are written under `models/DPT/logs` by the DPT training script.

Run training with uv:

```bash
uv run python src/models/DPT/AI_CLILearning.py
```

Then launch TensorBoard:

```bash
uv run tensorboard --logdir=models/DPT/logs
```

Open the URL shown by TensorBoard (typically http://localhost:6006).

## Useful Commands

```bash
# Sync dependencies after pyproject.toml changes
uv sync

# Run tests
uv run pytest
```