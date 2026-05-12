# ==============================================================================
# PROYECTO: Yelp Lead Master Pro
# DESCRIPCIÓN: Configuración de Navegador Indetectable (uc)
# DESCRIPTION: Undetectable Browser Configuration (uc)
# DESARROLLADO POR / DEVELOPED BY: VICTOR ARMANDO DE OLIVEIRA RODRÍGUEZ
# ==============================================================================

import undetected_chromedriver as uc
import time


def iniciar_browser_pro(version_chrome=148):
    """
    Inicia un motor de navegación avanzado que evade la detección de bots.
    Starts an advanced navigation engine that evades bot detection.

    Args:
        version_chrome (int): Versión de Chrome detectada en el sistema.
                              Chrome version detected on the system.
    """
    try:
        print(f"🚀 [INFO] Iniciando motor invisible (UC) - Versión: {version_chrome}")
        print(f"🚀 [INFO] Starting invisible engine (UC) - Version: {version_chrome}")

        options = uc.ChromeOptions()

        # Opciones para reducir la huella digital del bot
        # Options to reduce the bot's digital footprint
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-first-run")

        # Mantenemos la ventana visible para evitar bloqueos agresivos
        # Keep the window visible to avoid aggressive blocks
        driver = uc.Chrome(
            options=options,
            version_main=version_chrome
        )

        driver.maximize_window()
        return driver

    except Exception as e:
        print(f"❌ [ERROR] Error al iniciar UC / Error starting UC: {e}")
        return None