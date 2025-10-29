"use client";
import axios from "axios"
import { useAuth } from "@clerk/nextjs";
import { useEffect, useState } from "react";

export default function upload() {
  const { isSignedIn, getToken } = useAuth();
  const [me, setMe] = useState<any>(null);

	const [selectedFile, setSelectedFile] = useState(null);
	const onFileChange = (event) => {
		setSelectedFile(event.target.files[0]);
	};
	const onFileUpload = async () => {
        const token = await getToken({ template: "fastapi" });
		const formData = new FormData();
		formData.append(
			"file",
			selectedFile,
			selectedFile.name
		);
		console.log(selectedFile);
		axios.post(`${process.env.NEXT_PUBLIC_API_BASE_URL}/notes/upload`, formData,{
            headers: {
                'Authorization': `Bearer ${token}`,
            }
        });
	};
	const fileData = () => {
		if (selectedFile) {
			return (
				<div>
					<h2>File Details:</h2>
					<p>File Name: {selectedFile.name}</p>
					<p>File Type: {selectedFile.type}</p>
					<p>
						Last Modified: {selectedFile.lastModifiedDate.toDateString()}
					</p>
				</div>
			);
		} else {
			return (
				<div>
					<br />
					<h4>Choose before Pressing the Upload button</h4>
				</div>
			);
		}
	};

	return (
		<div>
			<div>
				<input type="file" onChange={onFileChange} />
				<button onClick={onFileUpload}>Upload!</button>
			</div>
			{fileData()}
		</div>
	);
}
