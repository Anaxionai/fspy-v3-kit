// Starter checks for src/api.ts. They replace the browser's fetch with a
// pretend server, so the replay server does not need to run.
// When you finish task 13, delete ".skip" from the group and run `npm test`.

import { afterEach, describe, expect, it, vi } from 'vitest'
import { fetchLive, fetchMeta } from '../src/api'

/** A pretend fetch that always gives this status and JSON body. */
function pretendServer(status: number, body: unknown) {
  return vi.fn(
    async (_url: string | URL | Request, _options?: RequestInit) =>
      new Response(JSON.stringify(body), {
        status,
        headers: { 'Content-Type': 'application/json' },
      }),
  )
}

afterEach(() => {
  vi.unstubAllGlobals()
})

// TODO(task 13): delete ".skip" on the next line when fetchLive and fetchMeta work.
describe.skip('task 13: reading the replay feed', () => {
  it('fetchLive asks for /live and gives back its JSON', async () => {
    const live = { match_id: '1', status: 'not started', innings: [] }
    const fetch = pretendServer(200, live)
    vi.stubGlobal('fetch', fetch)
    await expect(fetchLive()).resolves.toEqual(live)
    expect(String(fetch.mock.calls[0][0])).toBe('http://localhost:8765/live')
  })

  it('fetchLive throws when the answer is not ok', async () => {
    const fetch = pretendServer(500, { error: 'down' })
    vi.stubGlobal('fetch', fetch)
    await expect(fetchLive()).rejects.toThrow()
    expect(fetch).toHaveBeenCalled()
  })

  it('fetchMeta asks for /meta and gives back its JSON', async () => {
    const meta = { teams: ['Pune Panthers', 'Goa Gulls'], venue: 'Ground One' }
    const fetch = pretendServer(200, meta)
    vi.stubGlobal('fetch', fetch)
    await expect(fetchMeta()).resolves.toEqual(meta)
    expect(String(fetch.mock.calls[0][0])).toBe('http://localhost:8765/meta')
  })

  it('fetchMeta throws when the answer is not ok', async () => {
    const fetch = pretendServer(404, { error: 'no page' })
    vi.stubGlobal('fetch', fetch)
    await expect(fetchMeta()).rejects.toThrow()
    expect(fetch).toHaveBeenCalled()
  })
})
