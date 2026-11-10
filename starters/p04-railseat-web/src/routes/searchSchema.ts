import { z } from 'zod'

// One schema for the search form (Search.tsx) and the URL (Results.tsx).
// TODO(task 10): replace these plain strings with the rules of task 10:
// - from and to are trimmed, uppercased, and must match ^[A-Z]{2,5}$;
// - date is YYYY-MM-DD and not before today;
// - a refine() so that from and to differ, with path: ['to'].
// Give every rule a message a passenger understands.
export const searchSchema = z.object({
  from: z.string(),
  to: z.string(),
  date: z.string(),
})

export type SearchValues = z.infer<typeof searchSchema>
