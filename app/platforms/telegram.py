
import httpx
from datetime import datetime, timezone

from app.config import settings
from app.platforms.base import BasePlatform


class TelegramPlatform(BasePlatform):

    @property
    def name(self):
        return "Telegram"

    async def publish(self, message: str) -> dict:

        if not settings.telegram_bot_token or not settings.telegram_chat_id:
            raise ValueError("Telegram credentials are not configured")

        api_url = (
            f"https://api.telegram.org/"
            f"bot{settings.telegram_bot_token}/sendMessage"
        )

        payload = {
            "chat_id": settings.telegram_chat_id,
            "text": message
        }

        async with httpx.AsyncClient(timeout=30) as client:

            response = await client.post(
                api_url,
                json=payload
            )

            response.raise_for_status()
            result = response.json()

        if not result.get("ok"):
            raise ValueError(
                result.get("description", "Telegram posting failed")
            )

        posted_message = result["result"]

        created_at = datetime.fromtimestamp(
            posted_message["date"],
            tz=timezone.utc
        )

        # Public URL is available only for public channels
        chat_username = posted_message["chat"].get("username")
        message_id = posted_message["message_id"]

        posted_url = (
            f"https://t.me/{chat_username}/{message_id}"
            if chat_username
            else None
        )

        return {
            "platform": self.name,
            "status": "success",
            "posted_url": posted_url,
            "public_access": bool(posted_url),
            "date": created_at.date().isoformat(),
            "time": created_at.time().replace(
                tzinfo=None
            ).isoformat(),
            "error": None
        }

