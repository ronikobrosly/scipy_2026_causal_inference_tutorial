# SciPy 2026 Tutorial: Introduction to Causal Inference

A hands-on tutorial introducing causal inference concepts and practical implementation using Python. This tutorial covers causal graphs, estimation methods, the DoWhy framework, and time-series causal impact analysis.

## Prerequisites

### Knowledge Requirements
- Familiarity with Python data science stack (NumPy, Pandas, Matplotlib)
- Basic understanding of classic machine learning concepts
- No prior causal inference experience required

### System Requirements

| Dependency | Version | Purpose |
|------------|---------|---------|
| Python | 3.12+ | Runtime for notebooks |
| uv | Latest | Python package manager |
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

```bash
# Check versions
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
├── makefile                    # Build automation
├── pyproject.toml              # Python dependencies
└── README.md                   # This file
```

## Resources

- [DoWhy Documentation](https://www.pywhy.org/dowhy/)
- [Causal Graphical Models](https://github.com/ijmbarr/causalgraphicalmodels)
- [TFP CausalImpact](https://github.com/google/tfp-causalimpact)
- [Marimo Notebooks](https://marimo.io/)
- [Slidev](https://sli.dev/)
