from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

EXECUTION_INTERVAL_SECONDS = 1

USE_CASE_PROBABILITIES = {
    "staff_get_all_products": 2,  # UC01 - Чтение продуктов
    "staff_get_sale_details": 23,  # UC02 - Чтение продажи с JOIN
    "staff_get_supply_details": 15,  # UC03 - Чтение поставки с JOIN
    "customer_get_own_sales": 18,  # UC04 - Клиент: самообслуживание
    "customer_get_own_sale": 10,  # UC05 - Клиент: доступ к своей продаже
    "supplier_get_own_supplies": 10,  # UC06 - Поставщик: самообслуживание
    "supplier_get_own_supply": 5,  # UC07 - Поставщик: доступ к своей поставке
    "staff_create_sale": 10,  # UC08 - Запись продажи
    "staff_create_supply": 5,  # UC09 - Запись поставки
    "staff_get_all_sales": 2,  # UC10 - Чтение всех продаж с JOINs
}

API_BASE_URL = "http://localhost:5031/"
API_TIMEOUT = 10

CONNECTION_STRING = "mssql+pymssql://sa:gRdpW6eEFqNG@127.0.0.1:1433/Storage"

engine = create_engine(CONNECTION_STRING)
SessionLocal = sessionmaker(bind=engine)


def load_generated_customers() -> list[str]:
    """Получить до 50 клиентов с IsGenerated = true"""
    session = SessionLocal()
    try:
        query = text("""
            SELECT TOP 50 u.UserName
            FROM Users u
            INNER JOIN Customers c ON u.Id = c.AppUserId
            WHERE u.IsGenerated = 1
            ORDER BY NEWID()
        """)
        result = session.execute(query)
        return [row.UserName for row in result]
    finally:
        session.close()


def load_generated_suppliers() -> list[str]:
    """Получить до 50 поставщиков с IsGenerated = true"""
    session = SessionLocal()
    try:
        query = text("""
            SELECT TOP 50 u.UserName
            FROM Users u
            INNER JOIN Suppliers s ON u.Id = s.AppUserId
            WHERE u.IsGenerated = 1
            ORDER BY NEWID()
        """)
        result = session.execute(query)
        return [row.UserName for row in result]
    finally:
        session.close()


customer_usernames = load_generated_customers()
supplier_usernames = load_generated_suppliers()


STAFF_CREDENTIALS = [
    {"username": "admin", "password": "admin"},
]

CUSTOMER_CREDENTIALS: list[dict[str, str]] = list(
    map(lambda c: {"username": c, "password": "123456789"}, customer_usernames)
)

SUPPLIER_CREDENTIALS: list[dict[str, str]] = list(
    map(lambda s: {"username": s, "password": "123456789"}, supplier_usernames)
)

# Вариация цены для обновления продуктов (±20%)
PRICE_VARIATION_PERCENT = 20

# Логирование
LOG_FILE = "db_test_app.log"
LOG_LEVEL = "INFO"
