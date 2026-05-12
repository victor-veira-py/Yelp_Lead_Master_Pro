# ==============================================================================
# PROYECTO: Yelp Lead Master Pro - CONFIGURACIÓN CENTRAL
# DESARROLLADO POR / DEVELOPED BY: VICTOR ARMANDO DE OLIVEIRA RODRÍGUEZ
# ==============================================================================
import os

# Al estar dentro de 'src/', subimos un nivel para encontrar la raíz del proyecto
# Since it's inside 'src/', we go up one level to find the project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Ruta de la base de datos en la raíz / Database path at the root
RUTA_DB = os.path.join(BASE_DIR, "data", "prospectos_negocios.db")

# Configuración del Driver (Tu sistema DELL Latitude)
# Driver configuration (Your DELL Latitude system)
CHROME_VERSION = 148

# Aseguramos la existencia de la carpeta 'data' al importar este módulo
# We ensure the existence of the 'data' folder when importing this module
os.makedirs(os.path.dirname(RUTA_DB), exist_ok=True)