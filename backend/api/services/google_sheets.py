# backend/api/services/google_sheets.py

"""
Servicio para sincronizar usuarios con Google Sheets.
"""
import gspread
from google.oauth2.service_account import Credentials
from django.conf import settings
import os


class GoogleSheetsService:
    """
    Maneja la conexión y escritura en Google Sheets.
    """
    
    def __init__(self):
        """Inicializa la conexión con Google Sheets usando credenciales de servicio."""
        
        # 1. DEFINE LOS PERMISOS QUE NECESITAMOS
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        # 2. CONSTRUYE LA RUTA AL ARCHIVO DE CREDENCIALES
        creds_path = os.path.join(
            settings.BASE_DIR, 
            'credentials', 
            'service-account.json'
        )
        
        # 3. VERIFICA QUE EL ARCHIVO EXISTA
        if not os.path.exists(creds_path):
            raise FileNotFoundError(
                f"Archivo de credenciales no encontrado en: {creds_path}\n"
                "Asegúrate de haber descargado service-account.json "
                "y colocarlo en la carpeta credentials/"
            )
        
        # 4. AUTENTICA CON GOOGLE
        creds = Credentials.from_service_account_file(creds_path, scopes=scopes)
        self.client = gspread.authorize(creds)
        
        # 5. ABRE LA HOJA DE CÁLCULO
        try:
            self.sheet = self.client.open_by_key(settings.GOOGLE_SHEET_ID).sheet1
        except Exception as e:
            raise Exception(
                f"No se pudo abrir la hoja de cálculo. "
                f"Verifica que:\n"
                f"1. El GOOGLE_SHEET_ID en .env es correcto\n"
                f"2. Compartiste la hoja con el service account\n"
                f"Error original: {e}"
            )
    
    def append_user(self, usuario):
        """
        Agrega una fila con los datos del usuario a la hoja de cálculo.
        """
        # 6. PREPARA LA FILA DE DATOS
        row = [
            str(usuario.id),
            usuario.nombre_completo,
            usuario.nombre,
            usuario.apellidos,
            str(usuario.fecha_nacimiento),
            usuario.ciudad,
            usuario.nivel_riesgo,
            usuario.alergenos_principales,
            usuario.email,
            str(usuario.created_at.strftime('%Y-%m-%d %H:%M:%S'))
        ]
        
        # 7. AGREGA LA FILA A LA HOJA
        try:
            self.sheet.append_row(row)
            return True
        except Exception as e:
            print(f"Error al agregar fila a Google Sheets: {e}")
            return False


# 8. PATRÓN SINGLETON - UNA SOLA CONEXIÓN PARA TODO
_sheets_service = None

def get_sheets_service():
    """Retorna una instancia singleton del servicio de Google Sheets."""
    global _sheets_service
    if _sheets_service is None:
        _sheets_service = GoogleSheetsService()
    return _sheets_service