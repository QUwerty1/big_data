import pyodbc
from pymongo import MongoClient
from bson import ObjectId, Decimal128
from datetime import timezone
import collections

sql_conn = pyodbc.connect(
    'DRIVER={ODBC Driver 18 for SQL Server};'
    'SERVER=127.0.0.1,1433;'
    'DATABASE=Storage;'
    'UID=sa;'
    'PWD=gRdpW6eEFqNG;'
    'TrustServerCertificate=Yes'
)
mongo_client = MongoClient("mongodb://sa:gRdpW6eEFqNG@localhost:27017/")
db = mongo_client["storage"]

product_map = {}
user_map = {}
customer_map = {}
supplier_map = {}

cursor = sql_conn.cursor()

cursor.execute("SELECT Id, ProductName, Price FROM Products")
batch = []
for row in cursor:
    new_id = ObjectId()
    product_map[row.Id] = new_id
    batch.append({
        "_id": new_id,
        "productName": row.ProductName,
        "price": Decimal128(str(row.Price))
    })
    if len(batch) >= 1000:
        db.products.insert_many(batch)
        batch.clear()
if batch:
    db.products.insert_many(batch)

cursor.execute("""
    SELECT 
        Id, UserName, NormalizedUserName, Email, NormalizedEmail,
        EmailConfirmed, PasswordHash, SecurityStamp, ConcurrencyStamp,
        PhoneNumber, PhoneNumberConfirmed, TwoFactorEnabled,
        CAST(LockoutEnd AS datetime2) AS LockoutEnd,
        LockoutEnabled, AccessFailedCount,
        IsStaff, IsGenerated
    FROM Users
""")
batch = []
for row in cursor:
    user_map[row.Id] = row.Id
    lockout_end = None
    if row.LockoutEnd:
        lockout_end = row.LockoutEnd.replace(tzinfo=timezone.utc)
    batch.append({
        "_id": row.Id,
        "userName": row.UserName,
        "normalizedUserName": row.NormalizedUserName,
        "email": row.Email,
        "normalizedEmail": row.NormalizedEmail,
        "emailConfirmed": bool(row.EmailConfirmed),
        "passwordHash": row.PasswordHash,
        "securityStamp": row.SecurityStamp,
        "concurrencyStamp": row.ConcurrencyStamp,
        "phoneNumber": row.PhoneNumber,
        "phoneNumberConfirmed": bool(row.PhoneNumberConfirmed),
        "twoFactorEnabled": bool(row.TwoFactorEnabled),
        "lockoutEnd": lockout_end,
        "lockoutEnabled": bool(row.LockoutEnabled),
        "accessFailedCount": int(row.AccessFailedCount),
        "isStaff": bool(row.IsStaff),
        "isGenerated": bool(row.IsGenerated)
    })
    if len(batch) >= 1000:
        db.users.insert_many(batch)
        batch.clear()
if batch:
    db.users.insert_many(batch)

cursor.execute("SELECT Id, CompanyName, Phone, Address, Email, AppUserId FROM Customers")
batch = []
for row in cursor:
    new_id = ObjectId()
    customer_map[row.Id] = new_id
    batch.append({
        "_id": new_id,
        "appUserId": user_map[row.AppUserId],
        "companyName": row.CompanyName,
        "phone": row.Phone,
        "address": row.Address,
        "email": row.Email
    })
    if len(batch) >= 1000:
        db.customers.insert_many(batch)
        batch.clear()
if batch:
    db.customers.insert_many(batch)

cursor.execute("SELECT Id, CompanyName, Phone, Address, Email, AppUserId FROM Suppliers")
batch = []
for row in cursor:
    new_id = ObjectId()
    supplier_map[row.Id] = new_id
    batch.append({
        "_id": new_id,
        "appUserId": user_map[row.AppUserId],
        "companyName": row.CompanyName,
        "phone": row.Phone,
        "address": row.Address,
        "email": row.Email
    })
    if len(batch) >= 1000:
        db.suppliers.insert_many(batch)
        batch.clear()
if batch:
    db.suppliers.insert_many(batch)

cursor.execute("""
    SELECT 
        Id, CustomerId, 
        CAST(RealDate AS datetime2) AS RealDate,
        CAST(PlannedDate AS datetime2) AS PlannedDate
    FROM Sales
""")
sales_data = {}
for r in cursor:
    real_date = r.RealDate.replace(tzinfo=timezone.utc) if r.RealDate else None
    planned_date = r.PlannedDate.replace(tzinfo=timezone.utc) if r.PlannedDate else None
    sales_data[r.Id] = {
        "_id": ObjectId(),
        "customerId": customer_map[r.CustomerId],
        "realDate": real_date,
        "plannedDate": planned_date,
        "saleUnits": []
    }

cursor.execute("SELECT SalesId, SaleUnitsId FROM SaleSaleUnit")
junction_map = collections.defaultdict(list)
for r in cursor:
    junction_map[r.SalesId].append(r.SaleUnitsId)

cursor.execute("SELECT Id, ProductId, Amount, Price FROM SaleUnits")
units_data = {r.Id: r for r in cursor}

batch = []
for sql_sale_id, sale_doc in sales_data.items():
    for unit_sql_id in junction_map.get(sql_sale_id, []):
        u = units_data[unit_sql_id]
        sale_doc["saleUnits"].append({
            "productId": product_map[u.ProductId],
            "amount": int(u.Amount),
            "price": Decimal128(str(u.Price))
        })
    batch.append(sale_doc)
    if len(batch) >= 500:
        db.sales.insert_many(batch)
        batch.clear()
if batch:
    db.sales.insert_many(batch)

cursor.execute("""
    SELECT 
        Id, SupplierId, 
        CAST(RealDate AS datetime2) AS RealDate,
        CAST(PlannedDate AS datetime2) AS PlannedDate
    FROM Supplies
""")
supplies_data = {}
for r in cursor:
    real_date = r.RealDate.replace(tzinfo=timezone.utc) if r.RealDate else None
    planned_date = r.PlannedDate.replace(tzinfo=timezone.utc) if r.PlannedDate else None
    supplies_data[r.Id] = {
        "_id": ObjectId(),
        "supplierId": supplier_map[r.SupplierId],
        "realDate": real_date,
        "plannedDate": planned_date,
        "supplyUnits": []
    }

cursor.execute("SELECT SuppliesId, SupplyUnitsId FROM SupplySupplyUnit")
junction_map = collections.defaultdict(list)
for r in cursor:
    junction_map[r.SuppliesId].append(r.SupplyUnitsId)

cursor.execute("SELECT Id, ProductId, Amount, Price FROM SupplyUnits")
units_data = {r.Id: r for r in cursor}

batch = []
for sql_supply_id, supply_doc in supplies_data.items():
    for unit_sql_id in junction_map.get(sql_supply_id, []):
        u = units_data[unit_sql_id]
        supply_doc["supplyUnits"].append({
            "productId": product_map[u.ProductId],
            "amount": int(u.Amount),
            "price": Decimal128(str(u.Price))
        })
    batch.append(supply_doc)
    if len(batch) >= 500:
        db.supplies.insert_many(batch)
        batch.clear()
if batch:
    db.supplies.insert_many(batch)

sql_conn.close()
mongo_client.close()