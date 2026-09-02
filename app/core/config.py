from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    redis_url: str

    email_provider: str = "gmail"

    smtp_host: str
    smtp_port: int
    smtp_username: str
    smtp_password: str

    sendgrid_api_key: str = ""
    sendgrid_from_email: str = ""

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()