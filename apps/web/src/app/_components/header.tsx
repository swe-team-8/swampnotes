"use client";

import Link from "next/link";
import { SignedIn, SignedOut, SignInButton, SignUpButton, UserButton } from "@clerk/nextjs";

// Create a basic header
const DotIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 8 8" aria-hidden>
    <circle cx="4" cy="4" r="4" />
  </svg>
);

export default function Header() {
  return (
    <header className="flex items-center justify-between p-4 border-b">
      <Link href="/" className="font-semibold">SwampNotes</Link>

      <nav className="flex items-center gap-3">
        <SignedIn>
          <a href="/upload">Upload +</a>
          <UserButton
            afterSignOutUrl="/"
            userProfileMode="navigation"
            userProfileUrl="/profile"
          >
            <UserButton.MenuItems>
              <UserButton.Link
                label="Notes"
                labelIcon={<DotIcon />}
                href="/notes"
              />
            </UserButton.MenuItems>
          </UserButton>
        </SignedIn>

        <SignedOut>
          <a href="/sign-in">Sign In</a>
          <SignUpButton mode="modal" />
        </SignedOut>
      </nav>
    </header>
  );
}