import requests
import json

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def _make_request(self, method, endpoint, headers=None, params=None, data=None, json_data=None):
        url = f"{self.base_url}{endpoint}"
        print(f"Making {method} request to: {url}")
        print(f"Headers: {headers}")
        print(f"Params: {params}")
        print(f"Data: {data}")
        print(f"JSON Data: {json_data}")

        try:
            response = requests.request(method, url, headers=headers, params=params, data=data, json=json_data)
            response.raise_for_status()  # Raise an exception for HTTP errors
            print(f"Response Status Code: {response.status_code}")
            print(f"Response Body: {response.text}")
            return {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "body": response.json() if response.headers.get('Content-Type', '').startswith('application/json') else response.text
            }
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
            return {
                "status_code": e.response.status_code,
                "headers": dict(e.response.headers),
                "body": e.response.text,
                "error": str(e)
            }
        except requests.exceptions.ConnectionError as e:
            print(f"Connection Error: {e}")
            return {"error": f"Connection Error: {e}"}
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return {"error": f"An unexpected error occurred: {e}"}

    def get(self, endpoint, headers=None, params=None):
        return self._make_request("GET", endpoint, headers=headers, params=params)

    def post(self, endpoint, headers=None, data=None, json_data=None):
        return self._make_request("POST", endpoint, headers=headers, data=data, json_data=json_data)

    def put(self, endpoint, headers=None, data=None, json_data=None):
        return self._make_request("PUT", endpoint, headers=headers, data=data, json_data=json_data)

    def delete(self, endpoint, headers=None, params=None):
        return self._make_request("DELETE", endpoint, headers=headers, params=params)