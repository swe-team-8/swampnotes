"use client";

import { useState, useEffect } from "react";
import { useAuth } from "@clerk/nextjs";
import { coursesApi, notesApi, type Course } from "@/lib/api";
import { useRouter } from "next/navigation";

export default function UploadNotePage() {
    const { isSignedIn, getToken } = useAuth();
    const router = useRouter();
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [title, setTitle] = useState("");
    const [selectedCourse, setSelectedCourse] = useState<Course | null>(null);
    const [courses, setCourses] = useState<Course[]>([]);
    const [semester, setSemester] = useState("");
    const [description, setDescription] = useState("");
    const [price, setPrice] = useState("100");
    const [isFree, setIsFree] = useState(false);
    const [uploading, setUploading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [success, setSuccess] = useState<string | null>(null);

    useEffect(() => {
        async function loadCourses() {
            try {
                const data = await coursesApi.list();
                setCourses(data);
            } catch (err) {
                console.error("Failed to load courses:", err);
                setError("Failed to load courses. Please refresh the page.");
            }
        }
        if (isSignedIn) {
            loadCourses();
        }
    }, [isSignedIn]);

    function onFileChange(e: React.ChangeEvent<HTMLInputElement>) {
        const file = e.target.files?.[0] || null;
        setSelectedFile(file);
        setError(null);
    }

    async function onUpload() {
        setError(null);
        setSuccess(null);

        if (!isSignedIn) {
            setError("You must be signed in to upload notes.");
            return;
        }
        if (!selectedFile) {
            setError("Please select a PDF file.");
            return;
        }
        if (!selectedFile.name.toLowerCase().endsWith(".pdf")) {
            setError("Only PDF files are allowed.");
            return;
        }
        if (!title || !selectedCourse || !semester) {
            setError("Title, course, and semester are required.");
            return;
        }

        setUploading(true);
        try {
            const token = await getToken({ template: "fastapi" });
            if (!token) {
                throw new Error("Failed to get authentication token");
            }

            const formData = new FormData();
            formData.append("file", selectedFile, selectedFile.name);
            formData.append("title", title);
            formData.append("course_id", selectedCourse.id.toString());
            formData.append("course_name", `${selectedCourse.code} - ${selectedCourse.title}`);
            formData.append("semester", semester);
            if (description) formData.append("description", description);
            formData.append("price", isFree ? "0" : price);
            formData.append("is_free", isFree.toString());

            const note = await notesApi.upload(formData, token);

            setSuccess(`Upload complete! Note ID: ${note.id}`);
            
            // Reset form
            setSelectedFile(null);
            setTitle("");
            setSelectedCourse(null);
            setSemester("");
            setDescription("");
            setPrice("100");
            setIsFree(false);

            // Redirect after 2 seconds
            setTimeout(() => {
                router.push("/notes/uploaded");
            }, 2000);
        } catch (e: unknown) {
            const message = e instanceof Error ? e.message : "Upload failed";
            setError(message);
            console.error("Upload error:", e);
        } finally {
            setUploading(false);
        }
    }

    if (!isSignedIn) {
        return (
            <div className="w-full min-h-screen flex justify-center items-center">
                <p className="text-lg">Please sign in to upload notes.</p>
            </div>
        );
    }

    return (
        <div className="w-full min-h-screen flex justify-center items-center gap-8 py-16">
            <div className="max-w-md w-full space-y-6 bg-orange-50 p-10 pt-12 rounded-3xl shadow-lg border border-gray-200">
                <h1 className="text-2xl font-semibold text-center">Upload Note</h1>

                <div className="space-y-4">
                    <input
                        type="text"
                        placeholder="Title *"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                        className="w-full rounded-xl border border-gray-300 px-4 py-3 shadow-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition"
                        disabled={uploading}
                    />

                    <select
                        value={selectedCourse?.id || ""}
                        onChange={(e) => {
                            const course = courses.find(c => c.id === parseInt(e.target.value));
                            setSelectedCourse(course || null);
                        }}
                        className="w-full rounded-xl border border-gray-300 px-4 py-3 shadow-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition"
                        disabled={uploading}
                    >
                        <option value="">Select Course *</option>
                        {courses.map((course) => (
                            <option key={course.id} value={course.id}>
                                {course.code} - {course.title}
                            </option>
                        ))}
                    </select>

                    <input
                        type="text"
                        placeholder="Semester (e.g., Fall 2024) *"
                        value={semester}
                        onChange={(e) => setSemester(e.target.value)}
                        className="w-full rounded-xl border border-gray-300 px-4 py-3 shadow-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition"
                        disabled={uploading}
                    />

                    <textarea
                        placeholder="Description (optional)"
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                        className="w-full rounded-xl border border-gray-300 px-4 py-3 shadow-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition resize-none"
                        rows={3}
                        disabled={uploading}
                    />

                    <div className="flex items-center gap-4">
                        <label className="flex items-center gap-2 cursor-pointer">
                            <input
                                type="checkbox"
                                checked={isFree}
                                onChange={(e) => setIsFree(e.target.checked)}
                                className="rounded cursor-pointer"
                                disabled={uploading}
                            />
                            <span className="text-sm font-medium">Free Note</span>
                        </label>

                        {!isFree && (
                            <input
                                type="number"
                                placeholder="Price (points)"
                                value={price}
                                onChange={(e) => setPrice(e.target.value)}
                                className="flex-1 rounded-xl border border-gray-300 px-4 py-2 shadow-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition"
                                min="0"
                                disabled={uploading}
                            />
                        )}
                    </div>

                    <div className="space-y-2">
                        <label className="block text-sm font-medium text-gray-700">
                            Upload PDF File *
                        </label>
                        <input
                            type="file"
                            accept=".pdf,application/pdf"
                            onChange={onFileChange}
                            className="w-full text-sm file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 cursor-pointer"
                            disabled={uploading}
                        />
                    </div>

                    {selectedFile && (
                        <div className="text-sm text-gray-700 bg-gray-50 p-3 rounded-lg">
                            <p className="font-medium">{selectedFile.name}</p>
                            <p className="text-gray-500">
                                Size: {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                            </p>
                        </div>
                    )}

                    <button
                        disabled={uploading || !selectedFile || !title || !selectedCourse || !semester}
                        onClick={onUpload}
                        className="w-full px-4 py-3 bg-black text-white rounded-xl font-medium hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                    >
                        {uploading ? "Uploading..." : "Upload Note"}
                    </button>

                    {error && (
                        <div className="text-sm text-red-600 bg-red-50 p-3 rounded-lg border border-red-200">
                            {error}
                        </div>
                    )}
                    
                    {success && (
                        <div className="text-sm text-green-600 bg-green-50 p-3 rounded-lg border border-green-200">
                            {success}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
