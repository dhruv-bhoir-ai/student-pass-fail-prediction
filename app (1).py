import streamlit as st
import joblib
import numpy as np
import pandas as pd
import time

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="Student Report Card",
    page_icon="🎓",
    layout="wide"
)

# ---------------------------
# CSS (UI Enhancements)
# ---------------------------
st.markdown("""
<style>
/* Make it mobile friendly */
.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

/* Hide Streamlit branding */
footer {visibility: hidden;}
header {visibility: hidden;}

/* Animation */
@keyframes fadeUp {
    0% {opacity: 0; transform: translateY(10px);}
    100% {opacity: 1; transform: translateY(0);}
}
.fadeUp {
    animation: fadeUp 0.5s ease-in-out;
}

/* Card */
.card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 22px;
    padding: 18px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.18);
}

/* Report Header */
.reportTitle {
    font-size: 22px;
    font-weight: 900;
    margin-bottom: 4px;
}
.subText {
    opacity: 0.85;
    font-size: 13px;
}

/* Badge */
.badge {
    display: inline-block;
    padding: 7px 14px;
    border-radius: 999px;
    font-weight: 900;
    font-size: 13px;
    letter-spacing: 0.3px;
    border: 1px solid rgba(255,255,255,0.18);
}
.passBadge {
    background: rgba(46, 204, 113, 0.18);
    border: 1px solid rgba(46, 204, 113, 0.55);
    color: #2ecc71;
}
.failBadge {
    background: rgba(231, 76, 60, 0.18);
    border: 1px solid rgba(231, 76, 60, 0.55);
    color: #e74c3c;
}
.gradeBadge {
    background: rgba(52, 152, 219, 0.18);
    border: 1px solid rgba(52, 152, 219, 0.55);
    color: #3498db;
}

/* Buttons */
.stButton button {
    width: 100%;
    border-radius: 14px;
    padding: 0.75rem 1rem;
    font-weight: 900;
}

/* Responsive */
@media (max-width: 700px) {
    .reportTitle {font-size: 18px;}
    .block-container {padding-left: 0.8rem; padding-right: 0.8rem;}
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Load Model (same logic)
# ---------------------------
model = joblib.load("student_report_model.pkl")

# ---------------------------
# Header
# ---------------------------
st.markdown("<div class='fadeUp'>", unsafe_allow_html=True)
st.title("🎓 Pass/Fail Prediction System")
st.caption("Enter details → marks → generate a professional report card (with prediction).")
st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# Layout: Left Inputs | Right Preview
# ---------------------------
left, right = st.columns([1.05, 1.25], gap="large")

# ---------------------------
# LEFT SIDE: Inputs
# ---------------------------
with left:
    st.markdown("<div class='card fadeUp'>", unsafe_allow_html=True)
    st.subheader("🧾 Student Details")

    name = st.text_input("👤 Student Name", placeholder="Eg: palak")
    roll_no = st.text_input("🆔 Roll Number", placeholder="Eg: 24SCSE1430282")

    colA, colB = st.columns(2)
    with colA:
        division = st.selectbox("📌 Section ", ["A", "B", "C"])
    with colB:
        standard = st.selectbox("🏫 Standard", ["10th", "12th"])

    st.divider()
    st.subheader("📚 Enter Subject Marks")

    if standard == "10th":
        english = st.number_input("English", 0, 100)
        hindi = st.number_input("Hindi", 0, 100)
        punjabi = st.number_input("Punjabi", 0, 100)
        maths = st.number_input("Mathematics", 0, 100)
        science = st.number_input("Science", 0, 100)

        subjects = [english, hindi, punjabi, maths, science]
        subject_names = ["English", "Hindi", "punjabi", "Mathematics", "Science"]

    elif standard == "12th":
        physics = st.number_input("Physics", 0, 100)
        chemistry = st.number_input("Chemistry", 0, 100)
        maths = st.number_input("Mathematics", 0, 100)
        biology = st.number_input("Biology", 0, 100)
        english = st.number_input("English", 0, 100)

        subjects = [physics, chemistry, maths, biology, english]
        subject_names = ["Physics", "Chemistry", "Mathematics", "Biology", "English"]

    st.divider()
    generate = st.button("✨ Generate Report Card")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# RIGHT SIDE: Report Card Output
# ---------------------------
with right:
    st.markdown("<div class='card fadeUp'>", unsafe_allow_html=True)
    st.markdown("<div class='reportTitle'>📄 Report Card Preview</div>", unsafe_allow_html=True)
    st.markdown("<div class='subText'>Your report card will be generated here in a professional format.</div>", unsafe_allow_html=True)

    # Quick stats preview (before generate)
    total_preview = sum(subjects)
    percent_preview = (total_preview / 500) * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Marks", f"{total_preview}/500")
    col2.metric("Percentage", f"{percent_preview:.2f}%")
    col3.metric("Subjects", "5")

    st.progress(min(1.0, percent_preview / 100))
    st.caption("Progress bar shows overall percentage performance.")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# Generate Report Card (same logic)
# ---------------------------
if generate:

    with st.spinner("Generating report card... Please wait ⏳"):
        time.sleep(1.2)

        total_marks = sum(subjects)
        percentage = (total_marks / 500) * 100
        average_marks = total_marks / 5

        if percentage > 90:
            grade = "A"
        elif percentage >= 71:
            grade = "B"
        elif percentage >= 51:
            grade = "C"
        elif percentage >= 35:
            grade = "D"
        else:
            grade = "F"

        input_data = np.array([[average_marks, percentage]])
        prediction = model.predict(input_data)

        if any(mark < 35 for mark in subjects):
            result = "FAIL"
        else:
            if prediction[0] == 1:
                result = "PASS"
            else:
                result = "FAIL"

    st.markdown("<div class='fadeUp'>", unsafe_allow_html=True)
    st.subheader("📝 Student Details")

    student_info = pd.DataFrame({
        "Personal Details": ["Name", "Roll Number", "Section", "Standard"],
        "Value": [name, roll_no, division, standard]
    })
    st.dataframe(student_info, use_container_width=True, hide_index=True)

    st.subheader("📚 Subject-wise Marks")

    marks_table = pd.DataFrame({
        "Subject": subject_names,
        "Marks Obtained": subjects,
        "Max Marks": [100, 100, 100, 100, 100]
    })
    st.dataframe(marks_table, use_container_width=True, hide_index=True)

    st.subheader("📊 Result Summary")

    summary_table = pd.DataFrame({
        "Metric": ["Total Marks", "Percentage", "Grade", "Result"],
        "Value": [
            f"{total_marks} / 500",
            f"{round(percentage, 2)} %",
            grade,
            result
        ]
    })
    st.dataframe(summary_table, use_container_width=True, hide_index=True)

    # Badges
    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"<span class='badge gradeBadge'>🏅 Grade: {grade}</span>", unsafe_allow_html=True)
    with c2:
        if result == "PASS":
            st.markdown("<span class='badge passBadge'>✅ FINAL RESULT: PASS</span>", unsafe_allow_html=True)
        else:
            st.markdown("<span class='badge failBadge'>❌ FINAL RESULT: FAIL</span>", unsafe_allow_html=True)

    st.write("")
    if result == "PASS":
        st.success("✅ Result: PASS")
        st.balloons()
    else:
        st.error("❌ Result: FAIL")
        st.info("Suggestion: Improve marks above 35 in each subject for passing.")

    st.markdown("</div>", unsafe_allow_html=True)
