# ia-codex-api/app/__init__.py

from flask import Flask
import os
from dotenv import load_dotenv

# Importar la función de carga de modelos
from .models import load_models 

# Cargar las variables de entorno desde el archivo .env
# Esto debe hacerse antes de que se acceda a cualquier variable de entorno.
load_dotenv() 

def create_app():
    """
    Crea y configura la instancia de la aplicación Flask.
    """
    app = Flask(__name__)
    
    # --- Configuración de la aplicación desde variables de entorno ---
    # DEBUG: Convertir la cadena a booleano
    app.config['DEBUG'] = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
    # API_PORT: Convertir a entero
    app.config['API_PORT'] = int(os.getenv('API_PORT', 5000))
    # Nombres de los modelos de Hugging Face
    app.config['HF_MODEL_AUTOCOMPLETE'] = os.getenv('HF_MODEL_AUTOCOMPLETE')
    app.config['HF_MODEL_TEXT2TEXT'] = os.getenv('HF_MODEL_TEXT2TEXT')
    
    # --- Carga de modelos de IA ---
    # Es crucial cargar los modelos dentro del contexto de la aplicación para asegurar que
    # estén disponibles para todas las solicitudes y se carguen una sola vez.
    with app.app_context():
        load_models(app.config) # Pasar la configuración para que models.py acceda a los nombres de modelos

    # --- Registro de Blueprints ---
    # Un Blueprint organiza un conjunto de rutas y otras funciones relacionadas.
    # Es una buena práctica para modularizar aplicaciones Flask grandes.
    from .api import api_bp
    app.register_blueprint(api_bp)

    return app