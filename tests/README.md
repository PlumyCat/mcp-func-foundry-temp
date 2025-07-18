# Guide d'utilisation des tests REST Client

## Prérequis

1. **Extension REST Client** : Assurez-vous d'avoir installé l'extension REST Client dans VS Code
2. **Fonction Azure en cours d'exécution** : Démarrez votre fonction Azure localement avec `func start`

## Structure des tests

Le dossier `tests` contient les fichiers suivants :

### 📁 Fichiers de test

- **`mcp-server.http`** : Tests fonctionnels principaux
  - Tests GET et POST
  - Requêtes MCP valides
  - Tests d'erreurs de base (400, 405)

- **`performance.http`** : Tests de performance
  - Tests de charge avec requêtes multiples
  - Tests avec payloads de différentes tailles
  - Tests de timeout

- **`error-cases.http`** : Tests de cas d'erreur
  - JSON malformé
  - Caractères spéciaux
  - Cas limites et edge cases

- **`http-client.env.json`** : Configuration des environnements
  - Environnement de développement (local)
  - Environnement de staging
  - Environnement de production

## Comment utiliser

### 1. Démarrer la fonction Azure

```bash
# Dans le terminal, depuis le dossier racine de votre fonction
func start
```

### 2. Exécuter les tests

1. Ouvrez un fichier `.http` dans VS Code
2. Cliquez sur "Send Request" au-dessus de chaque requête
3. Ou utilisez le raccourci `Ctrl+Alt+R` (Windows/Linux) ou `Cmd+Alt+R` (Mac)

### 3. Changer d'environnement

Pour utiliser un environnement différent :

1. Ouvrez la palette de commandes (`Ctrl+Shift+P`)
2. Tapez "REST Client: Switch Environment"
3. Sélectionnez l'environnement désiré (dev, staging, production)

## Types de tests inclus

### ✅ Tests fonctionnels
- Vérification du statut du serveur (GET)
- Requêtes MCP valides (POST)
- Gestion des erreurs courantes

### ⚡ Tests de performance
- Requêtes multiples simultanées
- Payloads de tailles variées
- Tests de timeout

### 🚨 Tests d'erreur
- JSON malformé
- Méthodes HTTP non supportées
- Caractères spéciaux et cas limites
- Requêtes sans body ou avec Content-Type incorrect

## Résultats attendus

### Réponses de succès (200)
```json
{
  "message": "MCP Server is running",
  "status": "ok"
}
```

### Réponses d'erreur
- **400** : Bad Request (JSON invalide, pas de body)
- **405** : Method Not Allowed (méthode HTTP non supportée)
- **500** : Internal Server Error (erreur interne)

## Personnalisation

### Modifier les URLs
Éditez le fichier `http-client.env.json` pour pointer vers vos propres environnements Azure.

### Ajouter de nouveaux tests
Créez de nouveaux fichiers `.http` ou ajoutez des tests aux fichiers existants en suivant le format :

```http
### Description du test
POST {{baseUrl}}/api/{{functionName}}
Content-Type: application/json

{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "your_method",
  "params": {}
}
```

## Bonnes pratiques

1. **Organisez vos tests** : Séparez les tests par fonctionnalité
2. **Utilisez les variables** : Profitez des variables d'environnement
3. **Documentez vos tests** : Ajoutez des commentaires descriptifs
4. **Testez tous les cas** : Incluez les cas de succès et d'erreur
5. **Vérifiez les réponses** : Examinez les codes de statut et les réponses JSON

## Dépannage

- **Erreur de connexion** : Vérifiez que la fonction Azure est démarrée
- **Port différent** : Modifiez le `baseUrl` dans `http-client.env.json`
- **Timeout** : Ajustez la valeur `timeout` dans la configuration
