# TPMS Installation Script for Windows
# Проверяет зависимости и настраивает окружение

param(
    [switch]$SkipDocker,
    [switch]$SkipFrontend,
    [switch]$SkipBackend
)

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "TPMS Installation Script" -ForegroundColor Cyan
Write-Host "Telegram Publishing Management System" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Функция для проверки команды
function Test-Command {
    param([string]$Command)
    try {
        $null = Get-Command $Command -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

# Функция для проверки версии
function Get-Version {
    param([string]$Command, [string]$VersionArg = "--version")
    try {
        $output = & $Command $VersionArg 2>&1 | Select-Object -First 1
        return $output
    } catch {
        return $null
    }
}

# Функция для сравнения версий
function Compare-Version {
    param([string]$Current, [string]$Required)
    $currentVersion = [Version]$Current
    $requiredVersion = [Version]$Required
    return $currentVersion -ge $requiredVersion
}

$errors = @()
$warnings = @()

# Проверка Python
Write-Host "[1/6] Проверка Python..." -ForegroundColor Yellow
if (Test-Command "python") {
    $pythonVersion = (python --version) -replace "Python ", ""
    Write-Host "  ✓ Python найден: $pythonVersion" -ForegroundColor Green
    
    $versionMatch = $pythonVersion -match "(\d+)\.(\d+)\.(\d+)"
    if ($versionMatch) {
        $major = [int]$matches[1]
        $minor = [int]$matches[2]
        if ($major -ge 3 -and $minor -ge 11) {
            Write-Host "  ✓ Версия Python подходит (требуется 3.11+)" -ForegroundColor Green
        } else {
            $errors += "Python версия $pythonVersion не подходит. Требуется 3.11 или выше."
        }
    }
} else {
    $errors += "Python не найден. Установите Python 3.11+ с https://www.python.org/"
}

# Проверка pip
Write-Host "[2/6] Проверка pip..." -ForegroundColor Yellow
if (Test-Command "pip") {
    $pipVersion = (pip --version) -split " " | Select-Object -Index 1
    Write-Host "  ✓ pip найден: $pipVersion" -ForegroundColor Green
} else {
    $errors += "pip не найден. Установите pip вместе с Python."
}

# Проверка Node.js
Write-Host "[3/6] Проверка Node.js..." -ForegroundColor Yellow
if (Test-Command "node") {
    $nodeVersion = (node --version) -replace "v", ""
    Write-Host "  ✓ Node.js найден: $nodeVersion" -ForegroundColor Green
    
    $versionMatch = $nodeVersion -match "(\d+)\.(\d+)\.(\d+)"
    if ($versionMatch) {
        $major = [int]$matches[1]
        if ($major -ge 18) {
            Write-Host "  ✓ Версия Node.js подходит (требуется 18+)" -ForegroundColor Green
        } else {
            $errors += "Node.js версия $nodeVersion не подходит. Требуется 18 или выше."
        }
    }
} else {
    if (-not $SkipFrontend) {
        $warnings += "Node.js не найден. Фронтенд не будет установлен."
    }
}

# Проверка npm
Write-Host "[4/6] Проверка npm..." -ForegroundColor Yellow
if (Test-Command "npm") {
    $npmVersion = (npm --version)
    Write-Host "  ✓ npm найден: $npmVersion" -ForegroundColor Green
} else {
    if (-not $SkipFrontend) {
        $warnings += "npm не найден. Фронтенд не будет установлен."
    }
}

# Проверка Docker
Write-Host "[5/6] Проверка Docker..." -ForegroundColor Yellow
if (-not $SkipDocker) {
    if (Test-Command "docker") {
        $dockerVersion = (docker --version) -replace "Docker version ", ""
        Write-Host "  ✓ Docker найден: $dockerVersion" -ForegroundColor Green
        
        # Проверка, что Docker запущен
        try {
            docker ps | Out-Null
            Write-Host "  ✓ Docker запущен" -ForegroundColor Green
        } catch {
            $warnings += "Docker установлен, но не запущен. Запустите Docker Desktop."
        }
    } else {
        $warnings += "Docker не найден. Установите Docker Desktop с https://www.docker.com/"
    }
    
    # Проверка Docker Compose
    if (Test-Command "docker-compose") {
        $composeVersion = (docker-compose --version) -replace "docker-compose version ", ""
        Write-Host "  ✓ Docker Compose найден: $composeVersion" -ForegroundColor Green
    } elseif (Test-Command "docker") {
        # Docker Compose может быть встроен в Docker
        try {
            docker compose version | Out-Null
            Write-Host "  ✓ Docker Compose (встроенный) найден" -ForegroundColor Green
        } catch {
            $warnings += "Docker Compose не найден."
        }
    }
} else {
    Write-Host "  ⊘ Проверка Docker пропущена" -ForegroundColor Gray
}

# Проверка Git
Write-Host "[6/6] Проверка Git..." -ForegroundColor Yellow
if (Test-Command "git") {
    $gitVersion = (git --version) -replace "git version ", ""
    Write-Host "  ✓ Git найден: $gitVersion" -ForegroundColor Green
} else {
    $warnings += "Git не найден. Рекомендуется установить Git."
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Результаты проверки" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

if ($errors.Count -gt 0) {
    Write-Host ""
    Write-Host "ОШИБКИ:" -ForegroundColor Red
    foreach ($error in $errors) {
        Write-Host "  ✗ $error" -ForegroundColor Red
    }
    Write-Host ""
    Write-Host "Установка не может быть продолжена. Исправьте ошибки и запустите скрипт снова." -ForegroundColor Red
    exit 1
}

if ($warnings.Count -gt 0) {
    Write-Host ""
    Write-Host "ПРЕДУПРЕЖДЕНИЯ:" -ForegroundColor Yellow
    foreach ($warning in $warnings) {
        Write-Host "  ⚠ $warning" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "✓ Все основные зависимости проверены!" -ForegroundColor Green
Write-Host ""

# Создание .env файлов
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Настройка окружения" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Backend .env
if (-not $SkipBackend) {
    $backendEnvPath = "tpms-backend\.env"
    if (-not (Test-Path $backendEnvPath)) {
        Write-Host "Создание .env файла для backend..." -ForegroundColor Yellow
        $backendEnvContent = @"
# Database
DATABASE_URL=postgresql://tpms:tpms_password@localhost:5432/tpms_db
POSTGRES_SERVER=localhost
POSTGRES_USER=tpms
POSTGRES_PASSWORD=tpms_password
POSTGRES_DB=tpms_db

# Redis
REDIS_URL=redis://localhost:6379/0
REDIS_SERVER=localhost
REDIS_PORT=6379
REDIS_DB=0

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key-here-change-in-production-$(Get-Random -Minimum 1000 -Maximum 9999)
ENCRYPTION_KEY=your-encryption-key-32-chars!!$(Get-Random -Minimum 1000 -Maximum 9999)

# Telegram
TELEGRAM_BOT_TOKEN=
TELEGRAM_API_ID=
TELEGRAM_API_HASH=

# Application
DEBUG=true
PROJECT_NAME=TPMS
VERSION=1.3.0

# Allowed Origins (comma-separated)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080

# Allowed Hosts (comma-separated)
ALLOWED_HOSTS=localhost,127.0.0.1

# File Uploads
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=52428800

# Pagination
DEFAULT_PAGE_SIZE=25
MAX_PAGE_SIZE=100

# Rate Limiting
RATE_LIMIT_PER_MINUTE=300

# Monitoring
PROMETHEUS_ENABLED=true
"@
        Set-Content -Path $backendEnvPath -Value $backendEnvContent
        Write-Host "  ✓ Создан $backendEnvPath" -ForegroundColor Green
        Write-Host "  ⚠ ВАЖНО: Измените SECRET_KEY и ENCRYPTION_KEY в production!" -ForegroundColor Yellow
    } else {
        Write-Host "  ⊘ .env файл уже существует: $backendEnvPath" -ForegroundColor Gray
    }
}

# Frontend .env
if (-not $SkipFrontend -and (Test-Command "node")) {
    $frontendEnvPath = "tpms-frontend\.env"
    if (-not (Test-Path $frontendEnvPath)) {
        Write-Host "Создание .env файла для frontend..." -ForegroundColor Yellow
        $frontendEnvContent = @"
VITE_API_BASE_URL=http://localhost:8000/api/v1
"@
        Set-Content -Path $frontendEnvPath -Value $frontendEnvContent
        Write-Host "  ✓ Создан $frontendEnvPath" -ForegroundColor Green
    } else {
        Write-Host "  ⊘ .env файл уже существует: $frontendEnvPath" -ForegroundColor Gray
    }
}

Write-Host ""

# Установка зависимостей
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Установка зависимостей" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Backend зависимости
if (-not $SkipBackend) {
    Write-Host "Установка Python зависимостей..." -ForegroundColor Yellow
    Set-Location "tpms-backend"
    try {
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        Write-Host "  ✓ Python зависимости установлены" -ForegroundColor Green
    } catch {
        Write-Host "  ✗ Ошибка при установке Python зависимостей: $_" -ForegroundColor Red
    }
    Set-Location ".."
    Write-Host ""
}

# Frontend зависимости
if (-not $SkipFrontend -and (Test-Command "npm")) {
    Write-Host "Установка Node.js зависимостей..." -ForegroundColor Yellow
    Set-Location "tpms-frontend"
    try {
        npm install
        Write-Host "  ✓ Node.js зависимости установлены" -ForegroundColor Green
    } catch {
        Write-Host "  ✗ Ошибка при установке Node.js зависимостей: $_" -ForegroundColor Red
    }
    Set-Location ".."
    Write-Host ""
}

# Создание необходимых директорий
Write-Host "Создание необходимых директорий..." -ForegroundColor Yellow
$directories = @(
    "tpms-backend\uploads",
    "tpms-backend\logs"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "  ✓ Создана директория: $dir" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Установка завершена!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Следующие шаги:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Настройте .env файлы (особенно SECRET_KEY и ENCRYPTION_KEY)" -ForegroundColor White
Write-Host ""
Write-Host "2. Для запуска с Docker:" -ForegroundColor White
Write-Host "   cd tpms-backend" -ForegroundColor Gray
Write-Host "   docker-compose up -d" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Для локальной разработки:" -ForegroundColor White
Write-Host "   Backend:  cd tpms-backend && make dev" -ForegroundColor Gray
Write-Host "   Frontend: cd tpms-frontend && npm run dev" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Откройте в браузере:" -ForegroundColor White
Write-Host "   Backend API:  http://localhost:8000/docs" -ForegroundColor Gray
Write-Host "   Frontend:     http://localhost:3000" -ForegroundColor Gray
Write-Host ""



