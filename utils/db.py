from motor.motor_asyncio import AsyncIOMotorClient as MongoClient

MONGO_DB_URI = (
    "mongodb+srv://techz:bots@cluster0.uzrha.mongodb.net/?retryWrites=true&w=majority"
)

mongo_client = MongoClient(MONGO_DB_URI)
db = mongo_client.techzapi
userdb = db.userdb


class DB:
    async def get_user(self):
        return await userdb.find_one({"api_key": self})

    async def is_user(self):
        return bool(await userdb.find_one({"api_key": self}))

    async def reduce_credits(self, amount):
        user = await DB.get_user(self)
        if user["credits"] < amount:
            raise Exception("Not enough credits")
        await userdb.update_one(
            {"api_key": self}, {"$inc": {"credits": -amount, "used": amount}}
        )
