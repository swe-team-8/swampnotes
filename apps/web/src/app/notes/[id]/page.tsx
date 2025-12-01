"use client";

import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import { useAuth } from "@clerk/nextjs";
import { notesApi, type Note } from "@/lib/api";

export default function NoteDetailPage() {
  const params = useParams();
  const { getToken } = useAuth();
  const noteId = parseInt(params.id as string);

  const [note, setNote] = useState<Note | null>(null);
  const [ownership, setOwnership] = useState<{
    owned: boolean;
    is_author: boolean;
    can_download: boolean;
  } | null>(null);
  const [purchasing, setPurchasing] = useState(false);
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
                className="w-full py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
                onClick={() => {
                  // Download logic - you'll need to implement file download endpoint
                  window.open(`${process.env.NEXT_PUBLIC_API_BASE_URL}/notes/${noteId}/download`);
                }}
              >
                Download PDF
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
                className="w-full py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
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