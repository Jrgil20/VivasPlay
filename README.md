# Vivas Play

## Introducción
Vivas Play es una aplicación que permite gestionar una lista de correos electrónicos. La aplicación permite agregar correos electrónicos desde un archivo de texto o manualmente, eliminar correos electrónicos y mostrar un menú contextual para copiar la dirección de correo electrónico seleccionada.

## Interfaz de usuario
La interfaz de usuario de la aplicación se compone de los siguientes elementos:

- **Ventana principal**: La ventana principal contiene todos los elementos de la interfaz de usuario.
- **Marco**: El marco contiene los botones para agregar y eliminar correos electrónicos, la tabla que muestra la lista de correos electrónicos y el campo de entrada para ingresar un nuevo correo electrónico.
- **Menú de archivos**: El menú de archivos, identificado con la imagen ![clips](assets/image/clip_2891632.png), contiene las siguientes opciones:
    - **Adjuntar correos**: Permite agregar correos electrónicos desde un archivo de texto.
    - **Eliminar correos**: Permite eliminar correos electrónicos seleccionados de la lista.
    - **Conteo de correos**: Muestra el número total de correos electrónicos en la lista.
- **Tabla**: La tabla muestra la lista de correos electrónicos. La tabla tiene dos columnas: "Enumeración" y "Correo". La columna "Enumeración" muestra el número de orden del correo electrónico en la lista. La columna "Correo" muestra la dirección de correo electrónico.
- **Campo de entrada**: El campo de entrada permite ingresar un nuevo correo electrónico para agregar a la lista.
    - **Botón "Agregar correo"**: Este botón permite agregar el nuevo correo electrónico ingresado en el campo de entrada a la lista.
    - **Botón "Eliminar correo"**: Este botón permite eliminar el correo electrónico ingresado en el campo de entrada de la lista.

## Uso de la aplicación
Para usar la aplicación Vivas Play, siga estos pasos:

### Inicie la aplicación
Haga doble clic en el archivo ejecutable de la aplicación para iniciarla.

### Agregar correos electrónicos desde un archivo de texto
1. Haga clic en el botón "Añadir".
2. Seleccione el archivo de texto que contiene los correos electrónicos que desea agregar.
3. Los correos electrónicos del archivo de texto se agregarán a la lista.

### Agregar un correo electrónico manualmente
1. Ingrese la dirección de correo electrónico que desea agregar en el campo de entrada.
2. Haga clic en el botón "Agregar correo".
3. El correo electrónico se agregará a la lista.

### Eliminar un correo electrónico
1. Seleccione el correo electrónico que desea eliminar en la tabla.
2. Haga clic en el botón "Eliminar".
3. El correo electrónico seleccionado se eliminará de la lista.

### Copiar la dirección de correo electrónico de un correo electrónico seleccionado
1. Haga clic con el botón derecho del mouse en el correo electrónico seleccionado en la tabla.
2. Seleccione la opción "Copiar" en el menú contextual.
3. La dirección de correo electrónico seleccionada se copiará al portapapeles.

## Ejecutar en local
Para ejecutar la aplicación en local, siga estos pasos:
1. Abra una terminal o línea de comandos.
2. Navegue al directorio donde se encuentra el archivo `VivasPlay.py`.
3. Ejecute el siguiente comando:
    ```sh
    python .\VivasPlay.py
    ```

## build the application
Para construir la aplicación, siga estos pasos:
1. Abra una terminal o línea de comandos.
2. Navegue al directorio donde se encuentra el archivo `VivasPlay.py`.
3. Utilice una herramienta para convertir el script de Python en un ejecutable. Algunas opciones populares son:
    - **PyInstaller**: Puede instalar PyInstaller usando `pip install pyinstaller` y luego ejecutar `pyinstaller --onefile --noconsole --name VivasPlay VivasPlay.py` para crear un ejecutable.
    - **cx_Freeze**: Puede instalar cx_Freeze usando `pip install cx_Freeze` y luego crear un archivo de configuración para construir el ejecutable.
    - **py2exe**: Puede instalar py2exe usando `pip install py2exe` y luego crear un archivo de configuración para construir el ejecutable.
4. El ejecutable se generará en el directorio `dist` o en el directorio especificado en la configuración de la herramienta utilizada.
5. coppie todo los assets a la carpeta dist

## Consejos
- Puede usar el atajo de teclado Ctrl+C para copiar la dirección de correo electrónico de un correo electrónico seleccionado en la tabla.
- Puede usar el atajo de teclado Ctrl+V para pegar la dirección de correo electrónico del portapapeles en el campo de entrada.

## Solución de problemas
Se recomienda ignorar la aplicación de la lista de software leídos en los antivirus ya que está o tiene una firma de software, si esta opción no es posible, puede ejecutar el archivo `Vivas.py`, desde Python 3 o superior, usando un IDE.

## Agradecimientos
Esta aplicación fue creada utilizando el lenguaje de programación Python y la biblioteca Tkinter.

## Licencia
Esta aplicación se distribuye bajo la licencia MIT. Puede encontrar más información sobre la licencia MIT en [https://opensource.org/license/mit](https://opensource.org/license/mit).