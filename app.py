import streamlit as st
import pdfplumber
import os
from brain import ask_gemini_multimodal, translate_snippet, continue_chat_brain, generate_pdf_bytes

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Exam-Genie Pro AI",
    page_icon="🎓",
    layout="wide"
)

# --- CLEAN UI STYLING ---
st.markdown("""
    <style>
    .stButton>button {
        border-radius: 4px;
        background-color: #ff4b4b;
        color: white;
        font-weight: 600;
        border: none;
    }
    .stDownloadButton>button {
        background-color: #00c853 !important;
        border-radius: 4px;
    }
    div[data-testid="stExpander"] {
        border: 1px solid #30363d;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Controls")
    num_q = st.select_slider("No. of Questions", options=[3, 5, 7, 10], value=5)
    main_lang = st.radio("Primary Language", ["English", "Hinglish", "Hindi"], horizontal=True)
    st.markdown("---")
    # Mark kiya hua Status Box yahan se hata diya gaya hai

# --- MAIN INTERFACE ---
st.title("🎓 AI Exam-Genie")
st.caption("Professional Academic Analyzer & Question Generator")

# Top Metrics (Engine, Input, Output) yahan se hata diye gaye hain

st.markdown("---")

# File Upload Section
uploaded_file = st.file_uploader(
    "📂 Upload Study Material (PDF, JPG, PNG)", 
    type=["pdf", "jpg", "png", "jpeg"]
)

if uploaded_file:
    context = ""
    if uploaded_file.type == "application/pdf":
        try:
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    context += (page.extract_text() or "") + "\n"
        except: pass

    if st.button("GENERATE STUDY MATERIAL"):
        with st.spinner("Processing document..."):
            st.session_state.answer = ask_gemini_multimodal(context, num_q, uploaded_file, main_lang)
            st.session_state.messages = [] 

    # --- RESULTS DISPLAY ---
    if 'answer' in st.session_state:
        st.markdown("### 📋 Analysis Results")
        
        res_col, tool_col = st.columns([1.6, 1])
        
        with res_col:
            st.markdown(st.session_state.answer)
            
            # PDF Export
            pdf_data = generate_pdf_bytes(st.session_state.answer)
            st.download_button(
                label="📥 Export as PDF",
                data=pdf_data,
                file_name="Exam_Genie_Report.pdf",
                mime="application/pdf"
            )
        
        with tool_col:
            st.subheader("🎯 Smart Decoder")
            snippet = st.text_area("Paste complex text for instant explanation:", height=120)
            t_lang = st.radio("Explain in:", ["Hinglish", "Hindi"], horizontal=True, key="t_lang")
            
            if snippet:
                with st.status("Decoding..."):
                    explained = translate_snippet(snippet, t_lang)
                    st.write(explained)

        # --- CHATBOT ---
        st.markdown("---")
        with st.expander("💬 Doubt Solver (Interactive Chat)", expanded=False):
            if "messages" not in st.session_state:
                st.session_state.messages = []

            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            if prompt := st.chat_input("Ask a follow-up question..."):
                with st.chat_message("user"):
                    st.markdown(prompt)
                st.session_state.messages.append({"role": "user", "content": prompt})

                with st.chat_message("assistant"):
                    response = continue_chat_brain(f"Context: {st.session_state.answer}\nQuery: {prompt}", st.session_state.messages[:-1])
                    st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

else:
    st.info("Waiting for file upload...")