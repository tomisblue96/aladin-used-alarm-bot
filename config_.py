from dataclasses import dataclass


@dataclass
class Config:
    aladin_account = {
        "id": "",           # 알라딘 아이디
        "password": "",     # 알라딘 비밀번호
    }
    telegram_tokens = {
        "bot_token": "",                  # 텔레그램 봇 토큰값
        "error_bot_token": "",     # 텔레그램 봇 토큰값
        "chat_id": 0                      # 텔레그램 봇 chat_id
    }