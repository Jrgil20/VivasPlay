"""
Servicio de parseo y validación de correos electrónicos.

Proporciona funciones para extraer y validar registros de correo
desde diferentes fuentes de texto.
"""

import re
from typing import List, Optional

from ..models.registro import RegistroCorreo
from ..config import PATRON_EMAIL, CODIGOS_PAIS


class ParserCorreos:
    """
    Parser para extraer registros de correo desde texto.
    
    Soporta múltiples formatos de entrada:
    - correo:puerto | VPN: PAIS notas
    - correo — PAIS
    - correo | VPN: PAIS1 PAIS2
    - correo:puerto notas
    """
    
    @staticmethod
    def validar_correo(correo: str) -> bool:
        """
        Valida si un string tiene formato de correo electrónico válido.
        Acepta correos con puerto opcional (ej: user@domain.com:12345).
        
        Args:
            correo: String a validar.
            
        Returns:
            True si el formato es válido, False en caso contrario.
        """
        if not correo:
            return False
        return bool(re.match(PATRON_EMAIL, correo))
    
    @staticmethod
    def extraer_email_con_puerto(texto: str) -> Optional[str]:
        """
        Extrae el email con puerto opcional de un texto.
        
        Args:
            texto: Texto que contiene el email.
            
        Returns:
            Email con puerto si se encuentra, None si no.
        """
        patron = r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})(:\d+)?'
        match = re.search(patron, texto)
        if match:
            email = match.group(1)
            puerto = match.group(2) if match.group(2) else ''
            return email + puerto
        return None
    
    @staticmethod
    def extraer_paises(texto: str) -> List[str]:
        """
        Extrae códigos de país de un texto.
        
        Args:
            texto: Texto que puede contener códigos de país.
            
        Returns:
            Lista de códigos de país encontrados (ISO 3166-1 alpha-2).
        """
        palabras = re.findall(r'\b([A-Z]{2})\b', texto.upper())
        return [p for p in palabras if p in CODIGOS_PAIS]
    
    @staticmethod
    def _extraer_notas(linea: str, correo: str, paises: List[str]) -> str:
        """
        Extrae notas de una línea, excluyendo el correo, VPN y países.
        
        Args:
            linea: Línea original.
            correo: Correo ya extraído.
            paises: Lista de países ya extraídos.
            
        Returns:
            Texto de notas limpio.
        """
        # Remover el correo de la línea
        texto = linea.replace(correo, '')
        
        # Remover separadores comunes
        texto = re.sub(r'[|—–\-]', ' ', texto)
        
        # Remover "VPN:" o "VPN"
        texto = re.sub(r'\bVPN\s*:?\s*', '', texto, flags=re.IGNORECASE)
        
        # Remover países
        for pais in paises:
            texto = re.sub(rf'\b{pais}\b', '', texto, flags=re.IGNORECASE)
        
        # Limpiar y retornar
        notas = ' '.join(texto.split()).strip()
        
        # Limpiar caracteres residuales
        notas = notas.strip('.,;:()[]{}"\' ')
        
        return notas
    
    @classmethod
    def parsear_linea(cls, linea: str) -> Optional[RegistroCorreo]:
        """
        Parsea una línea de texto y extrae un registro de correo.
        
        Args:
            linea: Línea de texto a parsear.
            
        Returns:
            RegistroCorreo si se encuentra un email válido, None si no.
        """
        if not linea.strip():
            return None
        
        # Extraer email con puerto
        correo = cls.extraer_email_con_puerto(linea)
        if not correo:
            return None
        
        # Determinar si tiene VPN
        tiene_vpn = bool(re.search(r'\bVPN\b', linea, re.IGNORECASE))
        
        # Extraer países
        paises = cls.extraer_paises(linea)
        
        # Extraer notas
        notas = cls._extraer_notas(linea, correo, paises)
        
        return RegistroCorreo(
            correo=correo,
            vpn=tiene_vpn,
            paises=paises,
            notas=notas
        )
    
    @classmethod
    def procesar_texto_a_registros(cls, texto: str) -> List[RegistroCorreo]:
        """
        Procesa un texto y extrae registros de correo.
        
        Esta función es la base para todas las operaciones de importación.
        Evita duplicados por email base.
        
        Args:
            texto: Texto a procesar (múltiples líneas).
            
        Returns:
            Lista de registros válidos encontrados (sin duplicados).
        """
        if not texto:
            return []
        
        registros = []
        emails_vistos = set()
        
        for linea in texto.splitlines():
            registro = cls.parsear_linea(linea)
            if registro:
                # Evitar duplicados por email base
                email_base = registro.get_email_base().lower()
                if email_base not in emails_vistos:
                    emails_vistos.add(email_base)
                    registros.append(registro)
        
        return registros
