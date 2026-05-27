from pymongo import MongoClient


mongo_client = MongoClient("mongodb://sa:gRdpW6eEFqNG@localhost:27017/")
db = mongo_client["storage"]

result = db.sales.aggregate([
    { "$unwind": "$saleUnits" },
    {
        "$group": {
            "_id": None,
            "totalRevenue": {
                "$sum": { "$multiply": ["$saleUnits.amount", "$saleUnits.price"] }
            }
        }
    },
    { "$project": { "_id": 0, "totalRevenue": 1 } }
])
print(list(result)[0]["totalRevenue"])  # Decimal128('12345.67')