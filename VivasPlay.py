import tkinter as tk
from tkinter import ttk  # Importar ttk

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Vivas Play")

# Crear el vector de Correos
Correos = ["Hola", "Mundo", "Python", "Tkinter"]

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

# Iniciar el bucle principal de la GUI
ventana.mainloop()