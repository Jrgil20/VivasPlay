"""
VivasPlay - Aplicación de gestión de correos electrónicos.

Esta aplicación permite gestionar una lista de correos electrónicos,
incluyendo funcionalidades para añadir, eliminar, contar y exportar correos.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import re
import json
import os


class VivasPlayApp:
    """
    Clase principal de la aplicación VivasPlay.
    
    Gestiona una lista de correos electrónicos con interfaz gráfica,
    permitiendo operaciones CRUD y persistencia en archivo JSON.
    """
    
    # Constantes de configuración
    ARCHIVO_DATOS = 'correos.json'
    PATRON_EMAIL = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Rutas de iconos
    ICONOS = {
        'clip': 'assets/image/clip_2891632.png',
        'mail': 'assets/image/mail_1849441.png',
        'eliminar': 'assets/image/remove_13922476.png',
        'copiar': 'assets/image/file_5632095.png'
    }
    
    def __init__(self, root: tk.Tk):
        """
        Inicializa la aplicación VivasPlay.
        
        Args:
            root: Ventana principal de Tkinter.
        """
        self.root = root
        self.root.title("Vivas Play")
        self.root.minsize(400, 300)
        
        # Lista de correos en memoria
        self.correos = []
        
        # Referencias a iconos (evitar garbage collection)
        self.iconos_cargados = {}
        
        # Cargar datos y configurar interfaz
        self._cargar_correos()
        self._configurar_estilos()
        self._crear_interfaz()
        self._actualizar_tabla()
    
    def _configurar_estilos(self):
        """Configura los estilos visuales de la aplicación usando ttk.Style."""
        style = ttk.Style()
        
        # Usar tema más moderno según disponibilidad
        temas_disponibles = style.theme_names()
        if 'clam' in temas_disponibles:
            style.theme_use('clam')
        elif 'vista' in temas_disponibles:
            style.theme_use('vista')
        
        # Configurar estilo de la tabla
        style.configure(
            "Treeview",
            rowheight=28,
            font=('Segoe UI', 10)
        )
        style.configure(
            "Treeview.Heading",
            font=('Segoe UI', 10, 'bold')
        )
        
        # Configurar colores de selección
        style.map(
            "Treeview",
            background=[('selected', '#0078D4')],
            foreground=[('selected', 'white')]
        )
    
    def _cargar_iconos(self):
        """
        Carga los iconos necesarios para la interfaz.
        
        Returns:
            dict: Diccionario con los iconos cargados.
        """
        for nombre, ruta in self.ICONOS.items():
            try:
                if os.path.exists(ruta):
                    self.iconos_cargados[nombre] = tk.PhotoImage(file=ruta)
                else:
                    self.iconos_cargados[nombre] = None
            except tk.TclError:
                self.iconos_cargados[nombre] = None
    
    def _cargar_correos(self):
        """
        Carga los correos desde el archivo JSON.
        
        Si el archivo no existe o está corrupto, inicializa una lista vacía.
        """
        try:
            if os.path.exists(self.ARCHIVO_DATOS):
                with open(self.ARCHIVO_DATOS, 'r', encoding='utf-8') as f:
                    self.correos = json.load(f)
            else:
                self.correos = []
                self._guardar_correos()
        except (json.JSONDecodeError, IOError) as e:
            messagebox.showwarning(
                "Advertencia",
                f"No se pudo cargar el archivo de correos: {e}\nSe iniciará con una lista vacía."
            )
            self.correos = []
    
    def _guardar_correos(self):
        """
        Guarda los correos en el archivo JSON.
        
        Returns:
            bool: True si se guardó correctamente, False en caso contrario.
        """
        try:
            with open(self.ARCHIVO_DATOS, 'w', encoding='utf-8') as f:
                json.dump(self.correos, f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            messagebox.showerror(
                "Error",
                f"No se pudo guardar el archivo de correos: {e}"
            )
            return False
    
    def _actualizar_tabla(self):
        """Recarga la tabla con los correos actuales."""
        # Limpiar tabla existente
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        # Insertar correos con enumeración
        for i, correo in enumerate(self.correos, start=1):
            self.tabla.insert("", tk.END, values=(i, correo))
    
    def validar_correo(self, correo: str) -> bool:
        """
        Valida si un string tiene formato de correo electrónico válido.
        
        Args:
            correo: String a validar.
            
        Returns:
            True si el formato es válido, False en caso contrario.
        """
        if not correo:
            return False
        return bool(re.match(self.PATRON_EMAIL, correo))
    
    def _leer_archivo_externo(self) -> list:
        """
        Abre un diálogo para seleccionar y leer un archivo de texto.
        
        Returns:
            Lista de líneas del archivo, o lista vacía si se cancela.
        """
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if not ruta:
            return []
        
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                return f.read().splitlines()
        except IOError as e:
            messagebox.showerror(
                "Error",
                f"No se pudo leer el archivo: {e}"
            )
            return []
    
    def _crear_interfaz(self):
        """Crea todos los elementos de la interfaz gráfica."""
        # Cargar iconos
        self._cargar_iconos()
        
        # Marco principal
        self.marco = tk.Frame(self.root)
        self.marco.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Crear barra de herramientas
        self._crear_barra_herramientas()
        
        # Crear tabla de correos
        self._crear_tabla()
        
        # Crear panel inferior de entrada
        self._crear_panel_entrada()
        
        # Configurar expansión del grid
        self.marco.grid_columnconfigure(0, weight=1)
        self.marco.grid_rowconfigure(1, weight=1)
    
    def _crear_barra_herramientas(self):
        """Crea la barra de herramientas con botones de acción."""
        barra = ttk.Frame(self.marco)
        barra.grid(row=0, column=0, sticky='w', pady=(0, 5))
        
        # Botón de archivo (clip)
        icono_clip = self.iconos_cargados.get('clip')
        if icono_clip:
            self.boton_archivo = tk.Button(barra, image=icono_clip)
            self.boton_archivo.image = icono_clip
        else:
            self.boton_archivo = ttk.Button(barra, text="📎 Archivo")
        
        self.boton_archivo.pack(side=tk.LEFT, padx=2)
        
        # Menú contextual para botón archivo
        self.menu_archivo = tk.Menu(self.root, tearoff=0)
        self.menu_archivo.add_command(
            label="Añadir correos mediante archivo",
            command=self.añadir_desde_archivo
        )
        self.menu_archivo.add_command(
            label="Eliminar correos mediante archivo",
            command=self.eliminar_desde_archivo
        )
        self.menu_archivo.add_command(
            label="Contar correos mediante archivo",
            command=self.contar_correos_archivo
        )
        self.menu_archivo.add_separator()
        self.menu_archivo.add_command(
            label="Exportar correos",
            command=self.exportar_correos
        )
        
        self.boton_archivo.bind("<Button-1>", self._mostrar_menu_archivo)
        
        # Botón de configuración (mail)
        icono_mail = self.iconos_cargados.get('mail')
        if icono_mail:
            self.boton_config = tk.Button(barra, image=icono_mail)
            self.boton_config.image = icono_mail
        else:
            self.boton_config = ttk.Button(barra, text="✉️ Config")
        
        self.boton_config.pack(side=tk.LEFT, padx=2)
        
        # Menú de configuración
        self.menu_config = tk.Menu(self.root, tearoff=0)
        self.menu_config.add_command(
            label="Correos Regex",
            command=lambda: messagebox.showinfo("Info", "Configuración de Regex")
        )
        
        self.boton_config.bind("<Button-1>", self._mostrar_menu_config)
    
    def _crear_tabla(self):
        """Crea la tabla de correos con scrollbar."""
        # Frame contenedor para tabla y scrollbar
        frame_tabla = ttk.Frame(self.marco)
        frame_tabla.grid(row=1, column=0, sticky='nsew')
        frame_tabla.grid_columnconfigure(0, weight=1)
        frame_tabla.grid_rowconfigure(0, weight=1)
        
        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL)
        scrollbar.grid(row=0, column=1, sticky='ns')
        
        # Tabla de correos
        self.tabla = ttk.Treeview(
            frame_tabla,
            columns=("Enumeración", "Correo"),
            yscrollcommand=scrollbar.set,
            selectmode='extended'
        )
        
        scrollbar.config(command=self.tabla.yview)
        
        # Configurar columnas
        self.tabla.column("#0", width=0, stretch=tk.NO)
        self.tabla.column("Enumeración", width=60, anchor=tk.CENTER)
        self.tabla.column("Correo", width=300, anchor=tk.W)
        
        # Configurar encabezados
        self.tabla.heading("Enumeración", text="No.")
        self.tabla.heading("Correo", text="Correo")
        
        self.tabla.grid(row=0, column=0, sticky='nsew')
        
        # Bindings de la tabla
        self.tabla.bind("<Double-Button-1>", self._on_doble_click)
        self.tabla.bind("<Button-3>", self._mostrar_menu_contextual)
        self.tabla.bind("<Control-c>", self._copiar_seleccion)
        
        # Menú contextual de la tabla
        self.menu_contextual = tk.Menu(self.root, tearoff=0)
        self.menu_contextual.add_command(
            label="Copiar valor",
            command=self._copiar_seleccion
        )
        self.menu_contextual.add_command(
            label="Eliminar selección",
            command=self._eliminar_seleccion
        )
    
    def _crear_panel_entrada(self):
        """Crea el panel inferior con campo de entrada y botones."""
        panel = ttk.Frame(self.root)
        panel.pack(fill=tk.X, padx=5, pady=5)
        
        # Etiqueta
        ttk.Label(panel, text="Correo:").pack(side=tk.LEFT, padx=(0, 5))
        
        # Campo de entrada
        self.entrada_correo = ttk.Entry(panel, width=40)
        self.entrada_correo.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.entrada_correo.bind("<Return>", lambda e: self.agregar_correo())
        
        # Botones
        ttk.Button(
            panel,
            text="Agregar",
            command=self.agregar_correo
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            panel,
            text="Eliminar",
            command=self.eliminar_correo
        ).pack(side=tk.LEFT, padx=2)
    
    def _mostrar_menu_archivo(self, event):
        """Muestra el menú contextual del botón archivo."""
        self.menu_archivo.post(event.x_root, event.y_root)
    
    def _mostrar_menu_config(self, event):
        """Muestra el menú contextual del botón configuración."""
        self.menu_config.post(event.x_root, event.y_root)
    
    def _mostrar_menu_contextual(self, event):
        """Muestra el menú contextual de la tabla."""
        self.menu_contextual.post(event.x_root, event.y_root)
    
    def _copiar_seleccion(self, event=None):
        """Copia los correos seleccionados al portapapeles."""
        seleccion = self.tabla.selection()
        if seleccion:
            correos = [self.tabla.item(sel, 'values')[1] for sel in seleccion]
            self.root.clipboard_clear()
            self.root.clipboard_append('\n'.join(correos))
    
    def _eliminar_seleccion(self):
        """Elimina los correos seleccionados de la tabla y la lista."""
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        
        for sel in seleccion:
            correo = self.tabla.item(sel, 'values')[1]
            if correo in self.correos:
                self.correos.remove(correo)
        
        self._guardar_correos()
        self._actualizar_tabla()
    
    def _on_doble_click(self, event):
        """Maneja el doble click en una celda para editar."""
        region = self.tabla.identify("region", event.x, event.y)
        if region != "cell":
            return
        
        row_id = self.tabla.identify_row(event.y)
        col = self.tabla.identify_column(event.x)
        
        if not row_id or not col:
            return
        
        item = self.tabla.item(row_id)
        col_index = int(col.replace("#", "")) - 1
        
        if col_index >= len(item['values']):
            return
        
        texto_original = item['values'][col_index]
        self._mostrar_dialogo_edicion(row_id, col_index, texto_original)
    
    def _mostrar_dialogo_edicion(self, row_id: str, col_index: int, texto_original: str):
        """
        Muestra un diálogo para editar el valor de una celda.
        
        Args:
            row_id: ID de la fila en la tabla.
            col_index: Índice de la columna.
            texto_original: Texto actual de la celda.
        """
        dialogo = tk.Toplevel(self.root)
        dialogo.title("Editar valor")
        dialogo.transient(self.root)
        dialogo.grab_set()
        
        # Campo de entrada
        frame_entrada = ttk.Frame(dialogo)
        frame_entrada.pack(padx=10, pady=10, fill=tk.X)
        
        entrada = ttk.Entry(frame_entrada, width=50)
        entrada.pack(fill=tk.X)
        entrada.insert(0, texto_original)
        entrada.select_range(0, tk.END)
        entrada.focus_set()
        
        # Botones
        frame_botones = ttk.Frame(dialogo)
        frame_botones.pack(padx=10, pady=(0, 10))
        
        def copiar():
            self.root.clipboard_clear()
            self.root.clipboard_append(entrada.get())
        
        def eliminar():
            self.tabla.delete(row_id)
            if col_index == 1 and texto_original in self.correos:
                self.correos.remove(texto_original)
                self._guardar_correos()
            dialogo.destroy()
        
        def guardar():
            nuevo_texto = entrada.get().strip()
            if nuevo_texto and nuevo_texto != texto_original:
                values = list(self.tabla.item(row_id, 'values'))
                values[col_index] = nuevo_texto
                self.tabla.item(row_id, values=tuple(values))
                
                if col_index == 1:
                    try:
                        index = self.correos.index(texto_original)
                        self.correos[index] = nuevo_texto
                        self._guardar_correos()
                    except ValueError:
                        pass
            dialogo.destroy()
        
        # Cargar iconos para botones si están disponibles
        icono_copiar = self.iconos_cargados.get('copiar')
        icono_eliminar = self.iconos_cargados.get('eliminar')
        
        if icono_copiar:
            btn_copiar = tk.Button(frame_botones, image=icono_copiar, command=copiar)
            btn_copiar.image = icono_copiar
        else:
            btn_copiar = ttk.Button(frame_botones, text="Copiar", command=copiar)
        btn_copiar.pack(side=tk.LEFT, padx=5)
        
        if icono_eliminar:
            btn_eliminar = tk.Button(frame_botones, image=icono_eliminar, command=eliminar)
            btn_eliminar.image = icono_eliminar
        else:
            btn_eliminar = ttk.Button(frame_botones, text="Eliminar", command=eliminar)
        btn_eliminar.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(frame_botones, text="Guardar", command=guardar).pack(side=tk.LEFT, padx=5)
        
        # Binding para Enter
        entrada.bind("<Return>", lambda e: guardar())
    
    def _mostrar_resultado(self, titulo: str, mensaje: str):
        """
        Muestra una ventana con el resultado de una operación.
        
        Args:
            titulo: Título de la ventana.
            mensaje: Mensaje a mostrar.
        """
        dialogo = tk.Toplevel(self.root)
        dialogo.title(titulo)
        dialogo.transient(self.root)
        
        ttk.Label(dialogo, text=mensaje).pack(padx=20, pady=20)
        ttk.Button(dialogo, text="Aceptar", command=dialogo.destroy).pack(pady=(0, 10))
    
    # ==================== Operaciones con correos ====================
    
    def agregar_correo(self):
        """Agrega un correo desde el campo de entrada."""
        correo = self.entrada_correo.get().strip()
        
        if not correo:
            return
        
        if not self.validar_correo(correo):
            messagebox.showwarning(
                "Correo inválido",
                "El formato del correo no es válido."
            )
            return
        
        if correo in self.correos:
            messagebox.showinfo(
                "Duplicado",
                "Este correo ya existe en la lista."
            )
            return
        
        self.correos.append(correo)
        self._guardar_correos()
        self._actualizar_tabla()
        self.entrada_correo.delete(0, tk.END)
    
    def eliminar_correo(self):
        """Elimina un correo desde el campo de entrada."""
        correo = self.entrada_correo.get().strip()
        
        if not correo:
            return
        
        if correo in self.correos:
            self.correos.remove(correo)
            self._guardar_correos()
            self._actualizar_tabla()
            self.entrada_correo.delete(0, tk.END)
        else:
            messagebox.showinfo(
                "No encontrado",
                "El correo no existe en la lista."
            )
    
    def añadir_desde_archivo(self):
        """Añade correos desde un archivo de texto externo."""
        lineas = self._leer_archivo_externo()
        
        if not lineas:
            return
        
        # Filtrar y validar correos
        correos_validos = []
        for linea in lineas:
            correo = linea.strip()
            if correo and self.validar_correo(correo) and correo not in self.correos:
                correos_validos.append(correo)
        
        # Agregar correos válidos
        self.correos.extend(correos_validos)
        self._guardar_correos()
        self._actualizar_tabla()
        
        self._mostrar_resultado(
            "Resultado de la inserción",
            f"Se insertaron {len(correos_validos)} correos válidos."
        )
    
    def eliminar_desde_archivo(self):
        """Elimina correos listados en un archivo de texto externo."""
        lineas = self._leer_archivo_externo()
        
        if not lineas:
            return
        
        eliminados = 0
        for linea in lineas:
            correo = linea.strip()
            if correo in self.correos:
                self.correos.remove(correo)
                eliminados += 1
        
        self._guardar_correos()
        self._actualizar_tabla()
        
        self._mostrar_resultado(
            "Resultado de la eliminación",
            f"Se eliminaron {eliminados} correos."
        )
    
    def contar_correos_archivo(self):
        """Cuenta los correos válidos en un archivo de texto externo."""
        lineas = self._leer_archivo_externo()
        
        if not lineas:
            return
        
        correos_validos = sum(
            1 for linea in lineas
            if linea.strip() and self.validar_correo(linea.strip())
        )
        
        self._mostrar_resultado(
            "Resultado del conteo",
            f"Se encontraron {correos_validos} correos válidos en el archivo."
        ) 
                "Sin datos",
                "No hay correos para exportar."
            )
            return
        
        ruta = filedialog.asksaveasfilename(
            title="Exportar correos",
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if not ruta:
            return
        
        try:
            with open(ruta, 'w', encoding='utf-8') as f:
                f.write('\n'.join(self.correos))
            
            messagebox.showinfo(
                "Éxito",
                f"Se exportaron {len(self.correos)} correos correctamente."
            )
        except IOError as e:
            messagebox.showerror(
                "Error",
                f"No se pudo exportar los correos: {e}"
            )


def main():
    """Punto de entrada principal de la aplicación."""
    root = tk.Tk()
    app = VivasPlayApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
