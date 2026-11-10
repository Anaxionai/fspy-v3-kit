import { describe, expect, it } from 'vitest'
import { parseMessage } from './messages.ts'

describe('parseMessage', () => {
  it('reads a point message', () => {
    const text =
      '{"type":"point","rider_id":7,"seq":12,"lat":18.52,"lng":73.85,"ts":"2026-11-10T10:00:00Z"}'
    expect(parseMessage(text)).toEqual({
      type: 'point',
      rider_id: 7,
      seq: 12,
      lat: 18.52,
      lng: 73.85,
      ts: '2026-11-10T10:00:00Z',
    })
  })

  it('gives null for text that is not JSON', () => {
    expect(parseMessage('hello')).toBeNull()
  })

  it('gives null for a message of an unknown type', () => {
    expect(parseMessage('{"type":"weather"}')).toBeNull()
  })
})
