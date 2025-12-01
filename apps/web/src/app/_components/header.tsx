"use client";

import Link from "next/link";
import { SignedIn, SignedOut, SignUpButton, UserButton, useUser } from "@clerk/nextjs";
import { UserPoints } from "./user-points";

export default function Header() {
  const { user } = useUser();
  const isAdmin = user?.publicMetadata?.is_admin === true || 
                  user?.publicMetadata?.role === "admin";

  return (
    <header className="sticky top-0 z-50 bg-white border-b shadow-sm">
      <div className="max-w-7xl mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <Link href="/" className="text-2xl font-bold">
            <span className="text-orange-600">Swamp</span>
            <span className="text-blue-600">Notes</span>
          </Link>

          <nav className="flex items-center gap-6">
            <SignedIn>
              <Link 
                href="/notes/discover"
                className="text-gray-700 hover:text-blue-600 font-medium transition-colors"
              >
                Discover
              </Link>
              <Link 
                href="/notes"
                className="text-gray-700 hover:text-blue-600 font-medium transition-colors"
              >
                My Notes
              </Link>
              <Link 
                href="/notes/upload"
                className="text-gray-700 hover:text-blue-600 font-medium transition-colors"
              >
                Upload
              </Link>
              {isAdmin && (
                <Link 
                  href="/admin/courses"
                  className="text-red-600 hover:text-red-700 font-semibold transition-colors"
                >
                  Admin
                </Link>
              )}
              <UserPoints />
              <UserButton
                afterSignOutUrl="/"
                userProfileMode="navigation"
                userProfileUrl="/profile"
                appearance={{
                  elements: {
                    avatarBox: "w-9 h-9 ring-2 ring-blue-100 hover:ring-blue-300 transition-all",
                  }
                }}
              />
            </SignedIn>

            <SignedOut>
              <Link 
                href="/sign-in"
                className="text-gray-700 hover:text-blue-600 font-medium transition-colors"
              >
                Sign In
              </Link>
              <SignUpButton mode="modal">
                <button className="px-5 py-2 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-colors shadow-sm hover:shadow-md">
                  Sign Up
                </button>
              </SignUpButton>
            </SignedOut>
          </nav>
        </div>
      </div>
    </header>
  );
}