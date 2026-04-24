"""
Sistema de Integración de APIs Veterinarias para TFG DAW2
VetCT - Sistema de Gestión Veterinaria con APIs Externas
Usa variables de entorno desde .env para claves de API
"""

import requests
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import random
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class VeterinaryAPIManager:
    """Gestor de APIs de servicios veterinarios para el TFG"""
    
    def __init__(self):
        # Cargar configuración desde variables de entorno simples
        self.api_clinicas_key = os.getenv('API_CLINICAS_KEY', 'demo_key')
        self.api_urgencias_key = os.getenv('API_URGENCIAS_KEY', 'demo_key')
        self.api_mascotas_key = os.getenv('API_MASCOTAS_KEY', 'demo_key')
        self.api_clima_key = os.getenv('API_CLIMA_KEY', 'demo_key')
        self.api_mapas_key = os.getenv('API_MAPAS_KEY', 'demo_key')
        
        # URLs base para las APIs
        self.veterinary_base_url = 'https://api.example-vet.com/v1'
        self.clinicas_base_url = 'https://api.clinicas-vet.com/v1'
        self.urgencias_base_url = 'https://api.urgencias-vet.com/v1'
        self.mascotas_base_url = 'https://api.mascotas-vet.com/v1'
        self.clima_base_url = 'https://api.clima.com/v1'
        self.mapas_base_url = 'https://api.mapas.com/v1'
    
    def get_clinicas_cercanas(self, latitud: float, longitud: float, radio_km: int = 10) -> List[Dict]:
        """Obtener clínicas veterinarias cercanas"""
        try:
            url = f"{self.clinicas_base_url}/clinicas/cercanas"
            params = {
                'lat': latitud,
                'lng': longitud,
                'radio': radio_km,
                'api_key': self.api_clinicas_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return data.get('clinicas', [])
            
        except requests.RequestException as e:
            print(f"Error obteniendo clínicas: {e}")
            return []
    
    def get_urgencias_disponibles(self, ciudad: str) -> List[Dict]:
        """Obtener urgencias disponibles en una ciudad"""
        try:
            url = f"{self.urgencias_base_url}/urgencias/disponibles"
            params = {
                'ciudad': ciudad,
                'api_key': self.api_urgencias_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return data.get('urgencias', [])
            
        except requests.RequestException as e:
            print(f"Error obteniendo urgencias: {e}")
            return []
    
    def get_info_mascota(self, tipo_mascota: str, raza: str) -> Dict:
        """Obtener información sobre una raza específica"""
        try:
            url = f"{self.mascotas_base_url}/razas/info"
            params = {
                'tipo': tipo_mascota,
                'raza': raza,
                'api_key': self.api_mascotas_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.RequestException as e:
            print(f"Error obteniendo info de mascota: {e}")
            return {}
    
    def get_clima_actual(self, ciudad: str) -> Dict:
        """Obtener el clima actual para recomendaciones veterinarias"""
        try:
            url = f"{self.clima_base_url}/clima/actual"
            params = {
                'ciudad': ciudad,
                'api_key': self.api_clima_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.RequestException as e:
            print(f"Error obteniendo clima: {e}")
            return {}
    
    def get_ruta_mapa(self, origen: str, destino: str) -> Dict:
        """Obtener ruta entre dos puntos"""
        try:
            url = f"{self.mapas_base_url}/rutas"
            params = {
                'origen': origen,
                'destino': destino,
                'api_key': self.api_mapas_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.RequestException as e:
            print(f"Error obteniendo ruta: {e}")
            return {}

# Instancia global del gestor de APIs
api_manager = VeterinaryAPIManager()
