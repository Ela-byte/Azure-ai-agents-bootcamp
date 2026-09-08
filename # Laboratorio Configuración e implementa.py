# Laboratorio  Configuración e implementación de soluciones en Azure AI Foundry en Python
#Instalando mi paquete dependencias
#pip install openai
#Liberias a usar
import os
import ENV
from openai import AzureOpenAI

"""Construir mi objeto cliente"""
#Api Rest para conectarme a Azure OpenAI
client = AzureOpenAI(
    azure_endpoint = "https://bancaempresas.openai.azure.com/",
    api_key= ENV.candado["api_key"],
    api_version="2024-08-01-preview"
)

#llamando a la API de Azure OpenAI para generar una respuesta a un mensaje de usuario
response = client.chat.completions.create(
    model="gpt-5-mini",
    messages=[
        {"role": "system", "content": "Eres un asistente muy útil."},
        {"role": "user", "content": "¿Cuál es tu nombre?"},
    ],
)
#Imprimir la respuesta generada por el modelo
print(response.choices[0].message.content)