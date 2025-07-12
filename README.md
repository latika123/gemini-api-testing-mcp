# **Gemini API Testing with Model Context Protocol (MCP)**

This project demonstrates how to set up an API testing framework using the Google Gemini Command Line Interface (CLI) integrated with a custom Model Context Protocol (MCP) server. This allows you to leverage Gemini's AI capabilities for understanding API specifications, generating test prompts, and orchestrating API calls for testing purposes.

## **Project Structure**

gemini-api-testing-mcp/  
├── .gemini/  
│   └── settings.json                  \# Gemini CLI settings and MCP server configuration  
├── mcp-server/  
│   ├── app.py                         \# Python Flask server acting as the MCP  
│   ├── requirements.txt               \# Python dependencies for the MCP server  
│   └── api\_client.py                  \# Module for making actual HTTP API calls  
├── api-specs/  
│   └── example\_api.yaml               \# OpenAPI/Swagger specification of the API to test  
├── test-data/  
│   └── users\_data.json                \# Sample data for API requests (adapt as needed)  
└── README.md                          \# Project documentation

## **Features**

* **AI-Driven API Interaction**: Use natural language prompts via Gemini CLI to trigger API requests.  
* **OpenAPI Specification Integration**: The MCP server can load and (conceptually) leverage your example\_api.yaml for better understanding of API endpoints and parameters.  
* **Extensible MCP Server**: Easily extend mcp-server/app.py to support more complex API operations, parameter parsing, and response validation logic.

## **Prerequisites**

Before you begin, ensure you have the following installed:

* **Node.js and npm**: Required for installing Gemini CLI.  
* **Python 3.8+**: Required for the Flask MCP server.  
* **Gemini CLI**: You have a couple of options for installation:

Quick Start (Recommended): This method directly executes the CLI from its GitHub repository without a global installation.

Bash

npx https://github.com/google-gemini/gemini-cli
Global Installation (Persistent): This installs the Gemini CLI globally on your system, allowing you to run gemini from any directory.

Bash

npm install -g @google/gemini-cli gemini

* **Google Account with Gemini API Access**: You will need to authenticate your Gemini CLI. The free tier generally works by logging in with your personal Google account.

## **Setup Instructions**

### **1\. Gemini CLI Configuration**

Navigate to the root of this project (gemini-api-testing-mcp/).

1. Authenticate Gemini CLI:  
   Run the configuration command and follow the browser prompts to log in with your Google account. This grants the CLI access to the Gemini API.  
   gemini configure

2. Create .gemini/settings.json:  
   Create a directory named .gemini at the root of your project, and inside it, create a file named settings.json with the following content:  
   {  
     "mcpServer": {  
       "url": "http://localhost:5000/mcp",  
       "apiKey": "YOUR\_SECRET\_API\_KEY"  
     },  
     "defaultModel": "gemini-2.5-pro"  
   }

   **Important**: Replace "YOUR\_SECRET\_API\_KEY" with a strong, secret key. This key will be used by your MCP server for basic authentication.

### **2\. MCP Server Setup**

Navigate into the mcp-server directory.

1. **Install Python Dependencies**:  
   cd mcp-server  
   pip install \-r requirements.txt

2. Update mcp-server/app.py:  
   Open mcp-server/app.py and make the following critical update:  
   * **API\_BASE\_URL**: Set this variable to the actual base URL of the API you want to test. For example, if you are testing the JSONPlaceholder API:  
     API\_BASE\_URL \= "https://jsonplaceholder.typicode.com" \# \<--- UPDATE THIS

   * **MCP\_API\_KEY**: Ensure this matches the apiKey you set in .gemini/settings.json. For security, consider loading this from an environment variable in a production setup.  
3. Place your OpenAPI Specification:  
   Ensure your OpenAPI/Swagger file is located in the api-specs directory:  
   gemini-api-testing-mcp/api-specs/example\_api.yaml

## **Running the Project**

1. Start the MCP Server:  
   From the mcp-server/ directory, run the Flask application:  
   python app.py

   Keep this terminal window open; the server needs to be running for Gemini CLI to communicate with it.

2. #### **Interact with Gemini CLI for API Testing:**    **Open a new terminal window and navigate to the root of your project (gemini-api-testing-mcp/).**    **You can now use Gemini CLI to send commands to your MCP server, which will in turn interact with your API.**    **Example Commands:**

   1. Get the API Specification (loaded by MCP):  
      This command will ask the MCP server to return the loaded OpenAPI spec.  
      gemini ask "Can you get the API specification from the MCP server?"

   2. **Send a GET Request (e.g., to /users):**  
      gemini ask "Using the API testing MCP, send a GET request to /users"

   3. **Send a POST Request (e.g., to /users with data):**  
      gemini ask "Using the API testing MCP, send a POST request to /users with body {'name': 'New User', 'username': 'newuser', 'email': 'new.user@example.com'}"

Observe the output in both your Gemini CLI terminal and the MCP server's console to see the interaction.

## **Next Steps & Further Enhancements**

This project provides a basic foundation. Consider these enhancements:

* **More Robust Prompt Parsing**: Improve the regex patterns in app.py or implement a more advanced NLP approach to parse complex user queries for all your API endpoints.  
* **Dynamic Parameter Handling**: Automatically extract required and optional parameters from the example\_api.yaml to guide Gemini's prompt generation and the MCP's request construction.  
* **Response Validation**: Add code to api\_client.py or app.py to validate API responses against the schemas defined in your example\_api.yaml.  
* **Error Handling and Reporting**: Provide more detailed error messages and suggestions back to Gemini when API calls fail.  
* **Test Case Generation**: Explore having Gemini generate entire test suites (e.g., positive, negative, edge cases) based on your API specification.  
* **Authentication**: If your API requires more than a basic bearer token (e.g., OAuth2), integrate that into api\_client.py.  
* **Test Data Management**: Implement ways for Gemini to interact with and utilize the test-data/ files for dynamic request bodies.