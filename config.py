import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

# === UZUPEŁNIJ TE ID PÓŹNIEJ ===
WELCOME_CHANNEL_ID = 0      # ID kanału #powitania
GOODBYE_CHANNEL_ID = 0      # ID kanału #pożegnalnia
LOG_CHANNEL_ID = 0          # ID kanału logów (opcjonalnie)
