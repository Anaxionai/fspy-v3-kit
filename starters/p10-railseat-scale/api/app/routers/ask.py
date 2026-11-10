"""POST /ask: Ask RailSeat answers travel-rule questions with citations, or refuses (P10 add-on).

Signed-in users only (P5's deny-by-default), which also protects your free-tier quota.
Never load-test this route: the free tier allows only a few calls a minute.
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.rag.gemini import GeminiClient, get_gemini
from app.rag.retrieve import Retrieved
from app.security import current_user

router = APIRouter(tags=["ask"], dependencies=[Depends(current_user)])

# TODO(task 12): the best distance above which Ask RailSeat refuses without calling the
# chat model. Choose it from the 10 distances of step 9 and write why in evidence.md.
REFUSE_ABOVE: float | None = None

REFUSAL = "I can only answer questions about RailSeat's travel rules, and none of them answers this."


class AskIn(BaseModel):
    question: str = Field(min_length=3, max_length=300)


class AskOut(BaseModel):
    answer: str
    citations: list[int]  # rule numbers cited in the answer that were also retrieved
    refused: bool


def build_prompt(question: str, rules: list[Retrieved]) -> tuple[str, str]:
    """Return `(instructions, prompt)` for the chat model (step 7).

    The instructions keep the model to its sources: answer only from these rules,
    cite them as [Rule N], and say so when they do not answer the question.
    The prompt holds the 3 rules, each with its number and title, then the question.
    """
    raise NotImplementedError("TODO(task 12): write the instructions and the prompt")


def cited_rules(answer: str, rules: list[Retrieved]) -> list[int]:
    """The rule numbers written as [Rule N] in `answer` that are also in `rules` (step 8).

    A number the model invents, or a rule that was not retrieved, is never a citation.
    """
    raise NotImplementedError("TODO(task 12): keep only citations of retrieved rules")


@router.post("/ask", response_model=AskOut)
async def ask(
    data: AskIn,
    session: AsyncSession = Depends(get_session),
    gemini: GeminiClient = Depends(get_gemini),
):
    """Answer one question from the travel rules (steps 6-8).

    - `top_rules()` for the 3 nearest rules. If the best distance is above
      REFUSE_ABOVE, return REFUSAL with `refused` true and no citations, without
      calling the chat model.
    - Else build the prompt, call `gemini.answer()` and return the answer with
      `cited_rules()`.
    """
    # TODO(task 13): log how long the embedding, the database query and the chat call take.
    raise NotImplementedError(
        "TODO(task 12): retrieve, refuse or answer with citations"
    )
