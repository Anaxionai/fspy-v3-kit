// Money for people to read (P6 add-on). The API sends whole paise; only the
// screen shows rupees: formatPaise(90000) gives "₹900.00".
export function formatPaise(paise: number): string {
  void paise; // only quiets TypeScript until you use the name; delete this line
  throw new Error('TODO(task 9): format with Intl.NumberFormat("en-IN", { style: "currency", currency: "INR" })');
}
