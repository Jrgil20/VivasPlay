"""
Componente de tabla para mostrar registros de correo.

Incluye funcionalidad de selección múltiple por arrastre del mouse.
"""

import tkinter as tk
from tkinter import ttk
from typing import List, Callable, Optional, Tuple

from ...models.registro import RegistroCorreo


class TablaCorreos(ttk.Frame):
    """
    Tabla para mostrar y gestionar registros de correo.
    
    Características:
    - Treeview con columnas: No., Correo, VPN, Países, Notas
    - Selección múltiple por arrastre del mouse
    - Soporte para Ctrl+Click y Shift+Click
    - Scrollbars horizontal y vertical
    
    Attributes:
        on_doble_click: Callback cuando se hace doble click en una fila.
        on_seleccion_cambio: Callback cuando cambia la selección.
        on_click_derecho: Callback para menú contextual.
    """
    
    def __init__(
        self,
        parent,
        on_doble_click: Optional[Callable[[int], None]] = None,
        on_seleccion_cambio: Optional[Callable[[int], None]] = None,
        on_click_derecho: Optional[Callable[[tk.Event], None]] = None
    ):
        """
        Inicializa la tabla de correos.
        
        Args:
            parent: Widget padre.
            on_doble_click: Callback(indice) al hacer doble click.
            on_seleccion_cambio: Callback(cantidad) cuando cambia la selección.
            on_click_derecho: Callback(event) para menú contextual.
        """
        super().__init__(parent)
        
        self.on_doble_click = on_doble_click
        self.on_seleccion_cambio = on_seleccion_cambio
        self.on_click_derecho = on_click_derecho
        
        # Variables para selección por arrastre
        self._arrastre_inicio_item = None
        self._arrastre_activo = False
        
        self._crear_widgets()
        self._configurar_bindings()
    
    def _crear_widgets(self):
        """Crea la tabla y scrollbars."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Scrollbars
        scrollbar_y = ttk.Scrollbar(self, orient=tk.VERTICAL)
        scrollbar_y.grid(row=0, column=1, sticky='ns')
        
        scrollbar_x = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
        scrollbar_x.grid(row=1, column=0, sticky='ew')
        
        # Tabla
        self.tabla = ttk.Treeview(
            self,
            columns=("No", "Correo", "VPN", "Países", "Notas"),
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set,
            selectmode='extended'
        )
        
        scrollbar_y.config(command=self.tabla.yview)
        scrollbar_x.config(command=self.tabla.xview)
        
        # Configurar columnas
        self.tabla.column("#0", width=0, stretch=tk.NO)
        self.tabla.column("No", width=50, anchor=tk.CENTER)
        self.tabla.column("Correo", width=280, anchor=tk.W)
        self.tabla.column("VPN", width=50, anchor=tk.CENTER)
        self.tabla.column("Países", width=100, anchor=tk.CENTER)
        self.tabla.column("Notas", width=150, anchor=tk.W)
        
        # Configurar encabezados
        self.tabla.heading("No", text="No.")
        self.tabla.heading("Correo", text="Correo")
        self.tabla.heading("VPN", text="VPN")
        self.tabla.heading("Países", text="Países")
        self.tabla.heading("Notas", text="Notas")
        
        self.tabla.grid(row=0, column=0, sticky='nsew')
    
    def _configurar_bindings(self):
        """Configura los eventos de la tabla."""
        # Doble click para editar
        self.tabla.bind("<Double-Button-1>", self._handle_doble_click)
        
        # Click derecho para menú contextual
        self.tabla.bind("<Button-3>", self._handle_click_derecho)
        
        # Copiar con Ctrl+C
        self.tabla.bind("<Control-c>", lambda e: self._copiar_seleccion())
        
        # Selección por arrastre
        self.tabla.bind("<Button-1>", self._on_click_inicio)
        self.tabla.bind("<B1-Motion>", self._on_arrastre_mouse)
        self.tabla.bind("<ButtonRelease-1>", self._on_click_fin)
        
        # Cambio de selección
        self.tabla.bind("<<TreeviewSelect>>", self._handle_seleccion_cambio)
        
        # Atajos de teclado
        self.tabla.bind("<Control-a>", lambda e: self.seleccionar_todos())
        self.tabla.bind("<Escape>", lambda e: self.deseleccionar_todos())
    
    def actualizar(self, registros: List[RegistroCorreo]):
        """
        Actualiza la tabla con los registros proporcionados.
        
        Args:
            registros: Lista de registros a mostrar.
        """
        # Limpiar tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        # Insertar registros
        for i, reg in enumerate(registros, start=1):
            vpn_texto = "✓" if reg.vpn else ""
            paises_texto = " ".join(reg.paises) if reg.paises else ""
            
            self.tabla.insert("", tk.END, values=(
                i,
                reg.correo,
                vpn_texto,
                paises_texto,
                reg.notas
            ))
        
        # Notificar cambio de selección (ahora es 0)
        self._handle_seleccion_cambio()
    
    def get_seleccion(self) -> List[Tuple[int, str]]:
        """
        Obtiene los elementos seleccionados.
        
        Returns:
            Lista de tuplas (índice, correo) de elementos seleccionados.
        """
        seleccion = []
        for item_id in self.tabla.selection():
            valores = self.tabla.item(item_id, 'values')
            indice = int(valores[0]) - 1
            correo = valores[1]
            seleccion.append((indice, correo))
        return seleccion
    
    def get_cantidad_seleccionados(self) -> int:
        """Retorna la cantidad de elementos seleccionados."""
        return len(self.tabla.selection())
    
    def seleccionar_todos(self):
        """Selecciona todos los elementos de la tabla."""
        todos_items = self.tabla.get_children()
        if todos_items:
            self.tabla.selection_set(todos_items)
        return "break"
    
    def deseleccionar_todos(self):
        """Deselecciona todos los elementos."""
        self.tabla.selection_remove(self.tabla.selection())
        return "break"
    
    def _copiar_seleccion(self) -> List[str]:
        """
        Obtiene los correos seleccionados para copiar.
        
        Returns:
            Lista de correos seleccionados.
        """
        return [correo for _, correo in self.get_seleccion()]
    
    # ==================== Handlers de eventos ====================
    
    def _handle_doble_click(self, event):
        """Maneja el doble click en una celda."""
        region = self.tabla.identify("region", event.x, event.y)
        if region != "cell":
            return
        
        row_id = self.tabla.identify_row(event.y)
        if not row_id:
            return
        
        valores = self.tabla.item(row_id, 'values')
        indice = int(valores[0]) - 1
        
        if self.on_doble_click:
            self.on_doble_click(indice)
    
    def _handle_click_derecho(self, event):
        """Maneja el click derecho para menú contextual."""
        if self.on_click_derecho:
            self.on_click_derecho(event)
    
    def _handle_seleccion_cambio(self, event=None):
        """Notifica cambios en la selección."""
        if self.on_seleccion_cambio:
            self.on_seleccion_cambio(self.get_cantidad_seleccionados())
    
    # ==================== Selección por arrastre ====================
    
    def _on_click_inicio(self, event):
        """Registra el inicio de un posible arrastre."""
        item = self.tabla.identify_row(event.y)
        
        # Solo activar arrastre si no hay modificadores
        if not (event.state & 0x4 or event.state & 0x1):  # Ctrl=0x4, Shift=0x1
            self._arrastre_inicio_item = item
            self._arrastre_activo = True
    
    def _on_arrastre_mouse(self, event):
        """Maneja la selección por arrastre del mouse."""
        if not self._arrastre_activo or not self._arrastre_inicio_item:
            return
        
        item_actual = self.tabla.identify_row(event.y)
        if not item_actual:
            return
        
        todos_items = self.tabla.get_children()
        if not todos_items:
            return
        
        try:
            indice_inicio = todos_items.index(self._arrastre_inicio_item)
            indice_actual = todos_items.index(item_actual)
        except ValueError:
            return
        
        inicio = min(indice_inicio, indice_actual)
        fin = max(indice_inicio, indice_actual)
        
        self.tabla.selection_set(todos_items[inicio:fin + 1])
    
    def _on_click_fin(self, event):
        """Finaliza la operación de arrastre."""
        self._arrastre_activo = False
    
    def focus_set(self):
        """Establece el foco en la tabla."""
        self.tabla.focus_set()
