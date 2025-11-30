"use client";

import Link from "next/link";
import { useState } from "react";

type Note = {
  id: string;
  title: string;
  preview: string;
  author: string;
  semester: string;
  color: string;
};

const mockSavedNotes: Note[] = [
  { id: "1", title: "Welcome to SwampNotes", preview: "A small starter note", author: "SwampNotes team", semester: "spring'25", color: "bg-blue-400" },
  { id: "2", title: "COP3502C", preview: "Insert OS cheat sheet here",author: "Santi", semester: "Fall'24",color: "bg-orange-400"},
];

const mockUploadedNotes: Note[] = [
    { id: "3", title: "Data Structures", preview: "Notes on data structures", author: "Alex", semester: "Spring'24", color: "bg-green-400" },
    { id: "4", title: "Calculus II", preview: "Integration techniques and applications", author: "Jamie", semester: "Fall'23", color: "bg-purple-400" },
]
type TabKey = "library" | "uploaded";

export default function NotesPage(){

    const [activeTab, setActiveTab] = useState<TabKey>("library");

    const notes = activeTab === "library" ? mockSavedNotes : mockUploadedNotes;

    return(
        <main className="mx-auto max-w-5xl p-8 space-y-8">
            <header className="flex items-center justify-between">
                <h1 className="text-5XL font-bold text-blue-700">Notes</h1>
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
                    
            {notes.length === 0 ? (
                <section className="rounded-2xl border p-8 text-center bg-white/50">
                    <h2 className="text-lg font-medium">
                        {activeTab === "library" ? "No saved notes yet" : "No uploads yet"}
                    </h2>
                    <p className="mt-2 text-sm text-gray-600">
                        {activeTab === "library" ? (
                        <>
                            Save notes to your <span className="font-medium">Library</span>{" "}
                            to see them here.
                        </>
                        ) : (
                        <>
                            Click <span className="font-medium">Upload notes</span> to share
                            your notes with others.
                        </>
                        )}    
                    </p>
                </section>
            ):(
                <section>
                    <h2 className="mb-4 text-sm font-medium uppercase tracking-wide text-gray-500">
                        {activeTab === "library" ? "Saved notes" : "Your uploads"}
                    </h2>

                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                        {notes.map((n) => (
                        <Link
                            key={n.id}
                            href={`/notes/${n.id}`}
                            className="group rounded-2xl border border-gray-200 bg-white shadow-sm hover:shadow-md hover:-translate-y-1 transition-all overflow-hidden"
                        >
                            <div className={`${n.color} h-2 w-full`} />

                            <div className="p-4 flex flex-col gap-2 h-full">
                            <div className="flex items-start justify-between gap-2">
                                <div className="flex items-center gap-2">
                                <span
                                    className="text-2xl"
                                    role="img"
                                    aria-label="notebook"
                                >
                                    📒
                                </span>
                                <h3 className="text-base font-semibold text-gray-900 group-hover:text-blue-700 line-clamp-2">
                                    {n.title}
                                </h3>
                                </div>
                                <span className="rounded-full bg-gray-100 px-2 py-0.5 text-xs text-gray-600 whitespace-nowrap">
                                {n.semester}
                                </span>
                            </div>

                            <p className="text-xs text-gray-500">
                                By <span className="font-medium">{n.author}</span>
                            </p>

                            <p className="mt-1 text-sm text-gray-700 line-clamp-3">
                                {n.preview}
                            </p>
                            </div>
                        </Link>
                        ))}
                    </div>
                </section>
            )}
        </main>
    ); 
}