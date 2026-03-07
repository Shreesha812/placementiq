# app/services/scoring_engine.py
from app.services.skill_extractor import extract_skills_from_text


def compute_skill_match(resume_skills: list[str], jd_skills: list[str]) -> dict:
    """
    Compute skill overlap between resume and JD.
    Returns matched, missing, and score.
    """
    if not jd_skills:
        return {"score": 0.0, "matched": [], "missing": []}

    resume_set = set(s.lower() for s in resume_skills)
    jd_set = set(s.lower() for s in jd_skills)

    matched = [s for s in jd_skills if s.lower() in resume_set]
    missing = [s for s in jd_skills if s.lower() not in resume_set]

    score = len(matched) / len(jd_skills) if jd_skills else 0.0

    return {
        "score": round(score, 4),
        "matched": matched,
        "missing": missing,
    }


def compute_project_relevance(resume_parsed: dict, jd_text: str) -> float:
    """
    Check how many JD skills appear in resume projects section.
    Proxy for project relevance score.
    """
    projects = resume_parsed.get("projects", [])
    if not projects:
        return 0.0

    project_text = " ".join(projects)
    project_skills = set(s.lower() for s in extract_skills_from_text(project_text))
    jd_skills = set(s.lower() for s in extract_skills_from_text(jd_text))

    if not jd_skills:
        return 0.0

    overlap = project_skills & jd_skills
    return round(len(overlap) / len(jd_skills), 4)


def compute_keyword_context(resume_text: str, jd_text: str) -> float:
    """
    TF-IDF inspired keyword overlap between full resume and JD text.
    Measures contextual similarity beyond just skill names.
    """
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    if not resume_text or not jd_text:
        return 0.0

    try:
        vectorizer = TfidfVectorizer(stop_words="english", max_features=500)
        tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
        score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return round(float(score), 4)
    except Exception:
        return 0.0


def compute_experience_weight(resume_parsed: dict) -> float:
    """
    Estimate experience weight from resume.
    Students with projects but no experience get a base score.
    """
    experience = resume_parsed.get("experience", [])
    projects = resume_parsed.get("projects", [])

    if len(experience) > 5:
        return 1.0
    elif len(experience) > 0:
        return 0.6
    elif len(projects) > 2:
        return 0.4  # Strong projects compensate
    elif len(projects) > 0:
        return 0.25
    else:
        return 0.1


def run_scoring_engine(
    resume_text: str,
    resume_parsed: dict,
    jd_text: str,
) -> dict:
    """
    Main scoring function. Runs all components and returns
    weighted overall score + full breakdown.

    Weights:
        Skill Match:        40%
        Experience:         20%
        Project Relevance:  20%
        Keyword Context:    20%
    """
    # Extract skills
    resume_skills = extract_skills_from_text(resume_text)
    jd_skills = extract_skills_from_text(jd_text)

    # Run each component
    skill_result = compute_skill_match(resume_skills, jd_skills)
    experience_score = compute_experience_weight(resume_parsed)
    project_score = compute_project_relevance(resume_parsed, jd_text)
    keyword_score = compute_keyword_context(resume_text, jd_text)

    # Weighted formula
    overall = (
        0.40 * skill_result["score"] +
        0.20 * experience_score +
        0.20 * project_score +
        0.20 * keyword_score
    )

    return {
        "overall_score": round(overall, 4),
        "score_breakdown": {
            "skill_match": {
                "score": skill_result["score"],
                "weight": 0.40,
                "contribution": round(0.40 * skill_result["score"], 4),
            },
            "experience_weight": {
                "score": experience_score,
                "weight": 0.20,
                "contribution": round(0.20 * experience_score, 4),
            },
            "project_relevance": {
                "score": project_score,
                "weight": 0.20,
                "contribution": round(0.20 * project_score, 4),
            },
            "keyword_context": {
                "score": keyword_score,
                "weight": 0.20,
                "contribution": round(0.20 * keyword_score, 4),
            },
        },
        "matched_skills": skill_result["matched"],
        "missing_skills": skill_result["missing"],
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
    }