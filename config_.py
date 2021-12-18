from dataclasses import dataclass


@dataclass
class Config:
    aladin_account = {
        "id": "",           # 알라딘 아이디
        "password": "",     # 알라딘 비밀번호
    }
    telegram_tokens = {
        "bot_token": "1925060456:AAG84CkWcY9590tGIh7bBS9KX09U-B5J0cs",                  # 텔레그램 봇 토큰값
        "my_something_bot_token": "1912641898:AAFAJWwPQ7jr5QHWl2I3Iwmj4Sad7UbokgQ",     # 텔레그램 봇 토큰값
        "chat_id": 1033055927                                                           # 텔레그램 봇 chat_id
    }