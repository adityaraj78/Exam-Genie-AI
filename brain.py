import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
import io

load_dotenv()

def ask_gemini_multimodal(context_text, num_questions, uploaded_file, target_language="English"):
    api_key = os.getenv("GOOGLE_API_KEY")
    client = genai.Client(api_key=api_key)
    
    lang_map = {
        "Hinglish": "Write in Hinglish (mix of Hindi + English like WhatsApp chat).",
        "Hindi": "Write in pure Hindi script.",
        "English": "Write in professional academic English."
    }

    prompt = f"""
    You are an academic expert. Based on the provided context, identify the core topics 
    and generate {num_questions} high-priority exam questions with detailed answers.
    
    STRICT FORMATTING RULES:
    1. For EVERY answer, provide a detailed explanation first.
    2. At the end of EACH answer, add a section called '📌 QUICK SUMMARY' or '🏁 REVISION NOTES'.
    3. In this summary, condense the entire answer into 3-4 very short, high-impact bullet points.
    4. Use bold text for keywords.
    
    STRICT LANGUAGE RULE: {lang_map.get(target_language, "English")}
    """

    contents = []
    if len(context_text) > 20: contents.append(f"Context: {context_text}")
    if uploaded_file:
        contents.append(types.Part.from_bytes(data=uploaded_file.getvalue(), mime_type=uploaded_file.type))
    contents.append(prompt)
    
    response = client.models.generate_content(model="gemini-2.5-flash", contents=contents)
    return response.text

def translate_snippet(snippet, target_lang):
    """Sirf selected text ko translate karne ke liye"""
    api_key = os.getenv("GOOGLE_API_KEY")
    client = genai.Client(api_key=api_key)
    
    prompt = f"Translate/Explain this specific technical part in {target_lang}. Keep keywords in English.\n\nText: {snippet}"
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return response.text

def continue_chat_brain(user_query, chat_history):
    api_key = os.getenv("GOOGLE_API_KEY")
    client = genai.Client(api_key=api_key)
    
    # Chat session start karna with history
    # chat_history ek list hogi [{'role': 'user', 'parts': [...]}, ...]
    chat = client.chats.create(model="gemini-2.5-flash", history=chat_history)
    
    try:
        response = chat.send_message(user_query)
        return response.text
    except Exception as e:
        return f"Chat Error: {e}"

def generate_pdf_bytes(text_content):
    """Text ko PDF bytes mein convert karta hai bina file save kiye (Memory mein)"""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Exam-Genie: Generated Q&A Report")
    c.line(50, height - 60, width - 50, height - 60)
    
    # Body Content
    c.setFont("Helvetica", 11)
    text_object = c.beginText(50, height - 80)
    
    # Text ko wrap karna taaki page se bahar na jaye
    lines = simpleSplit(text_content, "Helvetica", 11, width - 100)
    
    for line in lines:
        # Agar page khatam ho jaye toh naya page add karo
        if text_object.getY() < 50:
            c.drawText(text_object)
            c.showPage()
            c.setFont("Helvetica", 11)
            text_object = c.beginText(50, height - 50)
            
        text_object.textLine(line)
        
    c.drawText(text_object)
    c.save()
    
    buffer.seek(0)
    return buffer