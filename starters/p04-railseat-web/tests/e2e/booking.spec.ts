import { test } from '@playwright/test'

// End-to-end tests of the whole booking flow (task 15).
// They need PostgreSQL, a seeded API on http://localhost:8000, and journeys
// in the next few days. Run them with: npx playwright test
// Find elements only with getByRole, getByLabel and getByText, and never use
// waitForTimeout. Change `test.skip` to `test` as you write each test.

// The date 3 days from today as YYYY-MM-DD, in local time.
function inThreeDays(): string {
  // TODO(task 15): compute the date. Never type a fixed date: it will pass.
  throw new Error('TODO(task 15): return the date 3 days from today')
}

test.skip('book and cancel', async () => {
  // TODO(task 15): with the `page` fixture, search NDLS to BCT on
  // inThreeDays(), open the first train's seats, pick the first free seat,
  // fill in a passenger and book. Expect a 10-character PNR. Then open My
  // bookings, accept the confirm dialog with
  // page.once('dialog', (d) => d.accept()), cancel, and expect "cancelled".
  throw new Error(`TODO(task 15): book and cancel on ${inThreeDays()}`)
})

test.skip('conflict rolls back', async () => {
  // TODO(task 15): with the `request` fixture and full http://localhost:8000
  // URLs, find a journey and a free seat. Open that seat map in the `page`.
  // After the page has loaded, book that seat with
  // request.post('http://localhost:8000/bookings', ...), then try the same
  // seat in the page. Expect the someone-else alert and no PNR.
  throw new Error(`TODO(task 15): book a seat through the API on ${inThreeDays()}, then in the page`)
})
