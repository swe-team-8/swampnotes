export default function LoadingNotes() {
  return (
    <main className="mx-auto max-w-3xl p-6 space-y-6">
      <div className="h-7 w-40 animate-pulse rounded bg-gray-200" />
      <div className="space-y-3">
        {[0, 1, 2].map((i) => (
          <div key={i} className="rounded-2xl border p-4">
            <div className="flex items-center justify-between">
              <div className="h-5 w-48 animate-pulse rounded bg-gray-200" />
              <div className="h-4 w-24 animate-pulse rounded bg-gray-200" />
            </div>
            <div className="mt-2 h-4 w-full animate-pulse rounded bg-gray-200" />
            <div className="mt-2 h-4 w-2/3 animate-pulse rounded bg-gray-200" />
          </div>
        ))}
      </div>
    </main>
  );
}