// Starter checks for the parts of src/score.ts that no task asks you to test.
// (inningsRuns, inningsWickets and oversText are yours to test, in
// src/score.test.ts, in task 11.) Each group is skipped until its task.
// When you finish that task, delete ".skip" from the group and run `npm test`.
// They check results only, and only figures that every fair way of counting
// agrees on.

import { describe, expect, it } from 'vitest'
import { battingCard, bowlingCard, describeBall, runRateByOver } from '../src/score'

// A made-up innings in the format of the kit's replay feed: 2 overs and
// 2 balls, with one wide and one wicket.
const play = (over: number, ball: number, batter: string, bowler: string, runs: number) => ({
  over,
  ball,
  batter,
  non_striker: batter === 'A Kumar' ? 'C Das' : 'A Kumar',
  bowler,
  runs: { batter: runs, extras: 0, total: runs },
})

const innings = {
  number: 1,
  team: 'Pune Panthers',
  balls: [
    play(0, 1, 'A Kumar', 'D Rao', 4),
    play(0, 2, 'A Kumar', 'D Rao', 1),
    {
      over: 0,
      ball: 3,
      batter: 'B Singh',
      non_striker: 'A Kumar',
      bowler: 'D Rao',
      runs: { batter: 0, extras: 1, total: 1 },
      extras: { wides: 1 },
    },
    {
      over: 0,
      ball: 3,
      batter: 'B Singh',
      non_striker: 'A Kumar',
      bowler: 'D Rao',
      runs: { batter: 0, extras: 0, total: 0 },
      wicket: { player_out: 'B Singh', kind: 'bowled' },
    },
    play(0, 4, 'C Das', 'D Rao', 6),
    play(0, 5, 'C Das', 'D Rao', 0),
    play(0, 6, 'C Das', 'D Rao', 2),
    play(1, 1, 'A Kumar', 'E Iyer', 1),
    play(1, 2, 'C Das', 'E Iyer', 0),
    play(1, 3, 'C Das', 'E Iyer', 0),
    play(1, 4, 'C Das', 'E Iyer', 4),
    play(1, 5, 'C Das', 'E Iyer', 0),
    play(1, 6, 'C Das', 'E Iyer', 1),
    play(2, 1, 'C Das', 'D Rao', 0),
    play(2, 2, 'C Das', 'D Rao', 1),
  ],
}

const notStarted = { number: 1, team: 'Pune Panthers', balls: [] }

// TODO(task 12): delete ".skip" on the next line when these three functions work.
describe.skip('task 12: batting, bowling and commentary', () => {
  it('battingCard has one row per batter, with runs off the bat', () => {
    const rows = battingCard(innings)
    expect(rows.map((row) => row.name).sort()).toEqual(['A Kumar', 'B Singh', 'C Das'])
    const kumar = rows.find((row) => row.name === 'A Kumar')
    const das = rows.find((row) => row.name === 'C Das')
    expect(kumar).toMatchObject({ runs: 6, balls: 3, fours: 1, sixes: 0 })
    expect(das).toMatchObject({ runs: 14, balls: 10, fours: 1, sixes: 1 })
  })

  it('bowlingCard has one row per bowler', () => {
    const rows = bowlingCard(innings)
    expect(rows.map((row) => row.name).sort()).toEqual(['D Rao', 'E Iyer'])
    expect(rows.find((row) => row.name === 'D Rao')).toMatchObject({ wickets: 1 })
    expect(rows.find((row) => row.name === 'E Iyer')).toMatchObject({ balls: 6, runs: 6, wickets: 0 })
  })

  it('describeBall names the bowler and the batter', () => {
    const text = describeBall(innings.balls[0])
    expect(text).toContain('D Rao')
    expect(text).toContain('A Kumar')
  })
})

// TODO(task 14): delete ".skip" on the next line when runRateByOver works.
describe.skip('task 14: the run rate', () => {
  it('runRateByOver gives one point per completed over', () => {
    const points = runRateByOver(innings)
    expect(points.map((point) => point.over)).toEqual([1, 2])
    for (const point of points) {
      expect(Number.isFinite(point.runRate)).toBe(true)
    }
    expect(runRateByOver(notStarted)).toEqual([])
  })
})
