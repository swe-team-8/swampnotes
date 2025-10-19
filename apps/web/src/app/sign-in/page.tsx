"use client";
import { SignIn } from "@clerk/nextjs";

// Sign in page skeleton to start hooking up auth clerk (default clerk sign-in page)
export default function SignInPage() {
  return (
    <main className="p-8">
      <SignIn />
    </main>
  );
}