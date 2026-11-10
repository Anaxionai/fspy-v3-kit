// The bookings made in this browser. Route: "/bookings".
export default function MyBookings() {
  // TODO(task 13): read the PNRs with loadPnrs(), and show a BookingCard for
  // each: PNR, train, date, coach, seat and status, from useBooking(pnr).
  // - Confirmed bookings get a Cancel button. Ask first with window.confirm,
  //   and disable the button while the request runs (useCancelBooking()).
  // - Show "No bookings yet" with a link to Search when the list is empty,
  //   and a message when a PNR is not found.
  return <h1>My bookings</h1>
}
