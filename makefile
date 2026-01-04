.PHONY: setup setup-python setup-slides setup-all run-slides build-slides export-slides \
        notebook-1 notebook-2 notebook-3 notebook-4 notebooks \
        format lint clean help check-deps

# Colors for terminal output
BLUE := \033[34m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
NC := \033[0m

# Directories
SLIDES_DIR := slides/Introduction\ to\ Causal\ Inference
NOTEBOOKS_DIR := notebooks

#------------------------------------------------------------------------------
# Setup targets
#------------------------------------------------------------------------------

setup: setup-python setup-slides ## Complete setup (Python + Node dependencies)
	@echo "$(GREEN)Setup complete!$(NC)"

setup-python: ## Install Python dependencies with uv
	@echo "$(BLUE)Installing Python dependencies...$(NC)"
	uv sync
	@echo "$(GREEN)Python dependencies installed.$(NC)"

setup-slides: ## Install Node dependencies for Slidev
	@echo "$(BLUE)Installing Slidev dependencies...$(NC)"
	cd $(SLIDES_DIR) && npm install
	@echo "$(GREEN)Slidev dependencies installed.$(NC)"

setup-all: check-deps setup ## Check system deps and run full setup

check-deps: ## Check if required system dependencies are installed
	@echo "$(BLUE)Checking system dependencies...$(NC)"
	@command -v python3 >/dev/null 2>&1 || { echo "$(RED)Python 3 is not installed$(NC)"; exit 1; }
	@command -v uv >/dev/null 2>&1 || { echo "$(RED)uv is not installed. Install with: curl -LsSf https://astral.sh/uv/install.sh | sh$(NC)"; exit 1; }
	@command -v node >/dev/null 2>&1 || { echo "$(RED)Node.js is not installed$(NC)"; exit 1; }
	@command -v npm >/dev/null 2>&1 || { echo "$(RED)npm is not installed$(NC)"; exit 1; }
	@command -v dot >/dev/null 2>&1 || { echo "$(YELLOW)Warning: graphviz (dot) is not installed. Some notebooks may not work correctly.$(NC)"; }
	@echo "$(GREEN)All required dependencies found.$(NC)"

#------------------------------------------------------------------------------
# Slides targets
#------------------------------------------------------------------------------

run-slides: ## Start Slidev development server
	@echo "$(BLUE)Starting Slidev server...$(NC)"
	cd $(SLIDES_DIR) && npm run dev

build-slides: ## Build slides for production
	@echo "$(BLUE)Building slides...$(NC)"
	cd $(SLIDES_DIR) && npm run build

export-slides: ## Export slides to PDF
	@echo "$(BLUE)Exporting slides to PDF...$(NC)"
	cd $(SLIDES_DIR) && npm run export

#------------------------------------------------------------------------------
# Notebook targets
#------------------------------------------------------------------------------

notebook-1: ## Run Notebook 1: Causal Graphs (student version)
	@echo "$(BLUE)Opening Notebook 1: Causal Graphs...$(NC)"
	uv run marimo edit $(NOTEBOOKS_DIR)/01_causal_graphs/01_student.py

notebook-2: ## Run Notebook 2: Simple Estimators (student version)
	@echo "$(BLUE)Opening Notebook 2: Simple Estimators...$(NC)"
	uv run marimo edit $(NOTEBOOKS_DIR)/02_simple_estimator/02_student.py

notebook-3: ## Run Notebook 3: DoWhy Framework (student version)
	@echo "$(BLUE)Opening Notebook 3: DoWhy Framework...$(NC)"
	uv run marimo edit $(NOTEBOOKS_DIR)/03_dowhy/03_student.py

notebook-4: ## Run Notebook 4: Causal Impact (student version)
	@echo "$(BLUE)Opening Notebook 4: Causal Impact...$(NC)"
	uv run marimo edit $(NOTEBOOKS_DIR)/04_causal_impact/04_student.py

notebooks: ## List available notebooks
	@echo "$(BLUE)Available notebooks:$(NC)"
	@echo "  make notebook-1  - Causal Graphs"
	@echo "  make notebook-2  - Simple Estimators (G-computation/S-learner)"
	@echo "  make notebook-3  - DoWhy Framework"
	@echo "  make notebook-4  - Causal Impact (Time Series)"

#------------------------------------------------------------------------------
# Teacher/Solution notebooks
#------------------------------------------------------------------------------

teacher-1: ## Run Notebook 1 with solutions (teacher version)
	uv run marimo edit $(NOTEBOOKS_DIR)/01_causal_graphs/01_teacher.py

teacher-2: ## Run Notebook 2 with solutions (teacher version)
	uv run marimo edit $(NOTEBOOKS_DIR)/02_simple_estimator/02_teacher.py

teacher-3: ## Run Notebook 3 with solutions (teacher version)
	uv run marimo edit $(NOTEBOOKS_DIR)/03_dowhy/03_teacher.py

teacher-4: ## Run Notebook 4 with solutions (teacher version)
	uv run marimo edit $(NOTEBOOKS_DIR)/04_causal_impact/04_teacher.py

#------------------------------------------------------------------------------
# Development targets
#------------------------------------------------------------------------------

format: ## Format code with black and ruff
	@echo "$(BLUE)Formatting code...$(NC)"
	uv run black .
	uv run ruff check --fix .
	@echo "$(GREEN)Formatting complete.$(NC)"

lint: ## Run linting checks
	@echo "$(BLUE)Running linters...$(NC)"
	uv run ruff check .

#------------------------------------------------------------------------------
# Utility targets
#------------------------------------------------------------------------------

clean: ## Clean build artifacts and caches
	@echo "$(BLUE)Cleaning build artifacts...$(NC)"
	rm -rf $(SLIDES_DIR)/dist
	rm -rf .ruff_cache
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)Clean complete.$(NC)"

help: ## Show this help message
	@echo "$(BLUE)SciPy 2026 Causal Inference Tutorial$(NC)"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)Quick Start:$(NC)"
	@echo "  1. make setup      # Install all dependencies"
	@echo "  2. make notebook-1 # Start first notebook"
	@echo "  3. make run-slides # View presentation"

.DEFAULT_GOAL := help
