import { API_BASE } from "./config";

// Generic options
interface ApiOptions extends RequestInit {
  auth?: boolean; // include bearer token from Clerk client
  token?: string; // can optionally pass a pre-fetched token
}

export async function apiFetch<T>(path: string, opts: ApiOptions = {}): Promise<T> {
  const headers: Record<string, string> = {
    Accept: "application/json",
    ...(opts.headers as Record<string, string>),
  };
  if (opts.auth) {
    if (opts.token) {
      headers.Authorization = `Bearer ${opts.token}`;
    }
  }
  const res = await fetch(`${API_BASE}${path}`, {
    ...opts,
    headers,
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API ${res.status} ${res.statusText}: ${text}`);
  }
  if (res.status === 204) return undefined as T;
  return (await res.json()) as T;
}
