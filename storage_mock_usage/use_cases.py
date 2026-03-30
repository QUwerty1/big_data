# use_cases.py
# Сценарии нагрузочного тестирования базы данных StorageServer

import random
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any, Tuple
from api_client import APIClient
from settings import (
    STAFF_CREDENTIALS,
    CUSTOMER_CREDENTIALS,
    SUPPLIER_CREDENTIALS,
    PRICE_VARIATION_PERCENT
)

logger = logging.getLogger(__name__)


class UseCaseExecutor:
    def __init__(self):
        self.client = APIClient()

    def _get_random_credentials(self, credentials_list: List[Dict[str, str]]) -> Dict[str, str]:
        """Получить случайные учётные данные из списка"""
        return random.choice(credentials_list)

    def _calculate_new_price(self, current_price: float) -> float:
        """Рассчитать новую цену с вариацией ±20%"""
        variation = random.uniform(-PRICE_VARIATION_PERCENT, PRICE_VARIATION_PERCENT)
        new_price = current_price * (1 + variation / 100)
        return round(new_price, 2)

    def _get_random_item(self, items: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Получить случайный элемент из списка"""
        if items:
            return random.choice(items)
        return None

    def _generate_sale_unit_ids(self, product_ids: List[int], min_items: int = 1, max_items: int = 10) -> List[Dict[str, Any]]:
        """Сгенерировать единицы продажи со случайными продуктами"""
        num_items = random.randint(min_items, max_items)
        units = []
        for _ in range(num_items):
            units.append({
                "productId": random.choice(product_ids),
                "amount": random.randint(1, 100),
                "price": round(random.uniform(10, 5000), 2)
            })
        return units

    def _generate_supply_unit_ids(self, product_ids: List[int], min_items: int = 1, max_items: int = 10) -> List[Dict[str, Any]]:
        """Сгенерировать единицы поставки со случайными продуктами"""
        num_items = random.randint(min_items, max_items)
        units = []
        for _ in range(num_items):
            units.append({
                "productId": random.choice(product_ids),
                "amount": random.randint(1, 100),
                "price": round(random.uniform(10, 5000), 2)
            })
        return units

    # UC01: Staff - Получить все продукты (чтение)
    def staff_get_all_products(self) -> bool:
        """Сотрудник получает все продукты - тестирует производительность чтения таблицы Products"""
        logger.info("Выполнение UC01: Сотрудник получает все продукты")

        creds = self._get_random_credentials(STAFF_CREDENTIALS)
        if not self.client.login(creds["username"], creds["password"]):
            logger.error("UC01 Шаг 1 не удался: Вход сотрудника")
            return False

        try:
            products = self.client.get_products()
            if products:
                logger.info(f"UC01 Успех: Получено {len(products)} продуктов")
                return True
            logger.warning("UC01 Не удалось: Продукты не возвращены")
            return False
        finally:
            self.client.logout()

    # UC02: Staff - Получить продажу по ID с полными данными
    def staff_get_sale_details(self) -> bool:
        """Сотрудник получает конкретную продажу с SaleUnits - тестирует производительность JOIN"""
        logger.info("Выполнение UC02: Сотрудник получает детали продажи")

        creds = self._get_random_credentials(STAFF_CREDENTIALS)
        if not self.client.login(creds["username"], creds["password"]):
            logger.error("UC02 Шаг 1 не удался: Вход сотрудника")
            return False

        try:
            # Получить случайный ID продажи (1-5000)
            sale_id = random.randint(1, 5000)
            sale = self.client.session.get(
                f"{self.client.base_url}/sale/{sale_id}",
                headers=self.client._get_headers()
            )
            if sale.status_code == 200:
                sale_data = sale.json()
                logger.info(f"UC02 Успех: Получена продажа {sale_id} с {len(sale_data.get('saleUnits', []))} единицами")
                return True
            elif sale.status_code == 404:
                logger.info(f"UC02: Продажа {sale_id} не найдена (ожидаемо для разреженных ID)")
                return True
            logger.error(f"UC02 Не удалось: Статус {sale.status_code}")
            return False
        finally:
            self.client.logout()

    # UC03: Staff - Получить поставку по ID с полными данными
    def staff_get_supply_details(self) -> bool:
        """Сотрудник получает конкретную поставку с SupplyUnits - тестирует производительность JOIN"""
        logger.info("Выполнение UC03: Сотрудник получает детали поставки")

        creds = self._get_random_credentials(STAFF_CREDENTIALS)
        if not self.client.login(creds["username"], creds["password"]):
            logger.error("UC03 Шаг 1 не удался: Вход сотрудника")
            return False

        try:
            # Получить случайный ID поставки (1-6000)
            supply_id = random.randint(1, 6000)
            supply = self.client.session.get(
                f"{self.client.base_url}/supply/{supply_id}",
                headers=self.client._get_headers()
            )
            if supply.status_code == 200:
                supply_data = supply.json()
                logger.info(f"UC03 Успех: Получена поставка {supply_id} с {len(supply_data.get('supplyUnits', []))} единицами")
                return True
            elif supply.status_code == 404:
                logger.info(f"UC03: Поставка {supply_id} не найдена (ожидаемо для разреженных ID)")
                return True
            logger.error(f"UC03 Не удалось: Статус {supply.status_code}")
            return False
        finally:
            self.client.logout()

    # UC04: Customer - Получить свои продажи (самообслуживание с фильтром)
    def customer_get_own_sales(self) -> bool:
        """Клиент получает свои продажи через /sale/me - тестирует фильтрованное чтение"""
        logger.info("Выполнение UC04: Клиент получает свои продажи")

        creds = self._get_random_credentials(CUSTOMER_CREDENTIALS)
        if not self.client.login(creds["username"], creds["password"]):
            logger.error("UC04 Шаг 1 не удался: Вход клиента")
            return False

        try:
            sales = self.client.get_sale_me()
            logger.info(f"UC04 Успех: У клиента {len(sales)} продаж")
            return True
        finally:
            self.client.logout()

    # UC05: Customer - Получить конкретную свою продажу (тест контроля доступа)
    def customer_get_own_sale(self) -> bool:
        """Клиент получает конкретную свою продажу - тестирует контроль доступа + JOIN"""
        logger.info("Выполнение UC05: Клиент получает свою продажу")

        creds = self._get_random_credentials(CUSTOMER_CREDENTIALS)
        if not self.client.login(creds["username"], creds["password"]):
            logger.error("UC05 Шаг 1 не удался: Вход клиента")
            return False

        try:
            # Сначала получить продажи клиента
            sales = self.client.get_sale_me()
            if not sales:
                logger.info("UC05: У клиента нет продаж, пропускаем")
                return True

            # Выбрать случайную продажу из продаж клиента
            sale = self._get_random_item(sales)
            if sale and "id" in sale:
                sale_id = sale["id"]
                # Теперь получить эту конкретную продажу
                sale_response = self.client.session.get(
                    f"{self.client.base_url}/sale/{sale_id}",
                    headers=self.client._get_headers()
                )
                if sale_response.status_code == 200:
                    logger.info(f"UC05 Успех: Клиент получил свою продажу {sale_id}")
                    return True
                logger.error(f"UC05 Не удалось: Не удалось получить продажу {sale_id}")
                return False

            logger.info("UC05: Не найдено валидной продажи")
            return True
        finally:
            self.client.logout()

    # UC06: Supplier - Получить свои поставки через /supplier/me
    def supplier_get_own_supplies(self) -> bool:
        """Поставщик получает свой профиль - тестирует эндпоинт самообслуживания"""
        logger.info("Выполнение UC06: Поставщик получает свои поставки")

        creds = self._get_random_credentials(SUPPLIER_CREDENTIALS)
        if not self.client.login(creds["username"], creds["password"]):
            logger.error("UC06 Шаг 1 не удался: Вход поставщика")
            return False

        try:
            profile = self.client.get_supplier_me()
            if profile:
                logger.info(f"UC06 Успех: Поставщик {profile.get('companyName', 'Н/Д')} получил профиль")
                return True
            logger.warning("UC06 Не удалось: Не удалось получить профиль поставщика")
            return False
        finally:
            self.client.logout()

    # UC07: Supplier - Получить конкретную свою поставку
    def supplier_get_own_supply(self) -> bool:
        """Поставщик получает конкретную свою поставку - тестирует контроль доступа"""
        logger.info("Выполнение UC07: Поставщик получает свою поставку")

        creds = self._get_random_credentials(SUPPLIER_CREDENTIALS)
        if not self.client.login(creds["username"], creds["password"]):
            logger.error("UC07 Шаг 1 не удался: Вход поставщика")
            return False

        try:
            # Получить все поставки (только для staff, но поставщик может получить свою по ID)
            # Пробуем случайный ID поставки в диапазоне 1-6000
            supply_id = random.randint(1, 6000)
            supply_response = self.client.session.get(
                f"{self.client.base_url}/supply/{supply_id}",
                headers=self.client._get_headers()
            )
            # Успех (если владеет) или 404 (если не владеет) - оба валидны
            if supply_response.status_code in [200, 404]:
                logger.info(f"UC07: Доступ к поставке {supply_id} вернул {supply_response.status_code}")
                return True
            logger.error(f"UC07 Не удалось: Статус {supply_response.status_code}")
            return False
        finally:
            self.client.logout()

    # UC08: Staff - Создать новую продажу (запись с отношениями)
    def staff_create_sale(self) -> bool:
        """Сотрудник создаёт новую продажу с несколькими единицами - тестирует производительность записи"""
        logger.info("Выполнение UC08: Сотрудник создаёт продажу")

        creds = self._get_random_credentials(STAFF_CREDENTIALS)
        if not self.client.login(creds["username"], creds["password"]):
            logger.error("UC08 Шаг 1 не удался: Вход сотрудника")
            return False

        try:
            # Получить продукты для единиц продажи
            products = self.client.get_products()
            if not products:
                logger.warning("UC08: Нет продуктов для единиц продажи")
                return False

            product_ids = [p["id"] for p in products if "id" in p]
            if not product_ids:
                logger.warning("UC08: Не найдено валидных ID продуктов")
                return False

            # Получить клиентов для customerId (эндпоинт только для staff)
            customers_response = self.client.session.get(
                f"{self.client.base_url}/customer",
                params={"skip": 0, "take": 50},
                headers=self.client._get_headers()
            )
            if customers_response.status_code != 200:
                logger.error(f"UC08: Не удалось получить клиентов, статус: {customers_response.status_code}")
                return False

            customers = customers_response.json()
            if not customers:
                logger.warning("UC08: Нет доступных клиентов")
                return False

            customer_id = random.choice(customers)["id"]

            # Сгенерировать продажу с единицами
            sale_data = {
                "customerId": customer_id,
                "plannedDate": (datetime.now() + timedelta(days=7)).isoformat(),
                "realDate": datetime.now().isoformat(),
                "saleUnits": self._generate_sale_unit_ids(product_ids)
            }

            create_response = self.client.session.post(
                f"{self.client.base_url}/sale",
                json=sale_data,
                headers=self.client._get_headers()
            )
            if create_response.status_code in [200, 201]:
                logger.info(f"UC08 Успех: Создана продажа с {len(sale_data['saleUnits'])} единицами")
                return True
            logger.error(f"UC08 Не удалось: Создание продажи вернуло {create_response.status_code}: {create_response.text[:200]}")
            return False
        finally:
            self.client.logout()

    # UC09: Staff - Создать новую поставку (запись с отношениями)
    def staff_create_supply(self) -> bool:
        """Сотрудник создаёт новую поставку с несколькими единицами - тестирует производительность записи"""
        logger.info("Выполнение UC09: Сотрудник создаёт поставку")

        creds = self._get_random_credentials(STAFF_CREDENTIALS)
        if not self.client.login(creds["username"], creds["password"]):
            logger.error("UC09 Шаг 1 не удался: Вход сотрудника")
            return False

        try:
            # Получить продукты для единиц поставки
            products = self.client.get_products()
            if not products:
                logger.warning("UC09: Нет продуктов для единиц поставки")
                return False

            product_ids = [p["id"] for p in products if "id" in p]
            if not product_ids:
                logger.warning("UC09: Не найдено валидных ID продуктов")
                return False

            # Получить поставщиков для supplierId (эндпоинт только для staff)
            suppliers_response = self.client.session.get(
                f"{self.client.base_url}/supplier",
                params={"skip": 0, "take": 50},
                headers=self.client._get_headers()
            )
            if suppliers_response.status_code != 200:
                logger.error(f"UC09: Не удалось получить поставщиков, статус: {suppliers_response.status_code}")
                return False

            suppliers = suppliers_response.json()
            if not suppliers:
                logger.warning("UC09: Нет доступных поставщиков")
                return False

            supplier_id = random.choice(suppliers)["id"]

            # Сгенерировать поставку с единицами
            supply_data = {
                "supplierId": supplier_id,
                "plannedDate": (datetime.now() + timedelta(days=14)).isoformat(),
                "realDate": datetime.now().isoformat(),
                "supplyUnits": self._generate_supply_unit_ids(product_ids)
            }

            create_response = self.client.session.post(
                f"{self.client.base_url}/supply",
                json=supply_data,
                headers=self.client._get_headers()
            )
            if create_response.status_code in [200, 201]:
                logger.info(f"UC09 Успех: Создана поставка с {len(supply_data['supplyUnits'])} единицами")
                return True
            logger.error(f"UC09 Не удалось: Создание поставки вернуло {create_response.status_code}: {create_response.text[:200]}")
            return False
        finally:
            self.client.logout()

    # UC10: Staff - Получить все продажи (чтение с JOIN)
    def staff_get_all_sales(self) -> bool:
        """Сотрудник получает все продажи - тестирует производительность чтения с JOIN на SaleUnits"""
        logger.info("Выполнение UC10: Сотрудник получает все продажи")

        creds = self._get_random_credentials(STAFF_CREDENTIALS)
        if not self.client.login(creds["username"], creds["password"]):
            logger.error("UC10 Шаг 1 не удался: Вход сотрудника")
            return False

        try:
            sales = self.client.get_sales()
            if sales:
                total_units = sum(len(s.get('saleUnitIds', [])) for s in sales)
                logger.info(f"UC10 Успех: Получено {len(sales)} продаж с {total_units} всего ID единиц")
                return True
            logger.warning("UC10: Продажи не возвращены")
            return True  # Пустой результат тоже валиден
        finally:
            self.client.logout()
