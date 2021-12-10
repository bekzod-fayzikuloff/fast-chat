from pydantic import BaseSettings
import dotenv

dotenv.load_dotenv()


class Settings(BaseSettings):
    server_host: str = "0.0.0.0"
    server_port: int = 8000
    database_url: str
    debug: bool = True

    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_token_expiration: int = 3600


settings = Settings(
    _env_file=".env",
    _env_file_encoding="utf8",
)
