# PowerShell bootstrap script for AIBE v2.0
# Usage: .\setup.ps1

$ErrorActionPreference = "Stop"

Write-Host "═══════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  AIBE v2.0 — One-Command Setup" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# 1. Check Python 3.12+
Write-Host "[1/6] Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($pythonVersion -notmatch "3\.1[2-9]") {
    Write-Host "  ERROR: Python 3.12+ required. Found: $pythonVersion" -ForegroundColor Red
    exit 1
}
Write-Host "  OK: $pythonVersion" -ForegroundColor Green

# 2. Install uv if not present
Write-Host "[2/6] Installing uv package manager..." -ForegroundColor Yellow
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    pip install uv
    Write-Host "  OK: uv installed" -ForegroundColor Green
} else {
    Write-Host "  OK: uv already installed" -ForegroundColor Green
}

# 3. Install dependencies
Write-Host "[3/6] Installing project dependencies..." -ForegroundColor Yellow
uv pip install --system -e ".[dev,security]"
Write-Host "  OK: Dependencies installed" -ForegroundColor Green

# 4. Copy .env
Write-Host "[4/6] Setting up environment file..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "  OK: .env created from .env.example" -ForegroundColor Green
    Write-Host "  ACTION REQUIRED: Edit .env with your API keys" -ForegroundColor Yellow
} else {
    Write-Host "  OK: .env already exists" -ForegroundColor Green
}

# 5. Install pre-commit hooks
Write-Host "[5/6] Installing pre-commit hooks..." -ForegroundColor Yellow
pre-commit install
Write-Host "  OK: Pre-commit hooks installed" -ForegroundColor Green

# 6. Verify
Write-Host "[6/6] Verifying setup..." -ForegroundColor Yellow
python -c "import aibe; print(f'  OK: aibe v{aibe.__version__} importable')"

Write-Host ""
Write-Host "═══════════════════════════════════════════════" -ForegroundColor Green
Write-Host "  Setup complete!" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Edit .env with your API keys"
Write-Host "  2. Run 'docker compose up -d' to start infrastructure"
Write-Host "  3. Run 'make migrate' to run database migrations"
Write-Host "  4. Run 'make launch' to start the system"
Write-Host ""
