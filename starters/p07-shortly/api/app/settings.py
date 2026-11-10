"""Shortly's settings, read from environment variables.

pydantic-settings fills each field from the variable with the same name in
capitals: the field `database_url` comes from DATABASE_URL.

Nothing imports this file yet. In task 10 you write the class, then use
`settings.<name>` everywhere a value is hard-coded today (app/db.py,
alembic/env.py and the short_url of POST /links).
"""

# TODO(task 10): write `class Settings(BaseSettings)` (BaseSettings comes from pydantic_settings)
#   with these four fields, each with a type and a default for your laptop:
#     database_url, redis_url, public_base_url, log_level
#   Below the class, create the one shared instance: settings = Settings()
#
# TODO(task 17): add cache_enabled (default True), cache_ttl_seconds (default 3600)
#   and admin_token (default "", which means PATCH is switched off).
#
# TODO(task 18): add rate_limit_burst (default 5) and rate_limit_per_minute (default 10).
#
# TODO(task 21): add cors_origins: the web origins that CORS allows, such as http://localhost:5173.
