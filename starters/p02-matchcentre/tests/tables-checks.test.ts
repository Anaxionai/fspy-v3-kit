// Starter checks for BattingTable and BowlingTable. They draw each table as
// HTML text and look for what the rows prop holds.
// When you finish task 12, delete ".skip" from the group and run `npm test`.

import { createElement } from 'react'
import { renderToStaticMarkup } from 'react-dom/server'
import { describe, expect, it } from 'vitest'
import BattingTable from '../src/components/BattingTable'
import BowlingTable from '../src/components/BowlingTable'

// TODO(task 12): delete ".skip" on the next line when both tables work.
describe.skip('task 12: the tables draw their rows prop', () => {
  it('BattingTable has a caption, header cells and a row per batter', () => {
    const html = renderToStaticMarkup(
      createElement(BattingTable, {
        rows: [
          { name: 'A Kumar', runs: 45, balls: 30, fours: 4, sixes: 2 },
          { name: 'C Das', runs: 7, balls: 9, fours: 1, sixes: 0 },
        ],
      }),
    )
    expect(html).toContain('<caption')
    expect(html).toContain('<th')
    expect(html).toContain('A Kumar')
    expect(html).toContain('45')
    expect(html).toContain('C Das')
  })

  it('BowlingTable has a caption, header cells and a row per bowler', () => {
    const html = renderToStaticMarkup(
      createElement(BowlingTable, {
        rows: [{ name: 'D Rao', overs: '3.2', balls: 20, runs: 31, wickets: 2 }],
      }),
    )
    expect(html).toContain('<caption')
    expect(html).toContain('<th')
    expect(html).toContain('D Rao')
    expect(html).toContain('3.2')
    expect(html).toContain('31')
  })
})
