# SciPy 2026 Tutorial: Introduction to Causal Inference

A hands-on tutorial for SciPy 2026 that introduces causal inference concepts and gives attendees a practical implementation using Python. This tutorial covers causal graphs, estimation methods, the DoWhy framework, and time-series causal impact analysis.

This README provides instructions on how to setup the tutorial environment and slides (for Debian Linux, Mac OSX, and Windows).

The included `Makefile` contains all of the commands necessary to setup and run notebooks and slides.

```bash
# View all available commands
make help
```


## Prerequisites

### Knowledge Requirements
- Familiarity with Python data science stack (NumPy, Pandas, Matplotlib)
- Basic understanding of classic machine learning concepts
- **No prior causal inference experience required** 

### System Requirements

| Dependency | Version | Purpose |
|------------|---------|---------|
| Python | 3.12+ | Runtime for notebooks |
| uv | Latest | Python package manager |
| **or pixi** | **Latest** | **All-in-one package manager (alternative)** |
| Node.js | 20+ | Slidev presentation |
| npm | Latest | Node package manager |
| Graphviz | Latest | Graph visualization |

## Installation

### 1. Install System Dependencies

**macOS (Homebrew):**
```bash
# Install uv (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Node.js
brew install node

# Install Graphviz
brew install graphviz
```

**Ubuntu/Debian:**
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Node.js (v20+)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install Graphviz
sudo apt-get install -y graphviz graphviz-dev
```

**Windows:**
```powershell
# Install uv
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Install Node.js from https://nodejs.org/
# Install Graphviz from https://graphviz.org/download/
```

### 2. Verify Dependencies

Check that all required system dependencies are installed with correct versions:

```bash
# Automatic check (recommended)
make check-deps

# Or verify manually:
python3 --version   # Should be 3.12+
uv --version
node --version      # Should be v20+
npm --version
dot -V              # Graphviz
```

### 3. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/your-org/scipy_2026_causal_inference_tutorial.git
cd scipy_2026_causal_inference_tutorial

# Install all dependencies (Python + Node)
make setup

# Or install separately:
make setup-python   # Python dependencies only
make setup-slides   # Slidev dependencies only
```

### Pixi Setup (Alternative to the makefile)

[Pixi](https://pixi.sh/) is an all-in-one package manager built on conda that handles Python, system libraries (Graphviz), and Node.js in a single environment. With pixi, you can skip installing uv, Node.js, and Graphviz separately — pixi manages everything.

**Install pixi:**

```bash
# macOS/Linux
curl -fsSL https://pixi.sh/install.sh | bash

# Windows (PowerShell)
iwr -useb https://pixi.sh/install.ps1 | iex

# Or via Homebrew
brew install pixi
```

**Clone and set up:**

```bash
git clone https://github.com/your-org/scipy_2026_causal_inference_tutorial.git
cd scipy_2026_causal_inference_tutorial

# Install all Python + system dependencies in one command
pixi install

# Install Slidev (Node.js) dependencies
pixi run setup-slides
```

**Quick start with pixi:**

```bash
# List all available tasks
pixi task list

# Start the first notebook
pixi run notebook-1

# View the slides
pixi run run-slides
```

| Pixi Command | Purpose |
|-------------|---------|
| `pixi install` | Install all Python + system dependencies |
| `pixi run setup-slides` | Install Slidev (Node.js) dependencies |
| `pixi run notebook-1` through `pixi run notebook-4` | Run student notebooks |
| `pixi run teacher-1` through `pixi run teacher-4` | Run teacher (solution) notebooks |
| `pixi run run-slides` | Start Slidev dev server |
| `pixi run build-slides` | Build slides for production |
| `pixi run export-slides` | Export slides to PDF |
| `pixi run format` | Format code (ruff) |
| `pixi run lint` | Lint code (ruff) |
| `pixi run clean` | Clean build artifacts |
| `pixi shell` | Open a shell in the pixi environment |

## Quick Start

```bash
# View all available commands
make help

# Start the first notebook
make notebook-1

# View the slides
make run-slides
```

## Tutorial Structure

### Notebooks

The tutorial consists of four interactive [Marimo](https://marimo.io/) notebooks:

| # | Notebook | Topic | Command |
|---|----------|-------|---------|
| 1 | Causal Graphs | DAGs, confounding, colliders, d-separation | `make notebook-1` |
| 2 | Simple Estimators | S-learner and metalearning | `make notebook-2` |
| 3 | DoWhy Framework | Model, Identify, Estimate, Refute workflow | `make notebook-3` |
| 4 | Causal Impact | Bayesian structural time series | `make notebook-4` |

Each notebook has a student version (exercises) and a teacher version (with solutions):

```bash
# Student versions (recommended for attendees)
make notebook-1
make notebook-2
make notebook-3
make notebook-4

# Teacher versions (with solutions)
make teacher-1
make teacher-2
make teacher-3
make teacher-4
```

### Slides

The presentation is built with [Slidev](https://sli.dev/):

```bash
# Start development server (opens browser automatically)
make run-slides

# Build for production
make build-slides

# Export to PDF
make export-slides
```

## File Structure

```
scipy_2026_causal_inference_tutorial/
├── notebooks/
│   ├── 01_causal_graphs/       # Notebook 1: Causal graphs & DAGs
│   ├── 02_simple_estimator/    # Notebook 2: G-computation & S-learner
│   ├── 03_dowhy/               # Notebook 3: DoWhy framework
│   └── 04_causal_impact/       # Notebook 4: Time series causal impact
├── slides/
│   └── Introduction to Causal Inference/
│       ├── slides.md           # Main presentation
│       └── imgs/               # Slide images
├── data/
│   └── causal_churn.csv        # Sample dataset
├── makefile                    # Build automation (uv-based)
├── pixi.toml                   # Build automation (pixi-based)
├── pyproject.toml              # Python dependencies
└── README.md                   # This file
```

## Resources

- [DoWhy Documentation](https://www.pywhy.org/dowhy/)
- [Causal Graphical Models](https://github.com/ijmbarr/causalgraphicalmodels)
- [TFP CausalImpact](https://github.com/google/tfp-causalimpact)
- [Marimo Notebooks](https://marimo.io/)
- [Slidev](https://sli.dev/)
