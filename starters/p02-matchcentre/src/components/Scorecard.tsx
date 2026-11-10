import type { MatchState } from '../types'

interface ScorecardProps {
  match: MatchState
}

/**
 * The Scorecard section: one button per innings, and the batting and bowling
 * tables of the innings that is chosen.
 */
export default function Scorecard({ match }: ScorecardProps) {
  // TODO(task 12): remember which innings is chosen, where nothing chosen
  //   means "the latest innings". Each innings button switches both tables
  //   and shows whether it is pressed (aria-pressed). Make the rows with
  //   battingCard and bowlingCard from score.ts.
  throw new Error('TODO(task 12): write Scorecard')
}
