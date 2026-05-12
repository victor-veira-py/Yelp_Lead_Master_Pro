# ==============================================================================
# PROYECTO: Yelp Lead Master Pro
# DESCRIPCIÓN: Motor de Búsqueda y Extracción de Yelp
# DESCRIPTION: Yelp Search and Extraction Engine
# DESARROLLADO POR / DEVELOPED BY: VICTOR ARMANDO DE OLIVEIRA RODRÍGUEZ
# ==============================================================================
from tools.invisible_browser import iniciar_browser_pro
from manager.db_manager import actualizar_datos_enriquecidos, guardar_lead, obtener_leads_para_investigar
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import re
import urllib.parse


def ejecutar_extraccion_pro(categoria, ciudad, version_chrome=148):
    """
    Flujo de trabajo 100% automatizado con simulación de comportamiento humano.
    100% automated workflow with human behavior simulation.
    """
    # Inicialización del driver avanzado / Advanced driver initialization
    driver = iniciar_browser_pro(version_chrome=version_chrome)
    if not driver:
        return

    try:
        # Navegación inicial a Yelp / Initial navigation to Yelp
        driver.get("https://www.yelp.com")

        print("🔄 [INFO] Refrescando página para evitar detección...")
        driver.refresh()

        # Definimos la espera explícita / Define explicit wait
        wait = WebDriverWait(driver, 20)

        print("⏳ [INFO] Esperando carga de buscadores...")
        # Selectores optimizados para evitar errores de carga
        # Optimized selectors to avoid loading errors
        search_find = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input#search_description, input#find_desc")))
        search_near = driver.find_element(By.CSS_SELECTOR, "input#search_location, input#dropperText_pi_6c11")

        # Simulación de escritura humana para la categoría
        # Human typing simulation for the category
        print(f"⌨️ Escribiendo categoría / Typing category: {categoria}")
        for letra in categoria:
            search_find.send_keys(letra)
            time.sleep(random.uniform(0.1, 0.3))

        time.sleep(1)

        # Limpieza y escritura humana para la ubicación
        # Cleaning and human typing for the location
        search_near.send_keys(Keys.CONTROL + "a")
        search_near.send_keys(Keys.DELETE)

        print(f"⌨️ Escribiendo ubicación / Typing location: {ciudad}")
        for letra in ciudad:
            search_near.send_keys(letra)
            time.sleep(random.uniform(0.1, 0.3))

        search_near.send_keys(Keys.ENTER)

        # Esperar a que aparezcan los resultados
        # Wait for results to appear
        print("⏳ [INFO] Esperando resultados...")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h3 a")))
        time.sleep(5)

        # Extracción y guardado automático
        # Automatic extraction and storage
        print(f"📦 [INFO] Extrayendo leads...")
        resultados = driver.find_elements(By.CSS_SELECTOR, "h3 a")

        for res in resultados:
            nombre = res.text.strip()
            link = res.get_attribute("href")

            # FILTRO CRÍTICO: Solo enlaces de negocios reales
            # CRITICAL FILTER: Only real business links
            if nombre and link and "biz" in link:
                guardar_lead(nombre, categoria, ciudad, link)

    except Exception as e:
        print(f"⚠️ [ERROR] Error en el proceso de extracción / Extraction error: {e}")
    finally:
        # Mensaje final limpio y bilingüe
        # Clean and bilingual final message
        print("\n🎯 Extracción completada / Extraction completed.")
        driver.quit()


def ejecutar_investigacion_profunda(version_chrome=148):
    """
    Navega en los perfiles para extraer teléfonos y sitios web reales.
    Navigates through profiles to extract phone numbers and real websites.
    """
    # Patrón para teléfonos de USA / Pattern for USA phones
    patron_tel = re.compile(r'\(\d{3}\)\s\d{3}-\d{4}')

    try:
        # Obtenemos los pendientes que tienen URL de Yelp
        # Get pending leads that have a Yelp URL
        pendientes = obtener_leads_para_investigar(limite=15)

        if not pendientes:
            print("✅ [INFO] No hay leads pendientes / No pending leads.")
            return

        driver = iniciar_browser_pro(version_chrome=version_chrome)
        if not driver:
            return

        for l_id, nombre, url_yelp in pendientes:
            # Verificación de seguridad / Security check
            if not url_yelp or not isinstance(url_yelp, str):
                print(f"   ⏭️ Saltando {nombre}: URL inválida / Invalid URL.")
                continue

            print(f"🔎 Investigando / Investigating: {nombre}")
            try:
                driver.get(url_yelp)
                time.sleep(random.uniform(7, 10))

                # --- EXTRACCIÓN DE TELÉFONO / PHONE EXTRACTION ---
                elementos = driver.find_elements(By.XPATH, "//*[contains(text(), '(')]")
                telefono = "No encontrado"
                for el in elementos:
                    texto = el.text.strip()
                    if patron_tel.search(texto):
                        telefono = patron_tel.search(texto).group()
                        break

                # --- EXTRACCIÓN DE WEB REAL / REAL WEB EXTRACTION ---
                try:
                    elemento_web = driver.find_element(By.XPATH, "//a[contains(@href, '/biz_redir')]")
                    raw_url = elemento_web.get_attribute("href")
                    # Limpiamos la URL de redirección de Yelp
                    # We clean the Yelp redirection URL
                    web_real = urllib.parse.unquote(
                        raw_url.split("url=")[1].split("&")[0]) if "url=" in raw_url else elemento_web.text
                except:
                    web_real = "No tiene sitio web / No website"

                actualizar_datos_enriquecidos(l_id, telefono, web_real)
                print(f"   ✨ Encontrado / Found: {telefono} | {web_real}")

                time.sleep(random.uniform(4, 6))

            except Exception as e:
                print(f"   ⚠️ Error con / Error with {nombre}: {e}")
                continue

        print("\n✨ Investigación finalizada / Investigation finished.")
        driver.quit()

    except Exception as e:
        print(f"❌ [ERROR] Error general en investigación / General investigation error: {e}")