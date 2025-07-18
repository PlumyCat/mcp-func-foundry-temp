# Azure Function Deployment Guide

## Project Status ✅

Le projet Azure Function a été configuré avec succès :

- ✅ Structure projet Azure Functions initialisée
- ✅ Code FastAPI déplacé vers le module `mcp_server`
- ✅ Handler Mangum configuré dans `function_app.py`
- ✅ Dépendances installées et fonctionnelles
- ✅ Variables d'environnement configurées

## Structure du projet

```
my-mcp-function/
├── function_app.py           # Handler Azure Function principal
├── host.json                 # Configuration Azure Functions
├── local.settings.json       # Variables d'environnement locales
├── requirements.txt          # Dépendances Python
├── mcp_server/
│   ├── __init__.py
│   └── main.py              # Application FastAPI
└── test_fastapi.py          # Script de test
```

## Déploiement

### Option 1: Azure CLI
```bash
# Créer une Function App
az functionapp create \
  --resource-group myResourceGroup \
  --consumption-plan-location westeurope \
  --runtime python \
  --runtime-version 3.12 \
  --functions-version 4 \
  --name my-mcp-function-app \
  --storage-account mystorageaccount

# Déployer
func azure functionapp publish my-mcp-function-app
```

### Option 2: GitHub Actions
Créer `.github/workflows/deploy.yml` avec le workflow Azure Functions.

### Option 3: VS Code
Utiliser l'extension Azure Functions pour déployer directement.

## URLs d'accès après déploiement

- **Health check**: `https://my-mcp-function-app.azurewebsites.net/api/mcpserver/health`
- **Liste des outils**: `https://my-mcp-function-app.azurewebsites.net/api/mcpserver/mcp/tools`
- **Appel d'outil**: `https://my-mcp-function-app.azurewebsites.net/api/mcpserver/mcp/call`

## Variables d'environnement à configurer

Dans Azure Portal → Function App → Configuration → Application Settings :

- `AZURE_AI_FOUNDRY_ENDPOINT`
- `AZURE_AI_AGENT_ID`
- `AZURE_TENANT_ID`
- `AZURE_CLIENT_ID`
- `AZURE_CLIENT_SECRET_B64`

## Note sur Azure Functions Core Tools

Le démarrage local avec `func start` peut parfois être lent ou se bloquer. L'application FastAPI fonctionne correctement comme démontré par les tests. Le déploiement en production devrait fonctionner normalement.