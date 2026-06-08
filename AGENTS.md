# AGENTS.md

SciPy 2026 tutorial on causal inference. Marimo notebooks + Slidev slides.

## Key Commands

| Command | Purpose |
|----------|---------|
| `make help` | View all available commands |
| `make check-deps` | Check system dependencies |
| `make setup` | Install all deps (Python + Node) |
| `make setup-python` | Python dependencies only |
| `make setup-slides` | Slidev dependencies only |
| `make notebook-1` through `make notebook-4` | Run student notebooks |
| `make teacher-1` through `make teacher-4` | Run teacher (solution) notebooks |
| `make run-slides` | Slidev dev server |
| `make build-slides` | Build slides for production |
| `make export-slides` | Export slides to PDF |
| `make format` | Format code (black + ruff) |
| `make lint` | Lint code (ruff) |
| `make clean` | Clean build artifacts |

## Conventions

- Each notebook has `_student.py` (exercises) and `_teacher.py` (solutions)
- Notebooks use **Marimo**, not Jupyter — no `.ipynb` files
- Never modify `_teacher.py` files unless explicitly asked
- Python environment via `uv` (see `pyproject.toml`) — use `uv run ...` for Python commands
- Slidev project is in `slides/Introduction to Causal Inference/`
