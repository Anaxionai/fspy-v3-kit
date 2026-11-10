// Load-test one RailSeat endpoint with k6 (P10 add-on, task 8). Run it from railseat/:
//   k6 run -e URL="http://localhost:8000/trains/search?from=NDLS&to=BCT&date=2026-12-01" perf/endpoint.js
//   k6 run -e URL="http://localhost:8000/bookings" -e TOKEN="<token>" perf/endpoint.js
// Keep the URL in double quotes: an unquoted & splits the command in Git Bash.
import http from "k6/http";
import { check } from "k6";

// The same settings for every endpoint, so the numbers compare (step 3).
export const options = {
  vus: 10,
  duration: "20s",
  summaryTrendStats: ["avg", "p(50)", "p(95)", "max"],
};

export default function () {
  // TODO(task 8): GET __ENV.URL. When __ENV.TOKEN is set, send the header
  // `Authorization: Bearer <token>`. Then check() that the status is 200, so a
  // failing endpoint can never look fast.
  throw new Error("TODO(task 8): request __ENV.URL with the optional token");
}
