"""Index the travel rules into rule_chunks, once (P10 add-on, task 12, step 4).

Run it from railseat/api after the rule_chunks migration:

    uv run --env-file .env python -m app.rag.index

It reads the kit's travel-rules.md (or the path you give), splits it, embeds every
rule in one call and saves one row per rule. Running it again updates the rows.
"""

import asyncio
import sys
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession

from app.db import SessionLocal
from app.rag.chunk import Rule, split_rules
from app.rag.gemini import GeminiClient

RULES_PATH = Path.home() / "fspy-v3-kit" / "data" / "railseat" / "travel-rules.md"


async def upsert_rules(
    session: AsyncSession, rules: list[Rule], vectors: list[list[float]]
) -> int:
    """Save one rule_chunks row per rule (rule_no, title, body, embedding); return the count.

    Insert, or update the row with the same `rule_no`, so a second run adds no rows.
    Do not commit here; main() commits once.
    """
    raise NotImplementedError(
        "TODO(task 12): upsert the rules and their vectors by rule_no"
    )


async def main(path: Path) -> None:
    rules = split_rules(path.read_text(encoding="utf-8"))
    vectors = GeminiClient().embed_rules(rules)
    async with SessionLocal() as session:
        count = await upsert_rules(session, rules, vectors)
        await session.commit()
    print(f"Indexed {count} rules from {path}")


if __name__ == "__main__":
    asyncio.run(main(Path(sys.argv[1]) if len(sys.argv) > 1 else RULES_PATH))
