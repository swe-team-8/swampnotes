"use client";
import axios from "axios"
import { useAuth } from "@clerk/nextjs";
import { useEffect, useState } from "react";

export default function FileDownloader(){
  const { isSignedIn, getToken } = useAuth();
  const [me, setMe] = useState<any>(null);
  const [authorInput, setAuthorInput] = useState('');
  const [filenameInput, setFilenameInput] = useState('');

  const downloadFile = async () => {
      const token = await getToken({ template: "fastapi" });
      try {
        const response = await axios.get(`${process.env.NEXT_PUBLIC_API_BASE_URL}/notes/download/${authorInput}/${filenameInput}`,{
            headers: {
                'Authorization': `Bearer ${token}`,
            },
            responseType: "blob"
        });

        const fileBlob = new Blob([response.data]);

        const url = window.URL.createObjectURL(fileBlob);

        const tempLink = document.createElement("a");
        tempLink.href = url;
        tempLink.setAttribute(
          "download",
          `${filenameInput}`
        );

        document.body.appendChild(tempLink);
        tempLink.click();

        document.body.removeChild(tempLink);
        window.URL.revokeObjectURL(url);
      } catch (error) {
        console.error("Error downloading File:", error);
      }
    };

  return (
      <div>
          <input
              type="text"
              placeholder="Enter Author Name"
              value={authorInput}
              onChange={(e) => setAuthorInput(e.target.value)}
          />
          <input
              type="text"
              placeholder="Enter File Name"
              value={filenameInput}
              onChange={(e) => setFilenameInput(e.target.value)}
          />

          <button onClick={downloadFile}> Download File </button>
      </div>
  );
}