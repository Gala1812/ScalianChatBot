import os
import sys
from dotenv import load_dotenv

load_dotenv()


def get_openai_api_key():
    """
    Obtiene la clave API de OpenAI del entorno. Si no está disponible, detiene la ejecución del programa.

    Returns:
        La clave API de OpenAI.
    """
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print("Por favor crea una variable de ambiente OPENAI_API_KEY.")
        sys.exit()
    return openai_api_key
