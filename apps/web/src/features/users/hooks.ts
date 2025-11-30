"use client";
import { useAuth } from "@clerk/nextjs";
import { useEffect, useState, useCallback } from "react";
import { apiFetch } from "@/lib/http"; 
import type { UserMeResponse, UpdateUserPayload, User } from "./types";

export function useUser() {
  const { isSignedIn, getToken } = useAuth();
  const [data, setData] = useState<UserMeResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    if (!isSignedIn) { setData(null); return; }
    setLoading(true); setError(null);
    try {
      const token = (await getToken({ template: "fastapi" })) || undefined;
      const userData = await apiFetch<UserMeResponse>("/users/me", { auth: true, token });
      setData(userData);
    } catch (e: unknown) {
      const message = e instanceof Error ? e.message : "Failed to load user";
      setError(message);
    } finally {
      setLoading(false);
    }
  }, [isSignedIn, getToken]);

  useEffect(() => { refresh(); }, [refresh]);

  // Update helper
  const update = useCallback(async (payload: UpdateUserPayload) => {
    if (!data) return;
    try {
      const token = (await getToken({ template: "fastapi" })) || undefined;
      const updated = await apiFetch<{ ok: boolean; user: Partial<User> }>("/users/me", {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
        auth: true,
        token,
      });
      setData({ user: { ...data.user, ...updated.user } });
      return true;
    } catch (e: unknown) {
      const message = e instanceof Error ? e.message : "Update failed";
      setError(message);
      return false;
    }
  }, [data, getToken]);

  return { user: data?.user ?? null, loading, error, refresh, update };
}
