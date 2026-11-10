// The PNRs booked in this browser, kept in localStorage under the key
// "railseat.pnrs" as a JSON list. My bookings (task 13) shows them.
// P5 replaces this list with GET /bookings.

// Return the saved PNRs, or [] when nothing is saved yet.
export function loadPnrs(): string[] {
  // TODO(task 12): read and parse the list saved under "railseat.pnrs".
  throw new Error('TODO(task 12): load the saved PNRs')
}

// Add one PNR to the saved list.
export function savePnr(pnr: string): void {
  // TODO(task 12): load the list, add pnr, and save the list again.
  throw new Error(`TODO(task 12): save PNR ${pnr}`)
}
