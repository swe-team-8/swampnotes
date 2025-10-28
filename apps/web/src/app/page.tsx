"use client";
import Image from "next/image";
import { useAuth } from "@clerk/nextjs";
import { useEffect, useState } from "react";

export default function WhoAmI() {
  const { isSignedIn, getToken } = useAuth();
  const [me, setMe] = useState<any>(null);

  useEffect(() => {
    (async () => {
      const token = isSignedIn ? await getToken({ template: "fastapi" }) : null;
      console.log(token);
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/auth/me`, {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
        cache: "no-store",
      });
      setMe(await res.json());
    })();
  }, [isSignedIn, getToken]);

  return (
    <main className="relative h-screen w-full flex items-center justify-center text-center text-white">
      <Image
        src="/nice_lib.jpg"
        alt="nice place"
        fill
        className="object-cover brightness-75"
        priority
      />
 
      <div className="z-10 space-y-4">
        <h1 className="text-6xl font-extrabold drop-shadow-lg">
          Welcome to SwampNotes
        </h1>
        <p className="text-xl text-gray-100 max-w-xl mx-auto">
          Share and explore study materials at the University of Florida
        </p>
      </div>
    </main>
  );
}
