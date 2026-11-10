# Ask RailSeat: a free Gemini API key and the models to use

Ask RailSeat (P10) answers travel questions from [`travel-rules.md`](travel-rules.md) and cites the rule it used.
It uses Google's Gemini API through your own free API key (a secret code that lets your program call the API).

**Checked on 10 November 2026** against Google's Gemini API documentation.
Google moved those pages from `ai.google.dev/gemini-api/docs` to `aistudio.google.com/docs`; the old links still redirect.
Model names change every few months. If a model below stops working, check the [models page](https://aistudio.google.com/docs/models) and tell your mentor.

## 1. Get a free API key

1. Open [Google AI Studio's API keys page](https://aistudio.google.com/app/apikey) and sign in with your personal Google account.
2. Accept the terms if AI Studio asks you to.
3. Select **Create API key**. AI Studio makes a Google Cloud project for the key.
4. Copy the key. Treat it like a password: anyone with the key can use your quota.

### The free tier: what you get and what you give

- The models in section 3 are free of charge on the free tier. You do not need a card.
- **On the free tier, Google may use your prompts and the answers to improve its products.** So never send real personal data, such as a passenger's name, phone number or Aadhaar number. Use made-up test data.
- Rate limits (the number of requests you may make) are counted **per project, not per API key**. A second key in the same project does not give you more.
- Google no longer prints the free-tier numbers in its documentation. See your real limits on the [rate limit page in AI Studio](https://aistudio.google.com/rate-limit). It shows requests per minute (RPM), tokens per minute (TPM) and requests per day (RPD) for each model.
- The daily count starts again at midnight Pacific time: 13:30 in India from November to early March, and 12:30 from March to early November.
- When you go over a limit, the API answers `429 RESOURCE_EXHAUSTED`. Wait a minute and try again.
- A project created outside AI Studio may need verification before it can use the free tier. Create the key in AI Studio to avoid this.

## 2. Keep the key in `.env`, never in Git

In your `railseat/api/` folder, create a file named `.env` with one line:

```bash
GEMINI_API_KEY=paste-your-key-here
```

Commit a `.env.example` with the name only, so others know the setting exists:

```bash
GEMINI_API_KEY=
```

Your course repository's root `.gitignore` already lists `.env` (Launchpad task 26). Check that Git ignores your file:

```bash
git check-ignore -v railseat/api/.env
```

It prints the `.gitignore` line that matches. If it prints nothing, Git would commit your key: fix `.gitignore` first.
If a key ever reaches GitHub, delete it in AI Studio at once and create a new one.

`uv` can read `.env` for you when it runs a program:

```bash
uv run --env-file .env python chat_example.py
```

The Gemini library finds the key by itself in the `GEMINI_API_KEY` environment variable.

## 3. The models

| Job | Model name | Notes |
|---|---|---|
| Answering questions | `gemini-3.5-flash-lite` | Stable. Google's suggestion for new projects. Fast, and free on the free tier. Use this one. |
| Answering harder questions | `gemini-3.8-flash` | Stable. Better at reasoning, but slower. Free on the free tier. |
| Embeddings | `gemini-embedding-2` | Stable. Turns text (up to 8,192 tokens) into a list of numbers. Use this one. |
| Embeddings (older model) | `gemini-embedding-001` | Stable, text only, up to 2,048 tokens. Use it only if your code already does. |

An **embedding** is a list of numbers that stands for the meaning of a text. Texts with similar meanings get similar lists.
Do not start new code with `gemini-2.5-flash` or `gemini-2.5-pro`: Google has deprecated them. From 1 December 2026, it sends their requests to newer models.

## 4. The embedding settings for Ask RailSeat

- **Model:** `gemini-embedding-2`, for the rules and for every question. Vectors from different models cannot be compared, so never mix them.
- **Size:** set `output_dimensionality=768`. The default is 3,072 numbers. PostgreSQL's pgvector indexes work only up to 2,000 numbers, and Google recommends 768 as a smaller size. Store the vectors in a `vector(768)` column.
- **No `task_type`:** `gemini-embedding-2` does not accept the `task_type` setting. Write the task inside the text instead, as Google's documentation shows:
  - each rule: `title: Rule 26 | text: <the text of the rule>`
  - each question: `task: question answering | query: <the passenger's question>`
- **One text, one vector:** if you give `gemini-embedding-2` a plain list of texts, it returns **one combined vector** for all of them. Embed one text per call, or wrap each text in its own `types.Content` object.
- **Normalised:** `gemini-embedding-2` returns vectors of length 1, also at 768 numbers. Compare them with pgvector's cosine distance operator, `<=>`.

The older `gemini-embedding-001` works differently: it takes `task_type="RETRIEVAL_DOCUMENT"` for the rules and `task_type="RETRIEVAL_QUERY"` for questions. At 768 numbers, you must normalise its vectors yourself.

## 5. Two short examples

Add the official library to your project in `railseat/api/` (the version is in the kit's `VERSIONS.md`):

```bash
uv add google-genai
```

**Ask a question** (`chat_example.py`). This uses the Interactions API, as Google's current documentation does:

```python
# chat_example.py: ask Gemini one question, answered only from the rule we give it.
from google import genai

client = genai.Client()  # finds GEMINI_API_KEY in the environment
rule = "Rule 38: Only dogs and cats may travel. They travel only in 1A, when your group books the whole cabin."
interaction = client.interactions.create(
    model="gemini-3.5-flash-lite",
    system_instruction="Answer only from the rules given. Cite the rule number, like [Rule 38].",
    input=f"{rule}\n\nQuestion: Can I take my cat in 3A?",
)
print(interaction.output_text)
```

Run it with `uv run --env-file .env python chat_example.py`. You should see an answer that says no and cites [Rule 38].

**Make an embedding** (`embed_example.py`):

```python
# embed_example.py: turn one rule into a vector of 768 numbers.
from google import genai
from google.genai import types

client = genai.Client()  # finds GEMINI_API_KEY in the environment
result = client.models.embed_content(
    model="gemini-embedding-2",
    contents="title: Rule 38 | text: Only dogs and cats may travel. They travel only in 1A.",
    config=types.EmbedContentConfig(output_dimensionality=768),
)
print(len(result.embeddings[0].values))  # prints 768
```

## 6. If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `400` and `API_KEY_INVALID` | The key is wrong, or your program did not get it | Run with `uv run --env-file .env ...`, and check the key in `.env` has no spaces or quotes around it |
| `429` and `RESOURCE_EXHAUSTED` | You went over a rate limit | Wait a minute. Check your limits on the AI Studio rate limit page |
| `404` and the model name | The model name has a typing mistake, or Google retired the model | Copy the name from section 3, then check the models page |
| `ModuleNotFoundError: No module named 'google'` | The library is not in this project | Run `uv add google-genai` in `railseat/api/` |

Google's pages for this file: [models](https://aistudio.google.com/docs/models), [embeddings](https://aistudio.google.com/docs/embeddings), [pricing and the free tier](https://aistudio.google.com/docs/pricing), [rate limits](https://aistudio.google.com/docs/rate-limits) and [API keys](https://aistudio.google.com/docs/api-key).
