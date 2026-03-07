// app/(dashboard)/analyze/page.tsx
"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import api from "@/lib/api";

interface Resume {
  id: string;
  file_name: string;
  parse_status: string;
  created_at: string;
}

export default function AnalyzePage() {
  const router = useRouter();
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [selectedResume, setSelectedResume] = useState("");
  const [jdTitle, setJdTitle] = useState("");
  const [jdCompany, setJdCompany] = useState("");
  const [jdText, setJdText] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    api.get("/resumes/").then((res) => {
      setResumes(res.data);
      if (res.data.length > 0) setSelectedResume(res.data[0].id);
    });
  }, []);

  async function handleAnalyze(e: React.FormEvent) {
    e.preventDefault();
    if (!selectedResume || !jdText) return;

    setLoading(true);
    setError("");

    try {
      const res = await api.post("/analysis/run", {
        resume_id: selectedResume,
        jd_title: jdTitle,
        jd_company: jdCompany,
        jd_text: jdText,
      });
      // Store result and redirect to results page
      localStorage.setItem("latest_analysis", JSON.stringify(res.data));
      router.push("/results");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Analysis failed");
    } finally {
      setLoading(false);
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
        <h2 className="text-3xl font-bold mb-2">Analyze Against JD</h2>
        <p className="text-gray-400 mb-8">
          Paste a job description to get your placement score.
        </p>

        {error && (
          <div className="mb-4 p-3 bg-red-900/50 border border-red-700 rounded-lg text-red-300 text-sm">
            {error}
          </div>
        )}

        <form onSubmit={handleAnalyze} className="space-y-5">
          {/* Resume selector */}
          <div>
            <label className="block text-sm text-gray-400 mb-1">Select Resume</label>
            {resumes.length === 0 ? (
              <div className="p-4 bg-yellow-900/30 border border-yellow-700 rounded-lg text-yellow-300 text-sm">
                No resumes found.{" "}
                <Link href="/upload" className="underline">
                  Upload one first
                </Link>
              </div>
            ) : (
              <select
                value={selectedResume}
                onChange={(e) => setSelectedResume(e.target.value)}
                className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-blue-500"
              >
                {resumes.map((r) => (
                  <option key={r.id} value={r.id}>
                    {r.file_name}
                  </option>
                ))}
              </select>
            )}
          </div>

          {/* JD metadata */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm text-gray-400 mb-1">Job Title</label>
              <input
                type="text"
                value={jdTitle}
                onChange={(e) => setJdTitle(e.target.value)}
                className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-blue-500"
                placeholder="Backend Engineer"
              />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Company</label>
              <input
                type="text"
                value={jdCompany}
                onChange={(e) => setJdCompany(e.target.value)}
                className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-blue-500"
                placeholder="Google"
              />
            </div>
          </div>

          {/* JD text */}
          <div>
            <label className="block text-sm text-gray-400 mb-1">
              Job Description
            </label>
            <textarea
              value={jdText}
              onChange={(e) => setJdText(e.target.value)}
              rows={8}
              className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-blue-500 resize-none"
              placeholder="Paste the full job description here..."
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading || !selectedResume || !jdText}
            className="w-full py-3 bg-blue-600 hover:bg-blue-500 disabled:bg-gray-700 disabled:text-gray-500 text-white font-semibold rounded-lg transition"
          >
            {loading ? "Analyzing..." : "Run Analysis"}
          </button>
        </form>
      </main>
    </div>
  );
}