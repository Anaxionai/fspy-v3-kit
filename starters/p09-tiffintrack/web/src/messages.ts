// The messages the WebSocket server sends, as JSON text.

export type OrderStatus = 'placed' | 'picked_up' | 'nearby' | 'delivered'

/** One GPS point, from the Redis channel rider:{id} (task 8). */
export type PointMessage = {
  type: 'point'
  rider_id: number
  seq: number
  lat: number
  lng: number
  ts: string // the time the phone took the point, in UTC
}

/** One step of an order's timeline. */
export type TimelineEntry = { status: OrderStatus; at: string }

/** A status change, from the Redis channel order:{id} (task 18). */
export type StatusMessage = { type: 'status'; status: OrderStatus; at: string }

/** Sent once by /ws/orders/{id}, right after it subscribes (task 18). */
export type SnapshotMessage = {
  type: 'snapshot'
  timeline: TimelineEntry[]
  rider: PointMessage | null
}

export type LiveMessage = PointMessage | StatusMessage | SnapshotMessage

/** Turn the text of one WebSocket message into a LiveMessage, or null if it is not one. */
export function parseMessage(text: string): LiveMessage | null {
  let data: unknown
  try {
    data = JSON.parse(text)
  } catch {
    return null
  }
  if (typeof data !== 'object' || data === null) return null
  const type = (data as { type?: unknown }).type
  if (type === 'point' || type === 'status' || type === 'snapshot') {
    return data as LiveMessage
  }
  return null
}
