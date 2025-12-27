@echo off
REM Script para crear la distribución de VivasPlay
REM Genera un ejecutable único usando PyInstaller

echo ========================================
echo   Build de VivasPlay - Ejecutable
echo ========================================
echo.

REM Verificar si PyInstaller está instalado
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller no está instalado. Instalando...
    pip install pyinstaller
    if errorlevel 1 (
        echo ERROR: No se pudo instalar PyInstaller
        pause
        exit /b 1
    )
    echo PyInstaller instalado correctamente.
    echo.
)

REM Limpiar builds anteriores
if exist "build" (
    echo Limpiando builds anteriores...
    rmdir /s /q build
)
if exist "dist" (
    echo Limpiando distribuciones anteriores...
    rmdir /s /q dist
)

echo.
echo Compilando ejecutable...
echo.

REM Usar el archivo .spec si existe, sino usar comando directo
if exist "VivasPlay.spec" (
    pyinstaller VivasPlay.spec --clean
) else (
    echo Usando comando directo de PyInstaller...
    pyinstaller --onefile --name VivasPlay ^
        --add-data "src;src" ^
        --add-data "assets;assets" ^
        --hidden-import src ^
        --hidden-import src.app ^
        --hidden-import src.models.registro ^
        --hidden-import src.services.parser ^
        --hidden-import src.services.storage ^
        --noconsole ^
        VivasPlay.py --clean
)

if errorlevel 1 (
    echo.
    echo ERROR: La compilación falló
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Build completado exitosamente!
echo ========================================
echo.
echo El ejecutable se encuentra en: dist\VivasPlay.exe
echo.
echo Puedes copiar el archivo dist\VivasPlay.exe y entregarlo.
echo.
pause
