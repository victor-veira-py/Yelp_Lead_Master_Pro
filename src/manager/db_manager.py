# ==============================================================================
# PROYECTO: Yelp Lead Master Pro
# DESCRIPCIÓN: Gestión de Base de Datos para Prospectos (Rutas Blindadas)
# DESCRIPTION: Prospect Database Management (Shielded Paths)
# DESARROLLADO POR / DEVELOPED BY: VICTOR ARMANDO DE OLIVEIRA RODRÍGUEZ
# ==============================================================================
import pandas as pd
import sqlite3
import os
import sys
from datetime import datetime

# --- CONFIGURACIÓN DE RUTA DINÁMICA / DYNAMIC PATH CONFIGURATION ---
if getattr(sys, 'frozen', False):
    ROOT_DIR = os.path.dirname(sys.executable)
else:
    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

RUTA_DB_UNIVERSAL = os.path.join(ROOT_DIR, 'data', 'prospectos_negocios.db')


def inicializar_db(ruta_db=RUTA_DB_UNIVERSAL):
    """
    Crea la base de datos y la tabla de leads si no existen.
    Creates the database and the leads table if they do not exist.
    """
    try:
        directorio_data = os.path.dirname(ruta_db)
        os.makedirs(directorio_data, exist_ok=True)

        conn = sqlite3.connect(ruta_db)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha_extraccion TEXT,
                negocio_nombre TEXT,
                categoria TEXT,
                telefono TEXT,
                sitio_web TEXT,
                ubicacion TEXT,
                rating REAL
            )
        ''')

        conn.commit()
        conn.close()
        print(f"✅ [EXITO/SUCCESS] Base de datos configurada en / Database configured at: {ruta_db}")
        return True

    except Exception as e:
        print(f"❌ [ERROR] No se pudo crear la base de datos: {e}")
        return False


def vaciar_base_de_datos(ruta_db=RUTA_DB_UNIVERSAL):
    """
    Elimina todos los registros de la tabla para una búsqueda limpia.
    Deletes all records from the table for a clean search.
    """
    try:
        conn = sqlite3.connect(ruta_db)
        cursor = conn.cursor()

        # Eliminamos todos los datos de la tabla leads
        # Delete all data from leads table
        cursor.execute("DELETE FROM leads")

        # Reiniciamos el contador de ID de SQLite
        # Reset SQLite ID counter
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='leads'")

        conn.commit()
        conn.close()
        print("🧹 [DB] Base de datos vaciada con éxito / Database cleared successfully.")
        return True
    except Exception as e:
        print(f"❌ [ERROR DB] No se pudo vaciar la base de datos: {e}")
        return False


def limpieza_preventiva_db(ruta_db=RUTA_DB_UNIVERSAL):
    """
    Elimina registros incompletos que podrían causar errores.
    Removes incomplete records that could cause errors.
    """
    try:
        conn = sqlite3.connect(ruta_db)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM leads WHERE negocio_nombre IS NULL OR negocio_nombre = ''")

        borrados = cursor.rowcount
        conn.commit()
        conn.close()

        if borrados > 0:
            print(f"🧹 [DB] Limpieza completada: {borrados} eliminados / {borrados} removed.")
        return True
    except Exception as e:
        print(f"❌ [ERROR DB] Error en limpieza: {e}")
        return False


def obtener_leads_para_investigar(limite=10, ruta_db=RUTA_DB_UNIVERSAL):
    """
    Obtiene prospectos con URL de Yelp para investigación profunda.
    Gets prospects with Yelp URL for deep investigation.
    """
    try:
        conn = sqlite3.connect(ruta_db)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, negocio_nombre, sitio_web 
            FROM leads 
            WHERE sitio_web LIKE 'http%' 
            AND (telefono IS NULL OR telefono = '' OR telefono = 'No encontrado')
            LIMIT ?
        """, (limite,))

        leads = cursor.fetchall()
        conn.close()
        return leads
    except Exception as e:
        print(f"❌ [ERROR DB] Error al obtener pendientes: {e}")
        return []


def guardar_lead(nombre, categoria, ubicacion, url_yelp, ruta_db=RUTA_DB_UNIVERSAL):
    """
    Guarda un lead incluyendo su URL de Yelp.
    Saves a lead including its Yelp URL.
    """
    try:
        conn = sqlite3.connect(ruta_db)
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM leads WHERE negocio_nombre = ?", (nombre,))
        if not cursor.fetchone():
            fecha_hoy = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute('''
                INSERT INTO leads (fecha_extraccion, negocio_nombre, categoria, ubicacion, sitio_web)
                VALUES (?, ?, ?, ?, ?)
            ''', (fecha_hoy, nombre, categoria, ubicacion, url_yelp))
            conn.commit()
            print(f"   ✅ Guardado / Saved: {nombre}")
            guardado = True
        else:
            print(f"   ⏭️ Omitido (Duplicado) / Skipped (Duplicate): {nombre}")
            guardado = False

        conn.close()
        return guardado
    except Exception as e:
        print(f"❌ [ERROR DB] Error al guardar en DB: {e}")
        return False


def actualizar_datos_enriquecidos(lead_id, telefono, web_real, ruta_db=RUTA_DB_UNIVERSAL):
    """
    Sustituye la URL de Yelp por el teléfono y sitio web real del negocio.
    Replaces the Yelp URL with the business phone and real website.
    """
    try:
        conn = sqlite3.connect(ruta_db)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE leads 
            SET telefono = ?, sitio_web = ? 
            WHERE id = ?
        """, (telefono, web_real, lead_id))

        conn.commit()
        conn.close()
        print(f"   💾 [DB] ID {lead_id} actualizado / updated.")
        return True
    except Exception as e:
        print(f"   ❌ [ERROR DB] No se pudo actualizar: {e}")
        return False


def exportar_leads_pro(ruta_db=RUTA_DB_UNIVERSAL):
    """
    Genera un reporte Excel con estética azul empresarial.
    Generates an Excel report with business blue aesthetics.
    """
    try:
        conn = sqlite3.connect(ruta_db)
        query = """
                    SELECT fecha_extraccion, negocio_nombre, categoria, telefono, sitio_web, ubicacion 
                    FROM leads 
                    ORDER BY negocio_nombre ASC
                """
        df = pd.read_sql_query(query, conn)
        conn.close()

        if df.empty:
            print("❌ No hay datos para exportar / No data to export.")
            return

        df.columns = [
            'FECHA REGISTRO', 'NOMBRE DEL NEGOCIO',
            'CATEGORÍA', 'TELÉFONO', 'SITIO WEB REAL', 'UBICACIÓN'
        ]

        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        nombre_excel = os.path.join(ROOT_DIR, 'data', f"Reporte_Final_Leads_{fecha_hoy}.xlsx")

        with pd.ExcelWriter(nombre_excel, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Leads Validados', index=False)
            workbook = writer.book
            worksheet = writer.sheets['Leads Validados']

            formato_header = workbook.add_format({
                'bold': True, 'text_wrap': True, 'valign': 'vcenter', 'align': 'center',
                'fg_color': '#003366', 'font_color': 'white', 'border': 1
            })

            formato_centrado = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1})
            formato_texto = workbook.add_format({'align': 'left', 'valign': 'vcenter', 'border': 1})

            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, formato_header)

            worksheet.set_column('A:A', 18, formato_centrado)
            worksheet.set_column('B:B', 45, formato_texto)
            worksheet.set_column('C:C', 15, formato_centrado)
            worksheet.set_column('D:D', 18, formato_centrado)
            worksheet.set_column('E:E', 40, formato_texto)
            worksheet.set_column('F:F', 30, formato_centrado)
            worksheet.freeze_panes(1, 0)

        print(f"✅ ¡REPORTE GENERADO! / REPORT GENERATED!: {nombre_excel}")

    except Exception as e:
        print(f"❌ Error en la exportación / Export error: {e}")