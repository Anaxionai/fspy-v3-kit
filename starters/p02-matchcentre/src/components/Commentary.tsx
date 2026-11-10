import type { MatchState } from '../types'

interface CommentaryProps {
  match: MatchState
}

/** The Commentary section: the latest 12 balls, newest first. */
export default function Commentary({ match }: CommentaryProps) {
  // TODO(task 12): an ordered list of the latest 12 balls, newest first, with
  //   the text from describeBall in score.ts. Give each item a key that never
  //   changes, such as the ball's position in its innings: its place in your
  //   list of 12 changes with every new ball.
  throw new Error('TODO(task 12): write Commentary')
}
