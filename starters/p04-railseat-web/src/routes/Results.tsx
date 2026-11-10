// The trains for one search. Route: "/results?from=NDLS&to=BCT&date=2026-12-01".
export default function Results() {
  // TODO(task 8): read from, to and date with useSearchParams(), and show them
  // in the heading, such as "NDLS to BCT on 2026-12-01". Add a <Link> to
  // /journeys/1/seats.
  //
  // TODO(task 9): call api<TrainResult[]>() for /trains/search with the URL's
  // from, to and date in a useEffect, and log the result to the console.
  //
  // TODO(task 10): check the URL's values with searchSchema. If they fail,
  // show the problem and a link back to Search instead of calling the API.
  //
  // TODO(task 11): replace the useEffect with a TrainList component that calls
  // useTrainSearch(). Show loading, error and "No trains on this date" states,
  // and link each train to /journeys/{journey_id}/seats.
  return <h1>Results</h1>
}
