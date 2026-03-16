# app/services/llm_service.py
from groq import Groq
from app.core.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)


def generate_analysis_insights(
    overall_score: float,
    matched_skills: list[str],
    missing_skills: list[str],
    resume_skills: list[str],
    jd_skills: list[str],
    jd_title: str = "this role",
    jd_company: str = "",
) -> dict:
    """
    Call Groq LLM to generate human-readable insights from scoring data.
    Returns explanation, recommendations, and learning roadmap.
    """

    score_percent = round(overall_score * 100)
    company_str = f"at {jd_company}" if jd_company else ""

    prompt = f"""You are PlacementIQ, an AI placement advisor for students.

A student applied for: {jd_title} {company_str}

Their placement analysis results:
- Overall Match Score: {score_percent}%
- Skills they have that match: {', '.join(matched_skills) if matched_skills else 'None'}
- Skills required but missing: {', '.join(missing_skills) if missing_skills else 'None'}
- All their current skills: {', '.join(resume_skills) if resume_skills else 'None'}

Respond in this EXACT JSON format with no extra text:
{{
  "score_explanation": "2-3 sentence plain English explanation of why they got this score",
  "top_recommendations": [
    "Specific actionable recommendation 1",
    "Specific actionable recommendation 2", 
    "Specific actionable recommendation 3"
  ],
  "learning_roadmap": [
    {{
      "skill": "Skill name",
      "priority": "High/Medium/Low",
      "resource": "Best free resource to learn this",
      "time_estimate": "e.g. 2 weeks"
    }}
  ],
  "resume_tips": [
    "Specific resume improvement tip 1",
    "Specific resume improvement tip 2"
  ],
  "encouragement": "One motivating sentence personalized to their profile"
}}"""

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000,
        )

        import json
        raw = response.choices[0].message.content.strip()

        # Strip markdown code blocks if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]

        return json.loads(raw)

    except Exception as e:
        # Fallback if LLM fails
        return {
            "score_explanation": f"You matched {score_percent}% of the requirements for {jd_title}. You have {len(matched_skills)} of the required skills but are missing {len(missing_skills)} key skills.",
            "top_recommendations": [
                f"Learn {missing_skills[0]}" if missing_skills else "Strengthen your existing skills",
                f"Build a project using {missing_skills[1]}" if len(missing_skills) > 1 else "Add more projects to your resume",
                "Practice system design and DSA for interviews",
            ],
            "learning_roadmap": [
                {
                    "skill": skill,
                    "priority": "High",
                    "resource": "Official documentation + YouTube",
                    "time_estimate": "2-4 weeks"
                }
                for skill in missing_skills[:3]
            ],
            "resume_tips": [
                "Quantify your project impact with metrics",
                "Add keywords from the job description naturally",
            ],
            "encouragement": f"You already have {len(matched_skills)} matching skills — keep building and you'll get there!",
        }