# client.py
import requests
from typing import Optional, Any, Dict
from config import BASE_URL, TIMEOUT, TOKEN_FILE
from json import JSONDecodeError

class ApiClient:
    def __init__(self, token: Optional[str] = None):
        self.base_url = BASE_URL
        self.session = requests.Session()
        
        # Load token from file if not provided
        if not token and TOKEN_FILE.exists():
            token = TOKEN_FILE.read_text().strip()
        
        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})
        self.session.headers.update({"Content-Type": "application/json"})

    def _request(self, method: str, path: str, params: Optional[Dict] = None, json: Optional[Dict] = None, **kwargs) -> Any:
        url = f"{self.base_url}{path}"
        # Convert all param values to strings for requests library
        if params:
            params = {k: str(v) for k, v in params.items()}
        try:
            response = self.session.request(method, url, params=params, json=json, timeout=TIMEOUT, **kwargs)
            response.raise_for_status()
            if response.status_code == 204 or not response.content:
                return None
            # Try to parse as JSON, but return raw text if it fails (e.g., for token strings)
            try:
                return response.json()
            except JSONDecodeError:
                return response.text
        except requests.exceptions.HTTPError as e:
            if e.response:
                try:
                    error_data = e.response.json()
                    raise Exception(f"API Error {e.response.status_code}: {error_data}")
                except JSONDecodeError:
                    raise Exception(f"API Error {e.response.status_code}: {e.response.text}")
            raise e
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    def get(self, path: str, params: Optional[Dict] = None):
        return self._request("GET", path, params=params)

    def post(self, path: str, json: Optional[Dict] = None, params: Optional[Dict] = None):
        return self._request("POST", path, json=json, params=params)

    def put(self, path: str, json: Optional[Dict] = None, params: Optional[Dict] = None):
        return self._request("PUT", path, json=json, params=params)

def save_token_to_file(token: str):
    TOKEN_FILE.write_text(token)

def clear_token_file():
    if TOKEN_FILE.exists():
        TOKEN_FILE.unlink()