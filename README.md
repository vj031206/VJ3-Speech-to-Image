# 🎙️ VJ3-Speech-to-Image Generator

A Python desktop application that listens to your voice in any language, translates it to English, and generates a unique AI image based on what you said. This project was developed as part of the Codexintern Python Developer internship.

-----

## ✨ Features

  * **🗣️ Multi-Language Support**: Speak in your native language\! The app automatically detects the language and translates it.
  * **🖼️ AI Image Generation**: Utilizes a powerful AI model via the Gradio client to create high-quality images from text prompts. Used due to discontinuation of MonsterAPI
  * **🔴 Live Recording**: A simple "Record" button to capture your voice input directly through your microphone.
  * **🖥️ Modern UI**: Built with Tkinter and styled with ttkbootstrap for a clean and modern user interface.

-----

## 📸 Screenshot

<img width="602" height="539" alt="image" src="https://github.com/user-attachments/assets/7da1e0da-8334-4f1c-ae3a-2b41a1be93b8" />

-----

## 🛠️ Tech Stack

  * **GUI Framework**: `Tkinter`, `ttkbootstrap`
  * **Audio Input**: `pyaudio`, `wave`
  * **Speech Recognition**: `speech_recognition` (using Google's Speech Recognition API)
  * **Translation**: `deep_translator` (using Google Translate)
  * **AI Model Connection**: `gradio_client`, `huggingface_hub`
  * **Image Handling**: `Pillow (PIL)`

-----

## 🚀 Getting Started

Follow these steps to set up and run the project on your local machine.

### 1\. Clone the Repository

First, clone the repository to your local machine.

```bash
git clone https://github.com/vj031206/VJ3-Speech-to-Image.git
cd VJ3-Speech-to-Image
```

### 2\. Create and Activate a Virtual Environment

It's best practice to create a virtual environment to manage dependencies.

  * **On Windows:**
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```
  * **On Linux/macOS:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

### 3\. Install Dependencies

Install all the required Python packages from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

**Note**: `pyaudio` might have system-level dependencies. If you encounter issues on Linux, you may need to install `portaudio` first (`sudo apt-get install portaudio19-dev`).

### 4\. Hugging Face Authentication (Important\!)

This application connects to a model hosted on Hugging Face and **requires you to be authenticated**.

1.  **Get a Token**: If you don't have one, create a Hugging Face account and generate an Access Token with `write` permissions here: **[huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)**.
2.  **Log In**: Run the following command in your terminal and paste your token when prompted.
    ```bash
    huggingface-cli login
    ```

This will save your credentials locally and allow the application to connect successfully.

### 5\. Run the Application

Once your dependencies are installed and you are logged in to Hugging Face, run the main script to launch the application.

```bash
python main.py
```

*(Note: Replace `main.py` with the actual name of your main script if it's different.)*

-----

## 📁 Other Projects

Feel free to check out my other projects:

  * **Gemini Chatbot in Python**: [vj031206/gemini-chat-in-python](https://github.com/vj031206/gemini-chat-in-python.git)
  * **Sentiment Analyser**: [vj031206/VJ3-Sentiment-Analysis-flask](https://github.com/vj031206/VJ3-Sentiment-Analysis-flask.git)
