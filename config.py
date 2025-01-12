import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Flask configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'xxxxxxxxxxxxxx')  # Required for Flask sessions and security
    DEBUG = os.getenv('DEBUG', 'False') == 'True'  # Enable or disable debug mode

    # Trading Bot API credentials
    API_KEY = os.getenv('API_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')

    # Other configurations (optional)
    MAX_TRADE_QUANTITY = float(os.getenv('MAX_TRADE_QUANTITY', 1000.0))
    ALLOWED_SYMBOLS = os.getenv('ALLOWED_SYMBOLS', 'AAPL,GOOG,MSFT,AMZN,META').split(',')