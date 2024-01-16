import pymongo


uri = "mongodb://localhost:27017"
client = pymongo.MongoClient(uri)

db = client["news_aggregator"]
