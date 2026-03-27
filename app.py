import streamlit as st
from utils import extract_text_from_pdf, clean_text
from model import (
    detailed_scores,
    generate_feedback,
    get_missing_skills,
    generate_updated_resume,
    generate_professional_resume
)
st.markdown("""
<style>
.main {
    background-color: #0f172a;
    color: white;
}
h1, h2, h3 {
    color: #38bdf8;
}
.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)
st.set_page_config(page_title="AI Resume Screener", layout="wide")

st.title("📄 AI Resume Screening System")

# =========================
# 📌 JOB DESCRIPTION
# =========================
job_desc = st.text_area("Enter Job Description")

uploaded_files = st.file_uploader(
    "Upload Resumes (PDF)", 
    accept_multiple_files=True
)

# =========================
# 🧠 RESUME BUILDER
# =========================
st.subheader("🧠 AI Resume Builder")

name_input = st.text_input("Your Name")
skills_input = st.text_input("Skills (comma separated)")
experience_input = st.text_area("Experience")
projects_input = st.text_area("Projects (one per line)")

if st.button("✨ Generate Resume"):
    if name_input and skills_input:
        skills = [s.strip() for s in skills_input.split(",")]
        projects = [p.strip() for p in projects_input.split("\n") if p.strip()]

        resume = generate_professional_resume(
            name_input,
            skills,
            experience_input,
            projects
        )

        st.success("✅ Resume Generated!")
        st.text_area("Your Resume", resume, height=300)

        st.download_button(
            "📥 Download Resume",
            resume,
            file_name="generated_resume.txt"
        )
    else:
        st.warning("Enter name and skills")

# =========================
# 🔍 ANALYSIS
# =========================
if st.button("🔍 Analyze Resumes"):

    if not uploaded_files:
        st.warning("Upload resumes first")
    
    elif not job_desc:
        st.warning("Enter job description")
    
    else:
        resumes = []
        names = []

        # 📄 Extract text
        for file in uploaded_files:
            try:
                text = extract_text_from_pdf(file)
                text = clean_text(text)

                if text.strip():
                    resumes.append(text)
                    names.append(file.name)
            except:
                st.error(f"Error reading {file.name}")

        job_desc_clean = clean_text(job_desc)

        results = []

        # 📊 Scoring
        for i in range(len(resumes)):
            scores = detailed_scores(job_desc_clean, resumes[i])

            results.append((
                names[i],
                resumes[i],
                scores["skill_score"],
                scores["experience_score"],
                scores["education_score"],
                scores["final_score"]
            ))

        # 🏆 Sort
        results.sort(key=lambda x: x[5], reverse=True)

        # =========================
        # 🏆 TOP 3
        # =========================
        st.subheader("🏆 Top Candidates")

        for name, resume_text, skill, exp, edu, final in results[:3]:
            st.success(f"⭐ {name}")

            st.write(f"**Final Score:** {round(final*100,2)}%")
            st.progress(final)

            col1, col2, col3 = st.columns(3)
            col1.metric("Skill Match", f"{round(skill*100,2)}%")
            col2.metric("Experience Match", f"{round(exp*100,2)}%")
            col3.metric("Education Match", f"{round(edu*100,2)}%")

            # 🧠 Feedback
            feedback = generate_feedback(job_desc_clean, resume_text)

            st.write("🧠 AI Feedback:")
            for f in feedback:
                st.write(f"✔ {f}")

            # 📥 Improved Resume
            missing_skills = get_missing_skills(job_desc_clean, resume_text)
            updated_resume = generate_updated_resume(resume_text, missing_skills)

            st.download_button(
                label="📥 Download Improved Resume",
                data=updated_resume,
                file_name=f"improved_{name}.txt",
                mime="text/plain"
            )

            st.markdown("---")

        # =========================
        # 📄 ALL CANDIDATES
        # =========================
        st.subheader("📄 All Candidates")

        for name, _, _, _, _, final in results:
            st.write(f"{name} — {round(final*100,2)}%")