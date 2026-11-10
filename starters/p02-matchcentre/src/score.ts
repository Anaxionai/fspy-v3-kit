// All of Match Centre's cricket maths, worked out from the balls of an innings.
// The feed has no totals: every number on the page comes from these functions.
// Cricket rules matter less than the types and the data flow: close figures
// are fine.

import type { Ball, BattingRow, BowlingRow, Innings, RunRatePoint } from './types'

/** All the runs of an innings, extras included. An innings with no balls has 0. */
export function inningsRuns(innings: Innings): number {
  throw new Error('TODO(task 11): write inningsRuns')
}

/** How many wickets have fallen in an innings. An innings with no balls has 0. */
export function inningsWickets(innings: Innings): number {
  throw new Error('TODO(task 11): write inningsWickets')
}

/**
 * The overs bowled so far, as text such as "15.2": 15 overs and 2 balls.
 * Wides and no-balls are not among the six balls of an over.
 */
export function oversText(innings: Innings): string {
  throw new Error('TODO(task 11): write oversText')
}

/**
 * One BattingRow per batter who has faced a ball: runs off the bat, balls
 * faced, fours and sixes. Group the balls by batter, as you grouped spending
 * by merchant in P1.
 */
export function battingCard(innings: Innings): BattingRow[] {
  throw new Error('TODO(task 12): write battingCard')
}

/** One BowlingRow per bowler: overs, legal balls, runs given away and wickets. */
export function bowlingCard(innings: Innings): BowlingRow[] {
  throw new Error('TODO(task 12): write bowlingCard')
}

/** One line of commentary for a ball, such as "15.2 Bumrah to Kohli, FOUR". */
export function describeBall(ball: Ball): string {
  throw new Error('TODO(task 12): write describeBall')
}

/**
 * One point per completed over: the over number (1, 2, 3 and on) and the run
 * rate so far, which is the runs divided by the overs, to 2 decimal places.
 * An innings with no completed over gives an empty list.
 */
export function runRateByOver(innings: Innings): RunRatePoint[] {
  throw new Error('TODO(task 14): write runRateByOver')
}
