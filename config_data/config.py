
from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    target_chat_id: int

@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str | None) -> Config:
    env: Env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env("BOT_TOKEN"),
                               target_chat_id=env("TARGET_CHAT_ID"),
                               admin_ids=list(map(int, env.list("ADMIN_IDS")))))

def get_target_chat_id(path: str | None) -> int:
    env: Env = Env()
    env.read_env(path)
    return env("TARGET_CHAT_ID")

def get_admin_ids(path: str | None) -> list[int]:
    env: Env = Env()
    env.read_env(path)
    return list(map(int, env.list("ADMIN_IDS")))
