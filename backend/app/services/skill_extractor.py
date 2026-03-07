# app/services/skill_extractor.py
import re

# ── Canonical Skills Taxonomy ─────────────────────────────────
# 500+ skills organized by category.
# This is the single source of truth — all matching goes through here.

SKILLS_TAXONOMY = {
    # Programming Languages
    "Python", "Java", "C", "C++", "C#", "JavaScript", "TypeScript",
    "Go", "Rust", "Swift", "Kotlin", "Ruby", "PHP", "Scala", "R",
    "MATLAB", "Perl", "Shell", "Bash", "PowerShell", "Dart", "Lua",

    # Web Frameworks
    "React", "Next.js", "Vue.js", "Angular", "Svelte", "Django",
    "FastAPI", "Flask", "Express.js", "Node.js", "Spring Boot",
    "Laravel", "Ruby on Rails", "ASP.NET", "Nuxt.js", "Remix",

    # Databases
    "PostgreSQL", "MySQL", "SQLite", "MongoDB", "Redis", "Cassandra",
    "DynamoDB", "Elasticsearch", "Neo4j", "InfluxDB", "MariaDB",
    "Oracle", "MS SQL Server", "Supabase", "Firebase",

    # Cloud & DevOps
    "AWS", "GCP", "Azure", "Docker", "Kubernetes", "Terraform",
    "Ansible", "Jenkins", "GitHub Actions", "CircleCI", "ArgoCD",
    "Helm", "Prometheus", "Grafana", "Nginx", "Linux",

    # AI & ML
    "Machine Learning", "Deep Learning", "NLP", "Computer Vision",
    "PyTorch", "TensorFlow", "Keras", "scikit-learn", "Pandas",
    "NumPy", "Matplotlib", "Seaborn", "Hugging Face", "LangChain",
    "OpenAI API", "Claude API", "BERT", "GPT", "LLM", "RAG",
    "FAISS", "Pinecone", "Weaviate", "sentence-transformers",

    # Data Engineering
    "Spark", "Hadoop", "Kafka", "Airflow", "dbt", "Snowflake",
    "BigQuery", "Redshift", "Databricks", "ETL", "Data Pipeline",

    # Security
    "Cybersecurity", "Penetration Testing", "OWASP", "Cryptography",
    "Network Security", "Digital Forensics", "SIEM", "Burp Suite",
    "Metasploit", "Nmap", "Wireshark", "IDS", "IPS", "SOC",
    "Incident Response", "Malware Analysis", "Reverse Engineering",

    # Tools & Platforms
    "Git", "GitHub", "GitLab", "Bitbucket", "Jira", "Confluence",
    "VS Code", "IntelliJ", "Postman", "Figma", "Notion",
    "Slack", "Linux", "macOS", "Windows Server",

    # Concepts & Practices
    "REST API", "GraphQL", "gRPC", "WebSocket", "Microservices",
    "System Design", "CI/CD", "Agile", "Scrum", "TDD", "DevOps",
    "Data Structures", "Algorithms", "OOP", "Functional Programming",
    "Distributed Systems", "Cloud Native", "Serverless",

    # Mobile
    "React Native", "Flutter", "Android", "iOS", "SwiftUI",

    # Other
    "HTML", "CSS", "Tailwind CSS", "Bootstrap", "GraphQL",
    "LaTeX", "Markdown", "Excel", "Tableau", "Power BI",
}

# Alias map — maps variations to canonical names
SKILL_ALIASES = {
    "python3": "Python",
    "py": "Python",
    "js": "JavaScript",
    "javascript": "JavaScript",
    "typescript": "TypeScript",
    "ts": "TypeScript",
    "reactjs": "React",
    "react.js": "React",
    "nextjs": "Next.js",
    "vuejs": "Vue.js",
    "vue": "Vue.js",
    "nodejs": "Node.js",
    "node": "Node.js",
    "expressjs": "Express.js",
    "express": "Express.js",
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "mongo": "MongoDB",
    "mongodb": "MongoDB",
    "sk-learn": "scikit-learn",
    "sklearn": "scikit-learn",
    "tf": "TensorFlow",
    "tensorflow": "TensorFlow",
    "pytorch": "PyTorch",
    "torch": "PyTorch",
    "aws": "AWS",
    "amazon web services": "AWS",
    "gcp": "GCP",
    "google cloud": "GCP",
    "azure": "Azure",
    "microsoft azure": "Azure",
    "docker": "Docker",
    "k8s": "Kubernetes",
    "kubernetes": "Kubernetes",
    "git": "Git",
    "github": "GitHub",
    "gitlab": "GitLab",
    "ml": "Machine Learning",
    "machine learning": "Machine Learning",
    "dl": "Deep Learning",
    "deep learning": "Deep Learning",
    "nlp": "NLP",
    "natural language processing": "NLP",
    "cv": "Computer Vision",
    "computer vision": "Computer Vision",
    "rest": "REST API",
    "restful": "REST API",
    "rest api": "REST API",
    "ci/cd": "CI/CD",
    "cicd": "CI/CD",
    "html5": "HTML",
    "css3": "CSS",
    "tailwind": "Tailwind CSS",
    "c plus plus": "C++",
    "cplusplus": "C++",
    "csharp": "C#",
    "dotnet": "ASP.NET",
    ".net": "ASP.NET",
    "springboot": "Spring Boot",
    "spring": "Spring Boot",
    "django": "Django",
    "fastapi": "FastAPI",
    "flask": "Flask",
    "llm": "LLM",
    "large language model": "LLM",
    "rag": "RAG",
    "retrieval augmented generation": "RAG",
    "pen testing": "Penetration Testing",
    "pentest": "Penetration Testing",
    "infosec": "Cybersecurity",
    "information security": "Cybersecurity",
}


def normalize_skill(raw: str) -> str | None:
    """
    Normalize a raw skill string to its canonical name.
    Returns None if not recognized.
    """
    cleaned = raw.strip().lower()
    cleaned = re.sub(r"[^a-z0-9.#+\s/-]", "", cleaned)
    cleaned = " ".join(cleaned.split())

    # Check alias map first
    if cleaned in SKILL_ALIASES:
        return SKILL_ALIASES[cleaned]

    # Check direct match against taxonomy (case-insensitive)
    for canonical in SKILLS_TAXONOMY:
        if canonical.lower() == cleaned:
            return canonical

    return None


def extract_skills_from_text(text: str) -> list[str]:
    """
    Extract canonical skills from any text (resume or JD).
    Uses both direct taxonomy matching and alias resolution.
    Returns deduplicated list of canonical skill names.
    """
    found = set()
    text_lower = text.lower()

    # Check each canonical skill and its aliases
    for canonical in SKILLS_TAXONOMY:
        # Build pattern that matches whole words only
        pattern = r'\b' + re.escape(canonical.lower()) + r'\b'
        if re.search(pattern, text_lower):
            found.add(canonical)

    # Check aliases
    for alias, canonical in SKILL_ALIASES.items():
        pattern = r'\b' + re.escape(alias.lower()) + r'\b'
        if re.search(pattern, text_lower):
            found.add(canonical)

    return sorted(list(found))