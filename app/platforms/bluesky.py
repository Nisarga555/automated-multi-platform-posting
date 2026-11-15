
import asyncio
from datetime import datetime, timezone

from atproto import Client

from app.config import settings
from app.platforms.base import BasePlatform


class BlueskyPlatform(BasePlatform):

    @property
    def name(self):
        return "Bluesky"

    def _publish_sync(self, message: str):

        client = Client()

        client.login(
            settings.bluesky_handle,
            settings.bluesky_app_password
        )

        post = client.send_post(message)

        return post

    async def publish(self, message: str) -> dict:

        if not settings.bluesky_handle or not settings.bluesky_app_password:
            raise ValueError("Bluesky credentials are not configured")

        post = await asyncio.to_thread(
            self._publish_sync,
            message
        )

        created_at = datetime.now(timezone.utc)

        record_key = post.uri.rsplit("/", 1)[-1]

        posted_url = (
            f"https://bsky.app/profile/"
            f"{settings.bluesky_handle}/post/{record_key}"
        )

        return {
            "platform": self.name,
            "status": "success",
            "posted_url": posted_url,
            "public_access": True,
            "date": created_at.date().isoformat(),
            "time": created_at.time().replace(tzinfo=None).isoformat(),
            "error": None
        }
