"use client";
import axios from "axios"
import { useAuth } from "@clerk/nextjs";
import { useEffect, useState } from "react";

export default function FileDeleter(){
  const { isSignedIn, getToken } = useAuth();
  const [me, setMe] = useState<any>(null);
  const [filenameInput, setFilenameInput] = useState('');

  const deleteFile = async () => {
      const token = await getToken({ template: "fastapi" });
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/delete/${filenameInput}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
        cache: "no-store",
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

          <button onClick={deleteFile}> Delete File </button>
      </div>
  );
}
