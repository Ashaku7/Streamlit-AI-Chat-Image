# AI Multi-Modal Assistant

This project is a Streamlit-based AI-powered multi-modal assistant that combines a Text Chat Assistant and an Image Generator Bot in a single web application. It leverages Google Generative AI for conversational text assistance and Stability AI's Stable Diffusion models for image generation from text prompts.

---

## Features

### Text Chat Assistant
- Interactive chat interface powered by Google Generative AI via Langchain.
- Provides intelligent conversational assistance for questions, information, writing help, problem-solving, and more.
- Maintains chat history for a seamless user experience.
- Responsive and visually appealing UI with custom styling.

### Image Generator Bot
- Generates images from user-provided text prompts using Stability AI's Stable Diffusion API.
- Supports multiple Stable Diffusion endpoints for image generation.
- Displays generated images in a gallery with options to download.
- Allows clearing the gallery to start fresh.
- Handles API errors gracefully with user feedback.

---

## Technologies Used

- [Streamlit](https://streamlit.io/) for building the interactive web UI.
- [Langchain](https://langchain.com/) with Google Generative AI for text-based conversational AI.
- [Stability AI](https://stability.ai/) Stable Diffusion API for text-to-image generation.
- Python 3.x
- dotenv for environment variable management.

---

## Setup and Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your API keys:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   STABILITY_API_KEY=your_stability_ai_api_key_here
   ```

5. Run the Streamlit app:
   ```bash
   streamlit run combined_bot.py
   ```

---

## Usage

- **Text Chat Assistant:** Use the left panel to type your messages and interact with the AI assistant. The assistant can answer questions, provide explanations, and engage in conversations.
- **Image Generator Bot:** Use the right panel to enter descriptive text prompts to generate images. Generated images will appear in the gallery below with options to download or clear the gallery.

---

## Project Structure

- `combined_bot.py`: Main Streamlit application combining chat and image generation functionalities.
- `ai.chatbox.html`: (Optional) HTML file with UI design for the image generator bot.
- Other supporting scripts and configuration files.

---

## Notes

- Ensure you have valid API keys for both Google Generative AI and Stability AI.
- The app uses session state to maintain chat history and image gallery during the session.
- The UI is styled with custom CSS for a modern and engaging user experience.

---

## License

This project is licensed under the MIT License.

---

## Acknowledgments

- Google Generative AI and Langchain for conversational AI capabilities.
- Stability AI for providing powerful text-to-image generation models.
- Streamlit for making web app development simple and fast.
"# Streamlit-AI-Chat-Image" 

## 🚀 Live Demo

👉 [Click here to try the app](https://app-ai-chat-image-generator.streamlit.app/)
