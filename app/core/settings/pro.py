from app.core.settings.settings import BaseSettings 
import os

class ProdSettings(BaseSettings):
    DEBUG = False                 
    DB_NAME = "library_prod"
    SECRET_KEY = os.getenv("SECRET_KEY")   