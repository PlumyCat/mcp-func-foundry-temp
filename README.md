
# Azure Functions MCP Server

A Model Context Protocol (MCP) server deployed on Azure Functions with Azure AI Foundry integration.

## 🚀 Features

- **MCP Server**: Full implementation of MCP protocol 2024-11-05
- **Azure Functions**: Serverless deployment with automatic scaling
- **Azure AI Foundry**: Integration with Azure AI services
- **FastAPI**: Modern, high-performance API with automatic documentation
- **Integrated tests**: REST Client test suite for validation

## 📁 Project Structure

```text
my-mcp-function/
├── function_app.py           # Main Azure Function handler
├── host.json                 # Azure Functions configuration
├── local.settings.json       # Local environment variables
├── requirements.txt          # Python dependencies
├── deploy.md                 # Deployment guide
├── mcp_server/              # MCP server module
│   ├── __init__.py
│   └── main.py              # FastAPI and MCP logic
└── tests/                   # Tests and validation
    ├── README.md            # Test guide
    ├── mcp-server.http      # Functional tests
    ├── performance.http     # Performance tests
    ├── error-cases.http     # Error tests
    └── azure-ai-tools.http  # Azure AI tests
```

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- Azure Functions Core Tools
- Azure CLI (for deployment)
- VS Code with REST Client extension (for tests)

### Local Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd my-mcp-function
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   
   Copy `local.settings.json.example` to `local.settings.json` and configure:

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

## 🚀 Getting Started

### Local Development

1. **Start the Azure Function**

   ```bash
   func start
   ```

2. **Test the API**
   
   The API will be available at `http://localhost:7071/api/mcpserver`

3. **Use REST Client tests**
   
   Open the `.http` files in VS Code and run the requests.

### Deploy to Azure

See `deploy.md` for detailed deployment instructions.

## 📡 API Endpoints

### GET /api/mcpserver

Check MCP server status.

**Response:**

```json
{
  "message": "MCP Server is running",
  "status": "ok"
}
```

### POST /api/mcpserver

Main endpoint for MCP requests.

**Supported MCP methods:**

- `initialize`: Server initialization
- `tools/list`: List available tools
- `tools/call`: Execute a tool
- `resources/list`: List available resources
- `resources/read`: Read a resource

**Request example:**

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

## 🔧 Available Azure AI Tools

The MCP server provides tools to interact with Azure AI Foundry:

- **create_project**: Create a new Azure AI project
- **list_projects**: List Azure AI projects
- **get_project_info**: Get project information
- **list_models**: List available models
- **deploy_model**: Deploy a model
- **create_evaluation**: Create an evaluation
- **list_evaluations**: List evaluations

## 🧪 Tests

### Functional tests

```bash
# Start the function locally
func start

# Use VS Code REST Client to run tests
# Open tests/mcp-server.http and click "Send Request"
```

### Performance tests

Performance tests are available in `tests/performance.http` and allow you to test:

- Concurrent load
- Response time
- Stability under load

### Error tests

Error tests in `tests/error-cases.http` validate:

- HTTP error handling
- Input data validation
- MCP error responses

## 📊 Monitoring

The server includes detailed logging for:

- MCP request tracking
- Error monitoring
- Performance metrics

## 🛡️ Security

- Integrated Azure AD authentication
- Secure secret management via Azure Key Vault
- Input data validation
- Secure logging (no secret exposure)

## 📚 Documentation

- [Azure Functions Documentation](https://docs.microsoft.com/en-us/azure/azure-functions/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Azure AI Foundry Documentation](https://docs.microsoft.com/en-us/azure/ai-services/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## 🆘 Support

For help:

1. See the documentation in `tests/README.md`
2. Check existing GitHub issues
3. Create a new issue with details of your problem


