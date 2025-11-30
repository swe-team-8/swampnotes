"use client";
import axios from "axios";
import { useAuth } from "@clerk/nextjs";
import { useState } from "react";

export default function UploadNotePage() {
  	const { isSignedIn, getToken } = useAuth();
	const [selectedFile, setSelectedFile] = useState<File | null>(null);
	const [title, setTitle] = useState("");
	const [courseId, setCourseId] = useState("");
	const [courseName, setCourseName] = useState("");
	const [semester, setSemester] = useState("");
	const [description, setDescription] = useState("");
	const [uploading, setUploading] = useState(false);
	const [error, setError] = useState<string | null>(null);
	const [success, setSuccess] = useState<string | null>(null);

	function onFileChange(e: React.ChangeEvent<HTMLInputElement>) {
		const file = e.target.files?.[0] || null;
		setSelectedFile(file);
	}

	async function onUpload() {
		setError(null); setSuccess(null);
		if (!isSignedIn) { setError("You must be signed in."); return; }
		if (!selectedFile) { setError("Please choose a file."); return; }
		if (!title || !courseId || !courseName || !semester) { setError("All required fields must be filled."); return; }
		setUploading(true);
		try {
			const token = await getToken({ template: "fastapi" });
			const formData = new FormData();
			formData.append("file", selectedFile, selectedFile.name);
			formData.append("title", title);
			formData.append("course_id", courseId);
			formData.append("course_name", courseName);
			formData.append("semester", semester);
			if (description) formData.append("description", description);
			await axios.post(`${process.env.NEXT_PUBLIC_API_BASE_URL}/notes/upload`, formData, {
				headers: { Authorization: token ? `Bearer ${token}` : "" },
			});
			setSuccess("Upload complete");
			setSelectedFile(null);
			setTitle(""); setCourseId(""); setCourseName(""); setSemester(""); setDescription("");
		} catch (e: unknown) {
			const message = e instanceof Error ? e.message : "Upload failed";
			setError(message);
		} finally {
			setUploading(false);
		}
	}

	return (
		<div className="w-full min-h-screen flex justify-center items-center gap-8 py-16">

			<div className="hidden md:flex w-1/4 justify-end">
				<img
					src=""
					alt="Upload Note left side"
					className="w-40 h-auto object-contain opacity-90"
				/>
			</div>

			<div className="max-w-md w-full space-y-6 bg-orange-50 p-10 pt-12 rounded-3xl shadow-lg border border-gray-200">
				<h1 className="text-2xl font-semibold text-center">Upload Note</h1>

				<div className="space-y-4">

					<input type="text" placeholder="Title" value={title} onChange={e => setTitle(e.target.value)} 
					className="w-full rounded-xl border border-gray-300 px-4 py-3 shadow-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition" />
					<input type="number" placeholder="Course ID" value={courseId} onChange={e => setCourseId(e.target.value)} 
					className="w-full rounded-xl border border-gray-300 px-4 py-3 shadow-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition" />
					<input type="text" placeholder="Course Name" value={courseName} onChange={e => setCourseName(e.target.value)} 
					className="w-full rounded-xl border border-gray-300 px-4 py-3 shadow-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition" />
					<input type="text" placeholder="Semester" value={semester} onChange={e => setSemester(e.target.value)} 
					className="w-full rounded-xl border border-gray-300 px-4 py-3 shadow-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition" />
					<textarea placeholder="Description (optional)" value={description} onChange={e => setDescription(e.target.value)} 
					className="w-full rounded-xl border border-gray-300 px-4 py-3 shadow-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition" rows={3} />
					<input type="file" onChange={onFileChange} />
					<button disabled={uploading} onClick={onUpload} className="px-4 py-2 bg-black text-white rounded disabled:opacity-50">
						{uploading ? "Uploading..." : "Upload"}
					</button>
					{error && <p className="text-sm text-red-600">{error}</p>}
					{success && <p className="text-sm text-green-600">{success}</p>}
					
				</div>
				{selectedFile && (
					<div className="text-sm text-gray-700">
						<p>File Name: {selectedFile.name}</p>
						<p>File Type: {selectedFile.type || "unknown"}</p>
						<p>Last Modified: {new Date(selectedFile.lastModified).toLocaleString()}</p>
					</div>
				)}
			</div>
			
			<div className="hidden md:flex w-1/4 justify-start">
				<img
				src="/right.png"
				alt="Notebook right"
				className="w-40 h-auto object-contain opacity-90"
				/>
			</div>
		</div>
	);
}
