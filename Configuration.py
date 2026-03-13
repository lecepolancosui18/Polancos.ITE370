import os
from dotenv import load_dotenv  # For loading .env files (install via `pip install python-dotenv`)
from typing import Dict, Optional

# ------------------------------
# 1. Load Environment Variables
# ------------------------------
def load_environment() -> None:
    """Load variables from .env file (prioritize system env vars if set)"""
    # Load .env file (only if it exists; system env vars take precedence)
    load_dotenv(override=False)  # Set override=True to prioritize .env over system vars

# ------------------------------
# 2. Validate & Fetch Configs
# ------------------------------
def get_app_config() -> Dict[str, Optional[str]]:
    """Fetch and validate application configuration"""
    required_vars = ["APP_ENV", "DB_HOST", "DB_PORT", "API_KEY"]
    config = {}

    # Check for required variables
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            raise ValueError(f"Missing required environment variable: {var}")
        config[var] = value

    # Set environment-specific defaults
    app_env = config["APP_ENV"].lower()
    if app_env == "development":
        config["DEBUG_MODE"] = os.getenv("DEBUG_MODE", "True")  # Default to True for dev
        config["LOG_LEVEL"] = os.getenv("LOG_LEVEL", "DEBUG")
    elif app_env == "production":
        config["DEBUG_MODE"] = os.getenv("DEBUG_MODE", "False")  # Default to False for prod
        config["LOG_LEVEL"] = os.getenv("LOG_LEVEL", "INFO")
    else:
        raise ValueError(f"Invalid APP_ENV: {app_env} (must be 'development' or 'production')")

    return config

# ------------------------------
# 3. Use Config in Application
# ------------------------------
def run_application(config: Dict[str, Optional[str]]) -> None:
    """Initialize and run the app with loaded config"""
    print("=== Application Configuration ===")
    for key, value in config.items():
        # Mask sensitive values (e.g., API keys)
        display_value = value if key not in ["API_KEY", "DB_PASSWORD"] else "***MASKED***"
        print(f"{key}: {display_value}")

    print("\n=== Starting Application ===")
    if config["DEBUG_MODE"].lower() == "true":
        print("Running in DEBUG mode (only for development!)")
    else:
        print("Running in PRODUCTION mode")

# Example usage
if __name__ == "__main__":
    try:
        load_environment()
        app_config = get_app_config()
        run_application(app_config)
    except ValueError as e:
        print(f"Configuration Error: {e}")
        exit(1)
