# ==============================================================================
# PROYECTO: Yelp Lead Master Pro
# DESCRIPCIÓN: Configuración del Navegador (Undetected Chromedriver)
# DESCRIPTION: Browser Configuration (Undetected Chromedriver)
# DESARROLLADO POR / DEVELOPED BY: VICTOR ARMANDO DE OLIVEIRA RODRÍGUEZ
# ==============================================================================

import undetected_chromedriver as uc
import time


def iniciar_browser(version_chrome=148):
    """
    Configura e inicia el navegador con tecnología invisible para evitar bloqueos.
    Configures and starts the browser with invisible technology to avoid blocks.

    Args:
        version_chrome (int): Versión principal del navegador instalado.
                              Main version of the installed browser.
    """
    options = uc.ChromeOptions()

    # Argumentos para mejorar el anonimato y estabilidad
    # Arguments to improve anonymity and stability
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-first-run")
    options.add_argument("--no-service-autorun")
    options.add_argument("--password-store=basic")

    # Iniciamos el driver con la versión específica detectada en el laboratorio
    # Start the driver with the specific version detected in the laboratory
    driver = uc.Chrome(
        options=options,
        version_main=version_chrome
    )

    driver.maximize_window()
    return driver