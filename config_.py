from dataclasses import dataclass


@dataclass
class Config:
    aladin_account = {
        "id": "",           # 알라딘 아이디
        "password": "",     # 알라딘 비밀번호
    }
    telegram_tokens = {
        "my_bot_token": "",
        "used_bot_token": "",
        "error_bot_token": "",
        "my_chat_id": 0,
        "used_chat_id": ""
    }