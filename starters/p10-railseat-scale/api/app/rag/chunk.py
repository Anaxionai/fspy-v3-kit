"""Split the travel rules into one chunk per numbered rule (P10 add-on, task 12, step 3)."""

from dataclasses import dataclass


@dataclass
class Rule:
    """One numbered rule: `### Rule 26: <title>` in travel-rules.md, then its text."""

    number: int
    title: str
    text: str


def split_rules(markdown: str) -> list[Rule]:
    """Return one Rule per `### Rule N: Title` heading, in the file's order.

    - `text` is everything up to the next heading, with spaces trimmed. It never
      holds a heading line such as `## Pets`.
    - The kit's travel-rules.md gives 40 rules, numbered 1 to 40.
    - Text before the first rule (the title, the notes and the word list) is not a rule.
    """
    raise NotImplementedError(
        "TODO(task 12): split the rules with a regular expression"
    )
