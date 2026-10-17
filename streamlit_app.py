import streamlit as st
from google import genai

# Konfigurasi Halaman
st.set_page_config(page_title="Kantor Virtual AI", page_icon="🏢", layout="wide")

st.title("🏢 Kantor Virtual AI")
st.markdown("Konsultasi bisnis praktis bersama para ahli virtual Anda: **Kang Roni** (Keuangan), **Bu Rina** (SDM & Operasional), dan **Dodit** (Pemasaran & Kreatif).")

# Sidebar untuk Pengaturan & API Key
st.sidebar.title("⚙️ Pengaturan")
api_key = st.sidebar.text_input("Masukkan Google Gemini API Key:", type="password")

persona = st.sidebar.selectbox(
    "Pilih Ahli Konsultasi:",
        ["Kang Roni (Keuangan & Angka)", "Bu Rina (SDM & Operasional)", "Dodit (Pemasaran & Bisnis Kreatif)"]
        )

        # Instruksi Persona
        system_prompts = {
            "Kang Roni (Keuangan & Angka)": "Anda adalah Kang Roni, seorang pakar keuangan dan akuntansi yang tegas, teliti, konservatif, dan selalu fokus pada efisiensi anggaran serta profitabilitas.",
                "Bu Rina (SDM & Operasional)": "Anda adalah Bu Rina, seorang manajer SDM dan operasional yang ramah, tegas, terstruktur, disiplin, serta sangat peduli pada kenyamanan kerja karyawan.",
                    "Dodit (Pemasaran & Bisnis Kreatif)": "Anda adalah Dodit, seorang ahli pemasaran dan ide kreatif yang santai, antusias, kekinian, suka out-of-the-box, dan penuh ide-ide viral."
                    }

                    selected_prompt = system_prompts[persona]

                    # Inisialisasi Riwayat Chat
                    if "messages" not in st.session_state:
                        st.session_state.messages = []

                        # Tampilkan Pesan Chat Terdahulu
                        for message in st.session_state.messages:
                            with st.chat_message(message["role"]):
                                    st.markdown(message["content"])

                                    # Input Pesan Pengguna
                                    if prompt := st.chat_input("Tulis pertanyaan atau topik bisnis Anda di sini..."):
                                        if not api_key:
                                                st.error("⚠️ Masukkan Google Gemini API Key Anda terlebih dahulu di menu sebelah kiri!")
                                                    else:
                                                            # Simpan dan tampilkan pesan pengguna
                                                                    st.session_state.messages.append({"role": "user", "content": prompt})
                                                                            with st.chat_message("user"):
                                                                                        st.markdown(prompt)

                                                                                                # Proses dengan Gemini API
                                                                                                        try:
                                                                                                                    client = genai.Client(api_key=api_key)
                                                                                                                                
                                                                                                                                            # Gabungkan system prompt dan riwayat chat untuk konteks
                                                                                                                                                        full_contents = f"Instruksi Karakter: {selected_prompt}\n\n"
                                                                                                                                                                    for m in st.session_state.messages:
                                                                                                                                                                                    full_contents += f"{m['role']}: {m['content']}\n"

                                                                                                                                                                                                with st.spinner(f"Menghubungi {persona.split(' ')[0]}..."):
                                                                                                                                                                                                                response = client.models.generate_content(
                                                                                                                                                                                                                                    model='gemini-2.5-flash',
                                                                                                                                                                                                                                                        contents=full_contents
                                                                                                                                                                                                                                                                        )
                                                                                                                                                                                                                                                                                        bot_reply = response.text

                                                                                                                                                                                                                                                                                                    # Tampilkan jawaban bot
                                                                                                                                                                                                                                                                                                                with st.chat_message("assistant"):
                                                                                                                                                                                                                                                                                                                                st.markdown(bot_reply)
                                                                                                                                                                                                                                                                                                                                            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                                                                                                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                                                                                                                except Exception as e:
                                                                                                                                                                                                                                                                                                                                                                            st.error(f"Terjadi kesalahan: {e}")
                                                                                                                                                                                                                                                                                                                                