# configuration file for Flask app (keys, database URLs ...)
from dotenv import load_dotenv
from datetime import timedelta 
import os

load_dotenv()

class Config:
  JWT_SECRET_KEY = os.environ.get('SECRET_KEY')
 
