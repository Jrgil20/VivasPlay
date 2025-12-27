"""
Diálogo para mostrar resultados de operaciones.

Proporciona una ventana simple para mostrar mensajes al usuario.
"""

import tkinter as tk
from tkinter import ttk


def mostrar_resultado(parent: tk.Tk, titulo: str, mensaje: str):
    """
    Muestra una ventana con el resultado de una operación.
    
    Args:
        parent: Ventana padre.
        titulo: Título de la ventana.
        mensaje: Mensaje a mostrar.
    """
    dialogo = tk.Toplevel(parent)
    dialogo.title(titulo)
    dialogo.transient(parent)
    
    ttk.Label(dialogo, text=mensaje, justify=tk.LEFT).pack(padx=20, pady=20)
    ttk.Button(dialogo, text="Aceptar", command=dialogo.destroy).pack(pady=(0, 10))
