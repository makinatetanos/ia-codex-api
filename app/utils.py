# ia-codex-api/app/utils.py

from flask import request, jsonify

def get_json_data(req):
    """
    Intenta obtener datos JSON de una solicitud.
    Devuelve los datos JSON y None para error si es exitoso,
    o None para datos y un mensaje de error con un código de estado si falla.
    """
    if not req.is_json:
        return None, "Formato JSON inválido. Content-Type debe ser application/json.", 415
    
    data = req.get_json()
    if data is None:
        return None, "No se proporcionaron datos JSON o el JSON está vacío.", 400
    
    return data, None, None # Datos, Sin error, Sin código de estado de error