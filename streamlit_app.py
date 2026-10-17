import streamlit as st
import google.generativeai as genai

# Konfigurasi Halaman
st.set_page_config(
    page_title="Kantor Virtual AI",
        page_icon="🏢",
            layout="wide"
            )

            # Sidebar untuk Pengaturan API Key dan Persona
            st.sidebar.title("🏢 Kantor Virtual AI")
            st.sidebar.markdown("---")

            api_key = st.sidebar.text_input("Masukkan Google Gemini API Key Anda", type="password")

            if not api_key:
                st.warning("⚠️ Silakan masukkan API Key Google Gemini Anda di sidebar sebelah kiri untuk mulai menggunakan Kantor Virtual AI.")
                    st.info("💡 Belum punya API Key? Anda bisa mendapatkannya secara gratis melalui Google AI Studio.")
                        st.stop()

                        # Konfigurasi Gemini API
                        genai.configure(api_key=api_key)
                        model = genai.GenerativeModel('gemini-1.5-flash')

                        st.sidebar.markdown("---")
                        selected_persona = st.sidebar.selectbox(
                            "Pilih Persona Konsultasi:",
                                ["Kang Roni (Pakar Keuangan & Akuntansi)", "Bu Rina (Ahli SDM & Manajemen Operasional)", "Dodit (Pemasaran Kreatif & Pengembangan Bisnis)"]
                                )

                                st.sidebar.markdown("---")
                                st.sidebar.info("Aplikasi Kantor Virtual ini siap membantu mendiskusikan berbagai strategi bisnis Anda.")

                                # Tampilan Utama
                                st.title("🏢 Selamat Datang di Kantor Virtual AI")
                                st.markdown(f"Anda sedang berkonsultasi di ruang kerja virtual dengan **{selected_persona}**.")

                                # Inisialisasi Riwayat Chat
                                if "messages" not in st.session_state:
                                    st.session_state.messages = []

                                    # Tampilkan Pesan Sebelumnya
                                    for message in st.session_state.messages:
                                        with st.chat_message(message["role"]):
                                                st.markdown(message["content"])

                                                # Input Pesan dari User
                                                if prompt := st.chat_input("Ketik pesan atau pertanyaan Anda di sini..."):
                                                    st.session_state.messages.append({"role": "user", "content": prompt})
                                                        with st.chat_message("user"):
                                                                st.markdown(prompt)

                                                                    # Tentukan System Instruction Berdasarkan Persona yang Dipilih
                                                                        if "Kang Roni" in selected_persona:
                                                                                system_prompt = "Anda adalah Kang Roni, seorang pakar keuangan dan akuntansi yang cerdas, teliti, konservatif, namun suportif dalam memberikan analisis finansial dan pengelolaan anggaran bisnis."
                                                                                    elif "Bu Rina" in selected_persona:
                                                                                            system_prompt = "Anda adalah Bu Rina, seorang ahli Sumber Daya Manusia (SDM) dan manajemen operasional yang bijaksana, tegas, profesional, serta fokus pada efisiensi kerja dan kenyamanan karyawan."
                                                                                                else:
                                                                                                        system_prompt = "Anda adalah Dodit, seorang spesialis pemasaran kreatif dan pengembangan bisnis yang energik, penuh ide out-of-the-box, dinamis, dan berorientasi pada pertumbuhan omzet."

                                                                                                            # Generate Respon dari Gemini
                                                                                                                with st.chat_message("assistant"):
                                                                                                                        message_placeholder = st.empty()
                                                                                                                                message_placeholder.markdown("Sedang berpikir...")
                                                                                                                                        try:
                                                                                                                                                    full_prompt = f"{system_prompt}\n\nPertanyaan/Pesan Klien: {prompt}"
                                                                                                                                                                response = model.generate_content(full_prompt)
                                                                                                                                                                            reply = response.text
                                                                                                                                                                                        message_placeholder.markdown(reply)
                                                                                                                                                                                                    st.session_state.messages.append({"role": "assistant", "content": reply})
                                                                                                                                                                                                            except Exception as e:
                                                                                                                                                                                                                        error_msg = f"Terjadi kesalahan saat memproses permintaan: {e}"
                                                                                                                                                                                                                                    message_placeholder.markdown(error_msg)
                                                                                                                                                                                                                                    