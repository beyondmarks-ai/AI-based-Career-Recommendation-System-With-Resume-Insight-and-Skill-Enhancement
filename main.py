import streamlit as st
import streamlit.components.v1 as components
import re
from ats_checker import check_ats_compliance
from resume_parser import extract_resume_text
from roadmap_generator import evaluate_resume


def extract_score(text):
    patterns = [
        r"(?i)(?:rating|score)\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*/\s*10",
        r"(?i)(?:rating|score)\s*[:\-]?\s*(\d+(?:\.\d+)?)\b",
        r"(\d+(?:\.\d+)?)\s*/\s*10",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            value = float(match.group(1))
            return max(0.0, min(10.0, value))
    return None


def to_bullet_markdown(text):
    lines = [line.strip(" -•\t") for line in text.splitlines() if line.strip()]
    if not lines:
        return "- No points generated."
    return "\n".join(f"- **{line}**" for line in lines)


def extract_section(text, section_name):
    pattern = rf"(?is){re.escape(section_name)}\s*:?\s*(.*?)(?=\n\s*[A-Z][A-Za-z ]+\s*:|\Z)"
    match = re.search(pattern, text)
    if not match:
        return ""
    return match.group(1).strip()


def render_score_donut(score_value, label, color):
    if score_value is None:
        st.info(f"{label}: score not found in model output.")
        return

    percent = max(0.0, min(100.0, (score_value / 10.0) * 100.0))

    st.markdown(
        f"<h4 style='margin-bottom:0; color:{color};'>{label}: <b>{score_value:.1f}/10</b></h4>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div style="display:flex; align-items:center; justify-content:center; margin:8px 0 14px 0;">
            <div style="
                width:120px;
                height:120px;
                border-radius:50%;
                background:conic-gradient({color} {percent:.1f}%, #E6EAF2 0);
                display:flex;
                align-items:center;
                justify-content:center;">
                <div style="
                    width:82px;
                    height:82px;
                    border-radius:50%;
                    background:#FFFFFF;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    color:{color};
                    font-weight:700;
                    font-size:18px;">
                    {percent:.0f}%
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.set_page_config(page_title="📄 Beyond Marks AI Academy", layout="centered")
st.title("📄 Beyond Marks AI Academy")

st.markdown(
    "<p style='color:#4B5563; font-size:16px;'>Upload your resume (<b>PDF</b> or <b>DOCX</b>), choose role and language, then get a styled analysis with visual scoring.</p>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align:center; color:#6B7280; font-size:13px; margin-top:-6px;'>Copyright © 2026 Beyond Marks AI Academy. All rights reserved.</p>",
    unsafe_allow_html=True,
)

# Upload resume
uploaded_file = st.file_uploader("📤 Upload Resume", type=["pdf", "docx"])

# Text input for target role (replaces dropdown)
target_role = st.text_input("🎯 Target Job Role", placeholder="e.g. Data Scientist, Backend Engineer")

# Output language selector
language = st.selectbox("🌐 Output Language", ["English", "Hindi", "French"])

# Evaluate button
if st.button("🔍 Evaluate Resume"):
    if uploaded_file is None or not target_role:
        st.error("⚠️ Please upload a resume and enter your target role.")
    else:
        with st.spinner("Analyzing your resume..."):
            # Extract resume text
            resume_text = extract_resume_text(uploaded_file)

            # Evaluate using LLM
            feedback = evaluate_resume(resume_text, tone=target_role, language=language)
            summary = feedback.strip()

            ats_feedback = check_ats_compliance(resume_text, target_role)

            resume_score = extract_score(summary)
            ats_score = extract_score(ats_feedback)

            st.markdown("### 🎯 Visual Score Overview")
            col1, col2 = st.columns(2)
            with col1:
                render_score_donut(resume_score, "Resume Quality", "#4F46E5")
            with col2:
                render_score_donut(ats_score, "ATS Compatibility", "#059669")

            with st.expander("📋 Resume Evaluation Results", expanded=True):
                st.markdown(
                    "<p style='color:#1D4ED8; font-weight:700;'>Key Insights</p>",
                    unsafe_allow_html=True,
                )
                areas_for_improvement = extract_section(summary, "Areas for Improvement")
                strengths = extract_section(summary, "Strengths")
                action_plan = extract_section(summary, "Action Plan")
                final_rating = extract_section(summary, "Final Rating")

                if areas_for_improvement:
                    st.markdown(
                        """
                        <div style="background:#FEF2F2; border-left:6px solid #DC2626; padding:12px 14px; border-radius:8px; margin-bottom:12px;">
                            <div style="color:#991B1B; font-size:17px; font-weight:800; margin-bottom:4px;">Areas for Improvement</div>
                            <div style="color:#7F1D1D; font-size:13px; font-weight:600;">Priority items to improve recruiter impact and role fit.</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.markdown(to_bullet_markdown(areas_for_improvement))

                    if strengths:
                        st.markdown(
                            "<p style='color:#1E3A8A; font-size:16px; font-weight:700; margin-top:12px;'>Strengths</p>",
                            unsafe_allow_html=True,
                        )
                        st.markdown(to_bullet_markdown(strengths))

                    if action_plan:
                        st.markdown(
                            "<p style='color:#0F766E; font-size:16px; font-weight:700; margin-top:12px;'>Action Plan</p>",
                            unsafe_allow_html=True,
                        )
                        st.markdown(to_bullet_markdown(action_plan))

                    if final_rating:
                        st.markdown(
                            f"<p style='color:#4C1D95; font-size:15px; font-weight:800; margin-top:10px;'>Final Rating: {final_rating}</p>",
                            unsafe_allow_html=True,
                        )
                else:
                    st.markdown(to_bullet_markdown(summary))

            with st.expander("🤖 ATS Analysis Results", expanded=False):
                st.markdown(
                    "<p style='color:#047857; font-weight:700;'>ATS Pointers</p>",
                    unsafe_allow_html=True,
                )
                st.markdown(to_bullet_markdown(ats_feedback))

            # Copy to clipboard button
            components.html(f"""
                <textarea id="copyText" style="display:none;">{summary}</textarea>
                <button onclick="copyText()" style="
                    background-color:#0072b1;
                    color:white;
                    padding:10px 16px;
                    font-size:14px;
                    border:none;
                    border-radius:8px;
                    cursor:pointer;
                    margin-top:10px;">
                    📋 Copy Resume Evaluation
                </button>
                <script>
                    function copyText() {{
                        var textArea = document.getElementById('copyText');
                        textArea.style.display = 'block';
                        textArea.select();
                        document.execCommand('copy');
                        textArea.style.display = 'none';
                        alert('✅ Evaluation copied to clipboard!');
                    }}
                </script>
            """, height=100)

        st.caption("💡 Tip: Improve your resume using these pointers and re-upload to increase both scores.")
