# ia-codex-api/app/models.py

import sys
import os
from transformers import pipeline
import torch

# Variables globales para almacenar los pipelines
generator_pipeline = None
text2text_pipeline = None
device = -1 # Valor por defecto, se actualiza en load_models

def load_models(app_config):
    """
    Carga los pipelines de modelos de Hugging Face.
    Esta función es llamada una vez al inicio de la aplicación Flask.
    """
    global generator_pipeline, text2text_pipeline, device

    device = 0 if torch.cuda.is_available() else -1
    print(f"Device set to use {'cuda' if device == 0 else 'cpu'}")

    # Carga de modelos preentrenados (se descargan si no existen localmente)
    # Los nombres de los modelos se obtienen de la configuración de la aplicación (que viene del .env).

    # Modelo para autocompletado de código
    autocomplete_model_name = app_config.get('HF_MODEL_AUTOCOMPLETE', 'distilgpt2')
    print(f"Cargando modelo de autocompletado: {autocomplete_model_name}...")
    try:
        generator_pipeline = pipeline(
            "text-generation",
            model=autocomplete_model_name,
            device=device,
            torch_dtype=torch.float16 if device == 0 else None # Usar float16 en GPU para menor consumo de memoria
        )
        print(f"Modelo '{autocomplete_model_name}' cargado para autocompletado.")
    except Exception as e:
        print(f"Error al cargar el modelo de autocompletado {autocomplete_model_name}: {e}", file=sys.stderr)
        generator_pipeline = None # Asegurarse de que el pipeline sea None si falla la carga

    # Modelo para corrección y conversión de código (text-to-text)
    text2text_model_name = app_config.get('HF_MODEL_TEXT2TEXT', 't5-small')
    print(f"Cargando modelo de texto a texto: {text2text_model_name}...")
    try:
        text2text_pipeline = pipeline(
            "text2text-generation",
            model=text2text_model_name,
            device=device,
            torch_dtype=torch.float16 if device == 0 else None
        )
        print(f"Modelo '{text2text_model_name}' cargado para corrección/conversión.")
    except Exception as e:
        print(f"Error al cargar el modelo de texto a texto {text2text_model_name}: {e}", file=sys.stderr)
        text2text_pipeline = None # Asegurarse de que el pipeline sea None si falla la carga


def get_generator_pipeline():
    """Devuelve el pipeline del modelo de generación/autocompletado."""
    return generator_pipeline

def get_text2text_pipeline():
    """Devuelve el pipeline del modelo de texto a texto/corrección/conversión."""
    return text2text_pipeline

# Las funciones de inferencia ahora usan los pipelines globales
def autocomplete_code(prompt: str) -> str:
    """
    Genera autocompletado de código para un prompt dado.
    """
    pipeline = get_generator_pipeline()
    if pipeline is None:
        raise RuntimeError("Modelo de autocompletado no disponible.")
    
    # max_length para controlar la longitud del código generado
    outputs = pipeline(prompt, max_new_tokens=100, num_return_sequences=1, do_sample=False)
    return outputs[0]['generated_text']

def fix_code(code: str) -> str:
    """
    Intenta corregir errores en un fragmento de código.
    """
    pipeline = get_text2text_pipeline()
    if pipeline is None:
        raise RuntimeError("Modelo de corrección no disponible.")
    
    input_text = f"Corrige el siguiente código:\n{code}" # Prompt más simple y directo
    outputs = pipeline(input_text, max_new_tokens=200, do_sample=False, return_full_text=False)
    return outputs[0]['generated_text']

def convert_code(code: str, target_language: str) -> str:
    """
    Convierte código de un lenguaje a otro.
    """
    pipeline = get_text2text_pipeline()
    if pipeline is None:
        raise RuntimeError("Modelo de conversión no disponible.")

    input_text = f"Traduce el siguiente código a {target_language}:\n{code}"
    outputs = pipeline(input_text, max_new_tokens=500, do_sample=False, return_full_text=False)
    return outputs[0]['generated_text']