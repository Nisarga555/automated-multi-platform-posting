
import asyncio

from app.platforms.mastodon import MastodonPlatform
from app.platforms.bluesky import BlueskyPlatform
from app.platforms.reddit import RedditPlatform
from app.platforms.telegram import TelegramPlatform
from app.platforms.discord import DiscordPlatform

from app.schemas import PlatformResult, PostingResponse


PLATFORMS = [
    MastodonPlatform(),
    BlueskyPlatform(),
    RedditPlatform(),
    TelegramPlatform(),
    DiscordPlatform()
]


async def publish_to_platform(platform, message):

    try:
        result = await platform.publish(message)
        return PlatformResult(**result)

    except Exception as error:
        return PlatformResult(
            platform=platform.name,
            status="failed",
            posted_url=None,
            public_access=False,
            date=None,
            time=None,
            error=str(error)
        )


async def publish_message(message: str):

    results = await asyncio.gather(
        *[
            publish_to_platform(platform, message)
            for platform in PLATFORMS
        ]
    )

    return PostingResponse(
        success=any(result.status == "success" for result in results),
        results=results
    )
