🩺 Aarogya-AI

An AI-powered health and wellness companion designed to provide general health information, wellness insights, health-data tracking, medication safety information, and personalized guidance.

✨ Features

- 🤖 AI Health Assistant
- 💬 AI Health Chatbot
- 📊 Health Data Tracking
- 📈 Health Analysis
- 📄 Health Reports
- 📂 Import Health Data
- 🎯 Health Goals
- ⚠️ Health Risk Assessment
- 🩺 Symptom Information
- 💡 Health Recommendations
- 💊 Medication Safety Information
- 🚨 Emergency Awareness

🛠️ Technologies Used

- Python
- Streamlit
- SQLite
- Pandas
- LangChain
- Google Gemini API
- Git & GitHub

📁 Project Structure

aarogya-ai/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── pages/
│   ├── 2_Chatbot.py
│   ├── 3_Health_Data.py
│   ├── 4_Health_Analysis.py
│   ├── 5_Health_Report.py
│   ├── 6_Import_Health_Data.py
│   ├── 7_Health_Goals.py
│   ├── 8_Risk_Assessment.py
│   ├── 9_Symptom_Information.py
│   ├── 10_Health_Recommendations.py
│   ├── 11_Medication_Safety.py
│   ├── 12_Emergency_Detection.py
│   └── 13_AI_Health_Assistant.py
│
└── src/
    ├── chatbot.py
    ├── medication_tool.py
    ├── fitness_tool.py
    └── __init__.py

▶️ How to Run

1. Clone the repository

git clone https://github.com/gayatrik9620-design/aarogya-ai.git
cd aarogya-ai

2. Install required packages

pip install -r requirements.txt

3. Configure the Gemini API

Create a ".env" file in the project root and add your Gemini API key:

GOOGLE_API_KEY=your_gemini_api_key

4. Run the Streamlit application

python -m streamlit run app.py

⚠️ Disclaimer

Aarogya-AI is an AI-based wellness and health information project intended for educational and general informational purposes only.

It does not provide medical diagnosis, prescriptions, or emergency medical treatment. Users should consult a qualified healthcare professional for medical advice.