"use client";
import { useAuth } from "@clerk/nextjs";
import { useState } from "react";

export default function FileDeleter() {
  const { getToken } = useAuth();
  const [filenameInput, setFilenameInput] = useState("");

  const deleteFile = async () => {
    const token = await getToken({ template: "fastapi" });
    await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/notes/delete/${filenameInput}`, {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
      cache: "no-store",
      method: "DELETE",
    });
  };

  return (
      <div>
        <input
          type="text"
          placeholder="Enter File Name"
          value={filenameInput}
          onChange={(e) => setFilenameInput(e.target.value)}
        />
        <button onClick={deleteFile}>Delete File</button>
      </div>
  );
}
