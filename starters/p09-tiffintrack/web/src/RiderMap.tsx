// The rider map (task 17). Leaflet 1.9.4 and its types are already in package.json.
// You will need: L from 'leaflet', the stylesheet 'leaflet/dist/leaflet.css',
// useEffect from 'react', WS_URL from './config.ts', and connectLive and isNewer from './live.ts'.
import type { ReactNode } from 'react'

/**
 * A Leaflet map of Pune, centred on 18.5204, 73.8567 at zoom 13, with OpenStreetMap tiles
 * and their attribution. Each rider is one circle marker that moves as points arrive.
 * Above the map: the connection status and the number of riders.
 * Every 10 seconds, log "markers on map: N" to the browser console.
 *
 * Edge cases: the map's div needs a fixed height (for example 80vh), or the map is grey;
 * React runs effects twice in development, so the clean-up must remove the map;
 * one marker per rider id; a late or repeated point never moves a marker.
 * TODO(task 17): write it, with your comment on the tile usage policy above the tile layer.
 */
export function RiderMap(): ReactNode {
  throw new Error('TODO(task 17): draw the riders on a Leaflet map')
}
