from dotenv import load_dotenv
import os


def load_environment_variables():
    load_dotenv()
    required_vars = ["API_ID", "API_HASH", "BOT_TOKEN", "SUPABASE_URL", "SUPABASE_KEY"]
    env_vars = {}

    for var in required_vars:
        value = os.getenv(var)
        assert value, f"Missing environment variable: {var}"
        env_vars[var] = value
    return env_vars


class Config:
    def __init__(
        self,
        API_ID: str,
        API_HASH: str,
        BOT_TOKEN: str,
        SUPABASE_URL: str,
        SUPABASE_KEY: str,
    ):
        self.API_ID = int(API_ID)
        self.API_HASH = API_HASH
        self.BOT_TOKEN = BOT_TOKEN
        self.SUPABASE_URL = SUPABASE_URL
        self.SUPABASE_KEY = SUPABASE_KEY


env_vars = load_environment_variables()
config = Config(**env_vars)
