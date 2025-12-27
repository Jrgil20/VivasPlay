"""
VivasPlay - Aplicación de gestión de correos electrónicos.

Esta aplicación permite gestionar una lista de correos electrónicos con:
- Correo con puerto opcional (correo:puerto)
- Estado VPN (booleano)
- Países asociados (lista)
- Notas adicionales

Estructura modular en src/:
- models/: Modelo de datos (RegistroCorreo)
- services/: Lógica de negocio (parser, storage)
- ui/: Interfaz gráfica (componentes, diálogos)
"""

import tkinter as tk
from src.app import VivasPlayApp


def main():
    """Punto de entrada principal de la aplicación."""
    root = tk.Tk()
    app = VivasPlayApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
