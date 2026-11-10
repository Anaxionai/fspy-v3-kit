// Every seat of one journey, coach by coach. Route: "/journeys/:journeyId/seats".
export default function SeatMap() {
  // TODO(task 8): read journeyId from the path with useParams(), and show it.
  //
  // TODO(task 11): call useSeats(Number(journeyId)). Show loading and error
  // states. Group the seats by coach, with one button per coach ("Coach B1"),
  // and keep the open coach in useState. Draw the open coach's seats as a CSS
  // grid of <button>s: 4 per row on a phone, 8 from 640 pixels.
  // - Booked seats are disabled and grey.
  // - Clicking a free seat selects it: keep its seat_id (not its position) in
  //   useState, and show "Coach B1, seat 12 selected".
  // - Each seat gets an aria-label such as "B1 seat 12, free", and
  //   aria-pressed when it is selected.
  //
  // TODO(task 12): under the map, add a form with a labelled Name (required,
  // minLength 2), Age (number, 1 to 120) and a Book button that calls
  // useBookSeat(). Disable Book while the booking is pending.
  // - On success, show the PNR, train, coach and seat, and call savePnr().
  // - On an ApiError with status 409, clear the selection and show "Sorry,
  //   someone else booked B1 seat 12 first. Please pick another seat."
  // - On any other error, show "Booking failed. Please try again."
  // - Show both messages in an element with role="alert".
  return <h1>Seat map</h1>
}
