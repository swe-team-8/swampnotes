"use client";
import { SignedIn, SignedOut, SignInButton, UserProfile, useAuth } from "@clerk/nextjs";
import { useEffect, useState } from "react";

const API = process.env.NEXT_PUBLIC_API_BASE_URL!;

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
  const {isSignedIn, getToken } = useAuth();
  const [data, setData] = useState<any>(null);
  const [saving, setSaving] = useState(false);
  const [msg, setMsg] = useState<string | null>(null);

  useEffect(() => {
    if (!isSignedIn) return;
    (async () => {
      const token = await getToken({ template: "fastapi" });
      const res = await fetch(`${API}/users/me`, { headers: token ? { Authorization: `Bearer ${token}` } : {} });
      setData(await res.json());
    })();
  }, [isSignedIn, getToken]);

  if (!data?.user) return null;
  const u = data.user;

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setSaving(true); setMsg(null);
    const form = new FormData(e.currentTarget);
    const payload = {
      display_name: form.get("display_name")?.toString() || null,
      bio: form.get("bio")?.toString() || null,
      is_profile_public: form.get("is_profile_public") === "on",
      show_email: form.get("show_email") === "on",
    };
    const token = await getToken({ template: "fastapi" });
    const res = await fetch(`${API}/users/me`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json", ...(token ? { Authorization: `Bearer ${token}` } : {}) },
      body: JSON.stringify(payload),
    });
    setSaving(false);
    if (!res.ok) { setMsg("Save failed"); return; }
    const j = await res.json();
    setData({ user: { ...u, ...j.user } }); setMsg("Saved!");
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
      </form>
    </section>
  );
}