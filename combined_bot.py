import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Shared CSS styles and particles background
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    
    /* Remove Streamlit's default padding and margins */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Remove any padding or margins from Streamlit's internal containers */
    [data-testid="stAppViewContainer"] {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Remove the transparent rectangles at the top (likely caused by Streamlit's toolbar or spacing) */
    [data-testid="stHeader"] {
        display: none !important;
    }
    
    .main-container {
        max-width: 100%;
        width: 100vw;
        margin: 0 !important;
        padding: 0 !important;
        display: flex;
        justify-content: stretch;
        align-items: stretch;
        gap: 0;
        flex: 1;
        min-height: 0;
    }
    
    .center-line {
        width: 4px;
        background: #ffffff;
        border-radius: 2px;
        margin: 0;
        height: 100%;
        align-self: stretch;
        z-index: 1; /* Ensure the line is visible above other elements */
    }
    
    .chat-container, .image-container {
        flex: 1;
        min-height: 100%;
        overflow-y: auto;
        padding: 10px;
        background: rgba(255, 255, 255, 0.2); /* Slightly transparent background for containers */
        border-radius: 0;
        box-shadow: none;
        margin: 0 !important;
        width: 100%;
    }
    
    .chat-title, .image-title {
        text-align: center;
        margin-bottom: 40px;
        color: white;
    }
    
    .chat-title h1, .image-title h1 {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
        background-size: 300% 300%;
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientShift 3s ease infinite;
        margin-bottom: 20px;
    }
    
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .chat-header, .image-header {
        display: flex;
        align-items: center;
        margin-bottom: 40px;
        padding-bottom: 25px;
        border-bottom: 4px solid #f0f0f0;
    }
    
    .bot-avatar {
        width: 70px;
        height: 70px;
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 25px;
        animation: pulse 2s infinite;
        font-size: 2rem;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .bot-info h3 {
        color: #333;
        margin-bottom: 10px;
        font-size: 1.8rem;
    }
    
    .bot-status {
        color: #4ecdc4;
        font-size: 1.3rem;
        display: flex;
        align-items: center;
    }
    
    .status-dot {
        width: 12px;
        height: 12px;
        background: #4ecdc4;
        border-radius: 50%;
        margin-right: 10px;
        animation: blink 1.5s infinite;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }
    
    .chat-messages {
        min-height: 400px;
        max-height: 500px;
        overflow-y: auto;
        padding: 25px 0;
        margin-bottom: 40px;
    }
    
    .message {
        margin-bottom: 20px;
        animation: slideIn 0.3s ease-out;
        word-wrap: break-word;
    }
    
    .message.user {
        text-align: right;
    }
    
    .message-content {
        display: inline-block;
        max-width: 85%;
        padding: 20px 25px;
        border-radius: 25px;
        position: relative;
        font-size: 1.3rem;
    }
    
    .message.bot .message-content {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-bottom-left-radius: 10px;
    }
    
    .message.user .message-content {
        background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
        color: white;
        border-bottom-right-radius: 10px;
    }
    
    .stTextInput > div > div > input {
        background: white;
        border: 4px solid #e0e0e0;
        border-radius: 25px;
        padding: 20px 25px;
        font-size: 1.4rem;
        color: #333;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 5px rgba(102, 126, 234, 0.1);
        outline: none;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        border: none;
        border-radius: 25px;
        color: white;
        font-size: 1.4rem;
        padding: 20px 40px;
        transition: all 0.3s ease;
        font-weight: 600;
        cursor: pointer;
    }
    
    .stButton > button:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
        border: none;
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    .gallery-grid {
        display: grid;
        gap: 20px;
        max-height: 500px;
        overflow-y: auto;
        grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    }
    
    .gallery-item {
        background: white;
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        animation: fadeIn 0.5s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: scale(0.9); }
        to { opacity: 1; transform: scale(1); }
    }
    
    .gallery-item:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
    }
    
    .gallery-item img {
        width: 100%;
        height: 180px;
        object-fit: cover;
    }
    
    .gallery-item-info {
        padding: 15px;
    }
    
    .gallery-item-prompt {
        font-size: 1rem;
        color: #666;
        margin-bottom: 12px;
        line-height: 1.4;
    }
    
    .download-btn {
        background: linear-gradient(45deg, #4ecdc4, #44a08d);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 25px;
        cursor: pointer;
        font-size: 1rem;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .download-btn:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 25px rgba(78, 205, 196, 0.4);
    }
    
    .loading-container {
        display: flex;
        align-items: center;
        padding: 20px 25px;
        background: rgba(102, 126, 234, 0.1);
        border-radius: 25px;
        margin: 20px 0;
    }
    
    .typing-dots {
        display: flex;
        gap: 8px;
        margin-right: 12px;
    }
    
    .typing-dot {
        width: 10px;
        height: 10px;
        background: #667eea;
        border-radius: 50%;
        animation: typingDots 1.4s infinite;
    }
    
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }
    
    @keyframes typingDots {
        0%, 60%, 100% { transform: scale(1); opacity: 0.5; }
        30% { transform: scale(1.2); opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# Create particles animation script
st.markdown("""
<script>
function createParticles() {
    const particles = document.getElementById('particles');
    if (particles) {
        for (let i = 0; i < 50; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.top = Math.random() * 100 + '%';
            particle.style.animationDelay = Math.random() * 6 + 's';
            particle.style.animationDuration = (Math.random() * 3 + 3) + 's';
            particles.appendChild(particle);
        }
    }
}
createParticles();
</script>
""", unsafe_allow_html=True)

# Main container with two columns and center line
st.markdown('<div class="main-container">', unsafe_allow_html=True)
col1, center_line, col2 = st.columns([0.495, 0.01, 0.495])

# Left column: Text Chat Bot UI and logic
with col1:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    st.markdown("""
    <div class="chat-title">
        <h1>💬 Text Chat Assistant</h1>
        <p>Your intelligent conversational companion</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="chat-header">
        <div class="bot-avatar">🤖</div>
        <div class="bot-info">
            <h3>AI Assistant</h3>
            <div class="bot-status">
                <div class="status-dot"></div>
                <span>Online & Ready</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": "Hello! I'm your AI text assistant. I can help you with questions, provide information, assist with writing, solve problems, and have engaging conversations. What would you like to talk about today?"
        })

    if 'processing' not in st.session_state:
        st.session_state.processing = False

    if 'temp_input' not in st.session_state:
        st.session_state.temp_input = ""

    for message in st.session_state.chat_history:
        if message["role"] == "assistant":
            st.markdown(f'<div class="message bot"><div class="message-content">{message["content"]}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="message user"><div class="message-content">{message["content"]}</div></div>', unsafe_allow_html=True)

    # Use a form to handle input submission
    with st.form(key="chat_form", clear_on_submit=True):
        input_text = st.text_input("Message Input", placeholder="Type your message here...", key="user_input", label_visibility="hidden")
        submit_button = st.form_submit_button("Send")

        if submit_button and input_text:
            st.session_state.temp_input = input_text

    # Process the input outside the form
    if st.session_state.temp_input and not st.session_state.processing:
        st.session_state.processing = True
        st.session_state.chat_history.append({"role": "user", "content": st.session_state.temp_input})

        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template("You are a helpful assistant. Answer the user's queries thoughtfully and concisely."),
            HumanMessagePromptTemplate.from_template("Question: {question}"),
        ])

        llm = ChatGoogleGenerativeAI(model='gemini-1.5-flash')
        output_parser = StrOutputParser()
        chain = prompt | llm | output_parser

        try:
            with st.spinner("AI is thinking..."):
                response = chain.invoke({"question": st.session_state.temp_input})
            st.session_state.chat_history.append({"role": "assistant", "content": response})
        except Exception:
            error_msg = "Sorry, I encountered an error while processing your request. Please try again."
            st.session_state.chat_history.append({"role": "assistant", "content": error_msg})

        st.session_state.processing = False
        st.session_state.temp_input = ""  # Clear the temp input
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# Center line
with center_line:
    st.markdown('<div class="center-line"></div>', unsafe_allow_html=True)

# Right column: Image Generation Bot UI and logic
with col2:
    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    st.markdown("""
    <div class="image-title">
        <h1>🎨 Image Generator Bot</h1>
        <p>Transform your imagination into stunning visuals</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="chat-header">
        <div class="bot-avatar">🤖</div>
        <div class="bot-info">
            <h3>AI Image Generator</h3>
            <div class="bot-status">
                <div class="status-dot"></div>
                <span>Online & Ready</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if 'gallery' not in st.session_state:
        st.session_state.gallery = []

    def generate_image(prompt):
        import requests
        API_KEY = "sk-meCJXa60pfjzDvo4PvaPLLS3xL7uXhmImNwLnKFI0FnTb9eW"
        endpoints = [
            "https://api.stability.ai/v1/generation/stable-diffusion-v1-6/text-to-image",
            "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
        ]
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        data = {
            "text_prompts": [{"text": prompt, "weight": 1}],
            "cfg_scale": 7,
            "height": 512,
            "width": 512,
            "samples": 1,
            "steps": 30
        }
        for url in endpoints:
            try:
                response = requests.post(url, headers=headers, json=data)
                if response.ok:
                    result = response.json()
                    if "artifacts" in result and len(result["artifacts"]) > 0:
                        return f"data:image/png;base64,{result['artifacts'][0]['base64']}"
            except Exception as e:
                continue
        return None

    def add_to_gallery(image_url, prompt):
        st.session_state.gallery.insert(0, {"url": image_url, "prompt": prompt})

    def clear_gallery():
        st.session_state.gallery = []

    image_prompt = st.text_input("Describe the image you want to generate...", key="image_input", label_visibility="hidden")
    generate_btn = st.button("Generate Image")

    if generate_btn and image_prompt.strip():
        with st.spinner("Generating image..."):
            image_url = generate_image(image_prompt)
            if image_url:
                add_to_gallery(image_url, image_prompt)
            else:
                st.error("Sorry, I couldn't generate the image. Please check your API key and try again.")

    if st.button("Clear Gallery"):
        clear_gallery()

    if st.session_state.gallery:
        st.markdown('<div class="gallery-grid">', unsafe_allow_html=True)
        for item in st.session_state.gallery:
            st.markdown(f'''
            <div class="gallery-item">
                <img src="{item["url"]}" alt="Generated image" />
                <div class="gallery-item-info">
                    <div class="gallery-item-prompt">{item["prompt"]}</div>
                    <button class="download-btn" onclick="window.open('{item["url"]}', '_blank')">Download</button>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; color: #FFFFFF; padding: 40px;">
            <div style="font-size: 5rem; margin-bottom: 20px;">🎨</div>
            <p>Your generated images will appear here!</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)