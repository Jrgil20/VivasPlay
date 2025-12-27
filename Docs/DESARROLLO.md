# Guía de Desarrollo y Build

Esta guía detallada explica cómo ejecutar la aplicación en modo desarrollo y cómo construir el ejecutable para distribución.

## Tabla de Contenidos

- [Requisitos Previos](#requisitos-previos)
- [Ejecutar en Local](#ejecutar-en-local)
- [Build de la Aplicación](#build-de-la-aplicación)
  - [PyInstaller (Recomendado)](#pyinstaller-recomendado)
  - [cx_Freeze](#cx_freeze)
  - [py2exe](#py2exe)
- [Estructura de Archivos para Build](#estructura-de-archivos-para-build)
- [Solución de Problemas](#solución-de-problemas)

---

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3.7 o superior**
  - Verifica tu versión: `python --version` o `python3 --version`
  - Descarga desde: [python.org](https://www.python.org/downloads/)

- **pip** (gestor de paquetes de Python)
  - Normalmente viene incluido con Python
  - Verifica: `pip --version` o `pip3 --version`

- **Librerías estándar** (incluidas con Python):
  - `tkinter` - Interfaz gráfica
  - `json` - Manejo de datos
  - `re` - Expresiones regulares
  - `os` - Operaciones del sistema

---

## Ejecutar en Local

### Windows

1. **Abre PowerShell o CMD**
   - Presiona `Win + R`, escribe `cmd` o `powershell` y presiona Enter
   - O busca "PowerShell" o "Símbolo del sistema" en el menú de inicio

2. **Navega al directorio del proyecto**
   ```powershell
   cd ruta\a\VivasPlay
   ```
   Ejemplo:
   ```powershell
   cd D:\VivasPlay
   ```

3. **Ejecuta la aplicación**
   ```powershell
   python VivasPlay.py
   ```
   O si tienes múltiples versiones de Python:
   ```powershell
   python3 VivasPlay.py
   ```

### Linux / macOS

1. **Abre una terminal**
   - Linux: `Ctrl + Alt + T` o busca "Terminal"
   - macOS: `Cmd + Espacio`, escribe "Terminal"

2. **Navega al directorio del proyecto**
   ```bash
   cd /ruta/a/VivasPlay
   ```

3. **Ejecuta la aplicación**
   ```bash
   python3 VivasPlay.py
   ```
   O si `python` apunta a Python 3:
   ```bash
   python VivasPlay.py
   ```

### Verificar que Funciona

Si la aplicación se ejecuta correctamente, deberías ver:
- Una ventana gráfica con la interfaz de la aplicación
- La tabla de correos (inicialmente vacía o con datos de `correos.json` si existe)
- Los botones y controles funcionando correctamente

Si aparece un error, consulta la sección [Solución de Problemas](#solución-de-problemas).

---

## Build de la Aplicación

El proceso de "build" convierte el script de Python en un ejecutable independiente que puede ejecutarse sin necesidad de tener Python instalado.

### PyInstaller (Recomendado)

PyInstaller es la herramienta más popular y fácil de usar para crear ejecutables desde scripts de Python.

#### Instalación

```bash
pip install pyinstaller
```

O si usas `pip3`:
```bash
pip3 install pyinstaller
```

#### Build Básico

El comando más simple para crear un ejecutable:

```bash
pyinstaller --onefile --noconsole --name VivasPlay VivasPlay.py
```

**Parámetros explicados:**
- `--onefile`: Crea un único archivo ejecutable (más fácil de distribuir)
- `--noconsole`: Oculta la ventana de consola (solo muestra la interfaz gráfica)
- `--name VivasPlay`: Nombre del ejecutable resultante
- `VivasPlay.py`: Archivo fuente

#### Build con Icono

Si quieres agregar un icono personalizado:

```bash
pyinstaller --onefile --noconsole --name VivasPlay --icon=assets/image/mail_1849441.png VivasPlay.py
```

#### Ubicación del Ejecutable

Después del build, encontrarás:
- **Ejecutable**: `dist/VivasPlay.exe` (Windows) o `dist/VivasPlay` (Linux/macOS)
- **Archivos temporales**: `build/` (puedes eliminarlos después)

#### Copiar Assets

**IMPORTANTE**: Después de crear el ejecutable, debes copiar la carpeta `assets` al directorio `dist`:

**Windows:**
```powershell
xcopy /E /I assets dist\assets
```

**Linux/macOS:**
```bash
cp -r assets dist/assets
```

O manualmente:
1. Abre la carpeta `dist`
2. Crea una carpeta `assets` si no existe
3. Copia todo el contenido de `assets/image/` a `dist/assets/image/`

#### Build Completo con Todos los Archivos

Comando completo que incluye todo:

```bash
# 1. Crear el ejecutable
pyinstaller --onefile --noconsole --name VivasPlay --icon=assets/image/mail_1849441.png VivasPlay.py

# 2. Copiar assets (Windows)
xcopy /E /I assets dist\assets

# 2. Copiar assets (Linux/macOS)
cp -r assets dist/assets
```

#### Opciones Avanzadas de PyInstaller

Si necesitas más control, puedes crear un archivo de especificación:

```bash
pyinstaller --name VivasPlay VivasPlay.py
```

Esto crea `VivasPlay.spec` que puedes editar para personalizar el build.

Ejemplo de `VivasPlay.spec` personalizado:

```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['VivasPlay.py'],
    pathex=[],
    binaries=[],
    datas=[('assets', 'assets')],  # Incluye assets automáticamente
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='VivasPlay',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Sin consola
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/image/mail_1849441.png'
)
```

Luego ejecuta:
```bash
pyinstaller VivasPlay.spec
```

### cx_Freeze

cx_Freeze es otra opción para crear ejecutables multiplataforma.

#### Instalación

```bash
pip install cx_Freeze
```

#### Configuración

Crea un archivo `setup.py` en la raíz del proyecto:

```python
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["tkinter", "json", "re", "os"],
    "include_files": ["assets/"],
    "excludes": ["matplotlib", "numpy", "pandas"]
}

setup(
    name="VivasPlay",
    version="2.0",
    description="Gestión de correos electrónicos",
    options={"build_exe": build_exe_options},
    executables=[Executable("VivasPlay.py", 
                           base="Win32GUI" if sys.platform == "win32" else None,
                           icon="assets/image/mail_1849441.png")]
)
```

#### Build

```bash
python setup.py build
```

El ejecutable estará en `build/exe.*/VivasPlay.exe` (o `VivasPlay` en Linux/macOS).

### py2exe

py2exe es específico para Windows.

#### Instalación

```bash
pip install py2exe
```

#### Configuración

Crea un archivo `setup.py`:

```python
from distutils.core import setup
import py2exe

setup(
    windows=[{
        'script': 'VivasPlay.py',
        'icon_resources': [(1, 'assets/image/mail_1849441.png')]
    }],
    options={
        'py2exe': {
            'packages': ['tkinter'],
            'includes': ['json', 're', 'os']
        }
    },
    data_files=[('assets/image', ['assets/image/clip_2891632.png',
                                  'assets/image/file_5632095.png',
                                  'assets/image/mail_1849441.png',
                                  'assets/image/remove_13922476.png'])]
)
```

#### Build

```bash
python setup.py py2exe
```

El ejecutable estará en `dist/VivasPlay.exe`.

---

## Estructura de Archivos para Build

Después de un build exitoso, la estructura debería verse así:

```
dist/
├── VivasPlay.exe          # Ejecutable (Windows)
│   o VivasPlay            # Ejecutable (Linux/macOS)
└── assets/
    └── image/
        ├── clip_2891632.png
        ├── file_5632095.png
        ├── mail_1849441.png
        └── remove_13922476.png
```

**Nota**: Si usas `--onefile` en PyInstaller, el ejecutable será un único archivo, pero aún necesitas los assets en la misma carpeta o en una subcarpeta `assets/`.

---

## Solución de Problemas

### Error: "python no se reconoce como comando"

**Problema**: Python no está en el PATH del sistema.

**Solución**:
- Verifica que Python esté instalado: descarga desde [python.org](https://www.python.org/downloads/)
- Durante la instalación, marca la opción "Add Python to PATH"
- O usa `py` en Windows: `py VivasPlay.py`
- O usa la ruta completa: `C:\Python3x\python.exe VivasPlay.py`

### Error: "No module named 'tkinter'"

**Problema**: tkinter no está instalado (raro en instalaciones estándar de Python).

**Solución**:
- **Windows**: Reinstala Python y asegúrate de marcar "tcl/tk and IDLE"
- **Linux**: Instala tkinter:
  ```bash
  sudo apt-get install python3-tk  # Debian/Ubuntu
  sudo yum install python3-tkinter  # RedHat/CentOS
  ```
- **macOS**: tkinter viene incluido con Python

### Error al ejecutar el ejecutable: "Falta assets"

**Problema**: Los archivos de assets no están en la ubicación correcta.

**Solución**:
1. Verifica que la carpeta `assets/` esté en el mismo directorio que el ejecutable
2. Verifica que `assets/image/` contenga todos los archivos PNG
3. Si usas PyInstaller con `--onefile`, asegúrate de incluir assets en el spec o copiarlos manualmente

### El ejecutable es muy grande

**Problema**: PyInstaller incluye muchas librerías por defecto.

**Solución**:
- Usa `--exclude-module` para excluir módulos no necesarios:
  ```bash
  pyinstaller --onefile --noconsole --exclude-module matplotlib --exclude-module numpy --name VivasPlay VivasPlay.py
  ```
- Edita el archivo `.spec` para excluir más módulos

### El antivirus marca el ejecutable como sospechoso

**Problema**: Los ejecutables creados con PyInstaller a veces son marcados como falsos positivos.

**Solución**:
- Agrega una excepción en tu antivirus para el ejecutable
- Considera firmar el ejecutable con un certificado de código (requiere compra)
- Informa a los usuarios que es un falso positivo común

### Error: "Failed to execute script"

**Problema**: Hay un error en el código o falta una dependencia.

**Solución**:
1. Ejecuta el script directamente primero para ver el error:
   ```bash
   python VivasPlay.py
   ```
2. Si funciona, prueba el build con consola visible:
   ```bash
   pyinstaller --onefile --name VivasPlay VivasPlay.py
   ```
   (sin `--noconsole` para ver los errores)
3. Verifica que todas las dependencias estén incluidas en el build

### Build muy lento

**Problema**: PyInstaller puede ser lento en la primera ejecución.

**Solución**:
- Es normal, especialmente con `--onefile`
- Las ejecuciones posteriores son más rápidas
- Considera usar `--onedir` en lugar de `--onefile` para builds más rápidos (pero genera una carpeta con múltiples archivos)

---

## Recursos Adicionales

- [Documentación oficial de PyInstaller](https://pyinstaller.org/)
- [Documentación de cx_Freeze](https://cx-freeze.readthedocs.io/)
- [Documentación de py2exe](https://www.py2exe.org/)

---

*Última actualización: 2025-12-26*
