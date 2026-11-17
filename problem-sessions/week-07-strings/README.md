# Week 7: Walking a string and normalising text

## The pattern in five lines

1. A string is a sequence of characters, so you can loop over it like a list.
2. Normalise text (change it to one standard form) before you compare it: one case, no spaces, no punctuation.
3. `str.lower()`, `str.isalnum()` and `"".join(...)` do most of the normalising work.
4. Reach for this pattern when two texts should count as the same even though they look different.
5. One walk over a string of length n is O(n). A slice such as `text[1:]` copies the string, so slicing inside a loop costs O(n²).

## Problem A (warm-up, 10 minutes): Labels that read the same backwards

Shortly lets a user choose a custom label for a short link. The team wants to mark labels that are palindromes (text that reads the same forwards and backwards), such as `Malayalam`. Spaces, punctuation and capital letters do not count.

```python
def is_palindrome(label: str) -> bool:
```

**Examples**

| Call | Returns | Why |
|---|---|---|
| `is_palindrome("Malayalam")` | `True` | It reads "malayalam" both ways. |
| `is_palindrome("Top spot")` | `True` | Without the space and the capital letter, it is "topspot". |
| `is_palindrome("Shortly")` | `False` | Backwards it reads "yltrohs". |
| `is_palindrome("")` | `True` | Empty text reads the same both ways. |

**Rules**

- `label` has 0 to 100,000 characters. They are English letters, digits, spaces and punctuation such as `-`, `.` and `!`.
- Compare letters and digits only. Ignore every other character.
- A capital letter and its small letter count as the same, so `M` matches `m`.
- Return `True` when the label has no letters or digits. The empty string also returns `True`.

## Problem B (main, 25 minutes): Look-alike short codes

Shortly makes short codes from letters and digits. Two codes that use the same characters in a different order look alike, and users mix them up. Group the codes that are anagrams (the same characters, each used the same number of times, in any order) of each other.

```python
def look_alike_groups(codes: list[str]) -> list[list[str]]:
```

**Examples**

| Call | Returns | Why |
|---|---|---|
| `look_alike_groups(["ab3k", "pq7r", "k3ba", "r7qp", "zz1"])` | `[["ab3k", "k3ba"], ["pq7r", "r7qp"]]` | `zz1` has no look-alike, so it is left out. |
| `look_alike_groups(["Tea9", "eat9", "ate9", "tan"])` | `[["Tea9", "eat9", "ate9"]]` | A capital letter counts as its small letter. |
| `look_alike_groups(["aab", "abb"])` | `[]` | The letters match, but not how many times each appears. |
| `look_alike_groups([])` | `[]` | There are no codes. |

**Rules**

- `codes` has 0 to 100,000 items. Each code has 1 to 12 characters: English letters and digits.
- Two codes look alike when they hold the same characters, each the same number of times, in any order.
- A capital letter and its small letter count as the same character.
- Return only groups with two or more codes. Keep each code exactly as it was written.
- Put the groups in the order of their first code in `codes`. Inside a group, keep the order of `codes`.
- A code that appears twice looks alike with itself, so both copies go in its group.
- Return `[]` when no codes look alike. An empty list also returns `[]`.
- Do not change the list `codes`.

## Say it aloud

Answer these three questions aloud for each problem before you write code.

1. What is the slow way to solve it, and what is its Big-O?
2. Which normalised form makes two matching texts exactly equal?
3. Which edge cases (unusual inputs, such as an empty string) could break your code? Name three.

## After the session

Write `same_characters(a, b)`, which says whether two codes look alike without sorting them. Count the characters of each code in a dict instead. Compare its Big-O with the sorting version.

## Run the tests

Open a terminal in this folder and run:

```bash
uv run --with pytest pytest -q
```

Every test fails with `NotImplementedError` until you write your solutions in `problems.py`. Do not change `test_problems.py`.
