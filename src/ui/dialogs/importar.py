"""
Diálogo para importar registros desde texto.

Permite pegar texto con múltiples registros y procesarlos.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, List

from ...models.registro import RegistroCorreo
from ...services.parser import ParserCorreos
from ...config import MENSAJES


class DialogoImportar:
    """
    Diálogo para importar registros desde texto pegado.
    
    Características:
    - Área de texto para pegar contenido
    - Pega automáticamente desde portapapeles
    - Procesa múltiples formatos de entrada
    """
    
    def __init__(
        self,
        parent: tk.Tk,
        titulo: str,
        on_procesar: Callable[[List[RegistroCorreo]], None]
    ):
        """
        Inicializa el diálogo de importación.
        
        Args:
            parent: Ventana padre.
            titulo: Título de la ventana.
            on_procesar: Callback con los registros procesados.
        """
        self.parent = parent
        self.titulo = titulo
        self.on_procesar = on_procesar
        
        self._crear_dialogo()
    
    def _crear_dialogo(self):
        """Crea y muestra el diálogo."""
        self.dialogo = tk.Toplevel(self.parent)
        self.dialogo.title(self.titulo)
        self.dialogo.transient(self.parent)
        self.dialogo.grab_set()
        self.dialogo.geometry("700x450")
        
        # Frame principal
        frame_principal = ttk.Frame(self.dialogo, padding=10)
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Instrucciones
        instrucciones = (
            "Pega los registros (uno por línea).\n"
            "Formatos soportados:\n"
            "  • correo:puerto | VPN: PAIS notas\n"
            "  • correo — PAIS\n"
            "  • correo | VPN: PAIS1 PAIS2"
        )
        ttk.Label(
            frame_principal,
            text=instrucciones,
            justify=tk.LEFT,
            font=('Consolas', 9)
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # Área de texto con scrollbar
        frame_texto = ttk.Frame(frame_principal)
        frame_texto.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        scrollbar = ttk.Scrollbar(frame_texto)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.texto_area = tk.Text(
            frame_texto,
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set,
            font=('Consolas', 10)
        )
        self.texto_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.texto_area.yview)
        self.texto_area.focus_set()
        
        # Intentar pegar automáticamente desde portapapeles
        self._pegar_portapapeles()
        
        # Frame de botones
        frame_botones = ttk.Frame(frame_principal)
        frame_botones.pack(fill=tk.X)
        
        ttk.Button(
            frame_botones,
            text="Procesar",
            command=self._procesar
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            frame_botones,
            text="Cancelar",
            command=self.dialogo.destroy
        ).pack(side=tk.LEFT, padx=5)
        
        # Atajo Ctrl+Enter para procesar
        self.texto_area.bind("<Control-Return>", lambda e: self._procesar())
    
    def _pegar_portapapeles(self):
        """Intenta pegar contenido del portapapeles automáticamente."""
        try:
            contenido = self.parent.clipboard_get()
            if contenido.strip():
                self.texto_area.insert("1.0", contenido)
                self.texto_area.tag_add("sel", "1.0", tk.END)
        except tk.TclError:
            pass
    
    def _procesar(self):
        """Procesa el texto y llama al callback."""
        texto = self.texto_area.get("1.0", tk.END).strip()
        
        if not texto:
            messagebox.showwarning(
                "Texto vacío",
                "Por favor, pega los registros en el área de texto."
            )
            return
        
        registros = ParserCorreos.procesar_texto_a_registros(texto)
        
        if not registros:
            messagebox.showwarning(*MENSAJES['sin_correos_validos'])
            return
        
        self.dialogo.destroy()
        self.on_procesar(registros)
