# ==============================================================================
# PROYECTO: Yelp Lead Master Pro
# DESCRIPCIÓN: Panel de Control Principal (Orquestador del Software)
# DESCRIPTION: Main Control Panel (Software Orchestrator)
# DESARROLLADO POR / DEVELOPED BY: VICTOR ARMANDO DE OLIVEIRA RODRÍGUEZ
# ==============================================================================

import os
import sys
from datetime import datetime

# Configuración de rutas para reconocer los módulos dentro de 'src'
# Path configuration to recognize modules inside 'src'
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Importación de funciones modulares (Asegúrate de tener vaciar_base_de_datos en db_manager)
# Importing modular functions (Ensure vaciar_base_de_datos exists in db_manager)
from src.manager.db_manager import (
    inicializar_db, exportar_leads_pro, limpieza_preventiva_db, vaciar_base_de_datos
)
from src.engine.yelp_engine import ejecutar_extraccion_pro, ejecutar_investigacion_profunda
from src.tools.notifier import enviar_reporte_email

# Constante de versión para el blindaje del driver (Basado en tu sistema DELL)
# Version constant for driver shielding (Based on your DELL system)
CHROME_VERSION = 148

# Obtener la ruta raíz del proyecto para localizar archivos
# Get the project root path to locate files
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def mostrar_menu():
    """
    Muestra la interfaz de usuario en consola con diseño bilingüe.
    Displays the user interface in console with bilingual design.
    """
    print(f"\n{'=' * 65}")
    print(f"   YELP LEAD MASTER PRO - BY VICTOR DE OLIVEIRA")
    print(f"{'=' * 65}")
    print(" 1. 🚀 Extracción Automática / Automatic Extraction")
    print(" 2. 🔎 Investigación Profunda / Deep Investigation")
    print(" 3. 📊 Generar Reporte Excel / Generate Excel Report")
    print(" 4. 🧹 Vaciar Base de Datos / Clear All Data")
    print(" 5. 📧 Enviar Reporte por Correo / Send Report via Email")
    print(" 6. ❌ Salir / Exit")
    print(f"{'=' * 65}")


def ejecutar_programa():
    """
    Orquestador principal de la lógica del software.
    Main orchestrator of the software logic.
    """
    # Asegura que la base de datos y carpeta data existan al iniciar
    # Ensures database and data folder exist on startup
    inicializar_db()

    while True:
        mostrar_menu()
        # Input de selección de opción bilingüe
        # Bilingual option selection input
        opcion = input("Seleccione una opción / Select an option (1-6): ")

        if opcion == "1":
            # PREGUNTA DE SEGURIDAD PARA EVITAR MEZCLAR RESULTADOS
            # SECURITY PROMPT TO AVOID MIXING RESULTS
            limpiar = input("\n¿Desea vaciar la base antes de empezar? / Clear database first? (s/n): ").lower()
            if limpiar == 's':
                vaciar_base_de_datos()

            categoria = input("Categoría de negocio / Business category (ej. Dentists): ")
            ciudad = input("Ciudad y Estado / City and State (ej. Miami, FL): ")
            print("\n" + "-" * 45)
            # Ejecutamos la extracción limpia
            # Executing clean extraction
            ejecutar_extraccion_pro(categoria, ciudad, version_chrome=CHROME_VERSION)
            print("-" * 45)

        elif opcion == "2":
            # Investigación profunda (Enriquecimiento de datos)
            # Deep investigation (Data enrichment)
            print("\n" + "-" * 45)
            ejecutar_investigacion_profunda(version_chrome=CHROME_VERSION)
            print("-" * 45)

        elif opcion == "3":
            # Generación de reporte Excel
            # Excel report generation
            print("\n" + "-" * 45)
            exportar_leads_pro()
            print("-" * 45)

        elif opcion == "4":
            # LIMPIEZA TOTAL MANUAL
            # MANUAL FULL CLEANUP
            confirmar = input("\n⚠️ ¿Seguro que desea borrar TODO? / Are you sure? (s/n): ").lower()
            if confirmar == 's':
                vaciar_base_de_datos()
                limpieza_preventiva_db()
            print("-" * 45)

        elif opcion == "5":
            # Envío de reporte por correo / Sending report via email
            print("\n" + "-" * 45)
            fecha_hoy = datetime.now().strftime("%Y-%m-%d")
            # Ruta del archivo Excel generado
            # Path of the generated Excel file
            ruta_reporte = os.path.join(ROOT_DIR, 'data', f"Reporte_Final_Leads_{fecha_hoy}.xlsx")

            if os.path.exists(ruta_reporte):
                enviar_reporte_email(ruta_reporte)
            else:
                print(f"⚠️ [!] Primero debe generar el reporte (Opción 3).")
                print(f"⚠️ [!] You must generate the report first (Option 3).")
            print("-" * 45)

        elif opcion == "6":
            # Cierre seguro del programa
            # Safe program shutdown
            print("\n" + "=" * 65)
            print(" 👋 ¡Éxito en tus ventas, VICTOR ARMANDO DE OLIVEIRA RODRÍGUEZ!")
            print(" 👋 Success in your sales, VICTOR ARMANDO DE OLIVEIRA RODRÍGUEZ!")
            print("=" * 65 + "\n")
            break

        else:
            print("\n⚠️ Opción no válida. Intente de nuevo.")
            print("⚠️ Invalid option. Please try again.")


if __name__ == "__main__":
    try:
        ejecutar_programa()
    except KeyboardInterrupt:
        print("\n\n🛑 Programa interrumpido por el usuario / Program interrupted by user.")
        sys.exit()