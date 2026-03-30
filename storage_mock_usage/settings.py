from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

EXECUTION_INTERVAL_SECONDS = 3

USE_CASE_PROBABILITIES = {
    "staff_product_update": 15,  # UC01
    "customer_self_service": 45,  # UC02
    "supplier_self_service": 40,  # UC03
}

API_BASE_URL = "http://localhost:5031/"
API_TIMEOUT = 10

CONNECTION_STRING = "mssql+pymssql://sa:gRdpW6eEFqNG@127.0.0.1:1433/Storage"

engine = create_engine(CONNECTION_STRING)
SessionLocal = sessionmaker(bind=engine)


def load_generated_customers() -> list[str]:
    """Get up to 50 customers with IsGenerated = true"""
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
    """Get up to 50 suppliers with IsGenerated = true"""
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

# Price variation for product updates (±20%)
PRICE_VARIATION_PERCENT = 20

# Logging
LOG_FILE = "db_test_app.log"
LOG_LEVEL = "INFO"
