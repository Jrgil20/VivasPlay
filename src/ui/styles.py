"""
Configuración de estilos visuales para la aplicación.

Define temas y estilos ttk utilizados en toda la interfaz.
"""

from tkinter import ttk


def configurar_estilos():
    """
    Configura los estilos visuales de la aplicación usando ttk.Style.
    
    Aplica el mejor tema disponible y personaliza los widgets principales.
    """
    style = ttk.Style()
    
    # Seleccionar el mejor tema disponible
    temas_disponibles = style.theme_names()
    if 'clam' in temas_disponibles:
        style.theme_use('clam')
    elif 'vista' in temas_disponibles:
        style.theme_use('vista')
    
    # Configurar estilo de la tabla (Treeview)
    style.configure(
        "Treeview",
        rowheight=28,
        font=('Segoe UI', 10)
    )
    style.configure(
        "Treeview.Heading",
        font=('Segoe UI', 10, 'bold')
    )
    style.map(
        "Treeview",
        background=[('selected', '#0078D4')],
        foreground=[('selected', 'white')]
    )
