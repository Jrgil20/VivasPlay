"""
Clase principal de la aplicación VivasPlay.

Coordina los componentes UI con los servicios de negocio.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import List, Optional

from .models.registro import RegistroCorreo
from .services.parser import ParserCorreos
from .services.storage import StorageJSON
from .config import PATRON_EMAIL, MENSAJES
from .ui.styles import configurar_estilos
from .ui.components.tabla import TablaCorreos
from .ui.components.toolbar import BarraHerramientas
from .ui.components.entrada import PanelEntrada
from .ui.components.menus import MenuContextual
from .ui.dialogs.edicion import DialogoEdicion
from .ui.dialogs.importar import DialogoImportar
from .ui.dialogs.resultado import mostrar_resultado


class VivasPlayApp:
    """
    Clase principal de la aplicación VivasPlay.
    
    Gestiona una lista de registros de correo con interfaz gráfica,
    permitiendo operaciones CRUD y persistencia en archivo JSON.
    """
    
    def __init__(self, root: tk.Tk):
        """
        Inicializa la aplicación VivasPlay.
        
        Args:
            root: Ventana principal de Tkinter.
        """
        self.root = root
        self.root.title("Vivas Play")
        self.root.minsize(700, 400)
        
        # Servicios
        self.storage = StorageJSON()
        
        # Lista de registros en memoria
        self.registros: List[RegistroCorreo] = []
        
        # Configurar estilos antes de crear UI
        configurar_estilos()
        
        # Crear interfaz
        self._crear_interfaz()
        
        # Cargar datos
        self._cargar_registros()
        self._actualizar_vista()
    
    def _crear_interfaz(self):
        """Crea todos los componentes de la interfaz."""
        # Frame principal
        self.marco = tk.Frame(self.root)
        self.marco.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Barra de herramientas
        self.toolbar = BarraHerramientas(self.marco, callbacks={
            'añadir_archivo': self.añadir_desde_archivo,
            'añadir_portapapeles': self.añadir_desde_portapapeles,
            'añadir_ventana': self.añadir_desde_ventana,
            'eliminar_archivo': self.eliminar_desde_archivo,
            'eliminar_portapapeles': self.eliminar_desde_portapapeles,
            'eliminar_ventana': self.eliminar_desde_ventana,
            'contar_archivo': self.contar_desde_archivo,
            'contar_portapapeles': self.contar_desde_portapapeles,
            'contar_ventana': self.contar_desde_ventana,
            'exportar': self.exportar_registros,
            'ver_patron': lambda: messagebox.showinfo("Patrón Email", f"Patrón actual:\n{PATRON_EMAIL}")
        })
        self.toolbar.grid(row=0, column=0, sticky='w', pady=(0, 5))
        
        # Tabla de correos
        self.tabla = TablaCorreos(
            self.marco,
            on_doble_click=self._editar_registro,
            on_seleccion_cambio=self._on_seleccion_cambio,
            on_click_derecho=self._mostrar_menu_contextual
        )
        self.tabla.grid(row=1, column=0, sticky='nsew')
        
        # Panel de entrada
        self.panel_entrada = PanelEntrada(
            self.root,
            on_agregar=self.agregar_correo,
            on_eliminar=self.eliminar_correo
        )
        self.panel_entrada.pack(fill=tk.X, padx=5, pady=5)
        
        # Menú contextual
        self.menu_contextual = MenuContextual(
            self.root,
            on_copiar=self._copiar_seleccion,
            on_copiar_fila=self._copiar_fila_completa,
            on_eliminar=self._eliminar_seleccion,
            on_seleccionar_todos=self.tabla.seleccionar_todos,
            on_deseleccionar=self.tabla.deseleccionar_todos
        )
        
        # Configurar grid
        self.marco.grid_columnconfigure(0, weight=1)
        self.marco.grid_rowconfigure(1, weight=1)
    
    # ==================== Carga y guardado ====================
    
    def _cargar_registros(self):
        """Carga los registros desde el archivo."""
        registros, error = self.storage.cargar_registros()
        self.registros = registros
        
        if error:
            messagebox.showwarning("Advertencia", f"{error}\nSe iniciará con una lista vacía.")
    
    def _guardar_registros(self) -> bool:
        """Guarda los registros en el archivo."""
        exito, error = self.storage.guardar_registros(self.registros)
        if not exito:
            messagebox.showerror("Error", error)
        return exito
    
    def _actualizar_vista(self):
        """Actualiza la tabla y contadores."""
        self.tabla.actualizar(self.registros)
        self.panel_entrada.actualizar_contador(0, len(self.registros))
    
    def _on_seleccion_cambio(self, cantidad: int):
        """Callback cuando cambia la selección."""
        self.panel_entrada.actualizar_contador(cantidad, len(self.registros))
    
    # ==================== Operaciones CRUD ====================
    
    def _obtener_emails_existentes(self) -> set:
        """Obtiene el conjunto de emails base existentes."""
        return {r.get_email_base().lower() for r in self.registros}
    
    def _ejecutar_añadir(self, registros: List[RegistroCorreo], origen: str = ""):
        """Añade registros a la lista."""
        emails_existentes = self._obtener_emails_existentes()
        
        registros_nuevos = []
        for reg in registros:
            email_base = reg.get_email_base().lower()
            if email_base not in emails_existentes:
                registros_nuevos.append(reg)
                emails_existentes.add(email_base)
        
        duplicados = len(registros) - len(registros_nuevos)
        
        if not registros_nuevos:
            messagebox.showinfo(
                "Registros duplicados",
                f"Todos los registros ({len(registros)}) ya existen en la lista."
            )
            return
        
        self.registros.extend(registros_nuevos)
        self._guardar_registros()
        self._actualizar_vista()
        
        mensaje = f"Se insertaron {len(registros_nuevos)} registros."
        if duplicados > 0:
            mensaje += f"\n{duplicados} ya existían y se omitieron."
        
        mostrar_resultado(self.root, f"Resultado - Añadir{origen}", mensaje)
    
    def _ejecutar_eliminar(self, registros: List[RegistroCorreo], origen: str = ""):
        """Elimina registros de la lista."""
        emails_a_eliminar = {r.get_email_base().lower() for r in registros}
        
        registros_originales = len(self.registros)
        self.registros = [
            r for r in self.registros
            if r.get_email_base().lower() not in emails_a_eliminar
        ]
        
        eliminados = registros_originales - len(self.registros)
        no_encontrados = len(registros) - eliminados
        
        self._guardar_registros()
        self._actualizar_vista()
        
        mensaje = f"Se eliminaron {eliminados} registros."
        if no_encontrados > 0:
            mensaje += f"\n{no_encontrados} no existían en la lista."
        
        mostrar_resultado(self.root, f"Resultado - Eliminar{origen}", mensaje)
    
    def _ejecutar_contar(self, registros: List[RegistroCorreo], origen: str = ""):
        """Cuenta y muestra información sobre registros."""
        emails_existentes = self._obtener_emails_existentes()
        
        total = len(registros)
        con_vpn = sum(1 for r in registros if r.vpn)
        con_paises = sum(1 for r in registros if r.paises)
        existentes = sum(1 for r in registros if r.get_email_base().lower() in emails_existentes)
        nuevos = total - existentes
        
        mensaje = f"Se encontraron {total} registros válidos."
        mensaje += f"\n\n• Con VPN: {con_vpn}"
        mensaje += f"\n• Con países: {con_paises}"
        mensaje += f"\n• Ya existen: {existentes}"
        mensaje += f"\n• Nuevos: {nuevos}"
        
        mostrar_resultado(self.root, f"Resultado - Contar{origen}", mensaje)
    
    # ==================== Desde archivo ====================
    
    def _obtener_registros_desde_archivo(self) -> Optional[List[RegistroCorreo]]:
        """Obtiene registros desde un archivo de texto."""
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if not ruta:
            return None
        
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                texto = f.read()
        except IOError as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")
            return None
        
        if not texto.strip():
            messagebox.showinfo(*MENSAJES['archivo_vacio'])
            return None
        
        registros = ParserCorreos.procesar_texto_a_registros(texto)
        
        if not registros:
            messagebox.showwarning(*MENSAJES['sin_correos_validos'])
            return None
        
        return registros
    
    def añadir_desde_archivo(self):
        """Añade registros desde un archivo."""
        registros = self._obtener_registros_desde_archivo()
        if registros:
            self._ejecutar_añadir(registros, " (archivo)")
    
    def eliminar_desde_archivo(self):
        """Elimina registros desde un archivo."""
        registros = self._obtener_registros_desde_archivo()
        if registros:
            self._ejecutar_eliminar(registros, " (archivo)")
    
    def contar_desde_archivo(self):
        """Cuenta registros desde un archivo."""
        registros = self._obtener_registros_desde_archivo()
        if registros:
            self._ejecutar_contar(registros, " (archivo)")
    
    # ==================== Desde portapapeles ====================
    
    def _obtener_registros_desde_portapapeles(self) -> Optional[List[RegistroCorreo]]:
        """Obtiene registros desde el portapapeles."""
        try:
            texto = self.root.clipboard_get()
        except tk.TclError:
            texto = ""
        
        if not texto.strip():
            messagebox.showinfo(*MENSAJES['portapapeles_vacio'])
            return None
        
        registros = ParserCorreos.procesar_texto_a_registros(texto)
        
        if not registros:
            messagebox.showwarning(*MENSAJES['sin_correos_validos'])
            return None
        
        return registros
    
    def añadir_desde_portapapeles(self):
        """Añade registros desde el portapapeles."""
        registros = self._obtener_registros_desde_portapapeles()
        if registros:
            self._ejecutar_añadir(registros, " (portapapeles)")
    
    def eliminar_desde_portapapeles(self):
        """Elimina registros desde el portapapeles."""
        registros = self._obtener_registros_desde_portapapeles()
        if registros:
            self._ejecutar_eliminar(registros, " (portapapeles)")
    
    def contar_desde_portapapeles(self):
        """Cuenta registros desde el portapapeles."""
        registros = self._obtener_registros_desde_portapapeles()
        if registros:
            self._ejecutar_contar(registros, " (portapapeles)")
    
    # ==================== Desde ventana ====================
    
    def añadir_desde_ventana(self):
        """Abre ventana para añadir registros."""
        DialogoImportar(
            self.root,
            "Añadir Registros",
            lambda regs: self._ejecutar_añadir(regs, " (ventana)")
        )
    
    def eliminar_desde_ventana(self):
        """Abre ventana para eliminar registros."""
        DialogoImportar(
            self.root,
            "Eliminar Registros",
            lambda regs: self._ejecutar_eliminar(regs, " (ventana)")
        )
    
    def contar_desde_ventana(self):
        """Abre ventana para contar registros."""
        DialogoImportar(
            self.root,
            "Contar Registros",
            lambda regs: self._ejecutar_contar(regs, " (ventana)")
        )
    
    # ==================== Entrada individual ====================
    
    def agregar_correo(self):
        """Agrega un registro desde el campo de entrada."""
        texto = self.panel_entrada.get_texto()
        
        if not texto:
            return
        
        registro = ParserCorreos.parsear_linea(texto)
        
        if not registro:
            messagebox.showwarning("Entrada inválida", "No se encontró un correo electrónico válido.")
            return
        
        email_base = registro.get_email_base().lower()
        if email_base in self._obtener_emails_existentes():
            messagebox.showinfo("Duplicado", "Este correo ya existe en la lista.")
            return
        
        self.registros.append(registro)
        self._guardar_registros()
        self._actualizar_vista()
        self.panel_entrada.limpiar()
    
    def eliminar_correo(self):
        """Elimina registros según contexto."""
        seleccion = self.tabla.get_seleccion()
        
        # Si hay selección, eliminar seleccionados
        if seleccion:
            self._eliminar_seleccion()
            return
        
        # Si no hay selección, usar campo de entrada
        texto = self.panel_entrada.get_texto()
        
        if not texto:
            messagebox.showinfo(
                "Sin selección",
                "Selecciona elementos en la tabla o escribe un correo en el campo de entrada."
            )
            return
        
        email = ParserCorreos.extraer_email_con_puerto(texto)
        if not email:
            return
        
        email_base = email.split(':')[0].lower() if ':' in email else email.lower()
        
        existe = any(r.get_email_base().lower() == email_base for r in self.registros)
        
        if not existe:
            messagebox.showinfo("No encontrado", "El correo no existe en la lista.")
            return
        
        if not messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Estás seguro de eliminar el correo?\n\n{email}"
        ):
            return
        
        self.registros = [
            r for r in self.registros
            if r.get_email_base().lower() != email_base
        ]
        
        self._guardar_registros()
        self._actualizar_vista()
        self.panel_entrada.limpiar()
    
    # ==================== Exportar ====================
    
    def exportar_registros(self):
        """Exporta los registros a archivo de texto."""
        if not self.registros:
            messagebox.showinfo("Sin datos", "No hay registros para exportar.")
            return
        
        ruta = filedialog.asksaveasfilename(
            title="Exportar registros",
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if not ruta:
            return
        
        try:
            with open(ruta, 'w', encoding='utf-8') as f:
                for reg in self.registros:
                    linea = reg.correo
                    if reg.vpn or reg.paises:
                        linea += " | VPN:" if reg.vpn else " |"
                        if reg.paises:
                            linea += " " + " ".join(reg.paises)
                    if reg.notas:
                        linea += " " + reg.notas
                    f.write(linea.strip() + "\n")
            
            messagebox.showinfo("Éxito", f"Se exportaron {len(self.registros)} registros correctamente.")
        except IOError as e:
            messagebox.showerror("Error", f"No se pudo exportar los registros: {e}")
    
    # ==================== Edición y selección ====================
    
    def _editar_registro(self, indice: int):
        """Abre el diálogo de edición para un registro."""
        if 0 <= indice < len(self.registros):
            DialogoEdicion(
                self.root,
                self.registros[indice],
                on_guardar=lambda reg: self._guardar_edicion(indice, reg),
                on_eliminar=lambda: self._eliminar_registro(indice)
            )
    
    def _guardar_edicion(self, indice: int, registro: RegistroCorreo):
        """Guarda los cambios de edición."""
        self.registros[indice] = registro
        self._guardar_registros()
        self._actualizar_vista()
    
    def _eliminar_registro(self, indice: int):
        """Elimina un registro por índice."""
        self.registros.pop(indice)
        self._guardar_registros()
        self._actualizar_vista()
    
    def _eliminar_seleccion(self):
        """Elimina los registros seleccionados."""
        seleccion = self.tabla.get_seleccion()
        if not seleccion:
            return
        
        cantidad = len(seleccion)
        
        # Mensaje de confirmación
        if cantidad == 1:
            correo = seleccion[0][1]
            mensaje = f"¿Estás seguro de eliminar este correo?\n\n{correo}"
            titulo = "Confirmar eliminación"
        else:
            mensaje = f"¿Estás seguro de eliminar {cantidad} correos seleccionados?\n\nEsta acción no se puede deshacer."
            titulo = "Confirmar eliminación múltiple"
        
        if not messagebox.askyesno(titulo, mensaje):
            return
        
        # Eliminar por índices
        indices_a_eliminar = {idx for idx, _ in seleccion}
        self.registros = [
            reg for i, reg in enumerate(self.registros)
            if i not in indices_a_eliminar
        ]
        
        self._guardar_registros()
        self._actualizar_vista()
        
        if cantidad == 1:
            messagebox.showinfo("Eliminado", "El correo ha sido eliminado.")
        else:
            messagebox.showinfo("Eliminados", f"Se han eliminado {cantidad} correos.")
    
    def _mostrar_menu_contextual(self, event):
        """Muestra el menú contextual."""
        cantidad = self.tabla.get_cantidad_seleccionados()
        self.menu_contextual.mostrar(event, cantidad)
    
    def _copiar_seleccion(self):
        """Copia los correos seleccionados al portapapeles."""
        seleccion = self.tabla.get_seleccion()
        if seleccion:
            correos = [correo for _, correo in seleccion]
            self.root.clipboard_clear()
            self.root.clipboard_append('\n'.join(correos))
    
    def _copiar_fila_completa(self):
        """Copia las filas completas seleccionadas."""
        seleccion = self.tabla.get_seleccion()
        if seleccion:
            filas = []
            for idx, _ in seleccion:
                reg = self.registros[idx]
                linea = reg.correo
                if reg.vpn or reg.paises:
                    linea += " | VPN:" if reg.vpn else " |"
                    if reg.paises:
                        linea += " " + " ".join(reg.paises)
                if reg.notas:
                    linea += " " + reg.notas
                filas.append(linea.strip())
            
            self.root.clipboard_clear()
            self.root.clipboard_append('\n'.join(filas))
