
import httpx
from datetime import datetime, timezone

from app.config import settings
from app.platforms.base import BasePlatform


class DiscordPlatform(BasePlatform):

    @property
    def name(self):
        return "Discord"

    async def publish(self, message: str) -> dict:

        if not settings.discord_webhook_url:
            raise ValueError("Discord webhook is not configured")

        webhook_url = settings.discord_webhook_url.rstrip("/") + "?wait=true"

        payload = {
            "content": message,
            "allowed_mentions": {"parse": []}
        }

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(webhook_url, json=payload)
            response.raise_for_status()
            result = response.json()

        created_at = datetime.now(timezone.utc)

        message_id = result.get("id")
        channel_id = result.get("channel_id")
        guild_id = result.get("guild_id")

        posted_url = None
        if message_id and channel_id and guild_id:
            posted_url = (
                f"https://discord.com/channels/"
                f"{guild_id}/{channel_id}/{message_id}"
            )

        return {
            "platform": self.name,
            "status": "success",
            "posted_url": posted_url,
            "public_access": False,
            "date": created_at.date().isoformat(),
            "time": created_at.time().replace(tzinfo=None).isoformat(),
            "error": None
        }
