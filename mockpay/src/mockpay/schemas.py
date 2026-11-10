"""The JSON bodies the API accepts, checked by Pydantic."""

from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

# strict=True: MockPay refuses 1250.0 and "1250". Money is a whole number of paise.
OrderAmount = Annotated[int, Field(strict=True, ge=100, le=1_000_000_000)]  # ₹1 to ₹1 crore
RefundAmount = Annotated[int, Field(strict=True, ge=1)]


class OrderCreate(BaseModel):
    # extra="forbid": a misspelt field name is an error, not silently ignored.
    model_config = ConfigDict(extra="forbid")

    amount_paise: OrderAmount
    currency: Literal["INR"]
    receipt: Annotated[str, Field(min_length=1, max_length=40)]
    notes: Annotated[dict[str, Any] | None, Field(max_length=15)] = None
    return_url: str | None = None  # where checkout sends the customer afterwards

    @field_validator("return_url")
    @classmethod
    def _must_be_a_web_address(cls, value: str | None) -> str | None:
        if value is not None and not value.startswith(("http://", "https://")):
            raise ValueError("must start with http:// or https://")
        return value


class RefundCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    payment_id: Annotated[str, Field(min_length=1)]
    amount_paise: RefundAmount


class WebhookResend(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_id: Annotated[str, Field(min_length=1)]
    copies: Annotated[int, Field(ge=1, le=5)] = 1  # several copies arrive at the same moment
