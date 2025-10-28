import Link from "next/link";

type Note = {
  id: string;
  title: string;
  preview: string;
  updatedAt: string;
};

const mockNotes: Note[] = [
  { id: "1", title: "Welcome to SwampNotes", preview: "A small starter note", updatedAt: new Date().toISOString() },
  { id: "2", title: "Second note", preview: "Insert OS cheat sheet here", updatedAt: new Date().toISOString() },
];

export default function NotesPage() {
  const notes = mockNotes;

  return (
    <main className="mx-auto max-w-3xl p-6 space-y-6">
      <header className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Notes</h1>

        {/* Temporary route - replace later */}
        <Link
          href="/notes/upload"
          className="rounded-xl border px-4 py-2 text-sm hover:bg-gray-50"
        >
          + Get notes
        </Link>
      </header>

      {notes.length === 0 ? (
        <section className="rounded-2xl border p-8 text-center">
          <h2 className="text-lg font-medium">No notes yet</h2>
          <p className="mt-2 text-sm text-gray-600">
            Click <span className="font-medium">Get notes</span> to get started!
          </p>
        </section>
      ) : (
        <ul className="grid gap-4">
          {notes.map((n) => (
            <li key={n.id} className="rounded-2xl border p-4 hover:bg-gray-50">
              <div className="flex items-center justify-between">
                <h3 className="text-base font-semibold">{n.title}</h3>
                <time className="text-xs text-gray-500">
                  {new Date(n.updatedAt).toLocaleString()}
                </time>
              </div>
              <p className="mt-1 text-sm text-gray-700 line-clamp-2">{n.preview}</p>

              <div className="mt-3">
                <Link href={`/notes/${n.id}`} className="text-sm underline">
                  Open
                </Link>
              </div>
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}