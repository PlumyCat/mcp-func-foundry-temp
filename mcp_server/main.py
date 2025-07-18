import os
import base64
import asyncio
from typing import Any, Sequence
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from mcp import McpError, Tool
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent
from pydantic import BaseModel
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential, ClientSecretCredential

# Charger les variables d'environnement
load_dotenv()

# Configuration Azure AI Foundry


def get_azure_credential():
    try:
        credential = DefaultAzureCredential()
        return credential
    except Exception:
        # Essayer de lire les secrets depuis les fichiers Docker secrets
        def read_secret(name):
            try:
                with open(f'/run/secrets/{name}', 'r') as f:
                    return f.read().strip()
            except FileNotFoundError:
                return os.getenv(name.upper().replace('-', '_'))

        tenant_id = read_secret(
            'azure-tenant-id') or os.getenv("AZURE_TENANT_ID")
        client_id = read_secret(
            'azure-client-id') or os.getenv("AZURE_CLIENT_ID")
        b64_secret = os.getenv("AZURE_CLIENT_SECRET_B64")
        client_secret = read_secret(
            'azure-client-secret') or base64.b64decode(b64_secret).decode("utf-8")

        if tenant_id and client_id and client_secret:
            return ClientSecretCredential(
                tenant_id=tenant_id,
                client_id=client_id,
                client_secret=client_secret
            )
        else:
            raise Exception("Variables d'environnement ou secrets manquants")

# Modèles Pydantic pour FastAPI


class ToolCallParams(BaseModel):
    name: str
    arguments: dict


class ToolCallRequest(BaseModel):
    method: str
    params: ToolCallParams


class TextContentResponse(BaseModel):
    type: str = "text"
    text: str


class ToolResponse(BaseModel):
    content: list[TextContentResponse]


class HealthResponse(BaseModel):
    status: str
    timestamp: str


# Créer l'application FastAPI
app = FastAPI(
    title="Azure AI Foundry MCP Server",
    description="Serveur MCP pour exécuter du code et analyser des données via Azure AI Foundry",
    version="1.0.0"
)

# Créer le serveur MCP
mcp_server = Server("azure-ai-foundry")


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Endpoint de vérification de santé"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat()
    )


@app.get("/mcp/tools")
async def list_tools():
    """Liste les outils disponibles"""
    return {
        "tools": [
            {
                "name": "execute_code",
                "description": "Exécute du code Python via Azure AI Foundry Code Interpreter",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "Le code Python à exécuter ou la tâche à accomplir"
                        }
                    },
                    "required": ["message"]
                }
            },
            {
                "name": "analyze_data",
                "description": "Analyse des données avec Azure AI Foundry",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "La question d'analyse ou la tâche d'analyse de données"
                        },
                        "data_context": {
                            "type": "string",
                            "description": "Contexte des données ou format des données à analyser"
                        }
                    },
                    "required": ["message"]
                }
            }
        ]
    }


async def call_tool_logic(tool_name: str, arguments: dict) -> str:
    """Logique de traitement des outils extraite pour utilisation dans Azure Functions"""
    try:
        # Configuration Azure
        credential = get_azure_credential()
        endpoint = os.getenv("AZURE_AI_FOUNDRY_ENDPOINT")
        agent_id = os.getenv("AZURE_AI_AGENT_ID")

        project = AIProjectClient(
            credential=credential,
            endpoint=endpoint
        )

        if tool_name == "execute_code":
            message = arguments.get("message", "")
            if not message:
                raise Exception("Message requis")

            # Créer un thread
            thread = project.agents.threads.create()

            # Envoyer le message
            project.agents.messages.create(
                thread_id=thread.id,
                role="user",
                content=f"Exécute ce code Python: {message}"
            )

            # Exécuter
            run = project.agents.runs.create_and_process(
                thread_id=thread.id,
                agent_id=agent_id
            )

            if run.status == "failed":
                return f"Erreur d'exécution: {run.last_error}"

            # Récupérer la réponse
            messages = project.agents.messages.list(thread_id=thread.id)

            for msg in messages:
                if msg.role == "assistant" and msg.text_messages:
                    response = msg.text_messages[-1].text.value
                    return f"✅ Code exécuté avec succès:\n\n{response}"

            return "✅ Code exécuté mais aucune réponse reçue"

        elif tool_name == "analyze_data":
            message = arguments.get("message", "")
            data_context = arguments.get("data_context", "")

            if not message:
                raise Exception("Message requis")

            # Créer un thread
            thread = project.agents.threads.create()

            # Construire le message d'analyse
            analysis_prompt = f"""
            Analyse les données suivantes:
            Context: {data_context}
            Question: {message}
            
            Fournis une analyse détaillée avec du code Python si nécessaire.
            """

            # Envoyer le message
            project.agents.messages.create(
                thread_id=thread.id,
                role="user",
                content=analysis_prompt
            )

            # Exécuter
            run = project.agents.runs.create_and_process(
                thread_id=thread.id,
                agent_id=agent_id
            )

            if run.status == "failed":
                return f"Erreur d'analyse: {run.last_error}"

            # Récupérer la réponse
            messages = project.agents.messages.list(thread_id=thread.id)

            for msg in messages:
                if msg.role == "assistant" and msg.text_messages:
                    response = msg.text_messages[-1].text.value
                    return f"📊 Analyse terminée:\n\n{response}"

            return "📊 Analyse terminée mais aucune réponse reçue"

        else:
            raise Exception(f"Outil inconnu: {tool_name}")

    except Exception as e:
        raise Exception(f"Erreur: {str(e)}")


@app.post("/mcp/call", response_model=ToolResponse)
async def call_tool(request: ToolCallRequest):
    """Appelle un outil spécifique"""

    if request.method != "tools/call":
        raise HTTPException(status_code=400, detail="Méthode non supportée")

    tool_name = request.params.name
    arguments = request.params.arguments

    try:
        result = await call_tool_logic(tool_name, arguments)
        return ToolResponse(content=[
            TextContentResponse(text=result)
        ])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Lancer le serveur FastAPI
    uvicorn.run(app, host="0.0.0.0", port=8000)
