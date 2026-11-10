"""The shared objects every part of MockPay needs, made once at start-up."""

import random
from dataclasses import dataclass

from mockpay.config import Settings
from mockpay.db import Database


@dataclass
class Context:
    settings: Settings
    db: Database
    # One random generator for every "chance" decision (duplicates, late
    # webhooks). Tests set the rates to 0 or 1 to make the results certain.
    rng: random.Random
