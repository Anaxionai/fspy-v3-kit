# Weekly problem sessions

Every week from week 5 to week 27 you join one 60-minute problem session with your cohort. You practise the problem types that technical interviews use, and you learn to talk about how fast your code is. It is a timetable session, not a portal task: nothing here is graded.

## How a session runs

| Minutes | What happens |
|---|---|
| 0 to 10 | Your mentor teaches the week's pattern. |
| 10 to 20 | You solve Problem A, the warm-up, alone. |
| 20 to 45 | You solve Problem B, the main problem, alone or in a pair. |
| 45 to 60 | Students show their solutions, and the group compares their Big-O (how the work grows with the input). |

Before you code each problem, answer the three "Say it aloud" prompts in the week's README. An interviewer wants to hear that reasoning first.

## The rules

- **No AI in the session.** No chat AI, no coding agent and no AxTutor while you solve. After the session, you may ask AxTutor to explain a solution you did not understand.
- **Run the tests.** Each week has tests. In the week's folder, run `uv run --with pytest pytest -q`. All tests fail until you write your solution. If Windows blocks `pytest.exe`, run `uv run --with pytest python -m pytest -q` instead: it runs the same tests.
- **Work outside your course repository.** Copy the week's folder to a practice folder of your own, for example `~/problems/week-05`. Never change the kit's own files.
- **A slow answer that works beats a fast answer that does not.** Get a correct solution first, then make it faster.

## Before week 5

Read [`big-o.md`](big-o.md). Your mentor teaches it in the first session.

## The weeks

| Week | Folder | Pattern |
|---|---|---|
| 5 | [`week-05-lists-and-loops`](week-05-lists-and-loops/) | One pass over a list |
| 6 | [`week-06-dicts-and-sets`](week-06-dicts-and-sets/) | Counting and fast lookup with a dict or a set |
| 7 | [`week-07-strings`](week-07-strings/) | Walking a string and normalising text |
| 8 | [`week-08-sorting-and-two-pointers`](week-08-sorting-and-two-pointers/) | Sort with a key, then two pointers |
| 9 | [`week-09-stacks`](week-09-stacks/) | Stacks |
| 10 | [`week-10-queues-and-sliding-window`](week-10-queues-and-sliding-window/) | Queues and a sliding window |
| 11 | [`week-11-binary-search`](week-11-binary-search/) | Binary search |
| 12 | [`week-12-recursion`](week-12-recursion/) | Recursion |
| 13 | [`week-13-linked-lists`](week-13-linked-lists/) | Linked lists |
| 14 | [`week-14-lru-cache`](week-14-lru-cache/) | A cache with a size limit |
| 15 | [`week-15-heaps-and-top-k`](week-15-heaps-and-top-k/) | Heaps and the top k |
| 16 | [`week-16-trees-depth-first`](week-16-trees-depth-first/) | Trees, depth first |
| 17 | [`week-17-trees-breadth-first`](week-17-trees-breadth-first/) | Trees, level by level, and binary search trees |
| 18 | [`week-18-graphs-breadth-first`](week-18-graphs-breadth-first/) | Graphs and the fewest steps |
| 19 | [`week-19-graphs-depth-first-and-order`](week-19-graphs-depth-first-and-order/) | Graphs, depth first, and a valid order |
| 20 | [`week-20-intervals`](week-20-intervals/) | Intervals |
| 21 | [`week-21-greedy`](week-21-greedy/) | Greedy choices |
| 22 | [`week-22-dynamic-programming-1`](week-22-dynamic-programming-1/) | Dynamic programming in one dimension |
| 23 | [`week-23-dynamic-programming-2`](week-23-dynamic-programming-2/) | Dynamic programming in two dimensions |
| 24 | [`week-24-backtracking`](week-24-backtracking/) | Backtracking |
| 25 | [`week-25-sql-problems`](week-25-sql-problems/) | SQL interview questions |
| 26 | [`week-26-mixed-mock-1`](week-26-mixed-mock-1/) | Mock interview 1 |
| 27 | [`week-27-mixed-mock-2`](week-27-mixed-mock-2/) | Mock interview 2 |

Weeks 26 and 27 are mock interviews. Their READMEs do not name the pattern: choosing it is part of the test.
