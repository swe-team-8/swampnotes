import Link from "next/link";

type Note = {
  id: string;
  title: string;
  preview: string;
  author: string;
  semester: string;
  color: string;
};

const mockNotes: Note[] = [
  { id: "1", title: "Welcome to SwampNotes", preview: "A small starter note", author: "SwampNotes team", semester: "spring'25", color: "bg-blue-400" },
  { id: "2", title: "COP3502C", preview: "Insert OS cheat sheet here",author: "Santi", semester: "Fall'24",color: "bg-orange-400"},
];

export default function NotesPage(){
    const notes = mockNotes; 

    return(
        <main className="mx-auto max-w-4xl p-8 space-y-8">
            <header className="flex items-center justify-between">
                <h1 className="text-5XL font-bold text-blue-700">Library</h1>
                <Link 
                    href="/notes/upload"
                    className="rounded-lg border border-blue-300 bg-blue-50 px-4 py-2 text-sm font-medium text-blue-700 hover:bg-blue-100 transition"
                >
                    + Get notes!
                </Link>
            </header>

            {notes.length === 0 ? (
                <section className="rounded-2xl border p-8 text-center bg-white/50">
                    <h2 className="text-lg font-medium">No notes yet</h2>
                    <p className="mt-2 text-sm text-gray-600">
                        Click <span className="font-medium">Get notes</span> to get started!
                    </p>
                </section>
            ) : (
                <ul className="space-y-3">
                    {notes.map((n) => (
                        <li 
                            key={n.id}
                            className={`flex items-center justify-between rounded-xl border border-gray-200 px-6 py-4 shadow-sm hover:shadow-md hover:brightness-95 transition-all ${n.color}`}
                        >
                            <div className="flex items-center gap-4 w-1/3">
                                <span className="text-xl" role="img" aria-label="notebook">
                                    📒
                                </span>
                                <Link  
                                    href={`/notes/${n.id}`}
                                    className="text-base font-semibold text-gray-800 hover:underline"
                                >
                                    {n.title}
                                </Link> 
                            </div>

                            <p className="text-sm text-gray-800 italic pl-45 w-1/4">
                                By: {n.author}
                            </p>

                            <p className="text-sm text-gray-700 text-right w-1/3">
                                {n.semester}
                            </p>
                        </li>
        
                    ))} 
                </ul>   
             )}
        </main>
    ); 
}