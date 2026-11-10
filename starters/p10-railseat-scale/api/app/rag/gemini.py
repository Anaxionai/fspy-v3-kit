"""The two model calls of Ask RailSeat, behind one small class (P10 add-on, task 12).

The kit's data/railseat/ask-railseat.md is the reference: your key, the model names
and the embedding settings. Routes get the client from `get_gemini()`, so tests swap in
a fake with `app.dependency_overrides[get_gemini]` and never call the real API.
"""

from app.rag.chunk import Rule

EMBED_DIMENSIONS = 768  # the N of your vector(N) column


class GeminiClient:
    """Embeddings and answers from Google's Gemini API, with the models from settings."""

    def __init__(self) -> None:
        """Make `self.client` with `genai.Client()` from the google-genai library (it finds
        GEMINI_API_KEY in the environment), and keep settings.GEMINI_EMBED_MODEL and
        settings.GEMINI_CHAT_MODEL for the calls below."""
        raise NotImplementedError("TODO(task 12): make the google-genai client")

    def embed_rules(self, rules: list[Rule]) -> list[list[float]]:
        """One vector of EMBED_DIMENSIONS numbers per rule, in the rules' order, in one call (step 4).

        Read section 4 of ask-railseat.md first: the text format for a rule (it uses
        the rule's number), the output size, and why a plain list of texts would give
        one combined vector.
        """
        raise NotImplementedError("TODO(task 12): embed every rule in one call")

    def embed_question(self, question: str) -> list[float]:
        """One vector for a passenger's question, in the question format of section 4 (step 5)."""
        raise NotImplementedError("TODO(task 12): embed the question")

    def answer(self, instructions: str, prompt: str) -> str:
        """Send the instructions and the prompt to the chat model; return its text (step 7)."""
        raise NotImplementedError("TODO(task 12): ask the chat model")


def get_gemini() -> GeminiClient:
    """FastAPI dependency: the client for one request. Tests override it with a fake."""
    return GeminiClient()
