"use client";
import { SignUp } from "@clerk/nextjs";

// Sign up page skeleton to start hooking up auth clerk (default clerk sign-up page)
export default function SignUpPage() {
  return (
    <main className="p-8">
      <SignUp />
    </main>
  );
}