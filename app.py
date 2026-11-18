

import streamlit as st
import re
from google import genai
# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="BrandShield AI",
    page_icon="🛡️",
    layout="wide"
)

# ==========================================
# CUSTOM CSS STYLING
# ==========================================

st.markdown("""
<style>

.stApp {
    background-color: #F5F7FB;
}

[data-testid="stSidebar"] {
    background-color: #172554;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

h1, h2, h3 {
    color: #172554;
    font-weight: 700;
}

.stButton > button {
    background-color: #2563EB;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 8px 18px;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #1D4ED8;
    color: white;
}

[data-testid="stMetric"] {
    background-color: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #E2E8F0;
}

.stTextInput input,
.stTextArea textarea {
    border-radius: 8px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# SESSION STORAGE
# ==========================================

if "brand" not in st.session_state:
    st.session_state.brand = {}

if "content" not in st.session_state:
    st.session_state.content = ""

if "issues" not in st.session_state:
    st.session_state.issues = []

if "ai_analysis" not in st.session_state:
    st.session_state.ai_analysis = ""

if "decision" not in st.session_state:
    st.session_state.decision = "Pending"

if "history" not in st.session_state:
    st.session_state.history = []

# ==========================================
# CONTENT ANALYSIS FUNCTION
# ==========================================

def analyze_content(content, brand):

    issues = []

    # 1. Check prohibited words

    
    # 1. Check prohibited words and their variations

    prohibited_words = [
        word.strip()
        for word in brand.get("prohibited", "").split(",")
        if word.strip()
    ]

    prohibited_variations = {
        "guaranteed": r"\bguarantee(?:s|d|ing)?\b",
        "best in the world": r"\bbest\b.{0,60}\bin the world\b",
        "100% cure": r"\b100\s*%\s*cure(?:s|d|ing)?\b",
        "permanent solution": r"\bpermanent(?:ly)?\b.{0,40}\b(?:solution|cure|results?)\b",
        "no side effects": r"\b(?:no|zero)\s+side effects?\b",
        "zero risk": r"\b(?:zero|no)\s+risk\b",
        "overnight transformation": r"\bovernight\b.{0,40}\b(?:transformation|results?|flawless skin)\b"
    }

    for word in prohibited_words:

        key = word.lower()

        pattern = prohibited_variations.get(
            key,
            r"\b" + re.escape(word) + r"\b"
        )

        if re.search(pattern, content, re.IGNORECASE):

            issue = "Prohibited word detected: " + word

            if issue not in issues:
                issues.append(issue)


    # 2. Check potentially unsupported claims

    risky_phrases = [
        r"\b100\s*%\s*results?\b",
        r"\bguarantee(?:s|d|ing)?\b",
        r"\bcures?\b",
        r"\bpermanent(?:ly)?\s+(?:cure|solution|results?)\b",
        r"\bclinically proven\b",
        r"\binstant results?\b",
        r"\brisk[- ]free\b",
        r"\bresults for everyone\b",
        r"\bzero side effects?\b",
        r"\bno side effects?\b",
        r"\bzero risk\b",
        r"\bovernight\b",
        r"\bflawless skin\b"
    ]

    for pattern in risky_phrases:

        match = re.search(pattern, content, re.IGNORECASE)

        if match:

            issue = (
                "Potentially unsupported claim: " + match.group(0)
            )

            if issue not in issues:
                issues.append(issue)


    # 3. Check brand tone

    tone = brand.get("tone", "").lower()

    formal_words = [
        "hereby",
        "therefore",
        "furthermore",
        "pursuant",
        "shall"
    ]

    casual_words = [
        "awesome",
        "hey",
        "wow",
        "super cool",
        "gonna"
    ]

    if tone == "friendly":

        for word in formal_words:

            if re.search(
                r"\b" + re.escape(word) + r"\b",
                content,
                re.IGNORECASE
            ):

                issues.append(
                    "The content may sound too formal "
                    "for a friendly brand tone."
                )
                break

    elif tone == "formal":

        for word in casual_words:

            if re.search(
                r"\b" + re.escape(word) + r"\b",
                content,
                re.IGNORECASE
            ):

                issues.append(
                    "The content may sound too casual "
                    "for a formal brand tone."
                )
                break

    # 4. Check additional brand rules

    rules = brand.get("rules", "").lower()

    if "medical claims" in rules or "medical claim" in rules:

        medical_phrases = [
            "cure",
            "treats disease",
            "heals disease",
            "medically proven"
        ]

        for phrase in medical_phrases:

            if re.search(
                r"\b" + re.escape(phrase) + r"\b",
                content,
                re.IGNORECASE
            ):

                issue = (
                    "Possible medical claim detected: " + phrase
                )

                if issue not in issues:
                    issues.append(issue)

    # 5. Create analysis report

    report = []

    report.append("BRANDSHIELD AI - CONTENT ANALYSIS")
    report.append("=" * 40)

    report.append(
        "Brand Name: " + brand.get("name", "")
    )

    report.append(
        "Expected Tone: " + brand.get("tone", "")
    )

    report.append("")

    report.append("CHECKING RESULTS")
    report.append("-" * 30)

    if issues:

        report.append(
            str(len(issues)) + " potential issue(s) found."
        )

        for issue in issues:
            report.append("- " + issue)

    else:

        report.append(
            "No issues detected by the current checking rules."
        )

    # 6. Suggestions

    report.append("")
    report.append("IMPROVEMENT SUGGESTIONS")
    report.append("-" * 30)

    if issues:

        report.append(
            "Review the flagged words and claims."
        )

        report.append(
            "Replace prohibited words with approved alternatives."
        )

        report.append(
            "Provide reliable evidence for factual and performance claims."
        )

        report.append(
            "Make sure the content matches the selected brand tone."
        )

    else:

        report.append(
            "Continue following the saved brand guidelines."
        )

        report.append(
            "Ensure all factual claims have supporting evidence."
        )

        report.append(
            "Maintain a consistent brand tone."
        )

    approved_words = brand.get("approved", "").strip()

    if approved_words:

        report.append("")
        report.append(
            "Approved brand words: " + approved_words
        )

    return issues, "\n".join(report)


# ==========================================
# SIDEBAR NAVIGATION
# ==========================================


# ==========================================
# SIDEBAR NAVIGATION
# ==========================================

st.sidebar.title("🛡️ BrandShield AI")

st.sidebar.caption(
    "Your Brand's Intelligent Guardian"
)

st.sidebar.divider()

st.sidebar.subheader("Main Menu")

page = st.sidebar.radio(
    "Navigate to",
    [
         "Dashboard",
        "Brand Guidelines",
        "Content Checker",
        "Review Suggestions",
        "Analysis History",
        "Project Information"
    ],
    index=0
)

st.sidebar.divider()

st.sidebar.subheader("About")

st.sidebar.write(
    "BrandShield AI helps maintain brand consistency "
    "by identifying content violations and supporting "
    "human review."
)

st.sidebar.divider()

st.sidebar.caption(
    "🛡️ BrandShield AI | Project Edition"
)

st.sidebar.caption(
    "Powered by Python and Streamlit"
)

# ==========================================
# DASHBOARD
# ==========================================



if page == "Dashboard":

    st.title("🛡️ BrandShield AI")

    st.subheader("Your Brand's Intelligent Guardian")

    st.write("Every Content. One Consistent Brand.")

    st.divider()

    # ==========================================
    # DASHBOARD METRICS
    # ==========================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Brand Profile",
            "Created" if st.session_state.brand else "Not Created"
        )

    with col2:
        st.metric(
            "Total Analyses",
            len(st.session_state.history)
        )

    with col3:
        st.metric(
            "Detected Issues",
            len(st.session_state.issues)
        )

    with col4:
        compliance_score = max(
            0,
            100 - len(st.session_state.issues) * 10
        )

        st.metric(
            "Compliance Score",
            f"{compliance_score}%"
        )

    st.divider()

    # ==========================================
    # PROJECT STATUS
    # ==========================================

    st.subheader("📊 Project Status")

    if st.session_state.brand:

        st.success(
            f"Brand Profile: "
            f"{st.session_state.brand.get('name', 'Created')}"
        )

    else:

        st.warning("Brand Profile: Not created yet")

    st.write(
        f"Total content analyses completed: "
        f"{len(st.session_state.history)}"
    )

    st.write(
        f"Current review decision: "
        f"{st.session_state.decision}"
    )

    st.divider()

    # ==========================================
    # RECENT ACTIVITY
    # ==========================================

    st.subheader("🕒 Recent Activity")

    if st.session_state.history:

        recent_history = st.session_state.history[-5:][::-1]

        for index, item in enumerate(recent_history, start=1):

            st.write(
                f"**{index}. Brand:** "
                f"{item.get('brand', 'Unknown')}"
            )

            st.write(
                f"Detected Issues: "
                f"{len(item.get('issues', []))}"
            )

            st.caption(
                item.get('content', '')[:100] + "..."
            )

            st.divider()

    else:

        st.info(
            "No recent activity yet. "
            "Check some content to see your activity here."
        )

    # ==========================================
    # ABOUT BRANDSHIELD AI
    # ==========================================

    st.subheader("About BrandShield AI")

    st.write(
        "BrandShield AI is a brand governance platform "
        "that checks marketing content against saved brand "
        "guidelines, identifies potential violations, and "
        "supports human review before publishing."
    )

    # ==========================================
    # HOW IT WORKS
    # ==========================================

    st.header("How it works")

    st.write("1. Add your brand guidelines.")
    st.write("2. Submit content for checking.")
    st.write("3. Identify possible brand violations.")
    st.write("4. Review suggestions before publishing.")

    st.divider()

    st.caption(
        "BrandShield AI uses Python-based rule checking. "
        "Gemini integration is optional and may be temporarily "
        "unavailable. Rule-based checking remains available."
    )


# ==========================================
# BRAND GUIDELINES
# ==========================================

elif page == "Brand Guidelines":

    st.title("📘 Brand Guidelines")

    st.write(
        "Define your brand identity and communication rules."
    )

    with st.form("brand_form"):

        brand_name = st.text_input(
            "Brand Name",
            value=st.session_state.brand.get("name", "")
        )

        description = st.text_area(
            "Brand Description",
            value=st.session_state.brand.get("description", ""),
            placeholder="Describe your brand and its products..."
        )

        audience = st.text_input(
            "Target Audience",
            value=st.session_state.brand.get("audience", ""),
            placeholder="Example: Young adults, professionals"
        )

        tone_options = [
            "Professional",
            "Friendly",
            "Formal",
            "Creative",
            "Casual",
            "Bold"
        ]

        saved_tone = st.session_state.brand.get(
            "tone", "Professional"
        )

        tone_index = (
            tone_options.index(saved_tone)
            if saved_tone in tone_options
            else 0
        )

        tone = st.selectbox(
            "Brand Tone",
            tone_options,
            index=tone_index
        )

        approved_terms = st.text_area(
            "Approved Words or Phrases",
            value=st.session_state.brand.get("approved", ""),
            placeholder="Example: Everyday comfort"
        )

        prohibited_words = st.text_area(
            "Words to Avoid",
            value=st.session_state.brand.get("prohibited", ""),
            placeholder="Example: Guaranteed, miracle"
        )

        additional_rules = st.text_area(
            "Additional Brand Rules",
            value=st.session_state.brand.get("rules", ""),
            placeholder="Example: Avoid unsupported medical claims."
        )

        submitted = st.form_submit_button(
            "Save Guidelines"
        )

        if submitted:

            if not brand_name.strip():

                st.error("Please enter your brand name.")

            else:

                st.session_state.brand = {
                    "name": brand_name,
                    "description": description,
                    "audience": audience,
                    "tone": tone,
                    "approved": approved_terms,
                    "prohibited": prohibited_words,
                    "rules": additional_rules
                }

                st.success(
                    "Brand guidelines saved successfully!"
                )

    if st.session_state.brand:

        st.divider()

        st.subheader("Saved Brand Information")

        for key, value in st.session_state.brand.items():

            st.write(
                f"**{key.title()}:** {value}"
            )


# ==========================================
# CONTENT CHECKER
# ==========================================


# ==========================================
# CONTENT CHECKER
# ==========================================

elif page == "Content Checker":

    st.title("🔍 Content Checker")

    if not st.session_state.brand:

        st.warning(
            "Please add your brand guidelines first."
        )

    else:

        brand = st.session_state.brand

        st.write(
            "Checking content for brand:",
            brand["name"]
        )

        content = st.text_area(
            "Enter content to check",
            value=st.session_state.content,
            placeholder="Paste your marketing content here..."
        )

        if st.button("Check Content"):

            if not content.strip():

                st.warning(
                    "Please enter some content."
                )

            else:

                # First perform rule-based checking

                issues, report = analyze_content(
                    content,
                    brand
                )

                # Then try Gemini AI analysis

                try:

                    client = genai.Client(
                        api_key=st.secrets["GEMINI_API_KEY"]
                    )

                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=f"""
You are BrandShield AI, a brand governance assistant.

Brand name: {brand.get("name", "")}
Brand description: {brand.get("description", "")}
Brand tone: {brand.get("tone", "")}
Approved words: {brand.get("approved", "")}
Prohibited words: {brand.get("prohibited", "")}
Additional rules: {brand.get("rules", "")}

Analyze this marketing content:

{content}

Explain:
1. Brand tone consistency.
2. Compliance with brand guidelines.
3. Unsupported or exaggerated claims.
4. Suggested improvements.

Be clear and concise.
"""
                    )

                    if response.text:

                        report += (
                            "\n\nGEMINI AI ANALYSIS\n"
                            + "=" * 40
                            + "\n"
                            + response.text
                        )

                    client.close()

                except Exception as e:

                    report += (
                        "\n\nGEMINI AI STATUS\n"
                        "Gemini is temporarily unavailable. "
                        "Rule-based analysis is still available.\n"
                    )

                # Save analysis results

                st.session_state.content = content

                st.session_state.issues = issues

                st.session_state.ai_analysis = report

                st.session_state.history.append({
                    "brand": brand.get("name", "Unknown"),
                    "content": content,
                    "issues": issues.copy(),
                    "report": report
                })

                st.session_state.decision = "Pending"

                st.success(
                    "Content analysis completed!"
                )

                st.subheader(
                    "🛡️ BrandShield AI Analysis"
                )

                st.text(report)

                if issues:

                    st.error(
                        "Potential content issues detected!"
                    )

                    for issue in issues:

                        st.warning(issue)

                else:

                    st.success(
                        "No issues detected by the current rule-based checker."
                    )

# ==========================================
# REVIEW SUGGESTIONS
# ==========================================

elif page == "Review Suggestions":

    st.title("📝 Review Suggestions")

    if not st.session_state.content:

        st.info(
            "Submit content in the Content Checker first."
        )

    else:

        st.subheader("Submitted Content")

        st.write(st.session_state.content)

        st.divider()

        st.subheader("Detected Issues")

        if st.session_state.issues:

            for issue in st.session_state.issues:
                st.warning(issue)

        else:

            st.success(
                "No issues were detected by the current rule-based checker."
            )

        # Brand Compliance Score

        st.divider()

        st.subheader("📊 Brand Compliance Score")

        compliance_score = max(
            0,
            100 - (len(st.session_state.issues) * 10)
        )

        st.metric(
            "Compliance Score",
            f"{compliance_score}%"
        )

        st.progress(compliance_score / 100)

        if compliance_score >= 80:
            st.success("Good brand compliance!")
        elif compliance_score >= 50:
            st.warning("Some improvements are required.")
        else:
            st.error("Major brand improvements are required.")

        # Analysis Report

        if st.session_state.ai_analysis:

            st.divider()

            st.subheader("🛡️ BrandShield Content Analysis")

            st.text(st.session_state.ai_analysis)

            report_content = f"""
BRANDSHIELD AI - ANALYSIS REPORT

Brand Name: {st.session_state.brand.get("name", "")}

Submitted Content:
{st.session_state.content}

Analysis Results:
{st.session_state.ai_analysis}

Human Review Decision:
{st.session_state.decision}
"""

            st.download_button(
                label="📥 Download Analysis Report",
                data=report_content,
                file_name="BrandShield_Analysis_Report.txt",
                mime="text/plain"
            )

        # Human Review

        st.divider()

        st.subheader("Human Review")

        decision_options = [
            "Pending",
            "Approved",
            "Needs Changes"
        ]

        current_decision = st.session_state.decision

        decision_index = decision_options.index(
            current_decision
        ) if current_decision in decision_options else 0

        decision = st.radio(
            "Review Decision",
            decision_options,
            index=decision_index
        )

        if st.button("Save Review Decision"):

            if decision == "Approved" and st.session_state.issues:

                st.warning(
                    "⚠️ This content has detected issues. "
                    "Please review and resolve them before approval."
                )

            else:

                st.session_state.decision = decision

                if decision == "Approved":

                    st.success(
                        "Content approved successfully!"
                    )

                elif decision == "Needs Changes":

                    st.warning(
                        "Changes are required before publishing."
                    )

                else:

                    st.info(
                        "Review decision saved as Pending."
                    )


# ==========================================
# ANALYSIS HISTORY
# ==========================================


elif page == "Analysis History":

    st.title("📚 Analysis History")

    st.write(
        "View and manage your previously checked marketing content."
    )

    if not st.session_state.history:

        st.info(
            "No previous analyses found. Check some content first."
        )

    else:

        st.metric(
            "Total Analyses",
            len(st.session_state.history)
        )
         # DOWNLOAD COMPLETE ANALYSIS HISTORY

        all_reports = ""

        for index, item in enumerate(
            reversed(st.session_state.history),
            start=1
        ):

            all_reports += f"""
========================================
ANALYSIS {index}
========================================

Brand: {item.get('brand', 'Unknown')}

Submitted Content:
{item.get('content', '')}

Detected Issues:
{chr(10).join(item.get('issues', []))}

Analysis Report:
{item.get('report', '')}

"""

        st.download_button(
            label="📥 Download Complete Analysis History",
            data=all_reports,
            file_name="BrandShield_Complete_History.txt",
            mime="text/plain"
        )
        st.divider()

        for index, item in enumerate(
            reversed(st.session_state.history),
            start=1
        ):

            brand_name = item.get("brand", "Unknown")
            content = item.get("content", "")
            issues = item.get("issues", [])
            report = item.get("report", "")

            compliance_score = max(
                0,
                100 - len(issues) * 10
            )

            with st.expander(
                f"Analysis {index} - {brand_name}"
            ):

                st.subheader("Analysis Summary")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Detected Issues",
                        len(issues)
                    )

                with col2:
                    st.metric(
                        "Compliance Score",
                        f"{compliance_score}%"
                    )

                st.divider()

                st.subheader("Submitted Content")

                st.write(content)

                st.subheader("Detected Issues")

                if issues:

                    for issue in issues:
                        st.warning(issue)

                else:

                    st.success("No issues detected.")

                st.subheader("Analysis Report")

                st.text(report)

                st.download_button(
                    label="📥 Download This Report",
                    data=report,
                    file_name=f"BrandShield_Analysis_{index}.txt",
                    mime="text/plain",
                    key=f"history_download_{index}"
                )
 
# ==========================================
# PROJECT INFORMATION
# ==========================================

elif page == "Project Information":

    st.title("ℹ️ Project Information")

    st.subheader("About BrandShield AI")

    st.write(
        "BrandShield AI is an intelligent brand governance "
        "platform designed to help businesses maintain a "
        "consistent brand identity across their marketing content."
    )

    st.divider()

    st.header("🎯 Project Objective")

    st.write(
        "To identify brand guideline violations, detect "
        "potentially unsupported marketing claims, and "
        "help users improve content before publishing."
    )

    st.divider()

    st.header("⚙️ Technologies Used")

    st.write("🐍 Python – Application logic and content checking")

    st.write("🎈 Streamlit – Interactive web application")

    st.write("🔍 Regular Expressions – Rule-based content detection")

    st.write("🤖 Gemini API – Optional AI-powered analysis")

    st.divider()

    st.header("✨ Key Features")

    st.write("1. Brand guideline management")

    st.write("2. Marketing content checking")

    st.write("3. Prohibited word detection")

    st.write("4. Unsupported claim detection")

    st.write("5. Brand tone checking")

    st.write("6. Content improvement suggestions")

    st.write("7. Human review and approval")

    st.write("8. Analysis history and report downloads")

    st.divider()

    st.header("⚠️ Project Limitations")

    st.write(
        "Content checking is based primarily on predefined "
        "rules and patterns. Results may require human verification. "
        "Gemini-powered analysis depends on API availability."
    )

    st.divider()

    st.success(
        "BrandShield AI – Building Consistent and Trustworthy Brands."
    )

