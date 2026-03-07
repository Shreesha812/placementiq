// lib/auth.ts
import api from "./api";

export interface LoginPayload {
  email: string;
  password: string;
}

export interface RegisterPayload {
  email: string;
  password: string;
  full_name?: string;
}

export interface User {
  id: string;
  email: string;
  full_name: string | null;
  role: string;
  is_active: boolean;
  created_at: string;
}

export async function login(payload: LoginPayload): Promise<string> {
  const res = await api.post("/auth/login", payload);
  const token = res.data.access_token;
  localStorage.setItem("token", token);
  return token;
}

export async function register(payload: RegisterPayload): Promise<User> {
  const res = await api.post("/auth/register", payload);
  return res.data;
}

export async function getMe(): Promise<User> {
  const res = await api.get("/auth/me");
  return res.data;
}

export function logout(): void {
  localStorage.removeItem("token");
  window.location.href = "/login";
}

export function isAuthenticated(): boolean {
  if (typeof window === "undefined") return false;
  return !!localStorage.getItem("token");
}