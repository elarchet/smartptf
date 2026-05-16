# smartptf

This project now uses uv for dependency and environment management.

## Prerequisites

- Python 3.13
- uv installed on your machine

## Install Dependencies

From the project root, run:

```bash
uv sync
```

This creates a local virtual environment in `.venv` and installs all dependencies from `pyproject.toml`.

## Run the Streamlit App

From the project root, run:

```bash
uv run streamlit run app.py
```

Streamlit should open automatically in your browser (typically at http://localhost:8501).

## AI Training and TensorBoard

Training logs are written under `models/DPT/logs` by the DPT training script.

Run training with uv:

```bash
uv run python models/DPT/AI_CLILearning.py
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