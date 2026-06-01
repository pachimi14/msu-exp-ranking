export function Input({ className = "", ...props }) {
  return (
    <input
      className={`rounded-lg border px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-blue-500 ${className}`}
      {...props}
    />
  );
}
