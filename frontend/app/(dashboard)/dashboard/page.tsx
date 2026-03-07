// app/(dashboard)/dashboard/page.tsx
"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getMe, logout, User } from "@/lib/auth";
import Link from "next/link";

export default function DashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getMe()
      .then(setUser)
      .catch(() => router.push("/login"))
      .finally(() => setLoading(false));
  }, [router]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-950 flex items-center justify-center">
        <p className="text-white">Loading...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      {/* Navbar */}
      <nav className="border-b border-gray-800 px-8 py-4 flex justify-between items-center">
        <h1 className="text-xl font-bold text-blue-400">PlacementIQ</h1>
        <div className="flex items-center gap-6">
          <span className="text-gray-400 text-sm">{user?.email}</span>
          <button
            onClick={logout}
            className="text-sm text-gray-400 hover:text-white transition"
          >
            Logout
          </button>
        </div>
      </nav>

      {/* Main */}
      <main className="max-w-4xl mx-auto px-8 py-12">
        <h2 className="text-3xl font-bold mb-2">
          Welcome, {user?.full_name || "Student"} 👋
        </h2>
        <p className="text-gray-400 mb-10">
          Check your placement readiness by analyzing your resume against job descriptions.
        </p>

        {/* Action Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Link href="/upload">
            <div className="p-6 bg-gray-900 border border-gray-800 rounded-2xl hover:border-blue-500 transition cursor-pointer">
              <div className="text-3xl mb-3">📄</div>
              <h3 className="text-lg font-semibold mb-1">Upload Resume</h3>
              <p className="text-gray-400 text-sm">
                Upload your PDF resume and let AI parse it automatically.
              </p>
            </div>
          </Link>

          <Link href="/analyze">
            <div className="p-6 bg-gray-900 border border-gray-800 rounded-2xl hover:border-blue-500 transition cursor-pointer">
              <div className="text-3xl mb-3">🎯</div>
              <h3 className="text-lg font-semibold mb-1">Analyze Against JD</h3>
              <p className="text-gray-400 text-sm">
                Paste a job description and get your placement score instantly.
              </p>
            </div>
          </Link>
        </div>
      </main>
    </div>
  );
}