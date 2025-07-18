# REST Client Test Guide

## Prerequisites

1. **REST Client Extension**: Make sure you have installed the REST Client extension in VS Code
2. **Azure Function running**: Start your Azure Function locally with `func start`

## Test Structure

The `tests` folder contains the following files:

### 📁 Test Files

- **`mcp-server.http`**: Main functional tests
  - GET and POST tests
  - Valid MCP requests
  - Basic error tests (400, 405)

- **`performance.http`**: Performance tests
  - Load tests with multiple requests
  - Tests with different payload sizes
  - Timeout tests

- **`error-cases.http`**: Error case tests
  - Malformed JSON
  - Special characters
  - Edge cases and limits

- **`http-client.env.json`**: Environment configuration
  - Development environment (local)
  - Staging environment
  - Production environment

## How to Use

### 1. Start the Azure Function

```bash
# In the terminal, from your function's root folder
func start
```

### 2. Run the tests

1. Open a `.http` file in VS Code
2. Click "Send Request" above each request
3. Or use the shortcut `Ctrl+Alt+R` (Windows/Linux) or `Cmd+Alt+R` (Mac)

### 3. Switch environment

To use a different environment:

1. Open the command palette (`Ctrl+Shift+P`)
2. Type "REST Client: Switch Environment"
3. Select the desired environment (dev, staging, production)

## Included Test Types

### ✅ Functional tests
- Server status check (GET)
- Valid MCP requests (POST)
- Common error handling

### ⚡ Performance tests
- Multiple simultaneous requests
- Various payload sizes
- Timeout tests

### 🚨 Error tests
- Malformed JSON
- Unsupported HTTP methods
- Special characters and edge cases
- Requests without body or with incorrect Content-Type

## Expected Results

### Success responses (200)
```json
{
  "message": "MCP Server is running",
  "status": "ok"
}
```

### Error responses
- **400**: Bad Request (invalid JSON, no body)
- **405**: Method Not Allowed (unsupported HTTP method)
- **500**: Internal Server Error (internal error)

## Customization

### Edit URLs
Edit the `http-client.env.json` file to point to your own Azure environments.

### Add new tests
Create new `.http` files or add tests to existing files using the format:

```http
### Test description
POST {{baseUrl}}/api/{{functionName}}
Content-Type: application/json

{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "your_method",
  "params": {}
}
```

## Best Practices

1. **Organize your tests**: Separate tests by feature
2. **Use variables**: Take advantage of environment variables
3. **Document your tests**: Add descriptive comments
4. **Test all cases**: Include both success and error cases
5. **Check responses**: Review status codes and JSON responses

## Troubleshooting

- **Connection error**: Make sure the Azure Function is running
- **Different port**: Change the `baseUrl` in `http-client.env.json`
- **Timeout**: Adjust the `timeout` value in the configuration
