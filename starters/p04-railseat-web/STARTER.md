# RailSeat web: the Guided starter for P4

This folder is a `railseat/web/` folder with the set-up already done: a Vite, React and TypeScript app with React Router, TanStack Query, Zod, Tailwind, Vitest and Playwright installed and configured, the five pages, the API's types and the hooks' signatures. All the logic that a task asks for is still yours. Each piece is marked `TODO(task NN)`, where NN is the task's number in module P4.

## What is included

| Path | What it gives you |
|---|---|
| `package.json`, `package-lock.json` | Every P4 package at a pinned version, and the scripts `dev`, `build`, `lint`, `preview` and `test` (`vitest run src`) |
| `vite.config.ts` | The React plugin, and port 5173 kept fixed for CORS. Tailwind is installed but switched off until task 14. |
| `src/main.tsx` | `<QueryClientProvider>` and `<BrowserRouter>` around `<App />` |
| `src/App.tsx` | Shows only the Search page. You add the header and the routes. |
| `src/routes/` | `Search`, `Results`, `SeatMap`, `MyBookings` and `NotFound`, each with an `<h1>`; `searchSchema.ts` (the shape only) and `searchSchema.test.ts` (four skipped cases) |
| `src/api/client.ts` | `BASE_URL`, `ApiError`, and the types `TrainResult`, `Seat`, `Booking` and `BookingIn`. `api()` is a TODO. |
| `src/api/queries.ts` | The signatures of `useTrainSearch`, `useSeats`, `useBookSeat`, `useBooking` and `useCancelBooking` |
| `src/pnrs.ts` | The signatures of `loadPnrs` and `savePnr` |
| `src/index.css` | Plain, readable styles until task 14 |
| `playwright.config.ts` | Chromium only, one worker, a trace for each failure, `baseURL`, and a `webServer` that runs `npm run dev` |
| `tests/e2e/booking.spec.ts` | The two end-to-end tests, skipped, and a date helper to write |
| `.gitignore` | Keeps `node_modules/`, `dist/` and Playwright's output out of Git |

## Copy it in (task 8, step 1)

You need Node 24 (`node --version`). In Git Bash, in task 8's folder, after you copy your `railseat/` folder from P3 and before you have a `railseat/web/` folder:

```bash
cp -r ~/fspy-v3-kit/starters/p04-railseat-web railseat/web
cd railseat/web
npm install
```

## Run it

In `railseat/web/`:

```bash
npm run dev     # then open http://localhost:5173
npm run build   # checks the types, then builds into dist/
npm test        # 4 skipped until task 10
```

For task 15, install the test browser once with `npx playwright install chromium`, then run `npx playwright test`. Playwright starts the web app itself, so start PostgreSQL and your API first.

## Steps already done for you

- **Task 8:** step 1 (copy this folder instead of `npm create vite`), step 2 (`react-router` is installed, so run only `npm install`), step 3 (the five pages exist), and the first half of step 4 (`<BrowserRouter>` is in `main.tsx`; you declare the routes in `App.tsx`).
- **Task 9:** the types and `ApiError` in `client.ts` (steps 2 and 3, but not `api()` itself). The CORS fix (step 7) goes in your own `railseat/api/app/main.py`, not here.
- **Task 10:** `zod` is installed (step 1), and Vitest and the `test` script are set up (step 8).
- **Task 11:** step 1 is done: TanStack Query is installed, and `<QueryClientProvider>` is in `main.tsx`.
- **Task 14:** the install in step 1 is done. You add the plugin and the `@import` line. There is no `App.css` to delete.
- **Task 15:** steps 1 to 3 are done, except installing the browser. There is no example test to delete.

## TODO map

| Task | File | What you write |
|---|---|---|
| 8 | `src/App.tsx` | The header with two `<NavLink>`s, and the five routes |
| 8 | `src/routes/Search.tsx`, `Results.tsx`, `SeatMap.tsx` | The temporary search button, `useSearchParams`, the `<Link>` and `useParams` |
| 9 | `src/api/client.ts` | `api<T>()`, which throws an `ApiError` for an answer that is not 2xx |
| 9 | `src/routes/Results.tsx` | The first API call, in a `useEffect` |
| 10 | `src/routes/searchSchema.ts`, `searchSchema.test.ts` | The schema's rules and its four test cases |
| 10 | `src/routes/Search.tsx`, `Results.tsx` | The form, and the check of the URL's values |
| 11 | `src/api/queries.ts` | `useTrainSearch` and `useSeats` |
| 11 | `src/routes/Results.tsx`, `SeatMap.tsx` | `TrainList`, and the seat grid with its coach buttons |
| 12 | `src/api/queries.ts` | `useBookSeat`: the optimistic update and the rollback |
| 12 | `src/routes/SeatMap.tsx`, `src/pnrs.ts` | The booking form and its messages, `loadPnrs` and `savePnr` |
| 13 | `src/api/queries.ts`, `src/routes/MyBookings.tsx` | `useBooking`, `useCancelBooking` and the booking cards |
| 14 | `vite.config.ts`, `src/index.css` | Switching Tailwind on, then the styles of every page |
| 15 | `tests/e2e/booking.spec.ts` | The date helper and both tests |

Task 7 is the concept check and task 16 is the wrap-up (`railseat/README.md` and `EXPLAIN.md`). Neither writes code, so neither has a TODO here.

## What you still write yourself

- Every route, page and form, and the whole seat map.
- `api()`, every hook in `queries.ts` (keys, `staleTime`, the optimistic update and the invalidations) and `pnrs.ts`.
- The schema, its unit tests and both Playwright tests.
- The CORS change in your API, `evidence.md`, `AI_LOG.md`, `railseat/README.md` and `EXPLAIN.md`.

Delete each TODO comment when you finish it. When none are left, you may delete this file.
