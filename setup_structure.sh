#!/bin/bash

echo "Creating AMGD package structure..."

# Create the main directory structure
mkdir -p src/amgd/{core,models,utils,benchmarks,visualization}
mkdir -p tests/fixtures
mkdir -p examples
mkdir -p docs/source/tutorials
mkdir -p benchmarks
mkdir -p .github/workflows

# Create all __init__.py files
touch src/amgd/__init__.py
touch src/amgd/core/__init__.py
touch src/amgd/models/__init__.py
touch src/amgd/utils/__init__.py
touch src/amgd/benchmarks/__init__.py
touch src/amgd/visualization/__init__.py
touch tests/__init__.py

# Create core module files
touch src/amgd/core/optimizer.py
touch src/amgd/core/penalties.py
touch src/amgd/core/convergence.py

# Create models module files
touch src/amgd/models/poisson.py
touch src/amgd/models/glm.py
touch src/amgd/models/base.py

# Create utils module files
touch src/amgd/utils/validation.py
touch src/amgd/utils/preprocessing.py
touch src/amgd/utils/metrics.py

# Create benchmarks module files
touch src/amgd/benchmarks/comparison.py
touch src/amgd/benchmarks/datasets.py

# Create visualization module files
touch src/amgd/visualization/convergence.py
touch src/amgd/visualization/coefficients.py

# Create test files
touch tests/test_optimizer.py
touch tests/test_poisson.py
touch tests/test_benchmarks.py
touch tests/fixtures/sample_data.py

# Create example files
touch examples/basic_usage.py
touch examples/ecological_health_analysis.py
touch examples/comparison_with_competitors.py
touch examples/custom_regularization.py

# Create documentation files
touch docs/source/conf.py
touch docs/source/index.rst
touch docs/source/api_reference.rst
touch docs/source/theory.rst
touch docs/source/benchmarks.rst

# Create benchmark files
touch benchmarks/performance_tests.py
touch benchmarks/reproduce_paper_results.py

# Create configuration and documentation files
touch pyproject.toml
touch README.md
touch LICENSE
touch CHANGELOG.md

# Create GitHub workflow files
touch .github/workflows/tests.yml
touch .github/workflows/docs.yml
touch .github/workflows/publish.yml

# Create .gitignore file
touch .gitignore

echo "✅ Directory structure created successfully!"
echo "📁 Created $(find . -type f | wc -l) files and $(find . -type d | wc -l) directories"
echo ""
echo "Next steps:"
echo "1. Initialize git: git init"
echo "2. Create virtual environment: python -m venv venv"
echo "3. Activate environment: source venv/bin/activate"
echo "4. Install development dependencies: pip install -e .[dev]"
