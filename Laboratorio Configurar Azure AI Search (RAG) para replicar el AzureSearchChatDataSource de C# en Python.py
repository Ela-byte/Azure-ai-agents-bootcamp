# Laboratorio Configurar Azure AI Search (RAG) para replicar el AzureSearchChatDataSource de C# en Python
import os
from openai import AzureOpenAI
from dotenv import load_dotenv

# 1. Cargar las variables de entorno (Equivalente a DotNetEnv en C#)
# Requiere instalar el paquete: pip install python-dotenv
load_dotenv()

# 2. Obtener los valores (puedes adaptarlo para usar tu archivo ENV.py si prefieres)
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_KEY")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o") # O "gpt-5-mini" según tu entorno

search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
search_key = os.getenv("AZURE_SEARCH_KEY")
search_index = os.getenv("AZURE_SEARCH_INDEX")

# 3. Inicializar el cliente de Azure OpenAI
client = AzureOpenAI(
    azure_endpoint=azure_endpoint,
    api_key=api_key,
    api_version="2024-08-01-preview" # Es crucial usar una versión preview para que soporte data_sources
)

# 4. Configurar Azure AI Search (RAG) para replicar el AzureSearchChatDataSource de C#
azure_search_config = {
    "data_sources": [
        {
            "type": "azure_search",
            "parameters": {
                "endpoint": search_endpoint,
                "index_name": search_index,
                "authentication": {
                    "type": "api_key",
                    "key": search_key
                }
            }
        }
    ]
}

# 5. Realizar la solicitud asíncrona con RAG habilitado
response = client.chat.completions.create(
    model=deployment_name, 
    messages=[
        {"role": "system", "content": "Eres un asistente que responde preguntas basándose exclusivamente en los documentos internos proporcionados."},
        {"role": "user", "content": "¿politicas?"},
    ],
    extra_body=azure_search_config # Aquí se enlaza la fuente de datos
)

# 6. Imprimir la respuesta generada
print("Respuesta:")
print(response.choices[0].message.content)

# Opcional: Extraer las citas (citations) devueltas por Azure Search
message_context = response.choices[0].message.model_dump().get("context")
if message_context and "citations" in message_context:
    print("\nFuentes consultadas:")
    for citation in message_context["citations"]:
        print(f"- {citation.get('title')} ({citation.get('url')})")