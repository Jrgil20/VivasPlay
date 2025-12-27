"""
Barra de herramientas con acciones principales.

Contiene botones con menús desplegables para las operaciones
de añadir, eliminar, contar y exportar registros.
"""

import tkinter as tk
from tkinter import ttk
import os
from typing import Dict, Callable, Optional

from ...config import ICONOS


class BarraHerramientas(ttk.Frame):
    """
    Barra de herramientas con botones de acción.
    
    Attributes:
        callbacks: Diccionario con las funciones callback para cada acción.
    """
    
    def __init__(self, parent, callbacks: Dict[str, Callable]):
        """
        Inicializa la barra de herramientas.
        
        Args:
            parent: Widget padre.
            callbacks: Diccionario con callbacks para las acciones:
                - añadir_archivo, añadir_portapapeles, añadir_ventana
                - eliminar_archivo, eliminar_portapapeles, eliminar_ventana
                - contar_archivo, contar_portapapeles, contar_ventana
                - exportar
                - ver_patron
        """
        super().__init__(parent)
        
        self.callbacks = callbacks
        self.iconos_cargados = {}
        
        self._cargar_iconos()
        self._crear_widgets()
    
    def _cargar_iconos(self):
        """Carga los iconos necesarios para los botones."""
        for nombre, ruta in ICONOS.items():
            try:
                if os.path.exists(ruta):
                    self.iconos_cargados[nombre] = tk.PhotoImage(file=ruta)
                else:
                    self.iconos_cargados[nombre] = None
            except tk.TclError:
                self.iconos_cargados[nombre] = None
    
    def _crear_widgets(self):
        """Crea los botones y menús de la barra."""
        # Botón de acciones (clip)
        icono_clip = self.iconos_cargados.get('clip')
        if icono_clip:
            self.boton_archivo = tk.Button(self, image=icono_clip)
            self.boton_archivo.image = icono_clip
        else:
            self.boton_archivo = ttk.Button(self, text="📎 Acciones")
        
        self.boton_archivo.pack(side=tk.LEFT, padx=2)
        
        # Menú de acciones
        self.menu_archivo = tk.Menu(self, tearoff=0)
        self._crear_menu_acciones()
        self.boton_archivo.bind("<Button-1>", self._mostrar_menu_archivo)
        
        # Botón de configuración (mail)
        icono_mail = self.iconos_cargados.get('mail')
        if icono_mail:
            self.boton_config = tk.Button(self, image=icono_mail)
            self.boton_config.image = icono_mail
        else:
            self.boton_config = ttk.Button(self, text="✉️ Config")
        
        self.boton_config.pack(side=tk.LEFT, padx=2)
        
        # Menú de configuración
        self.menu_config = tk.Menu(self, tearoff=0)
        self.menu_config.add_command(
            label="Ver patrón Email",
            command=self.callbacks.get('ver_patron', lambda: None)
        )
        self.boton_config.bind("<Button-1>", self._mostrar_menu_config)
    
    def _crear_menu_acciones(self):
        """Crea el menú de acciones con submenús."""
        # Submenú Añadir
        submenu_añadir = tk.Menu(self.menu_archivo, tearoff=0)
        submenu_añadir.add_command(
            label="Desde archivo...",
            command=self.callbacks.get('añadir_archivo', lambda: None)
        )
        submenu_añadir.add_command(
            label="Desde portapapeles",
            command=self.callbacks.get('añadir_portapapeles', lambda: None)
        )
        submenu_añadir.add_command(
            label="Desde ventana...",
            command=self.callbacks.get('añadir_ventana', lambda: None)
        )
        self.menu_archivo.add_cascade(label="Añadir registros", menu=submenu_añadir)
        
        # Submenú Eliminar
        submenu_eliminar = tk.Menu(self.menu_archivo, tearoff=0)
        submenu_eliminar.add_command(
            label="Desde archivo...",
            command=self.callbacks.get('eliminar_archivo', lambda: None)
        )
        submenu_eliminar.add_command(
            label="Desde portapapeles",
            command=self.callbacks.get('eliminar_portapapeles', lambda: None)
        )
        submenu_eliminar.add_command(
            label="Desde ventana...",
            command=self.callbacks.get('eliminar_ventana', lambda: None)
        )
        self.menu_archivo.add_cascade(label="Eliminar registros", menu=submenu_eliminar)
        
        # Submenú Contar
        submenu_contar = tk.Menu(self.menu_archivo, tearoff=0)
        submenu_contar.add_command(
            label="Desde archivo...",
            command=self.callbacks.get('contar_archivo', lambda: None)
        )
        submenu_contar.add_command(
            label="Desde portapapeles",
            command=self.callbacks.get('contar_portapapeles', lambda: None)
        )
        submenu_contar.add_command(
            label="Desde ventana...",
            command=self.callbacks.get('contar_ventana', lambda: None)
        )
        self.menu_archivo.add_cascade(label="Contar registros", menu=submenu_contar)
        
        self.menu_archivo.add_separator()
        self.menu_archivo.add_command(
            label="Exportar registros...",
            command=self.callbacks.get('exportar', lambda: None)
        )
    
    def _mostrar_menu_archivo(self, event):
        """Muestra el menú de acciones."""
        self.menu_archivo.post(event.x_root, event.y_root)
    
    def _mostrar_menu_config(self, event):
        """Muestra el menú de configuración."""
        self.menu_config.post(event.x_root, event.y_root)
