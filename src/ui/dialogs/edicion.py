"""
Diálogo para editar un registro de correo.

Permite modificar todos los campos de un registro existente.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional

from ...models.registro import RegistroCorreo
from ...services.parser import ParserCorreos
from ...config import CODIGOS_PAIS


class DialogoEdicion:
    """
    Diálogo modal para editar un registro de correo.
    
    Permite modificar: correo, VPN, países y notas.
    """
    
    def __init__(
        self,
        parent: tk.Tk,
        registro: RegistroCorreo,
        on_guardar: Optional[Callable[[RegistroCorreo], None]] = None,
        on_eliminar: Optional[Callable[[], None]] = None
    ):
        """
        Inicializa el diálogo de edición.
        
        Args:
            parent: Ventana padre.
            registro: Registro a editar.
            on_guardar: Callback al guardar cambios.
            on_eliminar: Callback al eliminar el registro.
        """
        self.parent = parent
        self.registro = registro
        self.on_guardar = on_guardar
        self.on_eliminar = on_eliminar
        
        self._crear_dialogo()
    
    def _crear_dialogo(self):
        """Crea y muestra el diálogo."""
        self.dialogo = tk.Toplevel(self.parent)
        self.dialogo.title("Editar Registro")
        self.dialogo.transient(self.parent)
        self.dialogo.grab_set()
        self.dialogo.geometry("500x300")
        
        frame = ttk.Frame(self.dialogo, padding=15)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Correo
        ttk.Label(frame, text="Correo:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entrada_correo = ttk.Entry(frame, width=50)
        self.entrada_correo.grid(row=0, column=1, columnspan=2, sticky=tk.EW, pady=5)
        self.entrada_correo.insert(0, self.registro.correo)
        
        # VPN
        self.var_vpn = tk.BooleanVar(value=self.registro.vpn)
        ttk.Label(frame, text="VPN:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Checkbutton(frame, variable=self.var_vpn).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Países
        ttk.Label(frame, text="Países:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entrada_paises = ttk.Entry(frame, width=50)
        self.entrada_paises.grid(row=2, column=1, columnspan=2, sticky=tk.EW, pady=5)
        self.entrada_paises.insert(0, " ".join(self.registro.paises))
        ttk.Label(
            frame,
            text="(separados por espacio, ej: BR US CA)",
            font=('Segoe UI', 8)
        ).grid(row=3, column=1, sticky=tk.W)
        
        # Notas
        ttk.Label(frame, text="Notas:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.entrada_notas = ttk.Entry(frame, width=50)
        self.entrada_notas.grid(row=4, column=1, columnspan=2, sticky=tk.EW, pady=5)
        self.entrada_notas.insert(0, self.registro.notas)
        
        frame.grid_columnconfigure(1, weight=1)
        
        # Botones
        frame_botones = ttk.Frame(frame)
        frame_botones.grid(row=5, column=0, columnspan=3, pady=20)
        
        ttk.Button(frame_botones, text="Guardar", command=self._guardar).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Eliminar", command=self._eliminar).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Cancelar", command=self.dialogo.destroy).pack(side=tk.LEFT, padx=5)
    
    def _guardar(self):
        """Valida y guarda los cambios."""
        nuevo_correo = self.entrada_correo.get().strip()
        correo_extraido = ParserCorreos.extraer_email_con_puerto(nuevo_correo)
        
        if not correo_extraido:
            messagebox.showwarning("Error", "El correo no es válido.")
            return
        
        # Validar países
        texto_paises = self.entrada_paises.get().strip().upper()
        nuevos_paises = [p for p in texto_paises.split() if p in CODIGOS_PAIS]
        
        nuevo_registro = RegistroCorreo(
            correo=correo_extraido,
            vpn=self.var_vpn.get(),
            paises=nuevos_paises,
            notas=self.entrada_notas.get().strip()
        )
        
        if self.on_guardar:
            self.on_guardar(nuevo_registro)
        
        self.dialogo.destroy()
    
    def _eliminar(self):
        """Elimina el registro."""
        if self.on_eliminar:
            self.on_eliminar()
        self.dialogo.destroy()
