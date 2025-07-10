# ia-codex-api/tests/test_api.py

import pytest
import json
import sys
import os

# Asegúrate de que la ruta de la aplicación Flask sea accesible
# Esto es necesario para que pytest encuentre tu app cuando se ejecute desde la raíz del proyecto.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app # Importa la función de creación de la aplicación Flask

# --- Fixture de Pytest para el Cliente de Prueba de Flask ---
@pytest.fixture
def client():
    """
    Fixture que configura un cliente de prueba de Flask para cada test.
    Esto permite simular solicitudes HTTP a la aplicación sin necesidad de ejecutar un servidor real.
    """
    # Configura la aplicación para el modo de prueba
    os.environ['FLASK_ENV'] = 'testing' # Puedes usar 'testing' como un entorno específico para pruebas
    os.environ['DEBUG'] = 'True'        # Activa el modo debug para ver más detalles en caso de error
    os.environ['API_PORT'] = '5000'     # Puedes establecer un puerto aunque no se use en el cliente de pruebas

    app = create_app()

    # Usa el contexto de la aplicación para las pruebas
    with app.test_client() as client:
        yield client # El cliente de prueba se pasa a las funciones de prueba

# --- Pruebas para el Endpoint /complete ---
def test_complete_success(client):
    """
    Prueba el endpoint /complete con una solicitud exitosa.
    Verifica que la respuesta sea 200 OK y contenga la clave 'suggestions'.
    """
    data = {"prompt": "def hello_world():"}
    response = client.post('/complete', json=data)

    assert response.status_code == 200
    assert response.is_json
    assert 'suggestions' in response.json
    assert isinstance(response.json['suggestions'], list)
    assert len(response.json['suggestions']) > 0

def test_complete_missing_prompt(client):
    """
    Prueba el endpoint /complete sin el campo 'prompt'.
    Espera una respuesta 400 Bad Request y un mensaje de error.
    """
    data = {} # No incluye el campo 'prompt'
    response = client.post('/complete', json=data)

    assert response.status_code == 400
    assert response.is_json
    assert 'error' in response.json
    assert "El campo 'prompt' es requerido." in response.json['error']

def test_complete_invalid_json(client):
    """
    Prueba el endpoint /complete con un cuerpo de solicitud no JSON.
    Espera una respuesta 415 Unsupported Media Type.
    """
    response = client.post('/complete', data="esto no es json", content_type='text/plain')

    assert response.status_code == 415 # ¡Cambiado de 400 a 415!
    assert response.is_json
    assert 'error' in response.json
    assert "Formato JSON inválido. Content-Type debe ser application/json." in response.json['error']

# --- Pruebas para el Endpoint /fix ---
def test_fix_success(client):
    """
    Prueba el endpoint /fix con una solicitud exitosa.
    """
    data = {"code": "pront 'hello world'"} # Código con un error tipográfico
    response = client.post('/fix', json=data)

    assert response.status_code == 200
    assert response.is_json
    assert 'fixed_code' in response.json
    assert isinstance(response.json['fixed_code'], str)
    assert len(response.json['fixed_code']) > 0

def test_fix_missing_code(client):
    """
    Prueba el endpoint /fix sin el campo 'code'.
    """
    data = {}
    response = client.post('/fix', json=data)

    assert response.status_code == 400
    assert response.is_json
    assert 'error' in response.json
    assert "El campo 'code' es requerido." in response.json['error']

# --- Pruebas para el Endpoint /convert ---
def test_convert_success(client):
    """
    Prueba el endpoint /convert con una solicitud exitosa.
    """
    data = {"code": "print('Hello')", "target_language": "javascript"}
    response = client.post('/convert', json=data)

    assert response.status_code == 200
    assert response.is_json
    assert 'converted_code' in response.json
    assert isinstance(response.json['converted_code'], str)
    assert len(response.json['converted_code']) > 0


def test_convert_missing_fields(client):
    """
    Prueba el endpoint /convert sin campos requeridos.
    """
    # Caso 1: Falta 'code'
    data = {"target_language": "javascript"}
    response = client.post('/convert', json=data)
    assert response.status_code == 400
    assert response.is_json
    assert "El campo 'code' es requerido." in response.json['error']

    # Caso 2: Falta 'target_language'
    data = {"code": "print('Hello')"}
    response = client.post('/convert', json=data)
    assert response.status_code == 400
    assert response.is_json
    assert "El campo 'target_language' es requerido." in response.json['error']


def test_convert_unsupported_language(client):
    """
    Prueba el endpoint /convert con un lenguaje objetivo no soportado (o no reconocido).
    """
    data = {"code": "some code", "target_language": "klingon"} # Lenguaje inventado
    response = client.post('/convert', json=data)

    assert response.status_code == 400
    assert response.is_json
    assert 'error' in response.json
    assert "El lenguaje objetivo 'klingon' no es soportado." in response.json['error']

# --- Prueba para el endpoint raíz / ---
def test_root_endpoint(client):
    """
    Prueba el endpoint raíz / para verificar que devuelve un mensaje de bienvenida.
    """
    response = client.get('/')

    assert response.status_code == 200
    assert response.is_json # Ahora esperamos que sea JSON
    assert 'message' in response.json
    assert "Bienvenido a la IA Codex API" in response.json['message']