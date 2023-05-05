import requests

from library_service import settings


def send_to_telegram(message: str) -> None:
    if settings.TELEGRAM_API_TOKEN:
        telegram_api_url = (
            f"https://api.telegram.org/bot{settings.TELEGRAM_API_TOKEN}/sendMessage"
        )
        try:
            requests.post(
                telegram_api_url,
                json={"chat_id": settings.TELEGRAM_CHAT_ID, "text": message},
            )
        except Exception as e:
            print(e)
