from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    BOT_TOKEN: str
    ADMIN_CHANNEL_ID: int

settings = Settings(
    BOT_TOKEN=os.getenv("BOT_TOKEN"),
    ADMIN_CHANNEL_ID=int(os.getenv("ADMIN_CHANNEL_ID"))
)