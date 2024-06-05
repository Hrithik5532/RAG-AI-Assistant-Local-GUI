import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from PIL import ImageGrab
from datetime import datetime
import sounddevice as sd
import scipy.io.wavfile as wavfile
from utils.database import init_db, save_profile, get_profile
from utils.handlers import handle_text_input, prepare_vectors
from dotenv import load_dotenv
import numpy as np

class AI_Assistant:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Assistant")
        self.root.geometry("600x700")
        self.root.configure(bg="#1e1e1e")  # Dark background

        init_db()
        self.check_profile()

        self.recording = False
        self.audio_data = None

    def check_profile(self):
        profile = get_profile()
        if profile:
            self.name, self.fireworks_key, self.groq_key = profile
            self.ask_use_existing_profile()
        else:
            self.init_profile_window()

    def ask_use_existing_profile(self):
        self.choice_frame = ttk.Frame(self.root, padding=20)
        self.choice_frame.pack(pady=20)

        ttk.Label(self.choice_frame, text="An existing profile was found.", font=("Helvetica", 14)).pack(pady=10)
        ttk.Label(self.choice_frame, text=f"Profile Name: {self.name}", font=("Helvetica", 12)).pack(pady=5)
        ttk.Button(self.choice_frame, text="Use Existing", command=self.use_existing_profile).pack(pady=5)
        ttk.Button(self.choice_frame, text="Input New", command=self.input_new_profile).pack(pady=5)

    def use_existing_profile(self):
        self.choice_frame.destroy()
        self.init_main_window()

    def input_new_profile(self):
        self.choice_frame.destroy()
        self.init_profile_window()

    def init_profile_window(self):
        self.profile_frame = ttk.Frame(self.root, padding=20)
        self.profile_frame.pack(pady=20)

        ttk.Label(self.profile_frame, text="Profile Information", font=("Helvetica", 16)).grid(row=0, columnspan=2, pady=10)
        ttk.Label(self.profile_frame, text="Profile Name").grid(row=1, column=0, padx=10, pady=5)
        ttk.Label(self.profile_frame, text="Fireworks API Key").grid(row=2, column=0, padx=10, pady=5)
        ttk.Label(self.profile_frame, text="Groq API Key").grid(row=3, column=0, padx=10, pady=5)

        self.name_entry = ttk.Entry(self.profile_frame)
        self.fireworks_entry = ttk.Entry(self.profile_frame)
        self.groq_entry = ttk.Entry(self.profile_frame)

        self.name_entry.grid(row=1, column=1, padx=10, pady=5)
        self.fireworks_entry.grid(row=2, column=1, padx=10, pady=5)
        self.groq_entry.grid(row=3, column=1, padx=10, pady=5)

        ttk.Button(self.profile_frame, text="Save", command=self.save_profile).grid(row=4, columnspan=2, pady=10)

    def save_profile(self):
        name = self.name_entry.get()
        fireworks_key = self.fireworks_entry.get()
        groq_key = self.groq_entry.get()

        save_profile(name, fireworks_key, groq_key)
        self.profile_frame.destroy()
        self.init_main_window()

    def init_main_window(self):
        self.button_frame = ttk.Frame(self.root, padding=10)
        self.button_frame.pack(pady=10)

        ttk.Button(self.button_frame, text="Text Input", command=self.init_chat_interface, width=25).grid(row=0, column=0, pady=5)
        ttk.Button(self.button_frame, text="Upload File", command=self.upload_file, width=25).grid(row=1, column=0, pady=5)
        ttk.Button(self.button_frame, text="Take Screenshot", command=self.take_screenshot, width=25).grid(row=2, column=0, pady=5)
        ttk.Button(self.button_frame, text="Start Recording", command=self.start_recording, width=25).grid(row=3, column=0, pady=5)
        ttk.Button(self.button_frame, text="Stop Recording", command=self.stop_recording, width=25).grid(row=4, column=0, pady=5)

        self.chat_frame = None
        self.vectors = None  # Initialize vectors to None

    def init_chat_interface(self):
        if self.chat_frame:
            self.chat_frame.destroy()

        self.chat_frame = ttk.Frame(self.root, padding=10)
        self.chat_frame.pack(pady=10, fill="both", expand=True)

        self.chat_display = scrolledtext.ScrolledText(self.chat_frame, wrap=tk.WORD, height=20, bg="#2e2e2e", fg="#ffffff", insertbackground="white")
        self.chat_display.pack(pady=10, padx=10, fill="both", expand=True)
        self.chat_display.config(state=tk.DISABLED)

        self.chat_display.tag_configure("user", background="#d3d3d3", foreground="#ffffff")
        self.chat_display.tag_configure("ai", background="#000000", foreground="#ffffff")

        self.chat_entry_frame = ttk.Frame(self.chat_frame)
        self.chat_entry_frame.pack(fill="x", padx=10, pady=10)

        self.chat_entry = ttk.Entry(self.chat_entry_frame, width=70)
        self.chat_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=5)

        self.chat_submit_button = ttk.Button(self.chat_entry_frame, text="Submit", command=self.submit_chat)
        self.chat_submit_button.pack(side=tk.RIGHT, padx=5)

    def submit_chat(self):
        user_input = self.chat_entry.get()
        if user_input.strip() == "":
            return

        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"You: {user_input}\n", "user")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_entry.delete(0, tk.END)

        response, context = handle_text_input(self.groq_key, user_input, self.vectors)

        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"AI: {response}\n", "ai")
        if context:
            for doc in context:
                self.chat_display.insert(tk.END, f"\n\n{doc.page_content}\n--------------------------------\n", "context")
        self.chat_display.config(state=tk.DISABLED)

    def upload_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.vectors = prepare_vectors(file_path, self.fireworks_key)
            messagebox.showinfo("Success", "File uploaded and processed successfully. You can now enter your question.")

    def take_screenshot(self):
        # Hide the root window
        self.root.withdraw()
        
        # Pause for a short moment to allow the GUI to be hidden
        self.root.after(500, self.capture_screenshot)

    def capture_screenshot(self):
        screenshot_dir = os.path.join(os.path.dirname(__file__), 'Screenshots')
        os.makedirs(screenshot_dir, exist_ok=True)
        
        # Generate a timestamped filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        screenshot_path = os.path.join(screenshot_dir, f'screenshot_{timestamp}.png')

        # Take the screenshot
        screenshot = ImageGrab.grab()
        screenshot.save(screenshot_path)

        # Show the root window again
        self.root.deiconify()

        messagebox.showinfo("Screenshot", f"Screenshot saved to {screenshot_path}")
        # Here you can add code to process the screenshot and send it to the AI model if needed.

    def start_recording(self):
        if not self.recording:
            self.recording = True
            self.audio_data = []
            messagebox.showinfo("Recording", "Recording started. Speak into the microphone.")
            self.record_audio()

    def record_audio(self):
        def callback(indata, frames, time, status):
            if self.recording:
                self.audio_data.append(indata.copy())

        self.stream = sd.InputStream(callback=callback)
        self.stream.start()

    def stop_recording(self):
        if self.recording:
            self.recording = False
            self.stream.stop()
            self.stream.close()

            audio_dir = os.path.join(os.path.dirname(__file__), 'Audio')
            os.makedirs(audio_dir, exist_ok=True)
            
            # Generate a timestamped filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            audio_path = os.path.join(audio_dir, f'audio_{timestamp}.wav')

            # Save the recorded audio data as a .wav file
            audio_data = np.concatenate(self.audio_data, axis=0)
            wavfile.write(audio_path, 44100, audio_data)

            messagebox.showinfo("Audio", f"Audio recorded and saved to {audio_path}")
            # Here you can add code to process the audio and send it to the AI model if needed.

if __name__ == "__main__":
    load_dotenv()
    root = tk.Tk()
    app = AI_Assistant(root)
    root.mainloop()
