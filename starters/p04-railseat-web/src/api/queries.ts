// TanStack Query hooks: every piece of server data the pages use.
// Each hook calls api() from ./client.ts. Write them with useQuery and
// useMutation from '@tanstack/react-query'.
import type { UseQueryResult } from '@tanstack/react-query'
import type { Booking, Seat, TrainResult } from './client'

// Trains from `from` to `to` on `date`: GET /trains/search.
export function useTrainSearch(from: string, to: string, date: string): UseQueryResult<TrainResult[]> {
  // TODO(task 11): useQuery with the key ['search', from, to, date] and a
  // queryFn that calls api(). Choose a staleTime and give your reason in a
  // comment next to it.
  throw new Error(`TODO(task 11): search the trains from ${from} to ${to} on ${date}`)
}

// Every seat of one journey: GET /journeys/{journeyId}/seats.
export function useSeats(journeyId: number): UseQueryResult<Seat[]> {
  // TODO(task 11): useQuery with the key ['seats', journeyId], where
  // journeyId is a number. Choose a staleTime and give your reason in a
  // comment next to it.
  throw new Error(`TODO(task 11): load the seats of journey ${journeyId}`)
}

// Book one seat on this journey: POST /bookings, shown at once (optimistic).
export function useBookSeat(journeyId: number) {
  // TODO(task 12): useMutation. Its mutationFn posts
  // { journey_id, seat_id, passenger: { name, age } } to /bookings with api().
  // - onMutate: cancel the ['seats', journeyId] queries, save the current
  //   seats, mark the chosen seat booked with setQueryData, return { previous }.
  // - onError: put `previous` back with setQueryData.
  // - onSettled: invalidate ['seats', journeyId].
  throw new Error(`TODO(task 12): book a seat on journey ${journeyId}`)
}

// One booking by its PNR: GET /bookings/{pnr}.
export function useBooking(pnr: string): UseQueryResult<Booking> {
  // TODO(task 13): useQuery with the key ['booking', pnr].
  throw new Error(`TODO(task 13): load booking ${pnr}`)
}

// Cancel a booking: DELETE /bookings/{pnr}. The API answers with the booking.
export function useCancelBooking() {
  // TODO(task 13): useMutation whose mutationFn sends DELETE /bookings/{pnr}
  // with api(). Give it no onSuccess at first: task 13 has you find the bug
  // that this causes, then fix it.
  throw new Error('TODO(task 13): cancel a booking')
}
