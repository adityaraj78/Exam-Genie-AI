# 🎓 AI Exam-Genie Pro

AI Exam-Genie Pro is a professional academic analyzer and question generator built with Streamlit and powered by Google's Gemini AI. It allows students and educators to upload study materials (PDF, JPG, PNG) and automatically generates high-priority exam questions with detailed explanations and revision notes. 

## ✨ Features

- **Document Analysis**: Upload study materials in PDF or image formats (JPG, PNG).
- **Customizable Question Generation**: Select the number of questions to generate (3-10).
- **Multilingual Support**: Generate questions and explanations in English, Pure Hindi, or Hinglish (a mix of Hindi and English).
- **Smart Decoder**: A dedicated tool to paste complex text snippets and get instant, simplified explanations in your preferred language.
- **Interactive Doubt Solver**: An integrated AI chatbot to ask follow-up questions based on the generated analysis.
- **PDF Export**: Download the generated Q&A report as a formatted PDF file for offline study.

## 🛠️ Tech Stack

- **Frontend/UI**: [Streamlit](https://streamlit.io/)
- **AI/LLM**: Google Gemini AI (`google-generativeai`, `gemini-2.5-flash`)
- **PDF Processing**: `pdfplumber` (for reading PDF content), `reportlab` (for generating PDF reports).
- **Environment Management**: `python-dotenv`

## 📋 Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.8+ installed.
- A Google Gemini API Key.

## 🚀 Installation & Setup

1. **Clone or Download the Repository:**
   Navigate to the project directory in your terminal.

2. **Create a Virtual Environment (Optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   Ensure all required packages are installed. 
   *(Note: Make sure `pdfplumber` and `reportlab` are installed as they are used in the codebase).*
   ```bash
   pip install -r requirements.txt
   pip install pdfplumber reportlab
   ```

4. **Environment Variables Configuration:**
   Create a `.env` file in the root directory and add your Google Gemini API key:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## 💻 Usage

1. Start the Streamlit server:
   ```bash
   streamlit run app.py
   ```
2. Open your web browser and navigate to the local URL provided in the terminal (usually `http://localhost:8501`).
3. Use the sidebar to set the desired number of questions and primary language.
4. Upload your study material and click **"GENERATE STUDY MATERIAL"**.
5. View the generated Q&A, interact with the Doubt Solver, or export the report as a PDF!

## 📁 Project Structure

- `app.py`: The main entry point for the Streamlit application. Contains the UI layout, file upload handling, and user interactions.
- `brain.py`: The core logic module. Handles the integration with Google Gemini AI, language translation prompts, chatbot memory, and PDF generation logic.
- `requirements.txt`: List of Python dependencies (make sure to also install `pdfplumber` and `reportlab`).
- `.env`: Environment variables file (not included in version control) to securely store the API key.