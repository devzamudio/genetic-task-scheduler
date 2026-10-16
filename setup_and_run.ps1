# ==============================================================================
# Script de Instalación y Ejecución - Genetic Task Scheduler
# Compatible con Windows (PowerShell)
# ==============================================================================

# Configuración de colores
$ColorSuccess = "Green"
$ColorError = "Red"
$ColorWarning = "Yellow"
$ColorInfo = "Cyan"

# Funciones de utilidad
function Write-Header {
    param([string]$Message)
    Write-Host "`n========================================" -ForegroundColor $ColorInfo
    Write-Host "  $Message" -ForegroundColor $ColorInfo
    Write-Host "========================================`n" -ForegroundColor $ColorInfo
}

function Write-Success {
    param([string]$Message)
    Write-Host "✓ $Message" -ForegroundColor $ColorSuccess
}

function Write-Error {
    param([string]$Message)
    Write-Host " $Message" -ForegroundColor $ColorError
}

function Write-Warning {
    param([string]$Message)
    Write-Host "⚠ $Message" -ForegroundColor $ColorWarning
}

function Write-Info {
    param([string]$Message)
    Write-Host "ℹ $Message" -ForegroundColor $ColorInfo
}

# ==============================================================================
# VALIDACIÓN DE DEPENDENCIAS DEL SISTEMA
# ==============================================================================
Write-Header "VALIDANDO DEPENDENCIAS DEL SISTEMA"

# Verificar Docker
try {
    $dockerVersion = docker --version
    Write-Success "Docker está instalado: $dockerVersion"
} catch {
    Write-Error "Docker no está instalado"
    Write-Host "Por favor instale Docker Desktop desde: https://docs.docker.com/desktop/install/windows-install/"
    exit 1
}

# Verificar Docker Compose
try {
    $composeVersion = docker compose version --short
    Write-Success "Docker Compose está disponible: $composeVersion"
} catch {
    Write-Error "Docker Compose no está disponible"
    exit 1
}

# Verificar Node.js
try {
    $nodeVersion = node --version
    Write-Success "Node.js está instalado: $nodeVersion"
} catch {
    Write-Error "Node.js no está instalado"
    Write-Host "Por favor instale Node.js desde: https://nodejs.org/"
    exit 1
}

# Verificar npm
try {
    $npmVersion = npm --version
    Write-Success "npm está instalado: $npmVersion"
} catch {
    Write-Error "npm no está instalado"
    exit 1
}

# Verificar Python (opcional)
try {
    $pythonVersion = python --version
    Write-Success "Python está instalado: $pythonVersion"
} catch {
    Write-Warning "Python no está instalado (opcional para scripts de prueba)"
}

# ==============================================================================
# DETECTAR DIRECTORIO DEL PROYECTO
# ==============================================================================
$ProjectRoot = $PSScriptRoot
$BackendDir = Join-Path $ProjectRoot "backend"
$FrontendDir = Join-Path $ProjectRoot "frontend"

Write-Header "DIRECTORIO DEL PROYECTO"
Write-Host "Ruta raíz: $ProjectRoot"
Write-Host "Backend: $BackendDir"
Write-Host "Frontend: $FrontendDir"

# Verificar que existan los directorios
if (-not (Test-Path $BackendDir)) {
    Write-Error "Directorio backend no encontrado: $BackendDir"
    exit 1
}

if (-not (Test-Path $FrontendDir)) {
    Write-Error "Directorio frontend no encontrado: $FrontendDir"
    exit 1
}

# ==============================================================================
# CONFIGURACIÓN DEL BACKEND
# ==============================================================================
Write-Header "CONFIGURANDO BACKEND"

# Verificar archivo .env
$envFile = Join-Path $BackendDir ".env"
$envExampleFile = Join-Path $BackendDir ".env.example"

if (-not (Test-Path $envFile)) {
    Write-Warning "Archivo .env no encontrado, creando desde .env.example..."
    if (Test-Path $envExampleFile) {
        Copy-Item $envExampleFile $envFile
        Write-Success "Archivo .env creado"
    } else {
        Write-Error "No se encontró .env.example para crear .env"
        exit 1
    }
} else {
    Write-Success "Archivo .env ya existe"
}

# ==============================================================================
# LEVANTAR SERVICIOS DEL BACKEND (Docker)
# ==============================================================================
Write-Header "LEVANTANDO SERVICIOS DEL BACKEND"

Set-Location $BackendDir

Write-Info "Construyendo y levantando contenedores Docker..."
docker compose up --build -d

Write-Success "Contenedores Docker levantados"

# Esperar a que los servicios estén saludables
Write-Info "Esperando a que los servicios estén listos..."
Start-Sleep -Seconds 5

# Verificar estado de los contenedores
Write-Info "Estado de los contenedores:"
docker compose ps

# ==============================================================================
# CONFIGURACIÓN DEL FRONTEND
# ==============================================================================
Write-Header "CONFIGURANDO FRONTEND"

Set-Location $FrontendDir

# Verificar si node_modules existe
$nodeModulesPath = Join-Path $FrontendDir "node_modules"
if (-not (Test-Path $nodeModulesPath)) {
    Write-Info "Instalando dependencias del frontend..."
    npm install
    Write-Success "Dependencias del frontend instaladas"
} else {
    Write-Success "Dependencias del frontend ya están instaladas"
}

# ==============================================================================
# INICIAR FRONTEND
# ==============================================================================
Write-Header "INICIANDO FRONTEND"

Write-Info "Iniciando servidor de desarrollo de Vite..."
Write-Info "La aplicación estará disponible en: http://localhost:5173"
Write-Info "Presione Ctrl+C para detener todos los servicios"

# Iniciar frontend en una nueva ventana de PowerShell
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$FrontendDir'; npm run dev"

# ==============================================================================
# MENSAJE FINAL
# ==============================================================================
Write-Header "SISTEMA INICIADO CORRECTAMENTE"

Write-Host "✓ Backend (API Flask): http://localhost:5000/api/v1" -ForegroundColor $ColorSuccess
Write-Host "✓ Frontend (React):    http://localhost:5173" -ForegroundColor $ColorSuccess
Write-Host "✓ MongoDB:             localhost:27017" -ForegroundColor $ColorSuccess
Write-Host "✓ Redis:               localhost:6379" -ForegroundColor $ColorSuccess
Write-Host ""
Write-Host "Para detener todos los servicios:" -ForegroundColor $ColorWarning
Write-Host "  1. Cierre la ventana de PowerShell del frontend"
Write-Host "  2. Ejecute: cd '$BackendDir'; docker compose down"
Write-Host ""
Write-Host "Logs del backend: cd '$BackendDir'; docker compose logs -f" -ForegroundColor $ColorInfo
Write-Host ""

# Mantener el script corriendo
Write-Info "Presione cualquier tecla para continuar..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")