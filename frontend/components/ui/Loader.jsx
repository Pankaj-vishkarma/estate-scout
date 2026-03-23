export default function Loader({ label = "Loading..." }) {
  return (
    <div className="flex items-center gap-3 text-slate-200">
      <div
        className="h-5 w-5 animate-spin rounded-full border-2 border-white/20 border-t-sky-300"
        aria-hidden="true"
      />
      <span className="text-sm">{label}</span>
    </div>
  );
}

