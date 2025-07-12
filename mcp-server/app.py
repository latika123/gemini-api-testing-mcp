from flask import Flask, request, jsonify
from api_client import APIClient
import os
import yaml
import json

app = Flask(__name__)

# Basic API Key for MCP server (should be in env vars for production)
MCP_API_KEY = os.environ.get("MCP_API_KEY", "YOUR_SECRET_API_KEY")

# --- Initialize API Client ---
# IMPORTANT: Replace with the base URL of the API you want to test
# For demonstration, we'll use a public API.
# Example: JSONPlaceholder for testing users API
API_BASE_URL = "https://jsonplaceholder.typicode.com"
api_client = APIClient(API_BASE_URL)

# --- Load OpenAPI Spec (if available) ---
# This helps Gemini understand the API structure.
API_SPEC = None
try:
    with open('../api-specs/example_api.yaml', 'r') as f:
        API_SPEC = yaml.safe_load(f)
    print("OpenAPI spec loaded successfully.")
except FileNotFoundError:
    print("Warning: example_api.yaml not found. API understanding will be limited.")
except Exception as e:
    print(f"Error loading OpenAPI spec: {e}")

@app.route('/mcp', methods=['POST'])
def mcp_handler():
    logging.info("mcp_handler called")
    # Authenticate requests (simple check)
    if request.headers.get('X-Api-Key') != MCP_API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    logging.info(f"Request data: {data}")
    prompt = data.get('prompt', '')
    context = data.get('context', {})
    files = data.get('files', {})

    print(f"Received prompt: {prompt}")
    logging.info(f"Received prompt: {prompt}")
    print(f"Received context: {context}")
    print(f"Received files: {files.keys()}") # Files contains file names as keys, content as values

    response_data = {"result": "MCP processed your request."}
    
    # --- Context for API Specification ---
    # Provide the OpenAPI spec if requested or relevant to the prompt
    logging.info(f"API_SPEC is not None: {API_SPEC is not None}")
    if "get_api_spec" in prompt.lower() and API_SPEC:
        print("Returning API spec")
        logging.info("Returning API spec")
        response_data["api_spec"] = API_SPEC
        response_data["result"] = "Here is the OpenAPI specification."
        return jsonify(response_data)

    # --- API Testing Logic based on Prompt ---
    # This is where you parse Gemini's intent and call your API client
    # Example: Simple intent recognition for common API operations
    if "send get request" in prompt.lower():
        # Example: "send get request to /users"
        endpoint = prompt.split("to ")[-1].strip()
        headers = {} # You can parse headers from the prompt/context
        params = {}  # You can parse params from the prompt/context

        api_response = api_client.get(endpoint, headers=headers, params=params)
        response_data["api_response"] = api_response
        response_data["result"] = f"GET request to {endpoint} completed. Status: {api_response.get('status_code', 'N/A')}"
        return jsonify(response_data)

    elif "send post request" in prompt.lower():
        # Example: "send post request to /users with body {'name': 'John Doe'}"
        parts = prompt.split("to ")
        endpoint = parts[1].split(" with body")[0].strip()
        body_str = parts[1].split(" with body", 1)[1].strip() if " with body" in parts[1] else "{}"
        try:
            json_body = json.loads(body_str.replace("'", "\"")) # Simple way to parse, be careful with complex strings
        except json.JSONDecodeError:
            json_body = {}
            response_data["error"] = "Could not parse JSON body."

        headers = {'Content-Type': 'application/json'} # Default for POST JSON
        
        api_response = api_client.post(endpoint, headers=headers, json_data=json_body)
        response_data["api_response"] = api_response
        response_data["result"] = f"POST request to {endpoint} completed. Status: {api_response.get('status_code', 'N/A')}"
        return jsonify(response_data)
        
    # --- File Processing Example (e.g., analyzing API spec provided by Gemini) ---
    if 'example_api.yaml' in files:
        api_spec_content = files['example_api.yaml']
        try:
            loaded_spec = yaml.safe_load(api_spec_content)
            # Here you can process the spec, e.g., list endpoints, suggest tests
            endpoints = loaded_spec.get('paths', {}).keys()
            response_data["analysis"] = f"Analyzed API spec. Found endpoints: {', '.join(endpoints)}"
            response_data["result"] = "API specification analyzed successfully."
        except Exception as e:
            response_data["error"] = f"Failed to parse example_api.yaml: {e}"
        return jsonify(response_data)

    return jsonify(response_data)

if __name__ == '__main__':
    # For production, use a more robust WSGI server like Gunicorn or uWSGI
    print(f"Starting MCP server on http://localhost:5000. API Base URL: {API_BASE_URL}")
    print(f"MCP_API_KEY: {MCP_API_KEY}")
    app.run(debug=False, port=5000, use_reloader=False)