"use client";

import { useParams } from "next/navigation";
import { useState, useEffect } from "react";
import { notesApi, type Note } from "@/lib/api";
import { useAuth } from "@clerk/nextjs";

export default function NoteDetailPage() {
  const params = useParams();
  const { getToken, isSignedIn } = useAuth();
  const noteId = parseInt(params.id as string);

  const [note, setNote] = useState<Note | null>(null);
  const [ownership, setOwnership] = useState<{
    owned: boolean;
    is_author: boolean;
    can_download: boolean;
  } | null>(null);
  const [purchasing, setPurchasing] = useState(false);
  const [downloading, setDownloading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchData() {
      try {
        const token = await getToken({ template: "fastapi" });
        if (!token) return;

        const [noteData, ownershipData] = await Promise.all([
          notesApi.getById(noteId, token),
          notesApi.checkOwnership(noteId, token),
        ]);

        setNote(noteData);
        setOwnership(ownershipData);
      } catch (err) {
        console.error("Failed to load note:", err);
      }
    }

    fetchData();
  }, [noteId, getToken]);

  async function handlePurchase() {
    if (!isSignedIn) {
      window.location.href = "/sign-in";
      return;
    }

    setPurchasing(true);
    setError(null);

    try {
      const token = await getToken({ template: "fastapi" });
      if (!token) throw new Error("Not authenticated");

      await notesApi.purchase(noteId, token);
      
      const newOwnership = await notesApi.checkOwnership(noteId, token);
      setOwnership(newOwnership);
    } catch (err: any) {
      setError(err.message || "Purchase failed");
    } finally {
      setPurchasing(false);
    }
  }

  async function handleDownload() {
    if (!isSignedIn) {
      window.location.href = "/sign-in";
      return;
    }

    if (!ownership?.can_download) {
      setError("You must purchase this note to download it");
      return;
    }

    setDownloading(true);
    setError(null);

    try {
      const token = await getToken({ template: "fastapi" });
      if (!token) throw new Error("Not authenticated");

      // Use the API wrapper to download
      const blob = await notesApi.download(noteId, token);

      // Create download link
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${note?.title || "note"}.pdf`;
      document.body.appendChild(a);
      a.click();

      // Cleanup
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      // Refresh note to get updated download count
      const updatedNote = await notesApi.getById(noteId, token);
      setNote(updatedNote);
    } catch (err: any) {
      console.error("Download error:", err);
      setError(err.message || "Failed to download note");
    } finally {
      setDownloading(false);
    }
  }

  if (!note) {
    return <div className="p-8 text-center">Loading...</div>;
  }

  return (
    <main className="mx-auto max-w-4xl p-8 space-y-6">
      <div className="bg-white rounded-2xl border p-8 space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">{note.title}</h1>
          <p className="text-gray-600 mt-2">
            {note.course_name} • {note.semester}
          </p>
        </div>

        <div className="flex items-center gap-4 text-sm text-gray-600">
          <span>👁 {note.views} views</span>
          <span>⬇ {note.downloads} downloads</span>
        </div>

        {note.description && (
          <div>
            <h2 className="font-semibold text-gray-900 mb-2">Description</h2>
            <p className="text-gray-700">{note.description}</p>
          </div>
        )}

        <div className="border-t pt-6">
          {ownership?.can_download ? (
            <div className="space-y-4">
              <p className="text-green-600 font-medium">
                ✓ You own this note
              </p>
              <button
                onClick={handleDownload}
                disabled={downloading}
                className="w-full py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed font-medium"
              >
                {downloading ? "Downloading..." : "📥 Download PDF"}
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              {note.is_free ? (
                <p className="text-lg font-semibold text-green-600">FREE</p>
              ) : (
                <p className="text-lg font-semibold text-blue-600">
                  Price: {note.price} points
                </p>
              )}

              {error && (
                <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
                  {error}
                </div>
              )}

              <button
                disabled={purchasing}
                onClick={handlePurchase}
                className="w-full py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed font-medium"
              >
                {purchasing ? "Processing..." : "Purchase & Download"}
              </button>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}