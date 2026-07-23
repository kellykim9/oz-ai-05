from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_USER: str = "root"
    DB_PASSWORD: str = "1234"
    DB_HOST: str = "localhost"  
    DB_PORT: str = "3306"
    DB_NAME: str = "oz_database"

    model_config = {
        # "env_file": ".env",  
        "extra": "ignore"
    }


settings = Settings()