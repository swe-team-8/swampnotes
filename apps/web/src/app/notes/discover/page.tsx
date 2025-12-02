"use client";

import { useState, useEffect } from "react";
import { notesApi, coursesApi, type Note, type Course } from "@/lib/api";
import { useAuth } from "@clerk/nextjs";
import Link from "next/link";

export default function DiscoverNotesPage() {
  const { getToken } = useAuth();
  const [notes, setNotes] = useState<Note[]>([]);
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCourse, setSelectedCourse] = useState<number | null>(null);
  const [selectedSemester, setSelectedSemester] = useState("");

  const getColorForNote = (index: number) => {
    const colors = [
      "bg-blue-400",
      "bg-orange-400",
      "bg-green-400",
      "bg-purple-400",
    ];
    return colors[index % colors.length];
  };


  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true);
        const token = await getToken({ template: "fastapi" });
        const [notesData, coursesData] = await Promise.all([
          notesApi.search(
            {
              query: searchQuery || undefined,
              course_id: selectedCourse || undefined,
              semester: selectedSemester || undefined,
              limit: 50,
            },
            token || undefined
          ),
          coursesApi.list(),
        ]);
        setNotes(notesData);
        setCourses(coursesData);
      } catch (error) {
        console.error("Failed to load data:", error);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, [searchQuery, selectedCourse, selectedSemester, getToken]);

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">
        Discover Notes
      </h1>

      <p className="text-gray-600 mb-6">
        Search by title, course, or semester 
      </p>

      <div className="flex flex-col md:flex-row gap-8">
        <aside className="w-full md:w-72 lg:w-80">
          <div className="bg-[#f7f3e9] border border-[#e3ddd0] rounded-2xl p-5 shadow-sm space-y-5">
            <h2 className="text-lg font-semibold">
              Filters
            </h2>

            <div className="space-y-1">
              <label className="text-sm font-medium text-gray-700">
                Course Title 
              </label>
              <input  
                type="text"
                placeholder="Search notes..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div className ="space-y-1">
              <label className="text-sm font-medium text-gray-700">
                Course
              </label>
              <select
                value={selectedCourse || ""}
                onChange={(e) =>
                  setSelectedCourse(e.target.value ? parseInt(e.target.value) : null)
                }
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">
                  All Courses
                </option>  

                <option value="">All courses</option>
                {courses.map((course) => (
                  <option key={course.id} value={course.id}>
                    {course.code} - {course.title}
                  </option>
                ))}
              </select>
            </div>

            <div className ="space-y-1">
              <label className="text-sm font-medium text-gray-700">
                Semester
              </label>
              <input
                type="text"
                placeholder="e.g., Fall 2024"
                value={selectedSemester}
                onChange={(e) => setSelectedSemester(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <button 
              type="button"
              onClick={() =>{
                setSearchQuery("");
                setSelectedCourse(null);
                setSelectedSemester("");
              }}
              className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
            >
              Clear Filters
            </button>
          </div>
        </aside>

        <main className="flex-1">
          {loading ? (
            <p className="text-center py-8">
              Loading...
            </p>
          ) : notes.length === 0 ? (
            <p className="text-center py-8 text-gray-500">
              No notes found. Try adjusting your search criteria.
            </p>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {notes.map((note, id) => (
                <Link
                  key={note.id}
                  href={`/notes/${note.id}`}
                  className="group rounded-2xl border border-gray-200 bg-white shadow-sm hover:shadow-md hover:-translate-y-1 transition-all overflow-hidden"
                >
                  <div className={`${getColorForNote(id)} h-2 w-full`} />

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

                    <div className="mt-auto flex items-center justify-between pt-2 text-xs">
                      <span
                        className={
                          note.is_free
                            ? "text-green-600 font-medium"
                            : "text-blue-600 font-medium"
                        }
                      >
                        {note.is_free ? "Free" : `${note.price} points`}
                      </span>

                      <div className="flex items-center gap-1 text-gray-500">
                        <span>{note.views} views</span>
                        <span>•</span>
                        <span>{note.downloads} downloads</span>
                      </div>
                    </div>
                  </div>
                </Link>       
              ))}
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
