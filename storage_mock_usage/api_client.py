# api_client.py
# API Client for StorageServer

import requests
import logging
from typing import Optional, Dict, Any, List
from settings import API_BASE_URL, API_TIMEOUT

logger = logging.getLogger(__name__)


class APIClient:
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.token: Optional[str] = None
    
    def _get_headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers
    
    def login(self, username: str, password: str) -> bool:
        """Authenticate and store JWT token"""
        try:
            response = self.session.post(
                f"{self.base_url}/user/login",
                json={"userName": username, "password": password},
                headers={"Content-Type": "application/json"},
                timeout=API_TIMEOUT
            )
            if response.status_code == 200:
                self.token = response.text.strip('"')
                logger.info(f"Login successful for user: {username}")
                return True
            else:
                logger.error(f"Login failed: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Login error: {e}")
            return False
    
    def logout(self):
        """Clear token"""
        self.token = None
    
    # Customer endpoints
    def get_customer_me(self) -> Optional[Dict[str, Any]]:
        try:
            response = self.session.get(
                f"{self.base_url}/customer/me",
                headers=self._get_headers(),
                timeout=API_TIMEOUT
            )
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            logger.error(f"Get customer me error: {e}")
            return None
    
    def get_customers(self, skip: int = 0, take: int = 10) -> List[Dict[str, Any]]:
        try:
            response = self.session.get(
                f"{self.base_url}/customer",
                params={"skip": skip, "take": take},
                headers=self._get_headers(),
                timeout=API_TIMEOUT
            )
            if response.status_code == 200:
                data = response.json()
                return data if isinstance(data, list) else [data]
            return []
        except Exception as e:
            logger.error(f"Get customers error: {e}")
            return []
    
    # Supplier endpoints
    def get_supplier_me(self) -> Optional[Dict[str, Any]]:
        try:
            response = self.session.get(
                f"{self.base_url}/supplier/me",
                headers=self._get_headers(),
                timeout=API_TIMEOUT
            )
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            logger.error(f"Get supplier me error: {e}")
            return None
    
    def get_suppliers(self, skip: int = 0, take: int = 10) -> List[Dict[str, Any]]:
        try:
            response = self.session.get(
                f"{self.base_url}/supplier",
                params={"skip": skip, "take": take},
                headers=self._get_headers(),
                timeout=API_TIMEOUT
            )
            if response.status_code == 200:
                data = response.json()
                return data if isinstance(data, list) else [data]
            return []
        except Exception as e:
            logger.error(f"Get suppliers error: {e}")
            return []
    
    # Product endpoints
    def get_products(self) -> List[Dict[str, Any]]:
        try:
            response = self.session.get(
                f"{self.base_url}/product",
                headers=self._get_headers(),
                timeout=API_TIMEOUT
            )
            if response.status_code == 200:
                data = response.json()
                return data if isinstance(data, list) else [data]
            return []
        except Exception as e:
            logger.error(f"Get products error: {e}")
            return []
    
    def get_product(self, product_id: int) -> Optional[Dict[str, Any]]:
        try:
            response = self.session.get(
                f"{self.base_url}/product/{product_id}",
                headers=self._get_headers(),
                timeout=API_TIMEOUT
            )
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            logger.error(f"Get product error: {e}")
            return None
    
    def update_product(self, product_data: Dict[str, Any]) -> bool:
        try:
            response = self.session.put(
                f"{self.base_url}/product",
                json=product_data,
                headers=self._get_headers(),
                timeout=API_TIMEOUT
            )
            if response.status_code in [200, 201]:
                return True
            logger.error(f"Update product failed: {response.status_code}")
            return False
        except Exception as e:
            logger.error(f"Update product error: {e}")
            return False
    
    # Sale endpoints
    def get_sales(self) -> List[Dict[str, Any]]:
        try:
            response = self.session.get(
                f"{self.base_url}/sale",
                headers=self._get_headers(),
                timeout=API_TIMEOUT
            )
            if response.status_code == 200:
                data = response.json()
                return data if isinstance(data, list) else [data]
            return []
        except Exception as e:
            logger.error(f"Get sales error: {e}")
            return []
    
    def get_sale_me(self) -> List[Dict[str, Any]]:
        try:
            response = self.session.get(
                f"{self.base_url}/sale/me",
                headers=self._get_headers(),
                timeout=API_TIMEOUT
            )
            if response.status_code == 200:
                data = response.json()
                return data if isinstance(data, list) else [data]
            return []
        except Exception as e:
            logger.error(f"Get sale me error: {e}")
            return []
    
    def create_sale(self, sale_data: Dict[str, Any]) -> bool:
        try:
            response = self.session.post(
                f"{self.base_url}/sale",
                json=sale_data,
                headers=self._get_headers(),
                timeout=API_TIMEOUT
            )
            if response.status_code in [200, 201]:
                return True
            logger.error(f"Create sale failed: {response.status_code}")
            return False
        except Exception as e:
            logger.error(f"Create sale error: {e}")
            return False
    
    # Supply endpoints
    def get_supplies(self) -> List[Dict[str, Any]]:
        try:
            response = self.session.get(
                f"{self.base_url}/supply",
                headers=self._get_headers(),
                timeout=API_TIMEOUT
            )
            if response.status_code == 200:
                data = response.json()
                return data if isinstance(data, list) else [data]
            return []
        except Exception as e:
            logger.error(f"Get supplies error: {e}")
            return []
    
    def create_supply(self, supply_data: Dict[str, Any]) -> bool:
        try:
            response = self.session.post(
                f"{self.base_url}/supply",
                json=supply_data,
                headers=self._get_headers(),
                timeout=API_TIMEOUT
            )
            if response.status_code in [200, 201]:
                return True
            logger.error(f"Create supply failed: {response.status_code}")
            return False
        except Exception as e:
            logger.error(f"Create supply error: {e}")
            return False
    
    # User endpoints
    def get_user_me(self) -> Optional[Dict[str, Any]]:
        try:
            response = self.session.get(
                f"{self.base_url}/user/me",
                headers=self._get_headers(),
                timeout=API_TIMEOUT
            )
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            logger.error(f"Get user me error: {e}")
            return None