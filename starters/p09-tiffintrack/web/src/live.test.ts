import { describe, expect, it } from 'vitest'
import { isNewer, retryDelayMs } from './live.ts'
import type { PointMessage } from './messages.ts'

const point = (rider_id: number, seq: number): PointMessage => ({
  type: 'point',
  rider_id,
  seq,
  lat: 18.52,
  lng: 73.85,
  ts: '2026-11-10T10:00:00Z',
})

// TODO(task 9): change describe.skip to describe when retryDelayMs is written.
describe.skip('retryDelayMs', () => {
  it('waits about 1 s before the first retry', () => {
    const ms = retryDelayMs(0)
    expect(ms).toBeGreaterThanOrEqual(1000)
    expect(ms).toBeLessThanOrEqual(1500)
  })

  it('waits twice as long each time', () => {
    const ms = retryDelayMs(2)
    expect(ms).toBeGreaterThanOrEqual(4000)
    expect(ms).toBeLessThanOrEqual(4500)
  })

  it('never waits more than 30 s, plus the jitter', () => {
    const ms = retryDelayMs(20)
    expect(ms).toBeGreaterThanOrEqual(30000)
    expect(ms).toBeLessThanOrEqual(30500)
  })
})

// TODO(task 9): change describe.skip to describe when isNewer is written.
describe.skip('isNewer', () => {
  it("accepts a rider's first point", () => {
    expect(isNewer(new Map(), point(7, 100))).toBe(true)
  })

  it('drops a repeated point and an older one', () => {
    const lastSeq = new Map<number, number>()
    expect(isNewer(lastSeq, point(7, 100))).toBe(true)
    expect(isNewer(lastSeq, point(7, 100))).toBe(false)
    expect(isNewer(lastSeq, point(7, 99))).toBe(false)
    expect(isNewer(lastSeq, point(7, 101))).toBe(true)
  })

  it('keeps each rider apart', () => {
    const lastSeq = new Map<number, number>()
    expect(isNewer(lastSeq, point(7, 100))).toBe(true)
    expect(isNewer(lastSeq, point(8, 50))).toBe(true)
  })
})
