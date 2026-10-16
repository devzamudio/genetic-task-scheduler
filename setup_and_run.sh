#!/bin/bash

# ==============================================================================
# Script de Instalación y Ejecución - Genetic Task Scheduler
# Compatible con Linux y macOS
# ==============================================================================

set -e  # Salir inmediatamente si hay un error

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

# ==============================================================================
# VALIDACIÓN DE DEPENDENCIAS DEL SISTEMA
# ==============================================================================
print_header "VALIDANDO DEPENDENCIAS DEL SISTEMA"

# Verificar Docker
if command_exists docker; then
    print_success "Docker está instalado: $(docker --version)"
else
    print_error "Docker no está instalado"
    echo "Por favor instale Docker desde: https://docs.docker.com/get-docker/"
    exit 1
fi

# Verificar Docker Compose
if docker compose version >/dev/null 2>&1; then
    print_success "Docker Compose está disponible: $(docker compose version --short)"
else
    print_error "Docker Compose no está disponible"
    exit 1
fi

# Verificar Node.js
if command_exists node; then
    NODE_VERSION=$(node --version)
    print_success "Node.js está instalado: $NODE_VERSION"
else
    print_error "Node.js no está instalado"
    echo "Por favor instale Node.js desde: https://nodejs.org/"
    exit 1
fi

# Verificar npm
if command_exists npm; then
    print_success "npm está instalado: $(npm --version)"
else
    print_error "npm no está instalado"
    exit 1
fi

# Verificar Python (opcional, para scripts de prueba)
if command_exists python3; then
    print_success "Python está instalado: $(python3 --version)"
else
    print_warning "Python no está instalado (opcional para scripts de prueba)"
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