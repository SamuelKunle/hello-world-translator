import streamlit as st
import openai
from langdetect import detect
from PIL import Image
import base64

# Set your OpenAI API Key
client = openai.OpenAI(api_key="")

# 🌟 Translator function
def translate_text(text, target_language):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"You are a professional multilingual translator specializing in world languages. Translate the user's text into perfect {target_language}. Preserve cultural meaning, style, and tone."
            },
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content.strip()

# 🌍 Streamlit app settings
st.set_page_config(page_title="Hello World Translator", page_icon="🌍", layout="centered")

# 📸 Load and encode logo
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_logo(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    html_code = f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <img src="data:image/png;base64,{bin_str}" width="100" alt="Hello World Translator Logo">
        </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)

# 🍀 Light Green Background + Black Text + Black Cursor
st.markdown("""
    <style>
    body, .stApp {
        background-color: #CCFFCC;
        color: black;
    }
    h1, h2, h3, h4, h5 {
        color: #004d00;
        text-align: center;
    }
    label, .stSelectbox label, .stTextArea label {
        color: black !important;
        font-weight: 600;
        font-size: 18px;
    }
    .stButton>button, .stDownloadButton>button {
        background-color: #66BB66;
        color: white;
        font-weight: bold;
        padding: 10px 20px;
        border: none;
        border-radius: 8px;
    }
    .stTextArea textarea {
        background-color: #ffffff;
        color: black;
        border: 2px solid #66BB66;
        font-size: 16px;
        border-radius: 8px;
        caret-color: black;
    }
    div.stAlert div {
        color: black !important;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# 🚀 Load Logo
set_logo("hello_world_logo.png")  # Make sure you have the logo file

# 🚀 App title and subtitle
st.title("")
st.caption("Translate across hundreds of world languages easily!")

# ℹ️ How to use section
with st.expander("ℹ️ How to Use"):
    st.markdown("""
    - ✏️ Type your text or upload a `.txt` file.
    - 🌍 Choose the target language.
    - 📥 Download your translated file if needed.
    """)

# 📂 Upload file section
uploaded_file = st.file_uploader("📂 Upload a .txt file (optional):", type=["txt"])

# 📝 Input area
if uploaded_file is not None:
    file_text = uploaded_file.read().decode('utf-8')
    text_input = st.text_area("📝 File loaded successfully! Edit or translate:", value=file_text, height=200)
else:
    text_input = st.text_area("📝 Enter your text here:", height=150, placeholder="Type something...")

# 🌍 Massive Language List (World Languages like Google Translate)
languages = sorted([
    "Afrikaans", "Albanian", "Amharic", "Arabic", "Armenian", "Azerbaijani",
    "Basque", "Belarusian", "Bengali", "Bosnian", "Bulgarian", "Burmese",
    "Catalan", "Cebuano", "Chinese (Simplified)", "Chinese (Traditional)", "Corsican",
    "Croatian", "Czech", "Danish", "Dutch", "English", "Esperanto", "Estonian",
    "Filipino", "Finnish", "French", "Frisian", "Galician", "Georgian", "German",
    "Greek", "Gujarati", "Haitian Creole", "Hausa", "Hawaiian", "Hebrew", "Hindi",
    "Hmong", "Hungarian", "Icelandic", "Igbo", "Indonesian", "Irish", "Italian",
    "Japanese", "Javanese", "Kannada", "Kazakh", "Khmer", "Kinyarwanda", "Korean",
    "Kurdish", "Kyrgyz", "Lao", "Latin", "Latvian", "Lithuanian", "Luxembourgish",
    "Macedonian", "Malagasy", "Malay", "Malayalam", "Maltese", "Maori", "Marathi",
    "Mongolian", "Nepali", "Norwegian", "Nyanja", "Odia", "Pashto", "Persian",
    "Polish", "Portuguese", "Punjabi", "Romanian", "Russian", "Samoan", "Scots Gaelic",
    "Serbian", "Sesotho", "Shona", "Sindhi", "Sinhala", "Slovak", "Slovenian",
    "Somali", "Spanish", "Sundanese", "Swahili", "Swedish", "Tajik", "Tamil",
    "Tatar", "Telugu", "Thai", "Turkish", "Turkmen", "Ukrainian", "Urdu",
    "Uyghur", "Uzbek", "Vietnamese", "Welsh", "Xhosa", "Yiddish", "Yoruba",
    "Zulu"
])

# 🌍 Auto-detect language
detected_language = None
if text_input.strip():
    try:
        detected_language_code = detect(text_input)
        st.info(f"🌟 Auto-detected input language code: {detected_language_code.upper()}")
    except Exception as e:
        st.warning(f"⚠️ Could not detect language: {e}")

target_language = st.selectbox("🌐 Translate to:", languages)

# 🔄 Translate button
if st.button("🔄 Translate Now"):
    if not text_input.strip():
        st.error("⚠️ Please enter some text to translate!")
    else:
        with st.spinner("🔄 Translating... Please wait..."):
            try:
                translation = translate_text(text_input, target_language)
                st.success("✅ Translation Completed!")
                st.text_area("🗣️ Translation Result:", translation, height=200)

                # 📥 Download button
                st.download_button(
                    label="📥 Download Translation",
                    data=translation,
                    file_name="translation.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"❌ Error: {e}")

# ❤️ Footer
st.markdown("""
    <hr style="border:1px solid #bbb; margin-top: 2em; margin-bottom: 1em;">
    <center style="font-size:12px; color:gray;">
        © 2024 Hello World Translator
    </center>
""", unsafe_allow_html=True)
