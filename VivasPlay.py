import tkinter as tk
from tkinter import ttk  # Importar ttk
from tkinter import filedialog
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
marco.pack()

def leer_archivo_externo():
    ruta = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])  # Abre el cuadro de diálogo para seleccionar el archivo
    with open(ruta, 'r') as f:
        correos = f.read().splitlines()
    return correos

def añadir():
    correos = leer_archivo_externo()  # Leer los correos del archivo seleccionado
    Correos.extend(correos)  # Agregar los correos a la lista
    # Borrar la tabla
    for i in tabla.get_children():
        tabla.delete(i)
    # Insertar los correos en la tabla con la nueva numeración
    for i, correo in enumerate(Correos, start=1):
        tabla.insert("", tk.END, values=(i, correo))
    with open('correos.json', 'w') as f:  # Abrir el archivo JSON en modo de escritura
        json.dump(Correos, f)  # Guardar la lista actualizada en el archivo JSON

# Crear el botón para agregar el nuevo correo
boton_agregar = tk.Button(marco, text="Añadir", command=añadir)
boton_agregar.grid(row=0, column=0, sticky='w')  # Colocar el botón en la esquina superior izquierda

def eliminar():
    correos_a_eliminar = leer_archivo_externo()  # Leer los correos del archivo seleccionado
    for correo in correos_a_eliminar:
        if correo in Correos:
            Correos.remove(correo)  # Eliminar el correo de la lista
    with open('correos.json', 'w') as f:  # Abrir el archivo JSON en modo de escritura
        json.dump(Correos, f)  # Guardar la lista actualizada en el archivo JSON
    # Recargar la tabla
    for i in tabla.get_children():
        tabla.delete(i)
    for i, correo in enumerate(Correos, start=1):
        tabla.insert("", tk.END, values=(i, correo))  # Insertar el correo en la tabla con enumeración

# Crear el botón para eliminar un correo
boton_eliminar = tk.Button(marco, text="Eliminar", command=eliminar)
boton_eliminar.grid(row=0, column=1, sticky='w')  # Colocar el botón a la derecha del botón de agregar

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
menu_contextual.add_command(label="Copiar", command=lambda: ventana.clipboard_append(tabla.item(tabla.selection(), 'values')[1]))

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
    correo = entrada_correo.get()  # Obtener el correo del campo de entrada
    Correos.append(correo)  # Agregar el correo a la lista
    tabla.insert("", tk.END, values=(len(Correos), correo))  # Insertar el correo en la tabla con enumeración
    entrada_correo.delete(0, tk.END)  # Limpiar el campo de entrada
    with open('correos.json', 'w') as f:  # Abrir el archivo JSON en modo de escritura
        json.dump(Correos, f)  # Guardar la lista actualizada en el archivo JSON

# Crear el botón para agregar el nuevo correo
boton_agregar = tk.Button(ventana, text="Agregar correo", command=agregar_correo)
boton_agregar.pack()

# Actualizar la función eliminar_correo para recargar la tabla con enumeración
def eliminar_correo():
    correo = entrada_correo.get()  # Obtener el correo del campo de entrada
    if correo in Correos:  # Si el correo está en la lista
        Correos.remove(correo)  # Eliminar el correo de la lista
        with open('correos.json', 'w') as f:  # Abrir el archivo JSON en modo de escritura
            json.dump(Correos, f)  # Guardar la lista actualizada en el archivo JSON
        # Recargar la tabla con enumeración
        for i in tabla.get_children():
            tabla.delete(i)
        for i, Correo in enumerate(Correos, start=1):
            tabla.insert("", tk.END, values=(i, Correo))
    entrada_correo.delete(0, tk.END)  # Limpiar el campo de entrada

# Crear el botón para eliminar un correo
boton_eliminar = tk.Button(ventana, text="Eliminar correo", command=eliminar_correo)
boton_eliminar.pack()

# Iniciar el bucle principal de la GUI
ventana.mainloop()