Este proyecto tiene como objetivo desarrollar un chatbot o asistente capaz de mantener conversaciones amigables y proporcionar respuestas precisas sobre el contenido presente en la página web de la empresa Scalian.

## **Características Principales:**

**Scraper para Descarga de Contenido:**

- Se diseñó un scraper para descargar de manera eficiente el contenido de cualquier pagina web con textos.
- El contenido extraído se sometió a un proceso de organización para asegurar la coherencia y relevancia de la información.
- El scraper fue dockerizado para encapsularlo en un contenedor independiente. Este enfoque ofrece portabilidad, gestión eficiente de dependencias, aislamiento y seguridad mejorada. Facilita el despliegue, escalabilidad, control de recursos y gestión de versiones, asegurando un entorno consistente y eficiente en diversos escenarios operativos.

**Desarrollo del Bot**

1. **Frontend con Reflex y Despliegue Integrado:**
    - El frontend fue desarrollado utilizando el framework Reflex, proporcionando una interfaz de usuario intuitiva. Además, se implementó un proceso de despliegue integrado para facilitar la implementación y actualización del sistema.
2. **Desarrollo del Backend con LangChain:**
    - Se generaron embeddings a partir del contenido organizado y se almacenaron en una base de datos vectorial Faiss para facilitar búsquedas rápidas y precisas durante las interacciones con el chatbot.
    - Utilizando el framework LangChain, se creó un backend robusto que gestiona las solicitudes del chatbot, la recuperación de información desde Faiss y la conexión con la API de OpenAI para respuestas contextuales.

## Instalación

Sigue las instrucciones para ver la documentacion


## 📖 Ver la documentación

[Documentación](https://www.notion.so/834c68c20997416dac22de61275b5c53?v=df1039e52bd64604b5cfa1b354a55bed&pvs=4)


## Autores

- [@Galyna](https://github.com/Gala1812)
- [@Carol](https://github.com/CGP20)
- [@Camilo](https://github.com/Gala1812)
- [@Javi](https://github.com/kamilodev)
- [@David](https://github.com/luisdavidtribino)

