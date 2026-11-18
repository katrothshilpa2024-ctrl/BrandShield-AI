
# 🛡️ BrandShield AI

### Your Brand's Intelligent Guardian

BrandShield AI is a brand governance platform that helps businesses maintain consistent brand identity across their marketing content.

It checks submitted content against saved brand guidelines, identifies potential violations, and supports human review before publishing.

## 🎯 Project Objective

To improve brand consistency by detecting prohibited words, unsupported marketing claims, and tone mismatches in marketing content.

## ✨ Key Features

- Brand guideline management
- Marketing content checking
- Prohibited word detection
- Unsupported claim detection
- Brand tone checking
- Content improvement suggestions
- Compliance score
- Human review and approval
- Analysis history
- Downloadable analysis reports
- Optional Gemini AI integration

## 🛠️ Technologies Used

- Python
- Streamlit
- Regular Expressions
- Google Gemini API (optional)

## 📁 Project Structure

BrandShield-AI/
│
├── app.py
├── test_gemini.py
├── requirements.txt
├── README.md
└── .streamlit/
    └── secrets.toml

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
```

### 2. Open the project folder

```bash
cd BrandShield-AI
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python -m streamlit run app.py
```

## 🤖 AI Integration

BrandShield AI includes optional Google Gemini API integration.

If the Gemini service is unavailable, the application can still perform rule-based content checking.

## ⚠️ Limitations

- Rule-based detection may not understand every context.
- Some flagged content may require human verification.
- Gemini analysis depends on API availability.
- Compliance scores are indicative, not legal or regulatory certification.

## 🚀 Future Enhancements

- Advanced AI-powered content analysis
- Multi-brand management
- User authentication
- Cloud database integration
- Advanced analytics and reporting

---

**BrandShield AI – Building Consistent and Trustworthy Brands.**
