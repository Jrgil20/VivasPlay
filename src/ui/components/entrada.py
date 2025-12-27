"""
Panel de entrada con campo de texto y botones de acción.

Incluye indicador de cantidad de elementos seleccionados.
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional


class PanelEntrada(ttk.Frame):
    """
    Panel inferior con campo de entrada y botones.
    
    Attributes:
        on_agregar: Callback cuando se presiona Agregar o Enter.
        on_eliminar: Callback cuando se presiona Eliminar.
    """
    
    def __init__(
        self,
        parent,
        on_agregar: Optional[Callable[[], None]] = None,
        on_eliminar: Optional[Callable[[], None]] = None
    ):
        """
        Inicializa el panel de entrada.
        
        Args:
            parent: Widget padre.
            on_agregar: Callback para agregar registro.
            on_eliminar: Callback para eliminar registro/selección.
        """
        super().__init__(parent)
        
        self.on_agregar = on_agregar
        self.on_eliminar = on_eliminar
        
        self._crear_widgets()
    
    def _crear_widgets(self):
        """Crea los widgets del panel."""
        ttk.Label(self, text="Entrada:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.entrada = ttk.Entry(self, width=50)
        self.entrada.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.entrada.bind("<Return>", lambda e: self._handle_agregar())
        
        ttk.Button(
            self,
            text="Agregar",
            command=self._handle_agregar
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            self,
            text="Eliminar",
            command=self._handle_eliminar
        ).pack(side=tk.LEFT, padx=2)
        
        # Separador visual
        ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Etiqueta de selección/total
        self.etiqueta_seleccion = ttk.Label(
            self,
            text="Total: 0 registros",
            font=('Segoe UI', 9),
            foreground='#666666'
        )
        self.etiqueta_seleccion.pack(side=tk.LEFT, padx=5)
    
    def get_texto(self) -> str:
        """Obtiene el texto del campo de entrada."""
        return self.entrada.get().strip()
    
    def limpiar(self):
        """Limpia el campo de entrada."""
        self.entrada.delete(0, tk.END)
    
    def actualizar_contador(self, seleccionados: int, total: int):
        """
        Actualiza el indicador de selección/total.
        
        Args:
            seleccionados: Cantidad de elementos seleccionados.
            total: Total de registros.
        """
        if seleccionados == 0:
            texto = f"Total: {total} registros"
        elif seleccionados == 1:
            texto = f"1 seleccionado de {total}"
        else:
            texto = f"{seleccionados} seleccionados de {total}"
        
        self.etiqueta_seleccion.config(text=texto)
    
    def _handle_agregar(self):
        """Maneja el evento de agregar."""
        if self.on_agregar:
            self.on_agregar()
    
    def _handle_eliminar(self):
        """Maneja el evento de eliminar."""
        if self.on_eliminar:
            self.on_eliminar()
