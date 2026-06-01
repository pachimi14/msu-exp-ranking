export function Button({ className = "", variant = "default", children, ...props }) {
  const base =
    variant === "outline"
      ? "border border-slate-700 bg-slate-950 text-slate-100 hover:bg-slate-800"
      : "bg-blue-600 text-white hover:bg-blue-500";
  return (
    <button
      type="button"
      className={`rounded-lg px-3 py-2 text-sm font-medium transition ${base} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}
