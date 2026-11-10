// The first page: where a passenger starts a search. Route: "/".
export default function Search() {
  // TODO(task 8): add a button that runs
  //   navigate('/results?from=NDLS&to=BCT&date=' + date)
  // with tomorrow's date, using useNavigate(). The real form comes in task 10.
  //
  // TODO(task 10): replace that button with a form: controlled, labelled
  // inputs for From, To and Date. On submit, call e.preventDefault() and
  // searchSchema.safeParse(...). Show each error under its own field, linked
  // with aria-describedby. If it passes, navigate to '/results?' plus
  // new URLSearchParams(result.data).
  return <h1>Search trains</h1>
}
