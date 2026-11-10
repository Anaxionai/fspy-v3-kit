import type { RunRatePoint } from '../types'

interface RunRateChartProps {
  points: RunRatePoint[]
}

/** The run-rate chart: one point per completed over, from runRateByOver. */
export default function RunRateChart({ points }: RunRateChartProps) {
  // TODO(task 14): first run `npm install recharts` in matchcentre/. Then draw
  //   a line chart of `points` that fits a phone, does not replay its
  //   animation on every update, has labelled axes, and has a sentence under
  //   it that gives the latest run rate.
  throw new Error('TODO(task 14): write RunRateChart')
}
