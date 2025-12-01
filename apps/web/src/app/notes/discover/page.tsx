"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { coursesApi, notesApi, type Course, type Note } from "@/lib/api";

export default function DiscoverPage() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState<Note[]>([]);
  const [selectedCourse, setSelectedCourse] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function fetchCourses() {
      try {
        const data = await coursesApi.list();
        setCourses(data);
      } catch (error) {
        console.error("Failed to fetch courses:", error);
      }
    }
    fetchCourses();
  }, []);

  async function handleSearch() {
    setLoading(true);
    try {
      const results = await notesApi.search({
        query: searchQuery || undefined,
        course_id: selectedCourse || undefined,
        limit: 50,
      });
      setSearchResults(results);
    } catch (error) {
      console.error("Search failed:", error);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    handleSearch();
  }, [selectedCourse]); // Auto-search when course filter changes

  const getColorForNote = (index: number) => {
    const colors = ["bg-blue-400", "bg-orange-400", "bg-green-400", "bg-purple-400"];
    return colors[index % colors.length];
  };

  return (
    <main className="mx-auto max-w-6xl p-8 space-y-8">
      <header>
        <h1 className="text-5xl font-bold text-blue-700 mb-4">Discover Notes</h1>
        <p className="text-gray-600">
          Browse courses and purchase notes to add to your library
        </p>
      </header>

      {/* Search Bar */}
      <div className="bg-white rounded-2xl border p-6 space-y-4">
        <div className="flex gap-4">
          <input
            type="text"
            placeholder="Search notes by title, description, or course..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSearch()}
            className="flex-1 rounded-lg border border-gray-300 px-4 py-2 focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
          />
          <button
            onClick={handleSearch}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
          >
            Search
          </button>
        </div>

        {/* Course Filter */}
        <div className="flex items-center gap-2 overflow-x-auto pb-2">
          <button
            onClick={() => setSelectedCourse(null)}
            className={`px-4 py-2 rounded-full whitespace-nowrap ${
              selectedCourse === null
                ? "bg-blue-600 text-white"
                : "bg-gray-100 text-gray-700 hover:bg-gray-200"
            }`}
          >
            All Courses
          </button>
          {courses.map((course) => (
            <button
              key={course.id}
              onClick={() => setSelectedCourse(course.id)}
              className={`px-4 py-2 rounded-full whitespace-nowrap ${
                selectedCourse === course.id
                  ? "bg-blue-600 text-white"
                  : "bg-gray-100 text-gray-700 hover:bg-gray-200"
              }`}
            >
              {course.code}
            </button>
          ))}
        </div>
      </div>

      {/* Results */}
      {loading ? (
        <div className="text-center py-12">
          <p className="text-gray-500">Searching...</p>
        </div>
      ) : searchResults.length === 0 ? (
        <div className="text-center py-12 bg-white/50 rounded-2xl border">
          <p className="text-gray-500">
            {searchQuery || selectedCourse
              ? "No notes found matching your criteria"
              : "Start searching to discover notes"}
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {searchResults.map((note, idx) => (
            <Link
              key={note.id}
              href={`/notes/${note.id}`}
              className="group rounded-2xl border border-gray-200 bg-white shadow-sm hover:shadow-md hover:-translate-y-1 transition-all overflow-hidden"
            >
              <div className={`${getColorForNote(idx)} h-2 w-full`} />

              <div className="p-4 flex flex-col gap-2">
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
                  {note.course_name} • {note.downloads} downloads
                </p>

                <p className="mt-1 text-sm text-gray-700 line-clamp-3">
                  {note.description || "No description"}
                </p>

                <div className="mt-auto pt-2 flex items-center justify-between">
                  {note.is_free ? (
                    <span className="text-green-600 font-semibold text-sm">FREE</span>
                  ) : (
                    <span className="text-blue-600 font-semibold text-sm">
                      {note.price} points
                    </span>
                  )}
                  <span className="text-xs text-gray-500">👁 {note.views}</span>
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </main>
  );
}