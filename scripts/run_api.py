# ia-codex-api/scripts/run_api.py

import subprocess
import sys
import os
import shutil # Para eliminar el venv si es necesario

def get_project_root():
    """Devuelve la ruta absoluta a la raíz del proyecto (donde esta .env, requirements.txt)."""
    # Asume que este script está en ia-codex-api/scripts/
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def create_and_activate_venv(project_root):
    """Crea y activa el entorno virtual si no existe, e instala dependencias."""
    venv_path = os.path.join(project_root, 'venv')
    
    # 1. Crear el entorno virtual si no existe
    if not os.path.exists(venv_path):
        print("Creando entorno virtual...")
        try:
            # Usa el 'python' que está ejecutando este script para crear el venv
            subprocess.check_call([sys.executable, '-m', 'venv', venv_path])
            print("Entorno virtual creado exitosamente.")
        except subprocess.CalledProcessError as e:
            print(f"Error al crear el entorno virtual: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("Entorno virtual ya existe.")

    # 2. Configurar sys.path para activar el entorno virtual programáticamente
    # Esto es equivalente a 'source venv/bin/activate' o 'call venv\Scripts\activate.bat'
    # Ajusta el PATH para que los ejecutables del venv sean los primeros
    venv_bin_dir = os.path.join(venv_path, 'Scripts' if sys.platform == 'win32' else 'bin')
    os.environ['PATH'] = venv_bin_dir + os.pathsep + os.environ['PATH']
    
    # Asegúrate de que sys.executable apunte al python del venv
    new_python_executable = os.path.join(venv_bin_dir, 'python')
    if os.path.exists(new_python_executable) and new_python_executable != sys.executable:
        # Reemplaza el ejecutable actual de Python con el del venv
        # Esto solo afecta al subprocess.check_call() subsiguiente, no al script actual.
        # Para que el script actual use el python del venv, tendríamos que re-ejecutarlo,
        # pero es más simple confiar en el PATH modificado para los subprocesos.
        pass # La modificación del PATH es suficiente para los subprocess.check_call

    # 3. Instalar dependencias
    requirements_path = os.path.join(project_root, 'requirements.txt')
    if not os.path.exists(requirements_path):
        print(f"Error: El archivo '{requirements_path}' no se encontró.", file=sys.stderr)
        sys.exit(1)

    print("Instalando/Actualizando dependencias...")
    try:
        # Usa el 'pip' que ahora está en el PATH (del venv)
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_path])
        print("Dependencias instaladas/actualizadas exitosamente.")
    except subprocess.CalledProcessError as e:
        print(f"Error al instalar dependencias: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    project_root = get_project_root()
    os.chdir(project_root) # Cambia el directorio de trabajo a la raíz del proyecto

    print(f"Directorio raíz del proyecto: {project_root}")

    # Asegúrate de que el .env esté presente
    env_path = os.path.join(project_root, '.env')
    if not os.path.exists(env_path):
        print("Advertencia: Archivo .env no encontrado en la raíz del proyecto.")
        print("Creando un archivo .env básico. Por favor, revisalo y configúralo.")
        with open(env_path, 'w') as f:
            f.write("FLASK_APP=\"app:create_app()\"\n")
            f.write("FLASK_ENV=development\n")
            f.write("DEBUG=True\n")
            f.write("API_PORT=5000\n")
            f.write("#HF_MODEL_AUTOCOMPLETE=distilgpt2\n")
            f.write("#HF_MODEL_TEXT2TEXT=t5-small\n")
        print("Archivo .env básico creado. Por favor, considera editarlo.")
    else:
        print("Archivo .env encontrado.")

    # Cargar variables de entorno desde .env
    # La librería 'python-dotenv' se encarga de esto cuando Flask arranca.
    # No necesitamos cargarlas explícitamente aquí para el script, a menos que el script
    # necesite acceder a ellas antes de que Flask se inicie.
    # Para la depuración, podemos printarlas:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=env_path) # Carga el .env para este script

    flask_app = os.getenv('FLASK_APP', "app:create_app()")
    flask_env = os.getenv('FLASK_ENV', 'development')
    debug_mode = os.getenv('DEBUG', 'False').lower() == 'true'
    api_port = int(os.getenv('API_PORT', 5000))

    print("\n--- Configuración de la API ---")
    print(f"FLASK_APP: {flask_app}")
    print(f"FLASK_ENV: {flask_env}")
    print(f"DEBUG: {debug_mode}")
    print(f"API_PORT: {api_port}")
    print("--------------------------\n")

    # Asegurarse de que el entorno virtual esté listo y dependencias instaladas
    create_and_activate_venv(project_root)

    # Comando para iniciar la aplicación
    if flask_env == 'development' and debug_mode:
        print("Ejecutando con el servidor de desarrollo de Flask (NO para producción)...")
        cmd = [sys.executable, '-m', 'flask', 'run', '--host=0.0.0.0', f'--port={api_port}']
    else:
        print("Ejecutando con Gunicorn...")
        # Gunicorn es un paquete de Python, su ejecutable estará en venv/bin o venv/Scripts
        # Lo llamamos vía python -m gunicorn para asegurar que se use el del venv.
        cmd = [sys.executable, '-m', 'gunicorn', '-w', '4', '-b', f'0.0.0.0:{api_port}', flask_app]

    try:
        print(f"Ejecutando comando: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
    except FileNotFoundError:
        print(f"Error: Asegúrate de que 'flask' o 'gunicorn' estén instalados en tu entorno virtual.", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error al iniciar la aplicación: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario.")
    
if __name__ == "__main__":
    main()