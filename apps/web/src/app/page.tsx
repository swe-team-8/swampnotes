"use client";
import Image from "next/image";
import { useAuth } from "@clerk/nextjs";

export default function WhoAmI() {
  useAuth();

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
