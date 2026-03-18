#!/usr/bin/env bash
# Bash bootstrap script for AIBE v2.0
# Usage: chmod +x setup.sh && ./setup.sh

set -euo pipefail

echo "═══════════════════════════════════════════════"
echo "  AIBE v2.0 — One-Command Setup"
echo "═══════════════════════════════════════════════"
echo ""

# 1. Check Python 3.12+
echo "[1/6] Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1)
if ! echo "$PYTHON_VERSION" | grep -qE "3\.1[2-9]"; then
    echo "  ERROR: Python 3.12+ required. Found: $PYTHON_VERSION"
    exit 1
fi
echo "  OK: $PYTHON_VERSION"

# 2. Install uv if not present
echo "[2/6] Installing uv package manager..."
if ! command -v uv &> /dev/null; then
    pip install uv
    echo "  OK: uv installed"
else
    echo "  OK: uv already installed"
fi

# 3. Install dependencies
echo "[3/6] Installing project dependencies..."
uv pip install --system -e ".[dev,security]"
echo "  OK: Dependencies installed"

# 4. Copy .env
echo "[4/6] Setting up environment file..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "  OK: .env created from .env.example"
    echo "  ACTION REQUIRED: Edit .env with your API keys"
else
    echo "  OK: .env already exists"
fi

# 5. Install pre-commit hooks
echo "[5/6] Installing pre-commit hooks..."
pre-commit install
echo "  OK: Pre-commit hooks installed"

# 6. Verify
echo "[6/6] Verifying setup..."
python3 -c "import aibe; print(f'  OK: aibe v{aibe.__version__} importable')"

echo ""
echo "═══════════════════════════════════════════════"
echo "  Setup complete!"
echo "═══════════════════════════════════════════════"
echo ""
echo "Next steps:"
echo "  1. Edit .env with your API keys"
echo "  2. Run 'docker compose up -d' to start infrastructure"
echo "  3. Run 'make migrate' to run database migrations"
echo "  4. Run 'make launch' to start the system"
echo ""
