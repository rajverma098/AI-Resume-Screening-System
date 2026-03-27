from sentence_transformers import SentenceTransformer, util
import re

# ==============================
# 🔹 LOAD MODEL (only once)
# ==============================
model = SentenceTransformer('all-MiniLM-L6-v2')

# ==============================
# 🎯 SKILL DATABASE
# ==============================
SKILLS_DB = [
    "python", "java", "c++", "machine learning", "deep learning",
    "nlp", "data analysis", "sql", "mongodb", "react", "node",
    "mern", "django", "flask", "aws", "docker", "kubernetes",
    "tensorflow", "pandas", "numpy", "scikit-learn", "html", "css", "javascript"
]

# ==============================
# 🧹 CLEAN TEXT
# ==============================
def clean_text(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# ==============================
# 🧠 SIMILARITY FUNCTION
# ==============================
def get_similarity(text1, text2):
    emb1 = model.encode(text1, convert_to_tensor=True)
    emb2 = model.encode(text2, convert_to_tensor=True)
    return float(util.cos_sim(emb1, emb2))

# ==============================
# 📂 SMART SECTION EXTRACTION
# ==============================
def extract_sections(text):
    text = clean_text(text)

    skills = ""
    experience = ""
    education = ""

    # Simple regex-based extraction
    skills_match = re.search(r"(skills|technical skills)(.*?)(experience|projects|education)", text, re.DOTALL)
    exp_match = re.search(r"(experience|work experience)(.*?)(education|projects|skills)", text, re.DOTALL)
    edu_match = re.search(r"(education)(.*)", text, re.DOTALL)

    if skills_match:
        skills = skills_match.group(2)

    if exp_match:
        experience = exp_match.group(2)

    if edu_match:
        education = edu_match.group(2)

    return skills, experience, education

# ==============================
# 🎯 SKILL EXTRACTION (Improved)
# ==============================
def extract_skills(text):
    text = clean_text(text)
    found = []

    for skill in SKILLS_DB:
        if re.search(rf"\b{skill}\b", text):
            found.append(skill)

    return list(set(found))

# ==============================
# ❌ MISSING SKILLS
# ==============================
def get_missing_skills(job_desc, resume):
    jd_skills = set(extract_skills(job_desc))
    resume_skills = set(extract_skills(resume))

    return list(jd_skills - resume_skills)

# ==============================
# 📊 DETAILED SCORING
# ==============================
def detailed_scores(job_desc, resume):
    skill_r, exp_r, edu_r = extract_sections(resume)

    skill_score = get_similarity(job_desc, skill_r or resume)
    exp_score = get_similarity(job_desc, exp_r or resume)
    edu_score = get_similarity(job_desc, edu_r or resume)

    final_score = (skill_score * 0.5) + (exp_score * 0.3) + (edu_score * 0.2)

    return {
        "skill_score": round(skill_score, 3),
        "experience_score": round(exp_score, 3),
        "education_score": round(edu_score, 3),
        "final_score": round(final_score, 3)
    }

# ==============================
# 💬 AI FEEDBACK SYSTEM
# ==============================
def generate_feedback(job_desc, resume):
    missing_skills = get_missing_skills(job_desc, resume)
    feedback = []

    if missing_skills:
        feedback.append(f"❗ Add missing skills: {', '.join(missing_skills)}")

    if len(extract_skills(resume)) < 5:
        feedback.append("⚠️ Add more technical skills.")

    if "project" not in resume.lower():
        feedback.append("📌 Add 1-2 strong projects with description.")

    if "experience" not in resume.lower():
        feedback.append("💼 Clearly mention your work experience.")

    if "achievements" not in resume.lower():
        feedback.append("🏆 Add measurable achievements (numbers, impact).")

    if not feedback:
        feedback.append("✅ Resume looks strong!")

    return feedback

# ==============================
# ✨ PROFESSIONAL RESUME GENERATOR
# ==============================
def generate_professional_resume(name, skills, experience, projects):

    skills_text = "\n".join([f"• {s}" for s in skills])
    projects_text = "\n".join([f"• {p}" for p in projects])

    resume = f"""
{name.upper()}

========================================

PROFESSIONAL SUMMARY
Results-driven professional skilled in {', '.join(skills[:5])}.
Experienced in building scalable, high-performance applications.

----------------------------------------

SKILLS
{skills_text}

----------------------------------------

EXPERIENCE
{experience}

----------------------------------------

PROJECTS
{projects_text}

----------------------------------------

ACHIEVEMENTS
• Built impactful AI/ML applications
• Strong problem-solving mindset
• Delivered real-world solutions

========================================
"""
    return resume.strip()

# ==============================
# 🔥 UPDATED RESUME GENERATOR
# ==============================
def generate_updated_resume(resume, missing_skills):

    if not missing_skills:
        return "✅ No major improvements needed."

    skills_section = "\n".join([f"• {skill}" for skill in missing_skills])

    updated_resume = f"""
UPDATED RESUME SUGGESTION
========================================

{resume}

----------------------------------------
ADD THESE SKILLS:

{skills_section}

----------------------------------------
IMPROVEMENTS:
• Add missing skills in Skills section
• Use action verbs (Developed, Built, Optimized)
• Add measurable results (e.g., increased performance by 30%)

========================================
"""
    return updated_resume.strip()