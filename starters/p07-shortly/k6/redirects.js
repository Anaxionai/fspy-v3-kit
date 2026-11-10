// Load test for Shortly's redirects (task 20). You write the test itself.
//
// Run it from shortly/, on the stack's network, so k6 reaches the API at http://api:8080:
//   docker run --rm -i --network shortly_default grafana/k6 run - < k6/redirects.js
// Change the rate with -e after `run`, for example: ... grafana/k6 run -e RATE=500 - < k6/redirects.js
import http from "k6/http";
import { check } from "k6";

export const options = {
  // TODO(task 20): one constant-arrival-rate scenario, with the rate from __ENV.RATE
  //   (default 1000), timeUnit, duration, preAllocatedVUs and maxVUs from step 3.
  // TODO(task 20): do not follow redirects, so k6 times your 302 and never visits the target.
  // TODO(task 20): summaryTrendStats, so the summary shows the median, p(95) and p(99).
};

export default function () {
  // TODO(task 20): request http://api:8080/ plus a random seeded code (t000001 to t001000),
  //   then check() that the status is 302.
}
