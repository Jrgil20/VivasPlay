"""
Servicio de persistencia de datos en JSON.

Maneja la carga y guardado de registros en archivo JSON,
incluyendo compatibilidad con formatos anteriores.
"""

import json
import os
from typing import List, Tuple, Optional

from ..models.registro import RegistroCorreo
from ..config import ARCHIVO_DATOS


class StorageJSON:
    """
    Gestiona la persistencia de registros en archivo JSON.
    
    Attributes:
        archivo: Ruta al archivo de datos.
    """
    
    def __init__(self, archivo: str = ARCHIVO_DATOS):
        """
        Inicializa el storage.
        
        Args:
            archivo: Ruta al archivo JSON de datos.
        """
        self.archivo = archivo
    
    def cargar_registros(self) -> Tuple[List[RegistroCorreo], Optional[str]]:
        """
        Carga los registros desde el archivo JSON.
        
        Soporta formato legacy (lista de strings) y formato actual (lista de dicts).
        
        Returns:
            Tupla con (lista de registros, mensaje de error o None si éxito).
        """
        registros = []
        error = None
        
        try:
            if os.path.exists(self.archivo):
                with open(self.archivo, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                    
                    if isinstance(datos, list):
                        for item in datos:
                            if isinstance(item, dict):
                                registros.append(RegistroCorreo.from_dict(item))
                            elif isinstance(item, str):
                                # Compatibilidad con formato antiguo (solo correos)
                                registros.append(RegistroCorreo(correo=item))
                    else:
                        error = "El archivo tiene un formato inválido."
            else:
                # Crear archivo vacío si no existe
                self.guardar_registros([])
                
        except json.JSONDecodeError as e:
            error = f"El archivo está corrupto: {e}"
        except IOError as e:
            error = f"No se pudo leer el archivo: {e}"
        
        return registros, error
    
    def guardar_registros(self, registros: List[RegistroCorreo]) -> Tuple[bool, Optional[str]]:
        """
        Guarda los registros en el archivo JSON.
        
        Args:
            registros: Lista de registros a guardar.
            
        Returns:
            Tupla con (éxito: bool, mensaje de error o None si éxito).
        """
        try:
            datos = [reg.to_dict() for reg in registros]
            with open(self.archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=2, ensure_ascii=False)
            return True, None
        except IOError as e:
            return False, f"No se pudo guardar el archivo: {e}"
    
    def existe_archivo(self) -> bool:
        """Verifica si el archivo de datos existe."""
        return os.path.exists(self.archivo)
