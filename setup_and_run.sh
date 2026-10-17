#!/bin/bash

# ==============================================================================
# Script de Instalación y Ejecución - Genetic Task Scheduler
# Compatible con Linux y macOS
# ==============================================================================

set -euo pipefail

AUTO_INSTALL_DEPS=false

# Permitir instalación automática de dependencias faltantes
if [[ $# -gt 0 ]]; then
    case "$1" in
        --install-deps)
            AUTO_INSTALL_DEPS=true
            ;;
        --help|-h)
            echo "Uso: $0 [--install-deps]"
            echo "  --install-deps   intenta instalar dependencias faltantes según la distro"
            exit 0
            ;;
        *)
            echo "Opción desconocida: $1"
            echo "Uso: $0 [--install-deps]"
            exit 1
            ;;
    esac
fi

# Colores para la terminal
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funciones de utilidad
print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Verificar si un comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

get_sudo_prefix() {
    if [[ "$EUID" -eq 0 ]]; then
        echo ""
    else
        echo "sudo"
    fi
}

get_linux_distro() {
    if [[ -f /etc/os-release ]]; then
        . /etc/os-release
        echo "${ID:-unknown}"
    else
        echo "unknown"
    fi
}

install_missing_dependencies() {
    OS_NAME="$(uname -s)"

    if [[ "$OS_NAME" != "Linux" ]]; then
        print_warning "Detección automática de dependencias solo está disponible en Linux."
        print_info "En macOS se recomienda instalar Docker Desktop y Node.js desde sus instaladores oficiales."
        return 0
    fi

    DISTRO="$(get_linux_distro)"
    SUDO_PREFIX="$(get_sudo_prefix)"

    print_header "INSTALANDO DEPENDENCIAS FALTANTES"
    echo "Distribución detectada: ${DISTRO}"

    case "$DISTRO" in
        ubuntu|debian|pop|linuxmint|raspbian)
            if [[ -n "$SUDO_PREFIX" ]]; then
                $SUDO_PREFIX apt-get update
                $SUDO_PREFIX DEBIAN_FRONTEND=noninteractive apt-get install -y ca-certificates curl gnupg docker.io docker-compose-plugin nodejs npm python3
            else
                apt-get update
                DEBIAN_FRONTEND=noninteractive apt-get install -y ca-certificates curl gnupg docker.io docker-compose-plugin nodejs npm python3
            fi
            ;;
        fedora|rhel|centos|rocky|almalinux)
            if [[ -n "$SUDO_PREFIX" ]]; then
                $SUDO_PREFIX dnf install -y docker docker-compose-plugin nodejs npm python3
            else
                dnf install -y docker docker-compose-plugin nodejs npm python3
            fi
            ;;
        arch|manjaro)
            if [[ -n "$SUDO_PREFIX" ]]; then
                $SUDO_PREFIX pacman -Sy --noconfirm docker nodejs npm python
            else
                pacman -Sy --noconfirm docker nodejs npm python
            fi
            ;;
        opensuse|opensuse-leap|opensuse-tumbleweed|sles)
            if [[ -n "$SUDO_PREFIX" ]]; then
                $SUDO_PREFIX zypper install -y docker docker-compose nodejs npm python3
            else
                zypper install -y docker docker-compose nodejs npm python3
            fi
            ;;
        alpine)
            if [[ -n "$SUDO_PREFIX" ]]; then
                $SUDO_PREFIX apk add --no-cache docker docker-compose nodejs npm python3
            else
                apk add --no-cache docker docker-compose nodejs npm python3
            fi
            ;;
        *)
            print_error "Distribución no soportada para instalación automática: ${DISTRO}"
            print_info "Instala manualmente Docker, Docker Compose, Node.js, npm y Python 3."
            return 1
            ;;
    esac

    if command_exists systemctl; then
        if [[ -n "$SUDO_PREFIX" ]]; then
            $SUDO_PREFIX systemctl enable --now docker || true
        else
            systemctl enable --now docker || true
        fi
    fi

    print_success "Intento de instalación finalizado. Verifica que el daemon de Docker esté corriendo."
}

check_docker_access() {
    if ! command_exists docker; then
        print_error "Docker no está instalado"
        echo "Instálalo desde: https://docs.docker.com/get-docker/"
        if [[ "$AUTO_INSTALL_DEPS" == true ]]; then
            install_missing_dependencies || true
        fi
        return 1
    fi

    if ! docker info >/dev/null 2>&1; then
        print_error "Docker no está accesible para este usuario"
        print_info "Causas comunes:"
        echo "  - El servicio de Docker no está iniciado"
        echo "  - Tu usuario no pertenece al grupo docker"
        echo "  - El socket de Docker no tiene permisos"
        echo ""

        if [[ "$(uname -s)" == "Linux" ]]; then
            if ! id -nG "$USER" | grep -qw docker; then
                echo "Solución recomendada:"
                echo "  sudo groupadd -f docker"
                echo "  sudo usermod -aG docker \"\$USER\""
                echo "  newgrp docker"
            fi
            if command_exists systemctl; then
                echo "  sudo systemctl enable --now docker"
            fi
        fi

        return 1
    fi

    return 0
}

check_program() {
    local prog="$1"
    local url="$2"
    local required="$3"

    if command_exists "$prog"; then
        return 0
    fi

    print_error "$required no está instalado"
    echo "Instálalo desde: $url"

    if [[ "$AUTO_INSTALL_DEPS" == true ]]; then
        install_missing_dependencies || true
    fi

    return 1
}

# ==============================================================================
# VALIDACIÓN DE DEPENDENCIAS DEL SISTEMA
# ==============================================================================
print_header "VALIDANDO DEPENDENCIAS DEL SISTEMA"

if [[ "$AUTO_INSTALL_DEPS" == true ]]; then
    print_info "Se intentará instalar automáticamente las dependencias faltantes."
fi

# Verificar Docker
if ! check_docker_access; then
    exit 1
fi
print_success "Docker está accesible: $(docker --version)"

# Verificar Docker Compose
if docker compose version >/dev/null 2>&1; then
    print_success "Docker Compose está disponible: $(docker compose version --short)"
else
    print_error "Docker Compose no está disponible"
    if [[ "$AUTO_INSTALL_DEPS" == true ]]; then
        install_missing_dependencies || true
    fi
    exit 1
fi

# Verificar Node.js
if ! check_program node "https://nodejs.org/" "Node.js"; then
    exit 1
fi
print_success "Node.js está instalado: $(node --version)"

# Verificar npm
if ! check_program npm "https://www.npmjs.com/" "npm"; then
    exit 1
fi
print_success "npm está instalado: $(npm --version)"

# Verificar Python (opcional, para scripts de prueba)
if command_exists python3; then
    print_success "Python está instalado: $(python3 --version)"
else
    print_warning "Python no está instalado (opcional para scripts de prueba)"
    if [[ "$AUTO_INSTALL_DEPS" == true ]]; then
        install_missing_dependencies || true
    fi
fi

# ==============================================================================
# DETECTAR DIRECTORIO DEL PROYECTO
# ==============================================================================
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$PROJECT_ROOT/backend"
FRONTEND_DIR="$PROJECT_ROOT/frontend"

print_header "DIRECTORIO DEL PROYECTO"
echo "Ruta raíz: $PROJECT_ROOT"
echo "Backend: $BACKEND_DIR"
echo "Frontend: $FRONTEND_DIR"

# Verificar que existan los directorios
if [ ! -d "$BACKEND_DIR" ]; then
    print_error "Directorio backend no encontrado: $BACKEND_DIR"
    exit 1
fi

if [ ! -d "$FRONTEND_DIR" ]; then
    print_error "Directorio frontend no encontrado: $FRONTEND_DIR"
    exit 1
fi

# ==============================================================================
# CONFIGURACIÓN DEL BACKEND
# ==============================================================================
print_header "CONFIGURANDO BACKEND"

# Verificar archivo .env
if [ ! -f "$BACKEND_DIR/.env" ]; then
    print_warning "Archivo .env no encontrado, creando desde .env.example..."
    if [ -f "$BACKEND_DIR/.env.example" ]; then
        cp "$BACKEND_DIR/.env.example" "$BACKEND_DIR/.env"
        print_success "Archivo .env creado"
    else
        print_error "No se encontró .env.example para crear .env"
        exit 1
    fi
else
    print_success "Archivo .env ya existe"
fi

# ==============================================================================
# LEVANTAR SERVICIOS DEL BACKEND (Docker)
# ==============================================================================
print_header "LEVANTANDO SERVICIOS DEL BACKEND"

cd "$BACKEND_DIR"

print_info "Construyendo y levantando contenedores Docker..."
docker compose up --build -d

print_success "Contenedores Docker levantados"

# Esperar a que los servicios estén saludables
print_info "Esperando a que los servicios estén listos..."
sleep 5

# Verificar estado de los contenedores
print_info "Estado de los contenedores:"
docker compose ps

# ==============================================================================
# CONFIGURACIÓN DEL FRONTEND
# ==============================================================================
print_header "CONFIGURANDO FRONTEND"

cd "$FRONTEND_DIR"

# Verificar si node_modules existe
if [ ! -d "node_modules" ]; then
    print_info "Instalando dependencias del frontend..."
    npm install
    print_success "Dependencias del frontend instaladas"
else
    print_success "Dependencias del frontend ya están instaladas"
fi

# ==============================================================================
# INICIAR FRONTEND
# ==============================================================================
print_header "INICIANDO FRONTEND"

print_info "Iniciando servidor de desarrollo de Vite..."
print_info "La aplicación estará disponible en: http://localhost:5173"
print_info "Presione Ctrl+C para detener todos los servicios"

# Iniciar frontend en segundo plano y guardar PID
npm run dev &
FRONTEND_PID=$!

# ==============================================================================
# MENSAJE FINAL
# ==============================================================================
print_header "SISTEMA INICIADO CORRECTAMENTE"

echo -e "${GREEN}✓ Backend (API Flask):${NC} http://localhost:5000/api/v1"
echo -e "${GREEN}✓ Frontend (React):${NC}    http://localhost:5173"
echo -e "${GREEN}✓ MongoDB:${NC}             localhost:27017"
echo -e "${GREEN}✓ Redis:${NC}               localhost:6379"
echo ""
echo -e "${YELLOW}Para detener todos los servicios:${NC}"
echo "  1. Presione Ctrl+C en esta terminal"
echo "  2. Ejecute: cd $BACKEND_DIR && docker compose down"
echo ""
echo -e "${BLUE}Logs del backend:${NC} cd $BACKEND_DIR && docker compose logs -f"
echo ""

# Mantener el script corriendo
wait $FRONTEND_PID