import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'uma-chave-padrão-fraca-para-testes')
    SQLACHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    if not SQLACHEMY_DATABASE_URI:
        raise ValueError("DATABASE_URL não está configurado no arquivo .env")
    
    SQLACHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(os.path.asbath(os.path.dirname(__file__)), 'static', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}