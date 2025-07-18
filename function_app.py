import json
import azure.functions as func
import logging
import asyncio

app = func.FunctionApp()


@app.route(route="mcpserver", auth_level=func.AuthLevel.ANONYMOUS)
def mcpserver(req: func.HttpRequest) -> func.HttpResponse:
    """Azure Function HTTP Trigger pour le serveur MCP - Proxy vers FastAPI"""
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # Pour les requêtes GET, retourner une réponse simple
        if req.method == "GET":
            return func.HttpResponse(
                json.dumps(
                    {"message": "MCP Server is running", "status": "ok"}),
                status_code=200,
                headers={"Content-Type": "application/json"}
            )

        # Pour les requêtes POST, traiter le contenu MCP
        if req.method == "POST":
            try:
                body = req.get_body()
                if body:
                    request_data = json.loads(body.decode('utf-8'))
                    logging.info(f'Received MCP request: {request_data}')

                    # Traiter les différentes méthodes MCP
                    method = request_data.get("method", "")
                    request_id = request_data.get("id", 1)
                    params = request_data.get("params", {})

                    if method == "initialize":
                        response_data = {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "result": {
                                "protocolVersion": "2024-11-05",
                                "capabilities": {
                                    "tools": {},
                                    "resources": {}
                                },
                                "serverInfo": {
                                    "name": "azure-ai-foundry-mcp",
                                    "version": "1.0.0"
                                }
                            }
                        }
                    elif method == "tools/list":
                        response_data = {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "result": {
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
                        }
                    elif method == "tools/call":
                        # Importer et utiliser la logique du serveur MCP
                        from mcp_server.main import call_tool_logic

                        tool_name = params.get("name", "")
                        arguments = params.get("arguments", {})

                        try:
                            # Appeler la fonction de traitement des outils
                            result = asyncio.run(
                                call_tool_logic(tool_name, arguments))

                            response_data = {
                                "jsonrpc": "2.0",
                                "id": request_id,
                                "result": {
                                    "content": [
                                        {
                                            "type": "text",
                                            "text": result
                                        }
                                    ]
                                }
                            }
                        except Exception as e:
                            logging.error(f'Error calling tool: {str(e)}')
                            response_data = {
                                "jsonrpc": "2.0",
                                "id": request_id,
                                "error": {
                                    "code": -32603,
                                    "message": f"Erreur lors de l'exécution de l'outil: {str(e)}"
                                }
                            }
                    elif method == "resources/list":
                        response_data = {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "result": {
                                "resources": []
                            }
                        }
                    elif method == "ping":
                        response_data = {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "result": {}
                        }
                    else:
                        response_data = {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "error": {
                                "code": -32601,
                                "message": f"Méthode non supportée: {method}"
                            }
                        }

                    return func.HttpResponse(
                        json.dumps(response_data),
                        status_code=200,
                        headers={"Content-Type": "application/json"}
                    )
                else:
                    return func.HttpResponse(
                        json.dumps({"error": "No body provided"}),
                        status_code=400,
                        headers={"Content-Type": "application/json"}
                    )
            except json.JSONDecodeError:
                return func.HttpResponse(
                    json.dumps({"error": "Invalid JSON"}),
                    status_code=400,
                    headers={"Content-Type": "application/json"}
                )

        # Méthode non supportée
        return func.HttpResponse(
            json.dumps({"error": "Method not supported"}),
            status_code=405,
            headers={"Content-Type": "application/json"}
        )

    except Exception as e:
        logging.error(f'Error processing request: {str(e)}')
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            headers={"Content-Type": "application/json"}
        )
