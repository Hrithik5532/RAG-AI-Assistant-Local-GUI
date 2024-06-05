# RAG-AI-Assistant-Local-GUI

# AI Assistant

AI Assistant is a local desktop application built with Python and Tkinter, providing various functionalities like text input, file upload, screenshot capture, and audio recording. The application interacts with an AI model for various tasks and stores user profiles and data locally.

## Features

- **Text Input**: Allows users to enter text and receive responses from the AI.
- **File Upload**: Users can upload files (txt, pdf) to process and query information using the AI model.
- **Screenshot Capture**: Capture screenshots of the screen excluding the GUI and save them locally.
- **Audio Recording**: Record audio using the microphone and save it as a `.wav` file locally.
- **Profile Management**: Save and load user profiles with API keys for easy setup.

## Prerequisites

- Python 3.7 or higher
- Pip (Python package installer)

## Installation

1. **Clone the repository**:
    ```sh
    git clone <your-repository-url>
    cd ai_assistant
    ```

2. **Create a virtual environment (optional but recommended)**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Set up environment variables**:
    - Create a `.env` file in the root directory.
    - Add your API keys in the following format:
      ```
      FIREWORKS_API_KEY=your_fireworks_api_key
      GROQ_API_KEY=your_groq_api_key
      ```

2. **Run the application**:
    ```sh
    python main.py
    ```

3. **Features**:
    - **Text Input**: Click on "Text Input" to open the chat interface.
    - **File Upload**: Click on "Upload File" to upload and process a file.
    - **Take Screenshot**: Click on "Take Screenshot" to capture and save a screenshot.
    - **Start Recording**: Click on "Start Recording" to begin recording audio.
    - **Stop Recording**: Click on "Stop Recording" to stop and save the audio recording.

## Project Structure

```plaintext
ai_assistant/
├── main.py                     # Main application script
├── ai_assistant.db             # SQLite database for storing profiles and data
├── .env                        # Environment variables file (not included in repo)
├── requirements.txt            # Python dependencies
├── Audio/                      # Directory for saving audio recordings
├── Screenshots/                # Directory for saving screenshots
└── utils/
    ├── database.py             # Database handling script
    ├── embedding.py            # Embedding processing script
    ├── handlers.py             # Handler functions for text, file, and audio processing
    └── whisper.py              # Placeholder for whisper functionalities
