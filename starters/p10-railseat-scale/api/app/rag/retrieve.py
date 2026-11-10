"""Find the rules nearest to a question in pgvector (P10 add-on, task 12, step 5)."""

from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.rag.gemini import GeminiClient


@dataclass
class Retrieved:
    """One rule found for a question. `distance` is the cosine distance: 0 is the
    same meaning, and a bigger number is further away."""

    rule_no: int
    title: str
    body: str
    distance: float


async def top_rules(
    session: AsyncSession, gemini: GeminiClient, question: str, k: int = 3
) -> list[Retrieved]:
    """Embed the question and return the k nearest rules, nearest first.

    Order rule_chunks by cosine distance to the question's vector (pgvector's `<=>`,
    or `cosine_distance()` on your Vector column) and return each rule with its
    distance. With raw SQL on asyncpg, read the Stuck section about the vector type.
    """
    raise NotImplementedError(
        "TODO(task 12): find the k nearest rules by cosine distance"
    )
