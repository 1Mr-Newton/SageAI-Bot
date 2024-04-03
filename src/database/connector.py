from supabase.client import Client, ClientOptions, create_client
from src.config.config import config


supabaseClient: Client = create_client(
    config.SUPABASE_URL,
    config.SUPABASE_KEY,
    options=ClientOptions(auto_refresh_token=True),
)
