# Azure Functions MCP Server

Un serveur MCP (Model Context Protocol) déployé sur Azure Functions avec intégration Azure AI Foundry.

## 🚀 Fonctionnalités

- **Serveur MCP** : Implémentation complète du protocole MCP 2024-11-05
- **Azure Functions** : Déploiement serverless avec montée en charge automatique
- **Azure AI Foundry** : Intégration avec les services Azure AI
- **FastAPI** : API moderne et performante avec documentation automatique
- **Tests intégrés** : Suite de tests REST Client pour validation

## 📁 Structure du projet

```text
my-mcp-function/
├── function_app.py           # Handler Azure Function principal
├── host.json                 # Configuration Azure Functions
├── local.settings.json       # Variables d'environnement locales
├── requirements.txt          # Dépendances Python
├── deploy.md                 # Guide de déploiement
├── mcp_server/              # Module serveur MCP
│   ├── __init__.py
│   └── main.py              # Logique FastAPI et MCP
└── tests/                   # Tests et validation
    ├── README.md            # Guide des tests
    ├── mcp-server.http      # Tests fonctionnels
    ├── performance.http     # Tests de performance
    ├── error-cases.http     # Tests d'erreurs
    └── azure-ai-tools.http  # Tests Azure AI
```

## 🛠️ Installation

### Prérequis

- Python 3.8+
- Azure Functions Core Tools
- Azure CLI (pour le déploiement)
- VS Code avec l'extension REST Client (pour les tests)

### Installation locale

1. **Cloner le repository**

   ```bash
   git clone <repository-url>
   cd my-mcp-function
   ```

2. **Installer les dépendances**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configurer les variables d'environnement**
   
   Copiez `local.settings.json.example` vers `local.settings.json` et configurez :

   ```json
   {
     "IsEncrypted": false,
     "Values": {
       "AzureWebJobsStorage": "UseDevelopmentStorage=true",
       "FUNCTIONS_WORKER_RUNTIME": "python",
       "AZURE_CLIENT_ID": "your-client-id",
       "AZURE_CLIENT_SECRET_B64": "your-client-secret",
       "AZURE_TENANT_ID": "your-tenant-id",
       "AZURE_SUBSCRIPTION_ID": "your-subscription-id",
       "AZURE_RESOURCE_GROUP_NAME": "your-resource-group",
       "AZURE_PROJECT_NAME": "your-project-name"
     }
   }
   ```

## 🚀 Démarrage

### Développement local

1. **Démarrer la fonction Azure**

   ```bash
   func start
   ```

2. **Tester l'API**
   
   L'API sera disponible à `http://localhost:7071/api/mcpserver`

3. **Utiliser les tests REST Client**
   
   Ouvrez les fichiers `.http` dans VS Code et exécutez les requêtes.

### Déploiement sur Azure

Voir le fichier `deploy.md` pour les instructions détaillées de déploiement.

## 📡 API Endpoints

### GET /api/mcpserver

Vérification de l'état du serveur MCP.

**Réponse :**

```json
{
  "message": "MCP Server is running",
  "status": "ok"
}
```

### POST /api/mcpserver

Endpoint principal pour les requêtes MCP.

**Méthodes MCP supportées :**

- `initialize` : Initialisation du serveur
- `tools/list` : Liste des outils disponibles
- `tools/call` : Exécution d'un outil
- `resources/list` : Liste des ressources disponibles
- `resources/read` : Lecture d'une ressource

**Exemple de requête :**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {
      "name": "test-client",
      "version": "1.0.0"
    }
  }
}
```

## 🔧 Outils Azure AI disponibles

Le serveur MCP fournit des outils pour interagir avec Azure AI Foundry :

- **create_project** : Créer un nouveau projet Azure AI
- **list_projects** : Lister les projets Azure AI
- **get_project_info** : Obtenir les informations d'un projet
- **list_models** : Lister les modèles disponibles
- **deploy_model** : Déployer un modèle
- **create_evaluation** : Créer une évaluation
- **list_evaluations** : Lister les évaluations

## 🧪 Tests

### Tests fonctionnels

```bash
# Démarrer la fonction localement
func start

# Utiliser VS Code REST Client pour exécuter les tests
# Ouvrir tests/mcp-server.http et cliquer sur "Send Request"
```

### Tests de performance

Les tests de performance sont disponibles dans `tests/performance.http` et permettent de tester :

- Charge simultanée
- Temps de réponse
- Stabilité sous charge

### Tests d'erreurs

Les tests d'erreurs dans `tests/error-cases.http` valident :

- Gestion des erreurs HTTP
- Validation des données d'entrée
- Réponses d'erreur MCP

## 📊 Monitoring

Le serveur inclut un logging détaillé pour :

- Suivi des requêtes MCP
- Monitoring des erreurs
- Métriques de performance

## 🛡️ Sécurité

- Authentification Azure AD intégrée
- Gestion sécurisée des secrets via Azure Key Vault
- Validation des données d'entrée
- Logging sécurisé (pas d'exposition de secrets)

## 📚 Documentation

- [Azure Functions Documentation](https://docs.microsoft.com/en-us/azure/azure-functions/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Azure AI Foundry Documentation](https://docs.microsoft.com/en-us/azure/ai-services/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## 🤝 Contribution

1. Fork le repository
2. Créer une branche feature (`git checkout -b feature/amazing-feature`)
3. Commit les changements (`git commit -m 'Add amazing feature'`)
4. Push vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 Support

Pour obtenir de l'aide :

1. Consultez la documentation dans `tests/README.md`
2. Vérifiez les issues GitHub existantes
3. Créez une nouvelle issue avec les détails du problème


