"use client";
import { SignedIn, SignedOut, UserButton, SignInButton, SignUpButton } from "@clerk/nextjs";

// Create a basic header
export default function Header() {
  return (
    <header className="flex items-center justify-between p-4 border-b">
      <a href="/" className="font-semibold">SwampNotes</a>
      <nav className="flex items-center gap-3">
        <a href="/notes" className="underline">Notes</a>
        <SignedOut>
          <SignInButton mode="modal" />
          <SignUpButton mode="modal" />
        </SignedOut>
      </nav>
    </header>
  );
}