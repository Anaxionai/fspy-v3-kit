// Types for Match Centre.
//
// The first four describe the replay server's JSON. They are empty in the
// starter, because writing them from the real feed is task 11. Start the
// replay server, then read `curl http://localhost:8765/live` and
// `curl http://localhost:8765/meta` field by field before you write a type.
// The feed sends the facts of each ball only: Match Centre works out every
// total itself, in score.ts.

/** One ball of the /live feed. */
export interface Ball {
  // TODO(task 11): one property per field of a ball, spelt as in the JSON.
  //   A field that only some balls have is optional (?). A field that holds
  //   an object gets an interface of its own.
}

/** One innings of the /live feed, as the JSON groups it. */
export interface Innings {
  // TODO(task 11): one property per field of an innings, spelt as in the JSON.
}

/** The whole answer of GET /live. */
export interface MatchState {
  // TODO(task 11): one property per field of the /live answer.
  //   Then save a real answer as src/live-sample.json and type it in
  //   src/sample.ts (steps 5 and 6): `npx tsc -b` proves your types match.
}

/** The answer of GET /meta: the teams, the venue and more. */
export interface MatchMeta {
  // TODO(task 11): the /meta fields you use, at least the teams and the venue,
  //   spelt as in the JSON.
}

/** One batter's line in the batting table, made by battingCard. */
export interface BattingRow {
  name: string
  runs: number
  /** Balls faced. A wide is not a ball faced. */
  balls: number
  fours: number
  sixes: number
}

/** One bowler's line in the bowling table, made by bowlingCard. */
export interface BowlingRow {
  name: string
  /** Overs bowled as text, such as "3.2": 3 overs and 2 balls. */
  overs: string
  /** Legal balls bowled (wides and no-balls do not count), for the economy rate. */
  balls: number
  /** Runs given away by the bowler. */
  runs: number
  wickets: number
}

/** One point of the run-rate chart: the run rate after a completed over. */
export interface RunRatePoint {
  over: number
  runRate: number
}
