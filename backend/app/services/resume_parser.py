# app/services/resume_parser.py
import re
import fitz  # PyMuPDF


def extract_text(file_bytes: bytes) -> str:
    """Extract raw text from PDF bytes using PyMuPDF."""
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text.strip()


def parse_sections(raw_text: str) -> dict:
    """
    Detect and extract resume sections from raw text.
    Returns structured JSON with skills, experience, education, projects.
    """
    lines = raw_text.split("\n")
    lines = [l.strip() for l in lines if l.strip()]

    sections = {
        "skills": [],
        "experience": [],
        "education": [],
        "projects": [],
        "raw_sections": {}
    }

    # Section header keywords
    section_map = {
        "skills": ["skills", "technical skills", "core competencies", "technologies"],
        "experience": ["experience", "work experience", "employment", "internship"],
        "education": ["education", "academic background", "qualifications"],
        "projects": ["projects", "personal projects", "academic projects"],
    }

    current_section = None
    current_content = []

    for line in lines:
        line_lower = line.lower()

        # Check if this line is a section header
        matched_section = None
        for section, keywords in section_map.items():
            if any(kw in line_lower for kw in keywords) and len(line) < 50:
                matched_section = section
                break

        if matched_section:
            # Save previous section content
            if current_section and current_content:
                sections["raw_sections"][current_section] = current_content
            current_section = matched_section
            current_content = []
        else:
            if current_section:
                current_content.append(line)

    # Save last section
    if current_section and current_content:
        sections["raw_sections"][current_section] = current_content

    # Extract skills as a flat list
    if "skills" in sections["raw_sections"]:
        skill_text = " ".join(sections["raw_sections"]["skills"])
        # Split by common delimiters
        raw_skills = re.split(r"[,|•·\n/]", skill_text)
        sections["skills"] = [s.strip() for s in raw_skills if len(s.strip()) > 1]

    # Keep experience/education/projects as line arrays
    sections["experience"] = sections["raw_sections"].get("experience", [])
    sections["education"] = sections["raw_sections"].get("education", [])
    sections["projects"] = sections["raw_sections"].get("projects", [])

    return sections