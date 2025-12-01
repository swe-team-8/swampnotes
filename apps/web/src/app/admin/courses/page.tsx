"use client";

import { useState, useEffect } from "react";
import { useAuth, useUser } from "@clerk/nextjs";
import { coursesApi, type Course } from "@/lib/api";

export default function AdminCoursesPage() {
  const { getToken } = useAuth();
  const { user } = useUser();
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  // Form state
  const [code, setCode] = useState("");
  const [title, setTitle] = useState("");
  const [school, setSchool] = useState("");

  // Check if user is admin
  const isAdmin = user?.publicMetadata?.is_admin === true || 
                  user?.publicMetadata?.role === "admin";

  useEffect(() => {
    async function fetchCourses() {
      try {
        const data = await coursesApi.list();
        setCourses(data);
      } catch (err) {
        console.error("Failed to fetch courses:", err);
      }
    }
    fetchCourses();
  }, []);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setSuccess(null);
    setLoading(true);

    try {
      const token = await getToken({ template: "fastapi" });
      if (!token) throw new Error("Not authenticated");

      await coursesApi.create({ code, title, school }, token);
      
      setSuccess("Course created successfully!");
      setCode("");
      setTitle("");
      setSchool("");
      
      // Refresh course list
      const updated = await coursesApi.list();
      setCourses(updated);
    } catch (err: any) {
      setError(err.message || "Failed to create course");
    } finally {
      setLoading(false);
    }
  }

  if (!isAdmin) {
    return (
      <div className="max-w-4xl mx-auto p-8">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
          <h1 className="text-xl font-semibold text-red-900">Access Denied</h1>
          <p className="text-red-700 mt-2">You need admin privileges to access this page.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-8 space-y-8">
      <header>
        <h1 className="text-4xl font-bold text-blue-700">Course Management</h1>
        <p className="text-gray-600 mt-2">Add and manage courses for the directory</p>
      </header>

      {/* Create Course Form */}
      <div className="bg-white rounded-2xl border p-8 space-y-6">
        <h2 className="text-2xl font-semibold">Add New Course</h2>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Course Code *
            </label>
            <input
              type="text"
              value={code}
              onChange={(e) => setCode(e.target.value)}
              placeholder="e.g. COP3530"
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Course Title *
            </label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g. Data Structures and Algorithms"
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              School *
            </label>
            <input
              type="text"
              value={school}
              onChange={(e) => setSchool(e.target.value)}
              placeholder="e.g. University of Florida"
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}

          {success && (
            <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg">
              {success}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
          >
            {loading ? "Creating..." : "Create Course"}
          </button>
        </form>
      </div>

      {/* Existing Courses */}
      <div className="bg-white rounded-2xl border p-8">
        <h2 className="text-2xl font-semibold mb-4">Existing Courses ({courses.length})</h2>
        
        {courses.length === 0 ? (
          <p className="text-gray-500 text-center py-8">No courses yet. Create one above!</p>
        ) : (
          <div className="space-y-2">
            {courses.map((course) => (
              <div
                key={course.id}
                className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50"
              >
                <div>
                  <h3 className="font-semibold text-gray-900">{course.code}</h3>
                  <p className="text-sm text-gray-600">{course.title}</p>
                  <p className="text-xs text-gray-500">{course.school}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}