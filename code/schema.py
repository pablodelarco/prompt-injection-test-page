"""Layer 3 (Constrain): accept only a fixed, validated shape from the reader model."""
import re

from pydantic import BaseModel, Field, field_validator

URL_OR_EMAIL = re.compile(r"https?://|www\.|[\w.+-]+@[\w-]+\.\w+", re.I)


class PageSummary(BaseModel, extra="forbid"):
    product_name: str = Field(max_length=120)
    price_usd: float | None = Field(default=None, ge=0, le=100_000)
    summary: str = Field(max_length=600)
    features: list[str] = Field(default_factory=list, max_length=8)

    @field_validator("summary", "product_name")
    @classmethod
    def no_links_or_addresses(cls, value: str) -> str:
        if URL_OR_EMAIL.search(value):
            raise ValueError("URLs and email addresses are not allowed in this field")
        return value
