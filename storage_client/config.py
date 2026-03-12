from pathlib import Path

BASE_URL = "http://localhost:5031/"
TIMEOUT = 10
TOKEN_FILE = Path("/home/mrquw/.cli_token")

def format_price(value: float) -> str:
    """Format number as Russian Rubles: 1 234 567,89 ₽"""
    if value is None:
        return "0,00 ₽"

    str_val = f"{value:.2f}"
    integer_part, decimal_part = str_val.split(".")
    integer_part = integer_part[::-1]
    integer_part = " ".join(integer_part[i:i+3] for i in range(0, len(integer_part), 3))
    integer_part = integer_part[::-1]
    return f"{integer_part},{decimal_part} ₽"