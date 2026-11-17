# Big-O: how the work grows

Your mentor teaches this page in the first problem session, in week 5. Read it again before each session until it feels familiar.

## The question Big-O answers

A program that is fast on 10 items can be slow on 10 million. Big-O (say "big oh") describes how the number of steps grows when the input grows. It does not measure seconds. It ignores small details and keeps only the shape of the growth.

We write the size of the input as `n`. For a list, `n` is its length.

## The five shapes you will meet

| Name | Written | What it means | 1,000 items | 1,000,000 items |
|---|---|---|---|---|
| Constant | O(1) | The same few steps, whatever the size | 1 step | 1 step |
| Logarithmic | O(log n) | Each step halves what is left | about 10 steps | about 20 steps |
| Linear | O(n) | One pass over the input | 1,000 steps | 1,000,000 steps |
| Linearithmic | O(n log n) | A good sort | about 10,000 steps | about 20,000,000 steps |
| Quadratic | O(n²) | A loop inside a loop over the same input | 1,000,000 steps | 1,000,000,000,000 steps |

A laptop does roughly 10 million simple Python steps in a second. So O(n²) on 1 million items takes more than a day, and O(n log n) takes about 2 seconds.

## The same shapes in Python you already know

```python
names = ["asha", "ravi", "meera", "john"]          # a list
seats = {"asha": "S4-23", "ravi": "S4-24"}         # a dict
booked = {"S4-23", "S4-24"}                        # a set

names[2]                 # O(1): go straight to position 2
seats["asha"]            # O(1): a dict finds a key without looking at the others
"S4-23" in booked        # O(1): the same is true of a set
"meera" in names         # O(n): a list must check the items one by one
max(names)               # O(n): one pass
sorted(names)            # O(n log n)
names.append("zoya")     # O(1): add at the end
names.insert(0, "zoya")  # O(n): every item moves one place
```

This is why you used a dict for spending by merchant in PaisaLens. With a list, finding a merchant is O(n) every time. With a dict, it is O(1).

## How to read Big-O from code

1. **One loop over the input is O(n).**
2. **A loop inside a loop over the same input is O(n²).**
3. **Halving the range on every step is O(log n).** Binary search works this way.
4. **Steps one after another add up, and the bigger one wins.** A sort, then one pass, is O(n log n) + O(n), which is O(n log n).
5. **Watch for hidden loops.** `x in some_list`, `some_list.count(x)`, `min`, `max`, `sum` and slicing each make one pass. Inside a loop, each of them turns O(n) into O(n²).

```python
def has_repeat_slow(pnrs: list[str]) -> bool:
    for i in range(len(pnrs)):              # n times
        for j in range(i + 1, len(pnrs)):   # up to n times each
            if pnrs[i] == pnrs[j]:
                return True
    return False                            # O(n²)


def has_repeat(pnrs: list[str]) -> bool:
    seen: set[str] = set()
    for pnr in pnrs:                        # n times
        if pnr in seen:                     # O(1) in a set
            return True
        seen.add(pnr)
    return False                            # O(n), and O(n) extra memory
```

## Time and space

Big-O also describes memory. `has_repeat` is faster because it keeps a set of up to `n` items, so its extra space is O(n). `has_repeat_slow` keeps nothing extra, so its extra space is O(1). A faster solution often pays with memory. Say both when you describe a solution.

## What to say in a session and in an interview

Use these three sentences, in this order, before you write code:

1. "The slow way is ... and it is O(...), because ..."
2. "I can do better with ..., because ..."
3. "That makes it O(...) time and O(...) extra space."

An interviewer wants to hear this reasoning. A correct answer with no reasoning scores lower than a clear plan with one small bug.

## Check yourself

Answer these without running code. Your mentor has the answers.

1. A function sorts a list of 500,000 click counts and returns the first 10. What is its Big-O?
2. Inside a `for` loop over `bookings`, you write `if booking.pnr in cancelled_pnrs`. Why does it matter whether `cancelled_pnrs` is a list or a set?
3. A sorted list has 1,000,000 station codes. About how many comparisons does a binary search need?
4. Your function makes one pass to find the largest spend, then a second pass to find the smallest. Is it O(n) or O(n²)? Why?
