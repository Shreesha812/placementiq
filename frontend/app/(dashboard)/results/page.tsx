// app/(dashboard)/results/page.tsx
"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { RadialBarChart, RadialBar, ResponsiveContainer } from "recharts";

interface ScoreBreakdown {
  skill_match: { score: number; weight: number; contribution: number };
  experience_weight: { score: number; weight: number; contribution: number };
  project_relevance: { score: number; weight: number; contribution: number };
  keyword_context: { score: number; weight: number; contribution: number };
}

interface Analysis {
  id: string;
  overall_score: number;
  score_breakdown: ScoreBreakdown;
  matched_skills: string[];
  missing_skills: string[];
  resume_skills: string[];
  jd_skills: string[];
  llm_insights: any;
  status: string;
  created_at: string;
}

export default function ResultsPage() {
  const [analysis, setAnalysis] = useState<Analysis | null>(() => {
    if (typeof window !== "undefined") {
      const stored = localStorage.getItem("latest_analysis");
      return stored ? JSON.parse(stored) : null;
    }
    return null;
  });

  if (!analysis) {
    return (
      <div className="min-h-screen bg-gray-950 flex items-center justify-center">
        <div className="text-center">
          <p className="text-white text-xl mb-4">No analysis found</p>
          <Link href="/analyze" className="text-blue-400 hover:underline">
            Run an analysis first
          </Link>
        </div>
      </div>
    );
  }

  const scorePercent = Math.round(analysis.overall_score * 100);
  const chartData = [{ value: scorePercent, fill: scorePercent >= 70 ? "#22c55e" : scorePercent >= 40 ? "#f59e0b" : "#ef4444" }];

  const breakdownItems = [
    { label: "Skill Match", key: "skill_match", emoji: "🎯" },
    { label: "Experience", key: "experience_weight", emoji: "💼" },
    { label: "Project Relevance", key: "project_relevance", emoji: "🚀" },
    { label: "Keyword Context", key: "keyword_context", emoji: "🔍" },
  ];

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <nav className="border-b border-gray-800 px-8 py-4 flex justify-between items-center">
        <Link href="/dashboard" className="text-xl font-bold text-blue-400">
          PlacementIQ
        </Link>
        <div className="flex gap-4">
          <Link href="/analyze" className="text-sm text-gray-400 hover:text-white">
            New Analysis
          </Link>
          <Link href="/dashboard" className="text-sm text-gray-400 hover:text-white">
            Dashboard
          </Link>
        </div>
      </nav>

      <main className="max-w-4xl mx-auto px-8 py-12">
        <h2 className="text-3xl font-bold mb-8">Analysis Results</h2>

        {/* Score Circle */}
        <div className="bg-gray-900 border border-gray-800 rounded-2xl p-8 mb-6 flex flex-col items-center">
          <div className="relative w-48 h-48">
            <ResponsiveContainer width="100%" height="100%">
              <RadialBarChart
                innerRadius="70%"
                outerRadius="100%"
                data={chartData}
                startAngle={90}
                endAngle={90 - 360 * (scorePercent / 100)}
              >
                <RadialBar dataKey="value" background={{ fill: "#1f2937" }} />
              </RadialBarChart>
            </ResponsiveContainer>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className="text-5xl font-bold">{scorePercent}%</span>
              <span className="text-gray-400 text-sm">Match Score</span>
            </div>
          </div>
          <p className="mt-4 text-gray-400 text-center">
            {scorePercent >= 70
              ? "🟢 Strong match — you're well positioned for this role"
              : scorePercent >= 40
              ? "🟡 Moderate match — some gaps to address"
              : "🔴 Low match — significant skill gaps detected"}
          </p>
        </div>

        {/* Score Breakdown */}
        <div className="grid grid-cols-2 gap-4 mb-6">
          {breakdownItems.map(({ label, key, emoji }) => {
            const item = analysis.score_breakdown[key as keyof ScoreBreakdown];
            const pct = Math.round(item.score * 100);
            return (
              <div key={key} className="bg-gray-900 border border-gray-800 rounded-xl p-5">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm text-gray-400">{emoji} {label}</span>
                  <span className="text-white font-semibold">{pct}%</span>
                </div>
                <div className="w-full bg-gray-800 rounded-full h-2">
                  <div
                    className="h-2 rounded-full bg-blue-500 transition-all"
                    style={{ width: `${pct}%` }}
                  />
                </div>
                <p className="text-xs text-gray-500 mt-1">
                  Weight: {item.weight * 100}% · Contribution: {Math.round(item.contribution * 100)}%
                </p>
              </div>
            );
          })}
        </div>

        {/* Skills */}
        <div className="grid grid-cols-2 gap-4 mb-6">
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
            <h3 className="font-semibold mb-3 text-green-400">✅ Matched Skills</h3>
            <div className="flex flex-wrap gap-2">
              {analysis.matched_skills.map((s) => (
                <span key={s} className="px-3 py-1 bg-green-900/40 border border-green-700 rounded-full text-green-300 text-xs">
                  {s}
                </span>
              ))}
            </div>
          </div>
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
            <h3 className="font-semibold mb-3 text-red-400">❌ Missing Skills</h3>
            <div className="flex flex-wrap gap-2">
              {analysis.missing_skills.map((s) => (
                <span key={s} className="px-3 py-1 bg-red-900/40 border border-red-700 rounded-full text-red-300 text-xs">
                  {s}
                </span>
              ))}
            </div>
          </div>
        </div>

        {/* LLM Insights */}
        {analysis.llm_insights && (
          <div className="space-y-4">

            {/* Score Explanation */}
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
              <h3 className="font-semibold mb-2 text-blue-400">🤖 AI Analysis</h3>
              <p className="text-gray-300 text-sm">{analysis.llm_insights.score_explanation}</p>
            </div>

            {/* Recommendations */}
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
              <h3 className="font-semibold mb-3 text-yellow-400">💡 Top Recommendations</h3>
              <ul className="space-y-2">
                {analysis.llm_insights.top_recommendations?.map((rec: string, i: number) => (
                  <li key={i} className="flex gap-2 text-sm text-gray-300">
                    <span className="text-yellow-400 mt-0.5">→</span>
                    <span>{rec}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Learning Roadmap */}
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
              <h3 className="font-semibold mb-3 text-purple-400">🗺️ Learning Roadmap</h3>
              <div className="space-y-3">
                {analysis.llm_insights.learning_roadmap?.map((item: any, i: number) => (
                  <div key={i} className="flex items-start justify-between p-3 bg-gray-800 rounded-lg">
                    <div>
                      <span className="text-white font-medium text-sm">{item.skill}</span>
                      <p className="text-gray-400 text-xs mt-0.5">{item.resource}</p>
                    </div>
                    <div className="text-right ml-4">
                      <span className={`text-xs px-2 py-0.5 rounded-full ${
                        item.priority === "High"
                          ? "bg-red-900/50 text-red-300"
                          : item.priority === "Medium"
                          ? "bg-yellow-900/50 text-yellow-300"
                          : "bg-green-900/50 text-green-300"
                      }`}>
                        {item.priority}
                      </span>
                      <p className="text-gray-500 text-xs mt-1">{item.time_estimate}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Resume Tips */}
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
              <h3 className="font-semibold mb-3 text-green-400">📝 Resume Tips</h3>
              <ul className="space-y-2">
                {analysis.llm_insights.resume_tips?.map((tip: string, i: number) => (
                  <li key={i} className="flex gap-2 text-sm text-gray-300">
                    <span className="text-green-400 mt-0.5">✓</span>
                    <span>{tip}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Encouragement */}
            <div className="bg-blue-900/20 border border-blue-800 rounded-xl p-5 text-center">
              <p className="text-blue-300 text-sm font-medium">
                {analysis.llm_insights.encouragement}
              </p>
            </div>

          </div>
        )}
      </main>
    </div>
  );
}