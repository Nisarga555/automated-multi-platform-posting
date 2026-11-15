
import re
from urllib.parse import urlsplit

from pydantic import BaseModel, Field, field_validator


class PostingRequest(BaseModel):

    message: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Message containing exactly one CTA link"
    )

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str) -> str:

        # Find URLs in the message
        urls = re.findall(
            r"https?://[^\s<>\[\]()]+",
            value
        )

        # Exactly one URL is required
        if len(urls) != 1:
            raise ValueError(
                "Message must contain exactly one CTA link"
            )

        # Validate URL structure
        try:
            parsed = urlsplit(urls[0])

            if (
                parsed.scheme not in ("http", "https")
                or not parsed.hostname
                or "." not in parsed.hostname
            ):
                raise ValueError()

            if parsed.port is not None:
                if not 1 <= parsed.port <= 65535:
                    raise ValueError()

        except ValueError:
            raise ValueError("Please provide a valid URL")

        return value


class PlatformResult(BaseModel):
    platform: str
    status: str
    posted_url: str | None = None
    public_access: bool = False
    date: str | None = None
    time: str | None = None
    error: str | None = None


class PostingResponse(BaseModel):
    success: bool
    results: list[PlatformResult]
