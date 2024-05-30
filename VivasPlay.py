import tkinter as tk
from tkinter import ttk  # Importar ttk
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

# Crear el marco para la tabla
marco_tabla = tk.Frame(ventana)
marco_tabla.pack()

# Crear la tabla
tabla = ttk.Treeview(marco_tabla, columns=("Correo",))  # Usar ttk.Treeview
tabla.heading("#0", text="")  # Ocultar la primera columna
tabla.heading("Correo", text="Correo")
tabla.pack()

# Insertar los Correos en la tabla
for Correo in Correos:
    tabla.insert("", tk.END, values=(Correo,))

# Crear el campo de entrada para el nuevo correo
entrada_correo = tk.Entry(ventana)
entrada_correo.pack()

# Función para agregar el nuevo correo a la tabla y al archivo JSON
def agregar_correo():
    correo = entrada_correo.get()  # Obtener el correo del campo de entrada
    tabla.insert("", tk.END, values=(correo,))  # Insertar el correo en la tabla
    entrada_correo.delete(0, tk.END)  # Limpiar el campo de entrada
    Correos.append(correo)  # Agregar el correo a la lista
    with open('correos.json', 'w') as f:  # Abrir el archivo JSON en modo de escritura
        json.dump(Correos, f)  # Guardar la lista actualizada en el archivo JSON

# Crear el botón para agregar el nuevo correo
boton_agregar = tk.Button(ventana, text="Agregar correo", command=agregar_correo)
boton_agregar.pack()

# Iniciar el bucle principal de la GUI
ventana.mainloop()