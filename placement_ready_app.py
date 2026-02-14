import pickle
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# ------------------------------
# Load ML model and encoder (optional if you plan to use later)
# ------------------------------
try:
    model = pickle.load(open('rf_model.pkl', 'rb'))
    le = pickle.load(open('le_encoder.pkl', 'rb'))
except FileNotFoundError:
    st.warning("Model files not found. CSV recommendations won't work.")

# ------------------------------
# 1️⃣ Readiness calculation function
# ------------------------------
def calculate_readiness(dsa, core_cs, aptitude, mock, communication, projects, internship, cgpa):
    communication_scaled = (communication / 5) * 100
    projects_scaled = (projects / 5) * 100
    internship_scaled = (internship / 6) * 100
    cgpa_scaled = (cgpa / 10) * 100

    score = (
        0.20 * dsa +
        0.15 * core_cs +
        0.15 * projects_scaled +
        0.15 * internship_scaled +
        0.12 * mock +
        0.09 * aptitude +
        0.09 * communication_scaled +
        0.05 * cgpa_scaled
    )

    if score < 40:
        category = "Beginner"
    elif score < 60:
        category = "Developing"
    elif score < 70:
        category = "Almost Ready"
    else:
        category = "Placement Ready"

    suggestions = []
    if dsa < 70:
        suggestions.append(f"Improve DSA by {max(0, 70 - dsa):.1f} points")
    if core_cs < 65:
        suggestions.append(f"Improve Core CS by {max(0, 65 - core_cs):.1f} points")
    if aptitude < 60:
        suggestions.append(f"Improve Aptitude by {max(0, 60 - aptitude):.1f} points")
    if mock < 60:
        suggestions.append(f"Practice Mock Interviews to reach 60+")
    if projects < 3:
        suggestions.append(f"Work on {max(0, 3 - projects):.0f} strong projects")
    if internship < 2:
        suggestions.append(f"Gain at least {max(0, 2 - internship):.0f} months internship")
    if cgpa < 7:
        suggestions.append(f"Focus on CGPA improvement to reach 7+")
    if communication < 3:
        suggestions.append(f"Improve communication skills")

    skill_data = {
        "DSA": dsa,
        "Core CS": core_cs,
        "Aptitude": aptitude,
        "Mock Interview": mock,
        "Communication": communication_scaled,
        "Projects": projects_scaled,
        "Internship": internship_scaled,
        "CGPA": cgpa_scaled
    }

    return score, category, suggestions, skill_data

# ------------------------------
# 2️⃣ Homepage
# ------------------------------
def show_homepage():
    st.title("🚀 AI-Powered Placement Readiness Tool")
    st.markdown("### Personalized insights and actionable suggestions to prepare for placements.")
    st.markdown("---")

    st.markdown("""
    <div style="background-color:#000000;padding:30px;border-radius:10px">
        <h2 style='color:#ffffff'>Get Ready for Your Dream Job</h2>
        <p>Enter your scores, understand your strengths, and get personalized suggestions to improve.</p>
        <a href="#calculator" style="background-color:#000000;color:white;padding:10px 20px;border-radius:5px;text-decoration:none;">Calculate Readiness</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### ⭐ Key Features")
    cols = st.columns(4)
    features = [
        ("🎯 Personalized Score", "Custom readiness score based on your skills and projects."),
        ("📊 Skill Analysis", "Color-coded bars showing your strengths and gaps."),
        ("💼 Project & Internship Insights", "Evaluate your hands-on experience."),
        ("📝 Mock Interview Guidance", "Get actionable suggestions for improvement.")
    ]
    for col, (title, desc) in zip(cols, features):
        col.markdown(f"""
        <div style="background-color:#000000;padding:15px;border-radius:10px;text-align:center">
            <h3>{title}</h3>
            <p>{desc}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🗣️ Testimonials")
    cols = st.columns(3)
    testimonials = [
        ("Priya Sharma", "Software Intern at Infosys", "I improved my readiness score by 30 points thanks to this tool!"),
        ("Rahul Verma", "Data Science Intern at TCS", "Clear actionable suggestions made preparation easier."),
        ("Ananya Singh", "AI Intern at Accenture", "I could focus on weak areas effectively and boost my skills.")
    ]
    for col, (name, role, text) in zip(cols, testimonials):
        col.markdown(f"""
        <div style="background-color:#000000;padding:15px;border-radius:10px">
            <strong>{name}</strong><br><em>{role}</em>
            <p>{text}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📌 Ready to Check Your Placement Readiness?")
    if st.button("Go to Calculator"):
        st.session_state.page = "calculator"

# ------------------------------
# 3️⃣ Calculator Page (Single Learner Only)
# ------------------------------
def show_calculator():
    import matplotlib.pyplot as plt
    import seaborn as sns

    st.title("📊 Placement Readiness Calculator")
    st.markdown("Enter your scores below to see your readiness, skill gaps, and improvement suggestions.")

    dsa = st.number_input("DSA Score (0-100)", min_value=0, max_value=100, value=50)
    core_cs = st.number_input("Core CS Score (0-100)", min_value=0, max_value=100, value=60)
    aptitude = st.number_input("Aptitude Score (0-100)", min_value=0, max_value=100, value=50)
    mock = st.number_input("Mock Interview Score (0-100)", min_value=0, max_value=100, value=45)
    communication = st.slider("Communication Rating (1-5)", 1.0, 5.0, 3.0)
    projects = st.number_input("Number of Strong Projects (0-5)", min_value=0, max_value=5, value=2)
    internship = st.number_input("Internship Duration (months)", min_value=0, max_value=6, value=1)
    cgpa = st.number_input("CGPA (0-10)", min_value=0.0, max_value=10.0, value=6.8)

    if st.button("Calculate"):
        score, category, suggestions, skill_data = calculate_readiness(
            dsa, core_cs, aptitude, mock, communication, projects, internship, cgpa
        )

        st.subheader(f"Your Readiness Score: {score:.2f}")
        st.subheader(f"Category: {category}")

        # -------------------- Skill Bars with Color --------------------
        st.markdown("### Skill Overview")
        for skill, val in skill_data.items():
            if val < 50:
                color = "#d62728"  # red
            elif val < 70:
                color = "#ff7f0e"  # orange
            else:
                color = "#2ca02c"  # green

            st.markdown(f"""
                <div style="margin-bottom:10px">
                    <strong>{skill}: {val:.1f}%</strong>
                    <div style="background-color:#e0e0e0;border-radius:5px;width:100%;height:20px;">
                        <div style="width:{val}%;background-color:{color};height:20px;border-radius:5px"></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        # -------------------- Radar Chart --------------------
        categories = list(skill_data.keys())
        values = list(skill_data.values())
        values += values[:1]  # close the loop
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories + categories[:1],
            fill='toself',
            name='Skill Levels'
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0,100])),
            showlegend=False
        )
        st.plotly_chart(fig)

        # -------------------- Suggestions --------------------
        st.markdown("### Suggestions to Improve")
        if suggestions:
            for s in suggestions:
                st.write(f"- {s}")
        else:
            st.write("Great job! You are Placement Ready!")

    if st.button("Return to Home"):
        st.session_state.page = "home"

# ------------------------------
# 4️⃣ App Navigation
# ------------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    show_homepage()
else:
    show_calculator()
