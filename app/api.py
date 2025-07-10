# ia-codex-api/app/api.py

import sys
from flask import Blueprint, request, jsonify
from .models import get_generator_pipeline, get_text2text_pipeline
from .utils import get_json_data # Importa la nueva función de utilidad

# Crear un Blueprint para la API. Esto permite organizar las rutas.
api_bp = Blueprint('api', __name__)

@api_bp.route('/')
def home():
    """
    Endpoint principal para verificar que la API está funcionando.
    Ahora devuelve JSON como se espera en los tests.
    """
    return jsonify({"message": "Bienvenido a la IA Codex API. Utiliza /complete, /fix o /convert."})

@api_bp.route('/complete', methods=['POST'])
def complete_code():
    """
    Endpoint para autocompletar código.
    Espera un JSON con el campo 'prompt'.
    """
    data, error_message, status_code = get_json_data(request)
    if error_message:
        return jsonify({"error": error_message}), status_code

    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": "El campo 'prompt' es requerido."}), 400 # Mensaje de error unificado

    # Obtener parámetros opcionales de la solicitud, con valores por defecto.
    max_tokens = data.get("max_tokens", 256)
    num_suggestions = data.get("num_suggestions", 1)

    # Obtener el pipeline del modelo de autocompletado.
    generator_pipeline = get_generator_pipeline()
    if generator_pipeline is None:
        return jsonify({"error": "Modelo de autocompletado no cargado."}), 500

    try:
        # Generar sugerencias de autocompletado usando el modelo.
        suggestions = generator_pipeline(
            prompt,
            max_new_tokens=max_tokens,
            num_return_sequences=num_suggestions,
            pad_token_id=generator_pipeline.tokenizer.eos_token_id,
            return_full_text=True # Para text-generation, si quieres el prompt + generacion
        )
        
        results = []
        for suggestion in suggestions:
            results.append(suggestion['generated_text'])
        
        return jsonify({"suggestions": results}), 200

    except Exception as e:
        print(f"Error al autocompletar código: {e}", file=sys.stderr)
        return jsonify({"error": f"Error interno del servidor al autocompletar código: {str(e)}"}), 500

@api_bp.route('/fix', methods=['POST'])
def fix_code():
    """
    Endpoint para corregir código (errores y sangrías).
    Espera un JSON con el campo 'code'.
    """
    data, error_message, status_code = get_json_data(request)
    if error_message:
        return jsonify({"error": error_message}), status_code

    code_snippet = data.get('code')
    if not code_snippet:
        return jsonify({"error": "El campo 'code' es requerido."}), 400 # Mensaje de error unificado

    max_tokens = data.get("max_tokens", 256)

    text2text_pipeline = get_text2text_pipeline()
    if text2text_pipeline is None:
        return jsonify({"error": "Modelo de corrección no cargado."}), 500

    try:
        # Formular el prompt para la corrección de código.
        prompt = f"Corrige los errores de sintaxis y ajusta la sangría de este código:\n{code_snippet}"
        
        # Generar el código corregido.
        corrected_code = text2text_pipeline(
            prompt, 
            max_new_tokens=max_tokens, # Usar max_new_tokens
            do_sample=False # Eliminado: return_full_text=False
        )[0]['generated_text']
        
        return jsonify({"fixed_code": corrected_code}), 200

    except Exception as e:
        print(f"Error al corregir código: {e}", file=sys.stderr)
        return jsonify({"error": f"Error interno del servidor al corregir código: {str(e)}"}), 500

@api_bp.route('/convert', methods=['POST'])
def convert_code():
    """
    Endpoint para convertir código entre lenguajes.
    Espera un JSON con los campos 'code' y 'target_language'.
    """
    data, error_message, status_code = get_json_data(request)
    if error_message:
        return jsonify({"error": error_message}), status_code

    code_snippet = data.get('code')
    target_language = data.get('target_language') # ¡Cambiado de 'to_lang' a 'target_language'!
    
    if not code_snippet:
        return jsonify({"error": "El campo 'code' es requerido."}), 400
    if not target_language:
        return jsonify({"error": "El campo 'target_language' es requerido."}), 400 # Mensaje de error unificado

    max_tokens = data.get("max_tokens", 256)

    text2text_pipeline = get_text2text_pipeline()
    if text2text_pipeline is None:
        return jsonify({"error": "Modelo de conversión no cargado."}), 500

    # Lista de lenguajes soportados (puedes ampliarla)
    # Es crucial que tu modelo T5 haya sido entrenado o pueda manejar estas traducciones.
    supported_languages = ['python', 'javascript', 'java', 'c++', 'go', 'ruby'] 
    if target_language.lower() not in supported_languages:
        return jsonify({"error": f"El lenguaje objetivo '{target_language}' no es soportado."}), 400

    try:
        # Formular el prompt para la traducción de código.
        prompt = f"Traduce el siguiente fragmento de código al lenguaje {target_language}:\n{code_snippet}"
        
        # Generar el código traducido.
        translated_code = text2text_pipeline(
            prompt, 
            max_new_tokens=max_tokens, # Usando max_new_tokens
            do_sample=False # Eliminado: return_full_text=False
        )[0]['generated_text']
        
        return jsonify({"converted_code": translated_code}), 200

    except Exception as e:
        print(f"Error al convertir código: {e}", file=sys.stderr)
        return jsonify({"error": f"Error interno del servidor al convertir código: {str(e)}"}), 500