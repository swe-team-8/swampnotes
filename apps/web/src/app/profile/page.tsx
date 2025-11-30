"use client";
import { SignedIn, SignedOut, SignInButton, UserProfile } from "@clerk/nextjs";
import { useState } from "react";
import { useUser } from "@/features/users/hooks";

// Profile settings page using typed user hook

export default function ProfilePage() {
  return (
    <main className="max-w-3xl mx-auto p-6 space-y-8">
      <h1 className="text-2xl font-semibold">Your Profile</h1>

      <SignedOut>
        <div className="p-4 border rounded bg-yellow-50">
          <p className="mb-2">You’re not signed in.</p>
          <SignInButton />
        </div>
      </SignedOut>

      <SignedIn>
        <section className="space-y-2">
          <div className="border rounded p-2">
            <UserProfile routing="hash" />
          </div>
        </section>

        <AppSettings />
      </SignedIn>
    </main>
  );
}

function AppSettings() {
  const { user, update, loading, error } = useUser();
  const [saving, setSaving] = useState(false);
  const [msg, setMsg] = useState<string | null>(null);

  if (loading && !user) return null;
  if (!user) return null;
  const u = user;

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setSaving(true); setMsg(null);
    const form = new FormData(e.currentTarget);
    const ok = await update({
      display_name: form.get("display_name")?.toString() || null,
      bio: form.get("bio")?.toString() || null,
      is_profile_public: form.get("is_profile_public") === "on",
      show_email: form.get("show_email") === "on",
    });
    setSaving(false);
    setMsg(ok ? "Saved!" : "Save failed");
  }

  return (
    <section className="space-y-2">
      <h2 className="text-xl font-medium">SwampNotes settings</h2>
      <form className="space-y-4 border rounded p-4" onSubmit={onSubmit}>
        <div>
          <label className="block text-sm font-medium">Display name</label>
          <input name="display_name" defaultValue={u.display_name ?? ""} className="mt-1 w-full border rounded px-3 py-2" />
        </div>
        <div>
          <label className="block text-sm font-medium">Bio</label>
          <textarea name="bio" defaultValue={u.bio ?? ""} rows={3} className="mt-1 w-full border rounded px-3 py-2" />
        </div>
        <div className="space-y-1">
          <label className="flex items-center gap-2">
            <input type="checkbox" name="is_profile_public" defaultChecked={u.is_profile_public} />
            <span>Make my profile public</span>
          </label>
          <label className="flex items-center gap-2">
            <input type="checkbox" name="show_email" defaultChecked={u.show_email} />
            <span>Show my email (hidden by default)</span>
          </label>
        </div>
        <button type="submit" disabled={saving} className="px-4 py-2 rounded bg-black text-white disabled:opacity-60">
          {saving ? "Saving..." : "Save"}
        </button>
        {msg && <p className="text-sm">{msg}</p>}
        {error && <p className="text-sm text-red-600">{error}</p>}
      </form>
    </section>
  );
}