import os

PORT = int(os.getenv("PORT", "29508"))
JWT_SECRET = os.getenv("JWT_SECRET", "change_me")
