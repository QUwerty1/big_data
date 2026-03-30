EXECUTION_INTERVAL_SECONDS = 3

USE_CASE_PROBABILITIES = {
    "staff_product_update": 15,  # UC01
    "customer_self_service": 45,  # UC02
    "supplier_self_service": 40,  # UC03
}

API_BASE_URL = "http://localhost:5031/"
API_TIMEOUT = 10

supplier_usernames = [
    "Trent.Bayer",
    "Sid.Swift51",
    "Emmanuelle_Greenholt48",
    "Princess64",
    "Tyra_Rolfson",
    "Lacy.Cormier20",
    "Lonzo.Terry",
    "Alexie_Pfeffer0",
    "Annamarie8",
    "Joanie.Brakus",
    "Dana_Hand",
    "Tyra.Hoppe45",
    "Arnoldo.Robel",
    "Theresia_Senger42",
    "Hilton.Kuhic",
    "Brandy_Kiehn",
    "Elenora.Kiehn",
    "Arlie42",
    "Christ_Stracke",
    "Merl_Ratke",
    "Dorthy.Upton61",
    "Esteban14",
    "Toby94",
    "Herminio.Wolff",
    "Gay.Vandervort",
    "Nathanael_Roob",
    "Mariah_Spencer",
    "Meda.Ankunding",
    "Colin_Kirlin",
    "Maybell_Trantow",
    "Shane_Mante25",
    "Desiree.Jerde68",
    "Sophie_Grant",
    "Laverna_Rippin",
    "Marlin_Streich58",
    "Christy88",
    "Marietta61",
    "Allan.Crist",
    "Cicero_Bins81",
    "Eric_Emmerich",
]

customer_usernames = [
    "Ellsworth.Nolan7",
    "Markus_Renner",
    "Austin.Ernser77",
    "Carissa.Nader",
    "Jarvis_Toy",
    "Ryley79",
    "Suzanne.Kerluke",
    "Gerhard_Rowe",
    "Alan37",
    "Jamey_Sanford30",
    "Kaya_OKeefe",
    "Rafaela39",
    "Thora_Ankunding82",
    "Reyes.Ratke99",
    "Chaz.McClure",
    "Mackenzie_Ruecker94",
    "Monica14",
    "Ozella8",
    "Edgar39",
    "Rowan.Konopelski46",
    "Eliseo_Smitham",
    "Hilbert20",
    "Kiara.Brown75",
    "Tre_Daniel",
    "Jaquelin34",
    "Valentin22",
    "Aida.Smitham64",
    "Armando.Farrell",
    "Jamey_Prosacco93",
    "Lorenzo_Boyer8",
    "Lamar_Carroll",
    "Conrad41",
    "Zechariah_Bins",
    "Mohamed.MacGyver34",
    "Jamaal_Russel",
    "Kris18",
    "Odie.Turcotte6",
    "Arielle.Parker26",
    "Elisabeth35",
    "Kurt.Hermann20",
]


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
