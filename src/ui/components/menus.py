"""
Menús contextuales para la tabla de correos.

Proporciona menú adaptable según la cantidad de elementos seleccionados.
"""

import tkinter as tk
from typing import Callable, Optional


class MenuContextual:
    """
    Menú contextual dinámico para la tabla de correos.
    
    Se adapta según la cantidad de elementos seleccionados.
    """
    
    def __init__(
        self,
        parent,
        on_copiar: Optional[Callable[[], None]] = None,
        on_copiar_fila: Optional[Callable[[], None]] = None,
        on_eliminar: Optional[Callable[[], None]] = None,
        on_seleccionar_todos: Optional[Callable[[], None]] = None,
        on_deseleccionar: Optional[Callable[[], None]] = None
    ):
        """
        Inicializa el menú contextual.
        
        Args:
            parent: Widget padre.
            on_copiar: Callback para copiar correos.
            on_copiar_fila: Callback para copiar filas completas.
            on_eliminar: Callback para eliminar selección.
            on_seleccionar_todos: Callback para seleccionar todos.
            on_deseleccionar: Callback para deseleccionar.
        """
        self.parent = parent
        self.menu = tk.Menu(parent, tearoff=0)
        
        self.on_copiar = on_copiar
        self.on_copiar_fila = on_copiar_fila
        self.on_eliminar = on_eliminar
        self.on_seleccionar_todos = on_seleccionar_todos
        self.on_deseleccionar = on_deseleccionar
    
    def mostrar(self, event: tk.Event, cantidad_seleccionados: int):
        """
        Muestra el menú contextual adaptado a la selección.
        
        Args:
            event: Evento del mouse con posición.
            cantidad_seleccionados: Cantidad de elementos seleccionados.
        """
        # Limpiar menú anterior
        self.menu.delete(0, tk.END)
        
        if cantidad_seleccionados == 0:
            self.menu.add_command(
                label="Seleccionar todos (Ctrl+A)",
                command=self.on_seleccionar_todos or (lambda: None)
            )
        elif cantidad_seleccionados == 1:
            self.menu.add_command(
                label="Copiar correo",
                command=self.on_copiar or (lambda: None)
            )
            self.menu.add_command(
                label="Copiar fila completa",
                command=self.on_copiar_fila or (lambda: None)
            )
            self.menu.add_separator()
            self.menu.add_command(
                label="Eliminar",
                command=self.on_eliminar or (lambda: None)
            )
        else:
            self.menu.add_command(
                label=f"Copiar {cantidad_seleccionados} correos",
                command=self.on_copiar or (lambda: None)
            )
            self.menu.add_command(
                label=f"Copiar {cantidad_seleccionados} filas completas",
                command=self.on_copiar_fila or (lambda: None)
            )
            self.menu.add_separator()
            self.menu.add_command(
                label=f"Eliminar {cantidad_seleccionados} seleccionados",
                command=self.on_eliminar or (lambda: None)
            )
            self.menu.add_separator()
            self.menu.add_command(
                label="Deseleccionar (Esc)",
                command=self.on_deseleccionar or (lambda: None)
            )
        
        self.menu.post(event.x_root, event.y_root)
