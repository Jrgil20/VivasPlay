import tkinter as tk
from tkinter import ttk  # Importar ttk
from tkinter import filedialog
import re
import json  # Importar el módulo json
import os  # Importar el módulo os

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Vivas Play")

# Verificar si el archivo correos.json existe
if not os.path.exists('correos.json'):
    with open('correos.json', 'w') as f:
        json.dump([], f)  # Crear un archivo JSON vacío


# Cargar los correos desde un archivo JSON
with open('correos.json', 'r') as f:
    Correos = json.load(f)

# Crear el marco para la tabla y los botones
marco = tk.Frame(ventana)
marco.pack(fill=tk.BOTH, expand=True)

def leer_archivo_externo():
    ruta = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])  # Abre el cuadro de diálogo para seleccionar el archivo
    with open(ruta, 'r') as f:
        correos = f.read().splitlines()
    return correos

def Correos_regex(Correo):

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, Correo):
        return False

    return True


def añadir():
    correos = [correo.strip() for correo in leer_archivo_externo()]  # Usar comprensión de lista con strip()
    correos_validos = [correo for correo in correos if Correos_regex(correo)]  # Filtrar correos válidos
    Correos.extend(correos_validos)
    for i in tabla.get_children():
        tabla.delete(i)
    for i, correo in enumerate(Correos, start=1):
        tabla.insert("", tk.END, values=(i, correo))
    with open('correos.json', 'w') as f:
        json.dump(Correos, f)
    respuesta = tk.Toplevel(ventana)
    respuesta.title("Resultado de la inserción")
    tk.Label(respuesta, text=f"Se insertaron {len(correos_validos)} correos válidos.").pack(padx=20, pady=20)

def eliminar():
    correos_a_eliminar = [correo.strip() for correo in leer_archivo_externo()]  # Usar comprensión de lista con strip()
    for correo in correos_a_eliminar:
        if correo in Correos:
            Correos.remove(correo)
    with open('correos.json', 'w') as f:
        json.dump(Correos, f)
    for i in tabla.get_children():
        tabla.delete(i)
    for i, correo in enumerate(Correos, start=1):
        tabla.insert("", tk.END, values=(i, correo))
    respuesta = tk.Toplevel(ventana)
    respuesta.title("Resultado de la eliminación")
    tk.Label(respuesta, text=f"Se eliminaron {len(correos_a_eliminar)} correos.").pack(padx=20, pady=20)

def Contar_Correos():
    correos = [correo.strip() for correo in leer_archivo_externo() if correo.strip()]  # Leer y filtrar líneas no vacías
    correos_validos = [correo for correo in correos if Correos_regex(correo)]  # Filtrar correos válidos
    print(f"Se encontraron {len(correos_validos)} correos válidos.")  # Imprimir la cantidad de correos válidos
    respuesta = tk.Toplevel(ventana)
    respuesta.title("Resultado del conteo")
    tk.Label(respuesta, text=f"Se encontraron {len(correos_validos)} correos válidos.").pack(padx=20, pady=20)
    return len(correos_validos)

def Exportar_Correos():
    correos = [correo for correo in Correos if Correos_regex(correo)]  # Filtrar correos válidos
    ruta = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])  # Abre el cuadro de diálogo para guardar el archivo
    if ruta:
        with open(ruta, 'w') as f:
            f.write('\n'.join(correos))  # Escribir los correos en el archivo

# Crear el botón para agregar el nuevo correo
clip_icon = tk.PhotoImage(file="assets/image/clip_2891632.png")
sub_menu = tk.Menu(ventana, tearoff=0)
sub_menu.add_command(label="Añadir correos mediante archivo", command=añadir)
sub_menu.add_command(label="Eliminar correos mediante archivo", command=eliminar)
sub_menu.add_command(label="Contar correos mediante archivo", command=Contar_Correos)
sub_menu.add_command(label="Exportar correos", command=Exportar_Correos)

def mostrar_submenu(event):
    sub_menu.post(event.x_root, event.y_root)

boton_adjuntar = tk.Button(marco, image=clip_icon)
boton_adjuntar.image = clip_icon
boton_adjuntar.bind("<Button-1>", mostrar_submenu)
boton_adjuntar.grid(row=0, column=0, sticky='w')


# Crear el botón para eliminar un correo
ConfiMail_ico = tk.PhotoImage(file="assets/image/mail_1849441.png")
boton_config = tk.Button(marco, image=ConfiMail_ico)
# Crear el submenú de configuración
config_menu = tk.Menu(ventana, tearoff=0)
config_menu.add_command(label="Correos Regex", command=lambda: print("Correos Regex seleccionado"))

def mostrar_config_menu(event):
    config_menu.post(event.x_root, event.y_root)

boton_config.bind("<Button-1>", mostrar_config_menu)
boton_config.grid(row=0, column=1, sticky='w')  # Colocar el botón a la derecha del botón de agregar

# Crear la tabla
tabla = ttk.Treeview(marco, columns=("Enumeración", "Correo"))  # Usar ttk.Treeview
tabla.column("#0", width=0, stretch=tk.NO)  # Ocultar la primera columna
tabla.column("Enumeración", width=50, anchor=tk.CENTER)  # Ajustar el ancho de la columna de enumeración
tabla.column("Correo", width=200, anchor=tk.W)  # Ajustar el ancho de la columna de correo
tabla.heading("Enumeración", text="No.")  # Agregar encabezado a la columna de enumeración
tabla.heading("Correo", text="Correo")  # Agregar encabezado a la columna de correo
tabla.grid(row=1, column=0, columnspan=2, sticky='nsew')  # Colocar la tabla debajo de los botones

# Permitir la selección de múltiples filas
tabla.configure(selectmode='extended')

# Crear un menú contextual para la tabla
menu_contextual = tk.Menu(ventana, tearoff=0)
menu_contextual.add_command(label="Copiar valor", command=lambda: ventana.clipboard_clear() or ventana.clipboard_append('\n'.join([tabla.item(sel, 'values')[1] for sel in tabla.selection()])))

def mostrar_menu_contextual(event):
    menu_contextual.post(event.x_root, event.y_root)

tabla.bind("<Button-3>", mostrar_menu_contextual)

marco.grid_columnconfigure(0, weight=1)  # Hacer que la primera columna se expanda para llenar el espacio disponible
marco.grid_rowconfigure(1, weight=1)  # Hacer que la segunda fila se expanda para llenar el espacio disponible
# Insertar los Correos en la tabla con enumeración
for i, Correo in enumerate(Correos, start=1):
    tabla.insert("", tk.END, values=(i, Correo))

# Crear el campo de entrada para el nuevo correo
entrada_correo = tk.Entry(ventana)
entrada_correo.pack()

# Actualizar la función agregar_correo para incluir la enumeración
def agregar_correo():
    correo = entrada_correo.get().strip()  # Usar strip() para eliminar espacios en blanco
    if correo and Correos_regex(correo):  # Verificar que el correo no esté vacío y sea válido
        Correos.append(correo)
        tabla.insert("", tk.END, values=(len(Correos), correo))
        entrada_correo.delete(0, tk.END)
        with open('correos.json', 'w') as f:
            json.dump(Correos, f)

# Crear el botón para agregar el nuevo correo
boton_agregar = tk.Button(ventana, text="Agregar correo", command=agregar_correo)
boton_agregar.pack()

# Actualizar la función eliminar_correo para recargar la tabla con enumeración
def eliminar_correo():
    correo = entrada_correo.get().strip()  # Usar strip() para eliminar espacios en blanco
    if correo in Correos:
        Correos.remove(correo)
        with open('correos.json', 'w') as f:
            json.dump(Correos, f)
        for i in tabla.get_children():
            tabla.delete(i)
        for i, Correo in enumerate(Correos, start=1):
            tabla.insert("", tk.END, values=(i, Correo))
    entrada_correo.delete(0, tk.END)

# Crear el botón para eliminar un correo
boton_eliminar = tk.Button(ventana, text="Eliminar correo", command=eliminar_correo)
boton_eliminar.pack()

# Iniciar el bucle principal de la GUI
ventana.mainloop()