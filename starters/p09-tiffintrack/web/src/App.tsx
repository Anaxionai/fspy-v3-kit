import { LiveTable } from './LiveTable.tsx'

export default function App() {
  return (
    <main>
      <h1>TiffinTrack</h1>
      {/* TODO(task 17): show <RiderMap /> here, above the table. */}
      {/* TODO(task 18): when the address has ?order=<id>, show <OrderTracker /> instead. */}
      <LiveTable />
    </main>
  )
}
