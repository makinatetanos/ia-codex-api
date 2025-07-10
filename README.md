# IA Codex API - Asistente de Programación con IA

Servicio RESTful que utiliza modelos de inteligencia artificial para autocompletar, corregir y convertir código entre lenguajes.

---

## Tabla de Contenidos

- [Características](#características)  
- [Estructura del Proyecto](#estructura-del-proyecto)  
- [Requisitos](#requisitos)  
- [Instalación](#instalación)  
- [Configuración](#configuración)  
- [Uso](#uso)  
  - [Ejecutar la API](#ejecutar-la-api)  
  - [Endpoints](#endpoints)  
- [Pruebas](#pruebas)  
- [Contribución](#contribución)  
- [Licencia](#licencia)  
- [Contacto](#contacto)  

---

## Características

- Autocompletado inteligente de código.  
- Corrección de sintaxis y formato.  
- Conversión entre diferentes lenguajes de programación.  
- API RESTful simple y modular.

---

## Estructura del Proyecto

ia-codex-api/
├── app/
│   ├── __init__.py          # Inicializa Flask y carga modelos.
│   ├── api.py               # Definición de rutas y lógica.
│   ├── models.py            # Gestión de modelos IA.
│   └── utils.py             # Funciones auxiliares.
├── tests/
│   └── test\_api.py          # Pruebas unitarias.
├── .env.example             # Ejemplo variables entorno.
├── .gitignore               # Ignora archivos en Git.
├── README.md                # Este archivo.
└── requirements.txt         # Dependencias.

---

## Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes)

---

## Instalación

Clona el repositorio y crea entorno virtual:

```bash
git clone https://github.com/tu-usuario/ia-codex-api.git
cd ia-codex-api
python -m venv venv
````

Activa el entorno:

Windows:

```bash
.\venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

Instala las dependencias:

```bash
pip install -r requirements.txt
```

---

## Configuración

Crea un archivo `.env` en la raíz con:

```env
DEBUG=True
API_PORT=5000
HF_MODEL_AUTOCOMPLETE=distilgpt2
HF_MODEL_TEXT2TEXT=t5-small
```

> Importante: No subir `.env` a Git.

---

## Uso

### Ejecutar la API

Para iniciar la API, simplemente ejecuta el script `run_api.py` desde la raíz del proyecto:

```bash
python scripts/run_api.py
```

O simplemente:

```bash
flask --app app run
```

La API estará disponible en `http://127.0.0.1:5000/`.

### Endpoints

| Método | Ruta        | Descripción                       |
| ------ | ----------- | --------------------------------- |
| GET    | `/`         | Estado y bienvenida de la API     |
| POST   | `/complete` | Autocompleta fragmentos de código |
| POST   | `/fix`      | Corrige código con errores        |
| POST   | `/convert`  | Convierte código entre lenguajes  |

#### Ejemplos de solicitudes y respuestas

- GET /

  Respuesta:

  ```json
  {
    "message": "Bienvenido a la IA Codex API. Utiliza /complete, /fix o /convert."
  }
  ```

- POST /complete

  Solicitud:

  ```json
  {
    "prompt": "def my_function():",
    "max_tokens": 100,
    "num_suggestions": 1
  }
  ```

  Respuesta:

  ```json
  {
    "suggestions": [
      "def my_function():\n    pass"
    ]
  }
  ```

- POST /fix

  Solicitud:

  ```json
  {
    "code": "pront('Hello World')"
  }
  ```

  Respuesta:

  ```json
  {
    "fixed_code": "print('Hello World')"
  }
  ```

- POST /convert

  Solicitud:

  ```json
  {
    "code": "console.log('Hello');",
    "target_language": "python"
  }
  ```

  Respuesta:

  ```json
  {
    "converted_code": "print('Hello')"
  }
  ```

---

## Pruebas

Ejecuta las pruebas con:

```bash
python -m pytest
```

---

## Contribución

1. Haz fork del repositorio.
2. Crea una rama nueva:

   ```bash
   git checkout -b feature/nueva-funcion
   ```

3. Realiza cambios y prueba.
4. Commit y push:

   ```bash
   git commit -m "Agrega nueva función"
   git push origin feature/nueva-funcion
   ```

5. Abre un Pull Request.

---

## Licencia

GPLv3. Consulta el archivo `LICENSE` para detalles.

---

## Contacto

[Repositorio GitHub](https://github.com/tu-usuario/ia-codex-api)
