from pathlib import Path

from pydantic import BaseModel


class Mysql(BaseModel):
    username: str
    password: str
    host: str
    port: str

    @property
    def connections(self) -> dict:
        return {
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
        }


class MailServer(BaseModel):
    smtp_server: str
    smtp_port: int
    email_from: str
    """自訂的發信人名稱"""
    sender_email: str
    sender_password: str


class Config(BaseModel):
    """ 設定
    """
    mysql: Mysql = None
    mail_server: MailServer = None


CONFIG: Config = Config.model_validate_json(
    (Path(__file__).parent.parent / "config.json")
    .read_text()
)
