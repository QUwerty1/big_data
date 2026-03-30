# api_client.py
# API клиент для StorageServer

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
        """Получить заголовки для запроса"""
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def login(self, username: str, password: str) -> bool:
        """Аутентификация и сохранение JWT токена"""
        try:
            response = self.session.post(
                f"{self.base_url}/user/login",
                json={"userName": username, "password": password},
                headers={"Content-Type": "application/json"},
                timeout=API_TIMEOUT
            )
            if response.status_code == 200:
                self.token = response.text.strip('"')
                logger.info(f"Вход успешен для пользователя: {username}")
                return True
            else:
                logger.error(f"Вход не удался: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Ошибка входа: {e}")
            return False

    def logout(self):
        """Очистить токен"""
        self.token = None

    # Эндпоинты клиентов
    def get_customer_me(self) -> Optional[Dict[str, Any]]:
        """Получить данные текущего клиента"""
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
            logger.error(f"Ошибка получения данных клиента: {e}")
            return None

    def get_customers(self, skip: int = 0, take: int = 10) -> List[Dict[str, Any]]:
        """Получить список клиентов с пагинацией"""
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
            logger.error(f"Ошибка получения клиентов: {e}")
            return []

    # Эндпоинты поставщиков
    def get_supplier_me(self) -> Optional[Dict[str, Any]]:
        """Получить данные текущего поставщика"""
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
            logger.error(f"Ошибка получения данных поставщика: {e}")
            return None

    def get_suppliers(self, skip: int = 0, take: int = 10) -> List[Dict[str, Any]]:
        """Получить список поставщиков с пагинацией"""
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
            logger.error(f"Ошибка получения поставщиков: {e}")
            return []

    # Эндпоинты продуктов
    def get_products(self) -> List[Dict[str, Any]]:
        """Получить все продукты"""
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
            logger.error(f"Ошибка получения продуктов: {e}")
            return []

    def get_product(self, product_id: int) -> Optional[Dict[str, Any]]:
        """Получить продукт по ID"""
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
            logger.error(f"Ошибка получения продукта: {e}")
            return None

    def update_product(self, product_data: Dict[str, Any]) -> bool:
        """Обновить продукт"""
        try:
            response = self.session.put(
                f"{self.base_url}/product",
                json=product_data,
                headers=self._get_headers(),
                timeout=API_TIMEOUT
            )
            if response.status_code in [200, 201]:
                return True
            logger.error(f"Обновление продукта не удалось: {response.status_code}")
            return False
        except Exception as e:
            logger.error(f"Ошибка обновления продукта: {e}")
            return False

    # Эндпоинты продаж
    def get_sales(self) -> List[Dict[str, Any]]:
        """Получить все продажи"""
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
            logger.error(f"Ошибка получения продаж: {e}")
            return []

    def get_sale_me(self) -> List[Dict[str, Any]]:
        """Получить свои продажи"""
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
            logger.error(f"Ошибка получения своих продаж: {e}")
            return []

    def create_sale(self, sale_data: Dict[str, Any]) -> bool:
        """Создать продажу"""
        try:
            response = self.session.post(
                f"{self.base_url}/sale",
                json=sale_data,
                headers=self._get_headers(),
                timeout=API_TIMEOUT
            )
            if response.status_code in [200, 201]:
                return True
            logger.error(f"Создание продажи не удалось: {response.status_code}")
            return False
        except Exception as e:
            logger.error(f"Ошибка создания продажи: {e}")
            return False

    # Эндпоинты поставок
    def get_supplies(self) -> List[Dict[str, Any]]:
        """Получить все поставки"""
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
            logger.error(f"Ошибка получения поставок: {e}")
            return []

    def create_supply(self, supply_data: Dict[str, Any]) -> bool:
        """Создать поставку"""
        try:
            response = self.session.post(
                f"{self.base_url}/supply",
                json=supply_data,
                headers=self._get_headers(),
                timeout=API_TIMEOUT
            )
            if response.status_code in [200, 201]:
                return True
            logger.error(f"Создание поставки не удалось: {response.status_code}")
            return False
        except Exception as e:
            logger.error(f"Ошибка создания поставки: {e}")
            return False

    # Эндпоинты пользователей
    def get_user_me(self) -> Optional[Dict[str, Any]]:
        """Получить данные текущего пользователя"""
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
            logger.error(f"Ошибка получения данных пользователя: {e}")
            return None
