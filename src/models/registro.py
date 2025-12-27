"""
Modelo de datos para registro de correo electrónico.

Define la estructura de datos principal de la aplicación.
"""

from dataclasses import dataclass, asdict, field
from typing import List, Dict, Any


@dataclass
class RegistroCorreo:
    """
    Representa un registro de correo con todos sus atributos.
    
    Attributes:
        correo: Email con puerto opcional (ej: user@domain.com:12345)
        vpn: Indica si tiene VPN activa
        paises: Lista de códigos de país (ej: ['BR', 'US'])
        notas: Texto adicional (ej: 'membresia')
    """
    correo: str
    vpn: bool = False
    paises: List[str] = field(default_factory=list)
    notas: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el registro a diccionario para serialización."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RegistroCorreo':
        """
        Crea un registro desde un diccionario.
        
        Args:
            data: Diccionario con los datos del registro.
            
        Returns:
            Nueva instancia de RegistroCorreo.
        """
        return cls(
            correo=data.get('correo', ''),
            vpn=data.get('vpn', False),
            paises=data.get('paises', []),
            notas=data.get('notas', '')
        )
    
    def get_email_base(self) -> str:
        """
        Obtiene solo el email sin el puerto.
        
        Returns:
            Email base sin el puerto (si lo tiene).
        """
        if ':' in self.correo:
            return self.correo.split(':')[0]
        return self.correo
