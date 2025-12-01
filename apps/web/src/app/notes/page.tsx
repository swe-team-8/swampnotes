"use client";

import Link from "next/link";
import { useState, useEffect } from "react";
import { notesApi, type Note } from "@/lib/api";
import { useAuth } from "@clerk/nextjs";

type TabKey = "library" | "uploaded";

export default function NotesPage() {
  const { getToken } = useAuth();
  const [activeTab, setActiveTab] = useState<TabKey>("library");
  const [notes, setNotes] = useState<Note[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchNotes() {
      setLoading(true);
      try {
        const token = await getToken({ template: "fastapi" });
        if (!token) return;

        const data =
          activeTab === "library"
            ? await notesApi.getLibrary(token)
            : await notesApi.getUploaded(token);
        setNotes(data);
      } catch (error) {
        console.error("Failed to fetch notes:", error);
      } finally {
        setLoading(false);
      }
    }

    fetchNotes();
  }, [activeTab, getToken]);

  const getColorForNote = (index: number) => {
    const colors = [
      "bg-blue-400",
      "bg-orange-400",
      "bg-green-400",
      "bg-purple-400",
    ];
    return colors[index % colors.length];
  };

  return (
    <main className="mx-auto max-w-5xl p-8 space-y-8">
      <header className="flex items-center justify-between">
        <h1 className="text-5xl font-bold text-blue-700">Notes</h1>
        <Link
          href={activeTab === "library" ? "/notes/discover" : "/notes/upload"}
          className="rounded-lg border border-blue-300 bg-blue-50 px-4 py-2 text-sm font-medium text-blue-700 hover:bg-blue-100 transition"
        >
          {activeTab === "library" ? "+ Get notes!" : "+ Upload notes"}
        </Link>
      </header>

      <div className="border-b border-gray-200">
        <nav className="flex space-x-4" aria-label="Tabs">
          <button
            type="button"
            onClick={() => setActiveTab("library")}
            className={`px-3 py-2 font-medium text-sm rounded-t-lg ${
              activeTab === "library"
                ? "border-b-2 border-blue-500 text-blue-600"
                : "text-gray-500 hover:text-gray-700"
            }`}
          >
            Library
          </button>
          <button
            type="button"
            onClick={() => setActiveTab("uploaded")}
            className={`px-3 py-2 font-medium text-sm rounded-t-lg ${
              activeTab === "uploaded"
                ? "border-b-2 border-blue-500 text-blue-600"
                : "text-gray-500 hover:text-gray-700"
            }`}
          >
            Uploaded
          </button>
        </nav>
      </div>

      {loading ? (
        <div className="text-center py-12">
          <p className="text-gray-500">Loading notes...</p>
        </div>
      ) : notes.length === 0 ? (
        <section className="rounded-2xl border p-8 text-center bg-white/50">
          <h2 className="text-lg font-medium">
            {activeTab === "library" ? "No saved notes yet" : "No uploads yet"}
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            {activeTab === "library" ? (
              <>
                Purchase notes from the{" "}
                <Link
                  href="/notes/discover"
                  className="text-blue-600 underline"
                >
                  directory
                </Link>{" "}
                to see them here.
              </>
            ) : (
              <>
                Click{" "}
                <Link
                  href="/notes/upload"
                  className="text-blue-600 underline"
                >
                  Upload notes
                </Link>{" "}
                to share your notes with others.
              </>
            )}
          </p>
        </section>
      ) : (
        <section>
          <h2 className="mb-4 text-sm font-medium uppercase tracking-wide text-gray-500">
            {activeTab === "library" ? "Saved notes" : "Your uploads"}
          </h2>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {notes.map((note, idx) => (
              <Link
                key={note.id}
                href={`/notes/${note.id}`}
                className="group rounded-2xl border border-gray-200 bg-white shadow-sm hover:shadow-md hover:-translate-y-1 transition-all overflow-hidden"
              >
                <div className={`${getColorForNote(idx)} h-2 w-full`} />

                <div className="p-4 flex flex-col gap-2 h-full">
                  <div className="flex items-start justify-between gap-2">
                    <div className="flex items-center gap-2">
                      <span className="text-2xl" role="img" aria-label="notebook">
                        📒
                      </span>
                      <h3 className="text-base font-semibold text-gray-900 group-hover:text-blue-700 line-clamp-2">
                        {note.title}
                      </h3>
                    </div>
                    <span className="rounded-full bg-gray-100 px-2 py-0.5 text-xs text-gray-600 whitespace-nowrap">
                      {note.semester}
                    </span>
                  </div>

                  <p className="text-xs text-gray-500">
                    Course:{" "}
                    <span className="font-medium">{note.course_name}</span>
                  </p>

                  <p className="mt-1 text-sm text-gray-700 line-clamp-3">
                    {note.description || "No description provided"}
                  </p>

                  {!note.is_free && (
                    <p className="text-xs text-blue-600 font-medium mt-auto">
                      {note.price} points
                    </p>
                  )}
                </div>
              </Link>
            ))}
          </div>
        </section>
      )}
    </main>
  );
}