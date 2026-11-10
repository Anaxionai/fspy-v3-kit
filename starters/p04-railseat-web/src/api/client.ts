// The RailSeat API from P3. Start it in railseat/api/ with:
//   uv run fastapi dev app/main.py
export const BASE_URL = 'http://localhost:8000'

// An answer from the API that is not 2xx, with its HTTP status (404, 409, 422 ...).
export class ApiError extends Error {
  status: number

  constructor(status: number, message: string) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

// The API's JSON, with the same field names as its Pydantic models in
// railseat/api/app/schemas.py. If you changed a type there, change it here.

// One journey in the search results (TrainResult).
export type TrainResult = {
  journey_id: number
  train_number: string
  train_name: string
  departs: string // date and time as text, such as "2026-12-01T16:30:00"
  arrives: string
  free_seats: number
}

// One seat of a journey (SeatOut).
export type Seat = {
  seat_id: number
  coach: string // such as "B1"
  travel_class: string // "1A", "2A", "3A", "SL" or "CC"
  number: number
  booked: boolean
}

// One booking (BookingOut).
export type Booking = {
  pnr: string
  status: string // "confirmed" or "cancelled"
  journey_id: number
  travel_date: string // "2026-12-01"
  train_number: string
  train_name: string
  coach: string
  seat_number: number
  passenger_name: string
}

// The body of POST /bookings (BookingIn).
export type BookingIn = {
  journey_id: number
  seat_id: number
  passenger: { name: string; age: number }
}

// Call the API and return its JSON as type T, for example:
//   const trains = await api<TrainResult[]>('/trains/search?from=NDLS&to=BCT&date=2026-12-01')
export async function api<T>(path: string, init?: RequestInit): Promise<T> {
  // TODO(task 9): fetch BASE_URL + path with init.
  // - If the response is not ok, throw new ApiError(res.status, ...) with the
  //   API's `detail` as the message.
  // - Otherwise return await res.json().
  // - When init has a body, send the header 'Content-Type: application/json'.
  throw new Error(`TODO(task 9): fetch ${BASE_URL}${path} (${init?.method ?? 'GET'})`)
}
