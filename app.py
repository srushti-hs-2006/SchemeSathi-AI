
from flask import Flask, render_template, request
from PyPDF2 import PdfReader
from google import genai
from dotenv import load_dotenv

import markdown
import bleach
import os
import re
import html


# --------------------------------
# LOAD ENVIRONMENT VARIABLES
# --------------------------------

load_dotenv()

app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024


# --------------------------------
# GEMINI CONFIGURATION
# --------------------------------

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key) if api_key else None

MODEL_NAME = "gemini-3.5-flash"

LANGUAGES = {
    "English": "English",
    "Kannada": "Kannada",
    "Hindi": "Hindi"
}


# --------------------------------
# FORMAT AI RESPONSE
# --------------------------------

def format_result(text):

    text = html.unescape(text)

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    text = text.strip()

    text = re.sub(
        r"^\s*```(?:markdown|md|html)?\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(r"\s*```\s*$", "", text)

    converted_html = markdown.markdown(
        text,
        extensions=[
            "extra",
            "sane_lists"
        ]
    )

    allowed_tags = [
        "h1", "h2", "h3", "h4",
        "p", "strong", "b", "em",
        "ul", "ol", "li",
        "br", "hr", "blockquote",
        "code", "a"
    ]

    allowed_attributes = {
        "a": ["href", "title"]
    }

    clean_html = bleach.clean(
        converted_html,
        tags=allowed_tags,
        attributes=allowed_attributes,
        protocols=["http", "https", "mailto"],
        strip=True
    )

    return clean_html


# --------------------------------
# GEMINI AI PROMPT
# --------------------------------

def create_prompt(document_text, language):

    prompt = f"""
You are SchemeSathi AI, an intelligent multilingual
government scheme and policy assistant.

FIRST TASK: DOCUMENT VALIDATION

Carefully examine the uploaded document.

Determine whether it contains information about
an official government scheme, government policy,
or government welfare programme.

If the document is unrelated to government schemes,
policies or programmes, DO NOT generate a report.

In that situation, respond with exactly this marker:

NOT_A_GOVERNMENT_SCHEME_DOCUMENT

Do not explain anything else when using this marker.

A genuine government scheme guideline, operational
guideline, notification or official scheme document
should be accepted.

SECOND TASK: SCHEME EXPLANATION

If the document is related to a government scheme,
policy or programme, explain it completely.

Write the entire report in {language}.

Use these nine sections:

## 1. Scheme Overview

Explain the purpose and objectives of the scheme.

## 2. Who Can Apply?

Explain who can apply for the scheme.

## 3. Eligibility Criteria

Explain the eligibility conditions and requirements.

## 4. Who Cannot Apply?

Explain the categories excluded from the scheme.

## 5. Documents Required

List the required documents using bullet points.

## 6. Benefits of the Scheme

Explain the financial assistance and other benefits.

## 7. How to Apply - Step by Step

Explain the application process using numbered steps.

## 8. Important Dates

Mention important dates and deadlines.

## 9. Official Website and Contact Details

Mention official website and contact information
only when provided in the document.

FORMATTING RULES:

1. Use meaningful Markdown headings.
2. Use bold formatting for important information.
3. Write short and clear paragraphs.
4. Use bullet points for lists.
5. Use numbered steps for application procedures.
6. Avoid unnecessary symbols and repeated content.
7. Keep proper spacing between sections.
8. Write in simple language understandable to citizens.

ACCURACY RULES:

1. Use information only from the uploaded document.
2. Never invent information.
3. Preserve official dates and financial amounts.
4. Preserve important eligibility exceptions.
5. Do not present assumptions as official facts.
6. If information is missing, clearly mention that
   the uploaded document does not specify it.
7. Do not confuse historical guidelines with
   current scheme rules.

FINAL INSTRUCTIONS:

Complete all nine sections.

Do not stop in the middle of a sentence.

End with a short verification note in {language},
advising users to check the official government source.

DOCUMENT CONTENT:

{document_text}
"""

    return prompt


# --------------------------------
# GEMINI ERROR HANDLING
# --------------------------------

def get_gemini_error(error):

    error_text = str(error).lower()

    print("Gemini API Error:", error)

    if "503" in error_text or "unavailable" in error_text:
        return (
            "Gemini AI is temporarily experiencing high demand. "
            "Please wait a few minutes and try again."
        )

    if "429" in error_text or "resource_exhausted" in error_text:
        return (
            "Gemini API request limit has been reached. "
            "Please check your API quota and try again later."
        )

    if "404" in error_text or "not_found" in error_text:
        return (
            "The selected Gemini model is unavailable for this API key. "
            "Please check your model access."
        )

    if "api key" in error_text or "401" in error_text or "403" in error_text:
        return (
            "Gemini API authentication failed. "
            "Please check your API key in the .env file."
        )

    if "empty response" in error_text:
        return (
            "Gemini AI returned an empty response. "
            "Please try again."
        )

    return (
        "Gemini AI could not analyse the document. "
        "Please try again."
    )


# --------------------------------
# HOME PAGE
# --------------------------------

@app.route("/")
def home():

    return render_template(
        "index.html",
        selected_language="English"
    )


# --------------------------------
# ANALYSE GOVERNMENT SCHEME PDF
# --------------------------------

@app.route("/analyze", methods=["POST"])
def analyze():

    language = request.form.get("language", "English")

    if language not in LANGUAGES:
        language = "English"

    # Check API key
    if not client:

        return render_template(
            "index.html",
            error=(
                "Gemini API key is missing. "
                "Please configure GEMINI_API_KEY in your .env file."
            ),
            selected_language=language
        )

    # Check uploaded file
    if "pdf_file" not in request.files:

        return render_template(
            "index.html",
            error="Please upload a government scheme PDF.",
            selected_language=language
        )

    file = request.files["pdf_file"]

    if not file.filename:

        return render_template(
            "index.html",
            error="Please select a PDF file.",
            selected_language=language
        )

    # Validate file extension
    if not file.filename.lower().endswith(".pdf"):

        return render_template(
            "index.html",
            error="Only PDF files are supported.",
            selected_language=language
        )

    try:

        # Read PDF
        reader = PdfReader(file, strict=False)

        # Check encrypted PDF
        if reader.is_encrypted:

            return render_template(
                "index.html",
                error="Password-protected PDFs are not supported.",
                selected_language=language
            )

        # Extract PDF text
        extracted_text = ""

        for page in reader.pages:

            page_text = page.extract_text() or ""

            extracted_text += page_text + "\n"

        extracted_text = extracted_text.strip()

        # Check readable content
        if not extracted_text:

            return render_template(
                "index.html",
                error=(
                    "No readable text was found in this PDF. "
                    "Please upload a text-based PDF document."
                ),
                selected_language=language
            )

        # Limit document size
        extracted_text = extracted_text[:100000]

        print("PDF successfully extracted.")
        print("Selected language:", language)
        print("Sending document to Gemini AI...")

        # Create prompt
        prompt = create_prompt(
            extracted_text,
            LANGUAGES[language]
        )

        # Generate Gemini response
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        result = response.text or ""

        if not result.strip():

            raise ValueError(
                "Gemini returned an empty response."
            )

        # --------------------------------
        # DOCUMENT VALIDATION
        # --------------------------------

        if "NOT_A_GOVERNMENT_SCHEME_DOCUMENT" in result:

            print("Document validation failed.")

            return render_template(
                "index.html",
                error=(
                    "This PDF does not appear to contain "
                    "a government scheme, policy or programme. "
                    "Please upload an official government scheme document."
                ),
                selected_language=language
            )

        print("Document validation passed.")
        print("Gemini AI analysis completed successfully.")

        # Format report
        result_html = format_result(result)

        # Display report
        return render_template(
            "index.html",
            result_html=result_html,
            filename=file.filename,
            selected_language=language,
            mode="Gemini AI Analysis"
        )

    except Exception as error:

        print("Processing Error:", error)

        error_message = get_gemini_error(error)

        return render_template(
            "index.html",
            error=error_message,
            selected_language=language
        )


# --------------------------------
# FILE SIZE ERROR
# --------------------------------

@app.errorhandler(413)
def file_too_large(error):

    return render_template(
        "index.html",
        error="PDF file size must be less than 10 MB.",
        selected_language="English"
    ), 413


# --------------------------------
# RUN FLASK APPLICATION
# --------------------------------

if __name__ == "__main__":

    app.run(debug=True)
