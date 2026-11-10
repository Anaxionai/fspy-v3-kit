"""TiffinTrack's settings, read from environment variables.

Each setting has a default that works on your laptop, so the API starts without a .env file.
`.env.example` lists every setting with a short note.
"""

import os

# Redis from the cloud lab's core profile (task 8).
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

# MongoDB from the cloud lab's mongo profile, with no password (task 15).
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
MONGO_DB = os.environ.get("MONGO_DB", "tiffintrack")

# The speed for an arrival estimate when a rider's own speed is unknown or too low (task 20).
CITY_SPEED_KMH = float(os.environ.get("CITY_SPEED_KMH", "18"))
