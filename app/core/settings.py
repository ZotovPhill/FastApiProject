from pydantic.env_settings import BaseSettings


class Settings(BaseSettings):
    environment: str
    secret_key: str
    algorithm: str
    access_token_expires: int
    refresh_token_expires: int
    new_refresh_on_update: bool
    database_url: str
    async_database_url: str
    celery_broker_url: str
    celery_result_backend: str
    root_path: str
    temp_media_path: str
    logging_config_path: str


settings = Settings()
