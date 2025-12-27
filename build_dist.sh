#!/bin/bash
# Script para crear la distribución de VivasPlay
# Genera un ejecutable único usando PyInstaller

echo "========================================"
echo "  Build de VivasPlay - Ejecutable"
echo "========================================"
echo ""

# Verificar si PyInstaller está instalado
if ! python -c "import PyInstaller" 2>/dev/null; then
    echo "PyInstaller no está instalado. Instalando..."
    pip install pyinstaller
    if [ $? -ne 0 ]; then
        echo "ERROR: No se pudo instalar PyInstaller"
        exit 1
    fi
    echo "PyInstaller instalado correctamente."
    echo ""
fi

# Limpiar builds anteriores
if [ -d "build" ]; then
    echo "Limpiando builds anteriores..."
    rm -rf build
fi

if [ -d "dist" ]; then
    echo "Limpiando distribuciones anteriores..."
    rm -rf dist
fi

echo ""
echo "Compilando ejecutable..."
echo ""

# Usar el archivo .spec si existe, sino usar comando directo
if [ -f "VivasPlay.spec" ]; then
    pyinstaller VivasPlay.spec --clean
else
    echo "Usando comando directo de PyInstaller..."
    pyinstaller --onefile --name VivasPlay \
        --add-data "src:src" \
        --add-data "assets:assets" \
        --hidden-import src \
        --hidden-import src.app \
        --hidden-import src.models.registro \
        --hidden-import src.services.parser \
        --hidden-import src.services.storage \
        --noconsole \
        VivasPlay.py --clean
fi

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: La compilación falló"
    exit 1
fi

echo ""
echo "========================================"
echo "  Build completado exitosamente!"
echo "========================================"
echo ""
echo "El ejecutable se encuentra en: dist/VivasPlay"
echo ""
echo "Puedes copiar el archivo dist/VivasPlay y entregarlo."
echo ""
