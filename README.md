# SchemeSathi AI 🌱

### An Intelligent Multilingual Government Scheme and Policy Assistant

**Making Government Schemes Simple and Accessible for Everyone.**

## 📌 About the Project

SchemeSathi AI is an AI-powered web application that helps people understand government schemes and policies easily.

Users can upload an official government scheme PDF document and receive a simplified explanation in their preferred language. The application uses Google's Gemini AI to analyze the document and present important information in a clear and structured format.

## 🎯 Problem Statement

Government scheme guidelines are often lengthy, complicated and difficult for ordinary citizens to understand. Language barriers also make it challenging for people to access important government information.

SchemeSathi AI aims to make these documents easier to understand and more accessible.

## ✨ Key Features

- **PDF Upload:** Upload government scheme and policy documents.
- **AI-Powered Analysis:** Uses Gemini AI to understand uploaded documents.
- **Multilingual Support:** Provides explanations in English, Kannada and Hindi.
- **Simple Explanations:** Presents complex information in easy-to-understand language.
- **Eligibility Details:** Explains eligibility criteria and exclusions.
- **Required Documents:** Lists documents needed to apply.
- **Benefits:** Explains the benefits offered by the scheme.
- **Application Process:** Provides step-by-step application guidance.
- **Document Validation:** Checks whether the uploaded PDF appears to be a government scheme or policy document.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| Google Gemini AI | AI-powered document analysis |
| PyPDF2 | PDF text extraction |
| HTML | Webpage structure |
| CSS | Website styling |
| JavaScript | Frontend interactions |
| Markdown | Report formatting |

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/srushti-hs-2006/SchemeSathi-AI.git
```

### 2. Open the Project Folder

```bash
cd SchemeSathi-AI
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

For Windows:

```powershell
venv\Scripts\activate
```

### 5. Install Required Packages

```bash
pip install -r requirements.txt
```

### 6. Configure the Gemini API Key

Create a `.env` file in the project root directory and add:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Replace `your_gemini_api_key` with your own Gemini API key.

### 7. Run the Application

```bash
python app.py
```

Open your browser and visit:

http://127.0.0.1:5000

## 🚀 How It Works

1. Open the SchemeSathi AI web application.
2. Select your preferred language.
3. Upload a government scheme PDF document.
4. Click the Analyse button.
5. The AI analyzes the document.
6. View the simplified scheme explanation in your selected language.

## 🌍 Supported Languages

- English
- Kannada
- Hindi

## 🔐 Security Note

Keep your Gemini API key private. Never upload your `.env` file or API credentials to GitHub.

## 🔮 Future Enhancements

- Support for more Indian languages.
- Improved document verification.
- Integration with official government scheme portals.
- More accessible features for rural citizens.
- Deployment for public access.

## 👩‍💻 Project Information

**Project Name:** SchemeSathi AI

**Track:** Civic Pulse – Digital Governance & Public Information

**Developed by:** Srushti HS

## ❤️ Our Vision

To make government schemes and public information easier to understand, accessible and useful for every citizen.
