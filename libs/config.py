from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Mysql(BaseModel):
    username: str
    password: str
    host: str
    port: str

    @property
    def connections(self) -> dict:
        return {
            "connections": {
                "default": {
                    "engine": "tortoise.backends.mysql",
                    "credentials": {
                        "user": self.username,
                        "password": self.password,
                        "host": self.host,
                        "port": self.port,
                        "database": None,
                    }
                }
            },
            'apps': {
                'my_app': {
                    'models': ['models'],
                    'default_connection': 'default',
                }
            }
        }


class MailServer(BaseModel):
    smtp_server: str
    smtp_port: int
    email_from: str
    """自訂的發信人名稱"""
    sender_email: str
    sender_password: str


class Redis(BaseModel):
    host: str
    port: int


class Queue(BaseModel):
    queue_name: str


class Sentry(BaseModel):
    dsn: str


class Config(BaseSettings):
    """ 設定
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )

    mysql: Mysql = None
    mail_server: MailServer = None
    redis: Redis = None
    queue: Queue = None
    sentry: Sentry = None


CONFIG = Config()
