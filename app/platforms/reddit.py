
import httpx
from datetime import datetime, timezone

from app.config import settings
from app.platforms.base import BasePlatform


class RedditPlatform(BasePlatform):

    @property
    def name(self):
        return "Reddit"

    async def publish(self, message: str) -> dict:

        required = [
            settings.reddit_client_id,
            settings.reddit_client_secret,
            settings.reddit_username,
            settings.reddit_password,
            settings.reddit_subreddit
        ]

        if not all(required):
            raise ValueError("Reddit credentials are not configured")

        user_agent = (
            f"python:AutoPostHub:v1.0 "
            f"(by /u/{settings.reddit_username})"
        )

        async with httpx.AsyncClient(
            timeout=30,
            auth=httpx.BasicAuth(
                settings.reddit_client_id,
                settings.reddit_client_secret
            ),
            headers={"User-Agent": user_agent}
        ) as client:

            # Step 1: Obtain OAuth access token
            token_response = await client.post(
                "https://www.reddit.com/api/v1/access_token",
                data={
                    "grant_type": "password",
                    "username": settings.reddit_username,
                    "password": settings.reddit_password
                }
            )

            token_response.raise_for_status()
            token_data = token_response.json()

            access_token = token_data.get("access_token")

            if not access_token:
                raise ValueError("Reddit authentication failed")

            # Step 2: Submit a text post
            response = await client.post(
                "https://oauth.reddit.com/api/submit",
                headers={
                    "Authorization": f"Bearer {access_token}"
                },
                data={
                    "api_type": "json",
                    "sr": settings.reddit_subreddit,
                    "kind": "self",
                    "title": "Update from AutoPostHub",
                    "text": message
                }
            )

            response.raise_for_status()
            result = response.json()

            # Reddit can return HTTP 200 even when posting fails
            errors = result.get("json", {}).get("errors", [])

            if errors:
                raise ValueError(f"Reddit posting failed: {errors}")

            post_data = result.get("json", {}).get("data", {})
            permalink = post_data.get("url")

            if not permalink:
                raise ValueError("Reddit did not return a post URL")

            created_at = datetime.now(timezone.utc)

            return {
                "platform": self.name,
                "status": "success",
                "posted_url": (
                    "https://www.reddit.com" + permalink
                ),
                "public_access": True,
                "date": created_at.date().isoformat(),
                "time": created_at.time().replace(
                    tzinfo=None
                ).isoformat(),
                "error": None
            }
