import streamlit as st
import google.generativeai as genai
import os

# ==============================================================================
# PENGATURAN API KEY DAN MODEL (PENTING! JANGAN UBAH DI SINI)
# ==============================================================================

# Ambil API Key dari variabel lingkungan.
# Nama variabelnya bisa Anda sesuaikan.
API_KEY = os.environ.get("GEMINI_API_KEY")

# Pastikan API Key ditemukan
if not API_KEY:
    st.error("Error: API Key Gemini tidak ditemukan.")
    st.info("Harap atur variabel lingkungan 'GEMINI_API_KEY' dengan API Key Anda.")
    st.stop()

try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error(f"Error saat mengkonfigurasi API Key: {e}")
    st.stop()

# Nama model Gemini yang akan digunakan
MODEL_NAME = 'gemini-1.5-flash'

# ==============================================================================
# KONTEKS AWAL CHATBOT
# ==============================================================================

# Definisikan peran chatbot Anda di sini.
INITIAL_CHATBOT_CONTEXT = [
    {
        "role": "user",
        "parts": ["Kamu adalah ahli apoteker. Tuliskan obat apa yang diinginkan untuk menyembuhkan penyakit Anda. Jawaban singkat dan faktual. Tolak pertanyaan selain tentang obat."]
    },
    {
        "role": "model",
        "parts": ["Baik! Saya akan menjawab pertanyaan Anda tentang Obat."]
    }
]

# ==============================================================================
# APLIKASI STREAMLIT
# ==============================================================================

st.title("👨‍⚕️ Apoteker Chatbot")
st.markdown("Bertanya tentang obat-obatan dan kesehatan umum.")

# Inisialisasi model dan sesi chat di Streamlit
if "chat" not in st.session_state:
    try:
        model = genai.GenerativeModel(
            MODEL_NAME,
            generation_config=genai.types.GenerationConfig(
                temperature=0.4,
                max_output_tokens=500
            )
        )
        st.session_state.chat = model.start_chat(history=INITIAL_CHATBOT_CONTEXT)
    except Exception as e:
        st.error(f"Error saat inisialisasi model: {e}")
        st.stop()
        
# Tampilkan pesan riwayat chat
for message in st.session_state.chat.history:
    if message.role == 'user':
        with st.chat_message("user"):
            st.markdown(message.parts[0])
    elif message.role == 'model':
        with st.chat_message("assistant"):
            st.markdown(message.parts[0])

# Tangani input dari pengguna
if prompt := st.chat_input("Tanyakan tentang obat..."):
    # Tambahkan input pengguna ke chat
    with st.chat_message("user"):
        st.markdown(prompt)

    # Kirim input pengguna ke model dan dapatkan respons
    try:
        response = st.session_state.chat.send_message(prompt)
        # Tampilkan respons dari model
        with st.chat_message("assistant"):
            st.markdown(response.text)
    except Exception as e:
        st.error(f"Maaf, terjadi kesalahan saat berkomunikasi dengan Gemini: {e}")
