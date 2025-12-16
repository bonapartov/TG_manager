#!/bin/bash

# TPMS Installation Script for Linux/Mac
# Проверяет зависимости и настраивает окружение

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Флаги
SKIP_DOCKER=false
SKIP_FRONTEND=false
SKIP_BACKEND=false

# Парсинг аргументов
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-docker)
            SKIP_DOCKER=true
            shift
            ;;
        --skip-frontend)
            SKIP_FRONTEND=true
            shift
            ;;
        --skip-backend)
            SKIP_BACKEND=true
            shift
            ;;
        *)
            echo "Неизвестный аргумент: $1"
            exit 1
            ;;
    esac
done

echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}TPMS Installation Script${NC}"
echo -e "${CYAN}Telegram Publishing Management System${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""

# Функция для проверки команды
check_command() {
    if command -v "$1" &> /dev/null; then
        return 0
    else
        return 1
    fi
}

# Функция для получения версии
get_version() {
    local cmd=$1
    local version_arg=${2:-"--version"}
    if check_command "$cmd"; then
        $cmd $version_arg 2>&1 | head -n 1
    else
        echo ""
    fi
}

# Функция для сравнения версий
compare_version() {
    local current=$1
    local required=$2
    if [ "$(printf '%s\n' "$required" "$current" | sort -V | head -n1)" = "$required" ]; then
        return 0
    else
        return 1
    fi
}

ERRORS=()
WARNINGS=()

# Проверка Python
echo -e "${YELLOW}[1/6] Проверка Python...${NC}"
if check_command python3; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "  ${GREEN}✓ Python найден: $PYTHON_VERSION${NC}"
    
    if compare_version "$PYTHON_VERSION" "3.11.0"; then
        echo -e "  ${GREEN}✓ Версия Python подходит (требуется 3.11+)${NC}"
    else
        ERRORS+=("Python версия $PYTHON_VERSION не подходит. Требуется 3.11 или выше.")
    fi
elif check_command python; then
    PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
    echo -e "  ${GREEN}✓ Python найден: $PYTHON_VERSION${NC}"
    
    if compare_version "$PYTHON_VERSION" "3.11.0"; then
        echo -e "  ${GREEN}✓ Версия Python подходит (требуется 3.11+)${NC}"
    else
        ERRORS+=("Python версия $PYTHON_VERSION не подходит. Требуется 3.11 или выше.")
    fi
else
    ERRORS+=("Python не найден. Установите Python 3.11+ с https://www.python.org/")
fi

# Проверка pip
echo -e "${YELLOW}[2/6] Проверка pip...${NC}"
if check_command pip3; then
    PIP_VERSION=$(pip3 --version | awk '{print $2}')
    echo -e "  ${GREEN}✓ pip найден: $PIP_VERSION${NC}"
elif check_command pip; then
    PIP_VERSION=$(pip --version | awk '{print $2}')
    echo -e "  ${GREEN}✓ pip найден: $PIP_VERSION${NC}"
else
    ERRORS+=("pip не найден. Установите pip вместе с Python.")
fi

# Проверка Node.js
echo -e "${YELLOW}[3/6] Проверка Node.js...${NC}"
if check_command node; then
    NODE_VERSION=$(node --version | sed 's/v//')
    echo -e "  ${GREEN}✓ Node.js найден: $NODE_VERSION${NC}"
    
    if compare_version "$NODE_VERSION" "18.0.0"; then
        echo -e "  ${GREEN}✓ Версия Node.js подходит (требуется 18+)${NC}"
    else
        ERRORS+=("Node.js версия $NODE_VERSION не подходит. Требуется 18 или выше.")
    fi
else
    if [ "$SKIP_FRONTEND" = false ]; then
        WARNINGS+=("Node.js не найден. Фронтенд не будет установлен.")
    fi
fi

# Проверка npm
echo -e "${YELLOW}[4/6] Проверка npm...${NC}"
if check_command npm; then
    NPM_VERSION=$(npm --version)
    echo -e "  ${GREEN}✓ npm найден: $NPM_VERSION${NC}"
else
    if [ "$SKIP_FRONTEND" = false ]; then
        WARNINGS+=("npm не найден. Фронтенд не будет установлен.")
    fi
fi

# Проверка Docker
echo -e "${YELLOW}[5/6] Проверка Docker...${NC}"
if [ "$SKIP_DOCKER" = false ]; then
    if check_command docker; then
        DOCKER_VERSION=$(docker --version | awk '{print $3}' | sed 's/,//')
        echo -e "  ${GREEN}✓ Docker найден: $DOCKER_VERSION${NC}"
        
        # Проверка, что Docker запущен
        if docker ps &> /dev/null; then
            echo -e "  ${GREEN}✓ Docker запущен${NC}"
        else
            WARNINGS+=("Docker установлен, но не запущен. Запустите Docker daemon.")
        fi
    else
        WARNINGS+=("Docker не найден. Установите Docker с https://www.docker.com/")
    fi
    
    # Проверка Docker Compose
    if check_command docker-compose; then
        COMPOSE_VERSION=$(docker-compose --version | awk '{print $4}' | sed 's/,//')
        echo -e "  ${GREEN}✓ Docker Compose найден: $COMPOSE_VERSION${NC}"
    elif check_command docker; then
        # Docker Compose может быть встроен в Docker
        if docker compose version &> /dev/null; then
            echo -e "  ${GREEN}✓ Docker Compose (встроенный) найден${NC}"
        else
            WARNINGS+=("Docker Compose не найден.")
        fi
    fi
else
    echo -e "  ${NC}⊘ Проверка Docker пропущена${NC}"
fi

# Проверка Git
echo -e "${YELLOW}[6/6] Проверка Git...${NC}"
if check_command git; then
    GIT_VERSION=$(git --version | awk '{print $3}')
    echo -e "  ${GREEN}✓ Git найден: $GIT_VERSION${NC}"
else
    WARNINGS+=("Git не найден. Рекомендуется установить Git.")
fi

echo ""
echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}Результаты проверки${NC}"
echo -e "${CYAN}========================================${NC}"

if [ ${#ERRORS[@]} -gt 0 ]; then
    echo ""
    echo -e "${RED}ОШИБКИ:${NC}"
    for error in "${ERRORS[@]}"; do
        echo -e "  ${RED}✗ $error${NC}"
    done
    echo ""
    echo -e "${RED}Установка не может быть продолжена. Исправьте ошибки и запустите скрипт снова.${NC}"
    exit 1
fi

if [ ${#WARNINGS[@]} -gt 0 ]; then
    echo ""
    echo -e "${YELLOW}ПРЕДУПРЕЖДЕНИЯ:${NC}"
    for warning in "${WARNINGS[@]}"; do
        echo -e "  ${YELLOW}⚠ $warning${NC}"
    done
fi

echo ""
echo -e "${GREEN}✓ Все основные зависимости проверены!${NC}"
echo ""

# Создание .env файлов
echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}Настройка окружения${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""

# Backend .env
if [ "$SKIP_BACKEND" = false ]; then
    BACKEND_ENV_PATH="tpms-backend/.env"
    if [ ! -f "$BACKEND_ENV_PATH" ]; then
        echo -e "${YELLOW}Создание .env файла для backend...${NC}"
        cat > "$BACKEND_ENV_PATH" << 'EOF'
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
SECRET_KEY=your-secret-key-here-change-in-production
ENCRYPTION_KEY=your-encryption-key-32-chars!!

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
EOF
        # Генерируем случайные ключи
        SECRET_KEY=$(openssl rand -hex 32 2>/dev/null || cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 64 | head -n 1)
        ENCRYPTION_KEY=$(openssl rand -hex 16 2>/dev/null || cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)
        
        # Заменяем ключи в файле
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            sed -i '' "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" "$BACKEND_ENV_PATH"
            sed -i '' "s/ENCRYPTION_KEY=.*/ENCRYPTION_KEY=$ENCRYPTION_KEY/" "$BACKEND_ENV_PATH"
        else
            # Linux
            sed -i "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" "$BACKEND_ENV_PATH"
            sed -i "s/ENCRYPTION_KEY=.*/ENCRYPTION_KEY=$ENCRYPTION_KEY/" "$BACKEND_ENV_PATH"
        fi
        
        echo -e "  ${GREEN}✓ Создан $BACKEND_ENV_PATH${NC}"
        echo -e "  ${YELLOW}⚠ ВАЖНО: Измените SECRET_KEY и ENCRYPTION_KEY в production!${NC}"
    else
        echo -e "  ${NC}⊘ .env файл уже существует: $BACKEND_ENV_PATH${NC}"
    fi
fi

# Frontend .env
if [ "$SKIP_FRONTEND" = false ] && check_command node; then
    FRONTEND_ENV_PATH="tpms-frontend/.env"
    if [ ! -f "$FRONTEND_ENV_PATH" ]; then
        echo -e "${YELLOW}Создание .env файла для frontend...${NC}"
        cat > "$FRONTEND_ENV_PATH" << 'EOF'
VITE_API_BASE_URL=http://localhost:8000/api/v1
EOF
        echo -e "  ${GREEN}✓ Создан $FRONTEND_ENV_PATH${NC}"
    else
        echo -e "  ${NC}⊘ .env файл уже существует: $FRONTEND_ENV_PATH${NC}"
    fi
fi

echo ""

# Установка зависимостей
echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}Установка зависимостей${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""

# Backend зависимости
if [ "$SKIP_BACKEND" = false ]; then
    echo -e "${YELLOW}Установка Python зависимостей...${NC}"
    cd tpms-backend
    
    # Определяем команду Python
    if check_command python3; then
        PYTHON_CMD="python3"
        PIP_CMD="pip3"
    else
        PYTHON_CMD="python"
        PIP_CMD="pip"
    fi
    
    $PIP_CMD install --upgrade pip
    $PIP_CMD install -r requirements.txt
    echo -e "  ${GREEN}✓ Python зависимости установлены${NC}"
    cd ..
    echo ""
fi

# Frontend зависимости
if [ "$SKIP_FRONTEND" = false ] && check_command npm; then
    echo -e "${YELLOW}Установка Node.js зависимостей...${NC}"
    cd tpms-frontend
    npm install
    echo -e "  ${GREEN}✓ Node.js зависимости установлены${NC}"
    cd ..
    echo ""
fi

# Создание необходимых директорий
echo -e "${YELLOW}Создание необходимых директорий...${NC}"
mkdir -p tpms-backend/uploads
mkdir -p tpms-backend/logs
echo -e "  ${GREEN}✓ Директории созданы${NC}"

echo ""
echo -e "${CYAN}========================================${NC}"
echo -e "${GREEN}Установка завершена!${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""
echo -e "${YELLOW}Следующие шаги:${NC}"
echo ""
echo -e "1. Настройте .env файлы (особенно SECRET_KEY и ENCRYPTION_KEY)" | sed "s/^/  /"
echo ""
echo -e "2. Для запуска с Docker:" | sed "s/^/  /"
echo -e "   cd tpms-backend" | sed "s/^/  /"
echo -e "   docker-compose up -d" | sed "s/^/  /"
echo ""
echo -e "3. Для локальной разработки:" | sed "s/^/  /"
echo -e "   Backend:  cd tpms-backend && make dev" | sed "s/^/  /"
echo -e "   Frontend: cd tpms-frontend && npm run dev" | sed "s/^/  /"
echo ""
echo -e "4. Откройте в браузере:" | sed "s/^/  /"
echo -e "   Backend API:  http://localhost:8000/docs" | sed "s/^/  /"
echo -e "   Frontend:     http://localhost:3000" | sed "s/^/  /"
echo ""



