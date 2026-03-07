// app/(dashboard)/upload/page.tsx
"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import api from "@/lib/api";

export default function UploadPage() {
  const router = useRouter();
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  async function handleUpload(e: React.FormEvent) {
    e.preventDefault();
    if (!file) return;

    setUploading(true);
    setError("");
    setSuccess("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await api.post("/resumes/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setSuccess(`Resume uploaded successfully! ID: ${res.data.id}`);
      setTimeout(() => router.push("/analyze"), 1500);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Upload failed");
    } finally {
      setUploading(false);
    }
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <nav className="border-b border-gray-800 px-8 py-4 flex justify-between items-center">
        <Link href="/dashboard" className="text-xl font-bold text-blue-400">
          PlacementIQ
        </Link>
        <Link href="/dashboard" className="text-sm text-gray-400 hover:text-white">
          ← Back to Dashboard
        </Link>
      </nav>

      <main className="max-w-2xl mx-auto px-8 py-12">
        <h2 className="text-3xl font-bold mb-2">Upload Resume</h2>
        <p className="text-gray-400 mb-8">Upload your PDF resume for AI-powered parsing.</p>

        {error && (
          <div className="mb-4 p-3 bg-red-900/50 border border-red-700 rounded-lg text-red-300 text-sm">
            {error}
          </div>
        )}
        {success && (
          <div className="mb-4 p-3 bg-green-900/50 border border-green-700 rounded-lg text-green-300 text-sm">
            {success}
          </div>
        )}

        <form onSubmit={handleUpload}>
          <div
            className="border-2 border-dashed border-gray-700 rounded-2xl p-12 text-center hover:border-blue-500 transition cursor-pointer"
            onClick={() => document.getElementById("fileInput")?.click()}
          >
            <div className="text-5xl mb-4">📄</div>
            {file ? (
              <p className="text-white font-medium">{file.name}</p>
            ) : (
              <>
                <p className="text-gray-300 font-medium">Click to select PDF</p>
                <p className="text-gray-500 text-sm mt-1">Max 5MB</p>
              </>
            )}
            <input
              id="fileInput"
              type="file"
              accept=".pdf"
              className="hidden"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
            />
          </div>

          <button
            type="submit"
            disabled={!file || uploading}
            className="mt-6 w-full py-3 bg-blue-600 hover:bg-blue-500 disabled:bg-gray-700 disabled:text-gray-500 text-white font-semibold rounded-lg transition"
          >
            {uploading ? "Uploading..." : "Upload Resume"}
          </button>
        </form>
      </main>
    </div>
  );
}