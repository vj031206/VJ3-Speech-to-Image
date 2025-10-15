import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import Style
import wave
import time
import requests
import threading
import pyaudio
import speech_recognition as sr
from deep_translator import GoogleTranslator
from PIL import Image, ImageTk
from gradio_client import Client

r = sr.Recognizer()

# recording user's speech and converting to text
class VoiceRecorder:

    def __init__(self, root, on_transcript=None):
        self.root = root
        self.on_transcript = on_transcript

        self.button = tk.Button(self.root, height=50, width=50, image=img_mic_on, command=self.click_handler, cursor="hand2")
        self.button.pack(pady=20)

        self.label = tk.Label(self.root, text="00:00", font=("Arial", 12))
        self.label.pack(pady=10)

        self.recording = False

    def click_handler(self):
        self.recording = not self.recording
        self.button.config(image=img_mic_off if self.recording else img_mic_on)

        if self.recording:
            threading.Thread(target=self.record, daemon=True).start()

    def record(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        frames = []

        start = time.time()
        while self.recording:
            try:
                data = stream.read(1024)
                frames.append(data)
                # update timer
                passed = time.time() - start
                t = f"{int(passed//60):02d}:{int(passed%60):02d}"
                self.root.after(0, lambda t=t: self.label.config(text=t))
            except Exception as e:
                print("Recording error:", e)
                break

        stream.stop_stream()
        stream.close()
        audio.terminate()

        sound_file = wave.open(f"rec.wav", 'wb')
        sound_file.setnchannels(1)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(44100)
        sound_file.writeframes(b''.join(frames))
        sound_file.close()

        # Open the audio file
        with sr.AudioFile("rec.wav") as source:
            audio_data = r.record(source)

            try:
                # Use Google Speech Recognition to convert audio to text
                untranslated_text = r.recognize_google(audio_data)
                translator_sync = GoogleTranslator(source='auto', target='en')
                translated_result = translator_sync.translate(untranslated_text)
                text = translated_result if translated_result else ""
                print("Transcribed text:", text)
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")

        if self.on_transcript:
            self.root.after(0, lambda t=text: self.on_transcript(t))

# passing user prompt to the image generation model and displaying the result
class ImageGenerator:

    def __init__(self, root):
        self.root = root
        try:
            self.client = Client("black-forest-labs/FLUX.1-schnell", hf_token="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")
        except requests.exceptions.ConnectionError as e:
            print("Network error: Could not connect to Hugging Face. Please check your internet.")
        except Exception as e:
            print("An error occurred:", e)

        self.input_frame = ttk.Frame(root)
        self.input_frame.pack(pady=20, fill=tk.X, padx=10)

        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_columnconfigure(1, weight=0)

        self.entry_widget = ttk.Entry(self.input_frame, font=("Arial", 14))
        self.button = tk.Button(self.input_frame, text="Generate", cursor="hand2", font=("Arial", 15, 'bold'), command=self.gen_image)
        self.img_label = tk.Label(root)

        self.entry_widget.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        self.button.grid(row=0, column=1, padx=(10, 0))
        self.img_label.pack(pady=20)

    # clearing and inserting user's prompt given by speech into the entry widget
    def set_prompt(self, text):
        self.entry_widget.delete(0, tk.END)
        self.entry_widget.insert(0, text)

    def gen_image(self):
        # Call the Gradio client to generate an image based on the text prompt
        result = self.client.predict(
            prompt=self.entry_widget.get(),
            seed=0,
            randomize_seed=True,
            width=512,
            height=512,
            num_inference_steps=4,
            api_name="/infer"
        )

        # image path set to first element of result list
        img_path = result[0]

        gen_img = Image.open(img_path).resize((256, 256), Image.LANCZOS)
        gen_img = ImageTk.PhotoImage(gen_img)

        # updating image for updated prompt
        self.img_label.config(image=gen_img)
        self.img_label.image = gen_img # keep a reference
        self.img_label.pack(pady=20)

if __name__ == "__main__":
    root = ttk.Window(themename="darkly") # darlkly theme using tkinterbootstrap
    root.title("Audio to Image Generator") # window title
    root.geometry("600x500") # window size
    root.resizable(False, False) # window not resizable

    img_mic_on = ImageTk.PhotoImage(Image.open("mic-on.png"))
    img_mic_off = ImageTk.PhotoImage(Image.open("mic-off.png"))

    images = [img_mic_on, img_mic_off]

    voice_rec = VoiceRecorder(root, on_transcript=None) # initializing voice recorder
    image_gen = ImageGenerator(root) # initializing image generator
    # linking voice recorder and image generator
    voice_rec.on_transcript = image_gen.set_prompt

    root.mainloop()