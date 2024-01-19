from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticClient
# internally relative imports
from .settings import GET_SETTINGS

setting = GET_SETTINGS()

# database server configuration
client: AgnosticClient = AsyncIOMotorClient("{0}://{1}:{2}".format(setting["DATABASE_DRIVER_NAME"],setting["DATABASE_HOST"], setting["DATABASE_PORT"]))
# grab database name
db = client["Fast_data"]

