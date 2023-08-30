MONGO_DB_URI = (
    "mongodb+srv://techz:bots@cluster0.uzrha.mongodb.net/?retryWrites=true&w=majority"
)
import pymongo

mongo_client = pymongo.MongoClient(MONGO_DB_URI)
db = mongo_client.techzapi
userdb = db.userdb


class DB:
    def get_user(self):
        return userdb.find_one({"api_key": self})

    def is_user(self):
        return bool(userdb.find_one({"api_key": self}))

    def reduce_credits(self, amount):
        user = DB.get_user(self)
        if user["credits"] < amount:
            raise Exception("Not enough credits")
        userdb.update_one(
            {"api_key": self}, {"$inc": {"credits": -amount, "used": amount}}
        )
