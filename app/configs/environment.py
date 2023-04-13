from pydantic import BaseSettings
from typing import Any
import json

class Settings(BaseSettings):
    DEBUG: bool = False
    TESTING: str = ''

    PROJECT_NAME: str = 'Demo'
    PROJECT_API_V1: str = '1.1'
    
    SQLALCHEMY_DATABASE_URI : str = 'mysql+pymysql://xxxx:xxxxx@localhost/xxxxxx?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_ENGINE_OPTIONS_POOL_PRE_PING : bool = True
    SQLALCHEMY_ENGINE_OPTIONS_POOL_RECYCLE: int = 200
    SQLALCHEMY_ENGINE_OPTIONS_POOL_TIMEOUT: int = 110

    CHUCKNORRIS_BASE_URL: str = 'https://xxxx.com/'
    ICANHASDADJOKE_BASE_URL: str = 'https://xxxx.com/'

    #OTROS
    TIME_ZONE: str = 'America/Lima'


    class Config:
        env_file = ".env"
        
Config = Settings()