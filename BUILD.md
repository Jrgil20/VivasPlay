# Guía de Build - VivasPlay

Esta guía explica cómo crear un ejecutable único de VivasPlay para distribuir.

## Requisitos

- Python 3.7 o superior
- PyInstaller (se instala automáticamente si no está presente)

## Método 1: Script Automático (Recomendado)

### Windows
```bash
build_dist.bat
```

### Linux/Mac
```bash
chmod +x build_dist.sh
./build_dist.sh
```

El script:
1. Verifica e instala PyInstaller si es necesario
2. Limpia builds anteriores
3. Compila el ejecutable
4. El resultado estará en `dist/VivasPlay.exe` (Windows) o `dist/VivasPlay` (Linux/Mac)

## Método 2: Comando Manual

### Con archivo .spec (Recomendado)
```bash
pyinstaller VivasPlay.spec --clean
```

### Comando directo
```bash
pyinstaller --onefile --name VivasPlay \
    --add-data "src;src" \
    --add-data "assets;assets" \
    --hidden-import src \
    VivasPlay.py --clean
```

**Nota para Linux/Mac:** Cambiar `;` por `:` en `--add-data`:
```bash
pyinstaller --onefile --name VivasPlay \
    --add-data "src:src" \
    --add-data "assets:assets" \
    --hidden-import src \
    VivasPlay.py --clean
```

## Resultado

Después de la compilación, encontrarás:
- **Windows:** `dist/VivasPlay.exe` (un solo archivo ejecutable)
- **Linux/Mac:** `dist/VivasPlay` (un solo archivo ejecutable)

## Entregar al Patrocinador

Simplemente copia el archivo ejecutable de la carpeta `dist/`:
- **Windows:** `VivasPlay.exe`
- **Linux/Mac:** `VivasPlay`

El ejecutable es completamente independiente y no requiere:
- Python instalado
- Archivos adicionales
- Dependencias externas

## Solución de Problemas

### Error: "No module named 'src'"
Asegúrate de que el comando se ejecuta desde la raíz del proyecto donde está `VivasPlay.py`.

### Error: "No se encuentran los iconos"
Verifica que la carpeta `assets/image/` existe y contiene los archivos PNG.

### El ejecutable es muy grande
Es normal. PyInstaller incluye Python y todas las dependencias. El tamaño típico es 20-50 MB.

### El ejecutable no inicia
- Verifica que no hay errores en la consola (puedes quitar `--noconsole` temporalmente)
- Asegúrate de que todas las dependencias están instaladas en tu entorno de desarrollo

## Personalización

### Añadir un icono personalizado
Edita `VivasPlay.spec` y cambia:
```python
icon=None,  # Cambiar por: icon='assets/icon.ico'
```

### Incluir archivos adicionales
Edita `VivasPlay.spec` y añade a `datas`:
```python
datas.append(('ruta/origen', 'ruta/destino'))
```
