
import httpx
from datetime import datetime
from uuid import uuid4

from app.config import settings
from app.platforms.base import BasePlatform


class MastodonPlatform(BasePlatform):

    @property
    def name(self):
        return "Mastodon"

    async def publish(self, message: str) -> dict:

        if not settings.mastodon_base_url or not settings.mastodon_access_token:
            raise ValueError("Mastodon credentials are not configured")

        base_url = settings.mastodon_base_url.rstrip("/")
        url = f"{base_url}/api/v1/statuses"

        headers = {
            "Authorization": f"Bearer {settings.mastodon_access_token}",
            "Idempotency-Key": str(uuid4())
        }

        payload = {
            "status": message,
            "visibility": "public"
        }

        async with httpx.AsyncClient(timeout=30) as client:

            response = await client.post(
                url,
                headers=headers,
                data=payload
            )

            response.raise_for_status()
            result = response.json()

        created_at = datetime.fromisoformat(
            result["created_at"].replace("Z", "+00:00")
        )

        return {
            "platform": self.name,
            "status": "success",
            "posted_url": result.get("url"),
            "public_access": (
                result.get("visibility") == "public"
                and bool(result.get("url"))
            ),
            "date": created_at.date().isoformat(),
            "time": created_at.time().replace(tzinfo=None).isoformat(),
            "error": None
        }
