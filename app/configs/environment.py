from pydantic import BaseSettings
from typing import Any
import json

class Settings(BaseSettings):
    DEBUG: bool = False
    TESTING: str = ''

    PROJECT_NAME: str = '2343'
    PROJECT_API_V1: str = '1.1'
    
    SQLALCHEMY_DATABASE_URI : str = 'postgresql://dbuser:dbpass@localhost:5432/agros-stage'
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_ENGINE_OPTIONS_POOL_PRE_PING : bool = True
    SQLALCHEMY_ENGINE_OPTIONS_POOL_RECYCLE: int = 200
    SQLALCHEMY_ENGINE_OPTIONS_POOL_TIMEOUT: int = 110

    # SMTP 
    SMTP_URL: str = 'smtp.gmail.com'
    SMTP_PORT: int = 587
    SMTP_USER: str = 'xxxx'
    SMTP_PASSWORD: str = 'xxxxx'

    # JWT AND HEADERS
    JWT_SECRET: str = 'wubcfy289veckwdbhc97q2veidcbwyhdcb86ve13vdyv93rg972bc972c927vf2bcfuiwebc792'
    JWT_PREFIX: str = 'Bearer'

    #OTROS
    TIME_ZONE: str = 'America/Lima'

    #LOGS
    LOG_NAME_GROUP:str = ''

    #Access Politica Aws
    AWS_ACCESS_KEY_ID:str = ''
    AWS_SECRET_ACCESS_KEY:str = ''
    AWS_REGION:str = ''

    #AWS S3
    AWS_S3_REGION:str = ''
    AWS_S3_BUCKET:str = ''

    class Config:
        env_file = ".env"
        
Config = Settings()