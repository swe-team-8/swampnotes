import axios from "axios";
import { apiFetch } from "./http";

export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000",
});

export type Note = {
  id: number;
  title: string;
  description: string | null;
  course_id: number;
  course_name: string;
  semester: string;
  price: number;
  is_free: boolean;
  author_id: number;
  downloads: number;
  views: number;
  created_at: string;
};

export type Course = {
  id: number;
  code: string;
  title: string;
  school: string;
};

export type Purchase = {
  id: number;
  user_id: number;
  note_id: number;
  price_paid: number;
  purchased_at: string;
};

// Helper to build query string from params
function buildQueryString(params?: Record<string, any>): string {
  if (!params) return "";
  const query = Object.entries(params)
    .filter(([_, v]) => v !== undefined && v !== null)
    .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`)
    .join("&");
  return query ? `?${query}` : "";
}

export const notesApi = {
  search: async (
    params: {
      query?: string;
      course_id?: number;
      semester?: string;
      limit?: number;
      offset?: number;
    },
    token?: string
  ) => {
    const qs = buildQueryString(params);
    return apiFetch<Note[]>(`/notes/search${qs}`, { auth: true, token });
  },

  getLibrary: (token?: string) =>
    apiFetch<Note[]>("/notes/library", { auth: true, token }),

  getUploaded: (token?: string) =>
    apiFetch<Note[]>("/notes/uploaded", { auth: true, token }),

  purchase: (noteId: number, token?: string) =>
    apiFetch<Purchase>(`/notes/${noteId}/purchase`, {
      method: "POST",
      auth: true,
      token,
    }),

  checkOwnership: (noteId: number, token?: string) =>
    apiFetch<{ owned: boolean; is_author: boolean; can_download: boolean }>(
      `/notes/${noteId}/owned`,
      { auth: true, token }
    ),

  getById: (noteId: number, token?: string) =>
    apiFetch<Note>(`/notes/${noteId}`, { auth: true, token }),
};

export const coursesApi = {
  list: () => apiFetch<Course[]>("/courses"),

  getNotes: (courseId: number) =>
    apiFetch<Note[]>(`/courses/${courseId}/notes`),

  create: (
    data: { code: string; title: string; school: string },
    token?: string
  ) =>
    apiFetch<Course>("/courses", {
      method: "POST",
      auth: true,
      token,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    }),
};