import Search from './routes/Search.tsx'

// The app's frame: a header on every page, and one route per page.
// main.tsx already wraps <App /> in <BrowserRouter>.
export default function App() {
  // TODO(task 8):
  // - Add a header with a <NavLink> to Search ("/") and one to My bookings
  //   ("/bookings"), so the current page is marked.
  // - Declare the routes with <Routes> and <Route>: "/" (Search), "/results"
  //   (Results), "/journeys/:journeyId/seats" (SeatMap), "/bookings"
  //   (MyBookings) and "*" (NotFound).
  // Until then, the app shows only the Search page.
  return (
    <main>
      <Search />
    </main>
  )
}
