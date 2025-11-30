export interface User {
  id: number;
  sub: string;
  email: string;
  name: string | null;
  display_name: string | null;
  bio: string | null;
  is_profile_public: boolean;
  show_email: boolean;
  points: number;
}

export interface UserMeResponse {
  user: User;
}

export interface UpdateUserPayload {
  display_name: string | null;
  bio: string | null;
  is_profile_public: boolean;
  show_email: boolean;
}
