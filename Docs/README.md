# VivasPlay - Documentación

## Descripción

VivasPlay es una aplicación de escritorio desarrollada en Python con Tkinter para la gestión de correos electrónicos. Permite administrar una lista de correos electrónicos con funcionalidades completas de CRUD (Crear, Leer, Actualizar, Eliminar) y operaciones de importación/exportación.

## Características

- ✅ **Gestión de correos**: Agregar y eliminar correos individuales
- ✅ **Validación de formato**: Verificación automática de formato de correo electrónico
- ✅ **Importación masiva**: Cargar múltiples correos desde archivos de texto
- ✅ **Exportación**: Guardar la lista de correos en archivos de texto
- ✅ **Conteo de correos**: Validar y contar correos en archivos externos
- ✅ **Edición en línea**: Editar correos directamente desde la tabla
- ✅ **Copia al portapapeles**: Copiar correos seleccionados fácilmente
- ✅ **Persistencia de datos**: Almacenamiento automático en formato JSON
- ✅ **Interfaz moderna**: Diseño limpio con estilos ttk mejorados

## Requisitos del Sistema

- **Python**: 3.7 o superior
- **Sistema Operativo**: Windows, Linux o macOS
- **Librerías incluidas en Python estándar**:
  - `tkinter` (interfaz gráfica)
  - `json` (persistencia de datos)
  - `re` (validación de correos)
  - `os` (operaciones de sistema)

## Instalación

No se requiere instalación adicional de paquetes. La aplicación utiliza únicamente librerías estándar de Python.

1. Asegúrate de tener Python 3.7+ instalado
2. Descarga o clona el proyecto
3. Ejecuta la aplicación:

```bash
python VivasPlay.py
```

## Estructura del Proyecto

``` bash
VivasPlay/
├── VivasPlay.py          # Archivo principal de la aplicación
├── correos.json          # Archivo de datos (se crea automáticamente)
├── assets/
│   └── image/            # Iconos de la aplicación
│       ├── clip_2891632.png
│       ├── file_5632095.png
│       ├── mail_1849441.png
│       └── remove_13922476.png
└── Docs/
    └── README.md         # Esta documentación
```

## Uso de la Aplicación

### Interfaz Principal

La aplicación consta de tres secciones principales:

1. **Barra de herramientas**: Botones para operaciones con archivos y configuración
2. **Tabla de correos**: Muestra todos los correos con numeración automática
3. **Panel de entrada**: Campo de texto y botones para agregar/eliminar correos individuales

### Operaciones Básicas

#### Agregar un Correo Individual

1. Escribe el correo en el campo de entrada inferior
2. Haz clic en "Agregar" o presiona Enter
3. El correo se validará automáticamente antes de agregarse

#### Eliminar un Correo Individual

1. Escribe el correo en el campo de entrada
2. Haz clic en "Eliminar"
3. El correo se eliminará si existe en la lista

#### Editar un Correo

1. Haz doble clic en cualquier celda de la tabla
2. Se abrirá un diálogo de edición
3. Modifica el correo y haz clic en "Guardar"

#### Copiar Correos

- **Desde la tabla**: Selecciona uno o más correos y presiona `Ctrl+C`
- **Menú contextual**: Clic derecho → "Copiar valor"

### Operaciones con Archivos

#### Añadir Correos desde Archivo

1. Haz clic en el botón de archivo (📎)
2. Selecciona "Añadir correos mediante archivo"
3. Elige un archivo `.txt` con un correo por línea
4. Solo se agregarán correos válidos y no duplicados

#### Eliminar Correos desde Archivo

1. Botón archivo → "Eliminar correos mediante archivo"
2. Selecciona un archivo con los correos a eliminar
3. Se eliminarán todos los correos que coincidan

#### Contar Correos en Archivo

1. Botón archivo → "Contar correos mediante archivo"
2. Selecciona un archivo de texto
3. Se mostrará la cantidad de correos válidos encontrados

#### Exportar Correos

1. Botón archivo → "Exportar correos"
2. Elige la ubicación y nombre del archivo
3. Se guardará un archivo `.txt` con todos los correos (uno por línea)

## Validación de Correos

La aplicación utiliza una expresión regular para validar el formato de correos electrónicos:

``` bash
^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
```

**Formato válido**: `usuario@dominio.com`

- Permite letras, números y caracteres especiales comunes
- Requiere un símbolo `@`
- Requiere un dominio con extensión de al menos 2 caracteres

## Almacenamiento de Datos

Los correos se guardan automáticamente en el archivo `correos.json` en formato JSON. Este archivo se crea automáticamente si no existe y se actualiza cada vez que se realizan cambios en la lista.

**Ubicación**: Mismo directorio que `VivasPlay.py`

## Atajos de Teclado

- `Enter`: Agregar correo desde el campo de entrada
- `Ctrl+C`: Copiar correos seleccionados al portapapeles
- `Doble clic`: Editar correo en la tabla

## Solución de Problemas

### La aplicación no inicia

- Verifica que Python 3.7+ esté instalado
- Asegúrate de que `tkinter` esté disponible (normalmente incluido con Python)

### Los iconos no se muestran

- Verifica que la carpeta `assets/image/` exista y contenga los archivos de iconos
- La aplicación funcionará sin iconos, mostrando texto alternativo

### Error al guardar/leer archivos

- Verifica permisos de escritura en el directorio
- Asegúrate de que el archivo `correos.json` no esté bloqueado por otra aplicación

## Características Técnicas

- **Arquitectura**: Orientada a objetos con clase principal `VivasPlayApp`
- **Persistencia**: JSON para almacenamiento de datos
- **Validación**: Expresiones regulares para formato de correo
- **UI Framework**: Tkinter con estilos ttk mejorados
- **Manejo de errores**: Try-except en todas las operaciones de archivo

## Versión

**Versión actual**: 2.0 (Refactorizada)

## Autor

Desarrollado para gestión eficiente de listas de correos electrónicos.

---

*Última actualización: 2025-12-26*
