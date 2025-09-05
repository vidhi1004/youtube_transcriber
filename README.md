# YouTube Video Transcriber And Q&A 📝

This project is a powerful tool that lets you "talk" to any YouTube video. It generates a full transcript of the video and then uses Google's powerful AI models as a knowledge base to answer your questions about the video's content.

## ✨ Features

-   **Optimized Video Transcription:** Automatically downloads audio and generates a complete, accurate transcript using the high-performance `faster-whisper` library.
-   **Interactive Q&A with Google AI:** Ask any question about the video's content, and the AI will find the answer from the transcript.
-   **Modern Web Stack:** A user-friendly Streamlit frontend for easy interaction and a robust FastAPI backend for handling the core logic.
-   **Downloadable Transcripts:** Supports downloading the full transcript in both plain text (`.txt`) and subtitle (`.srt`) formats.

## 🛠️ How It Works

The application is composed of two main parts that work together:

1.  **FastAPI Backend (`api.py`):** An API that exposes endpoints to download a YouTube video's audio, transcribe it using `faster-whisper`, and then use that transcript to answer user questions via Google's generative models.
2.  **Streamlit Frontend (`app.py`):** A web application that provides a simple UI to paste a YouTube URL. Once the transcript is generated, you can use the chat interface to ask questions and get answers from the backend API.

The backend uses `yt-dlp` for downloading, the `faster-whisper` library for transcription, and LangChain integrated with a Google model for the Q&A functionality.

## ▶️ Getting Started

### Prerequisites

-   Python 3.8+
-   A Google API key. You can get one from the [Google AI Studio](https://aistudio.google.com/).

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/youtube_transcriber.git](https://github.com/your-username/youtube_transcriber.git)
    cd youtube_transcriber
    ```

2.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your environment variables:**
    Create a file named `.env` in the project's root directory and add your API key:
    ```
    GOOGLE_API_KEY="your_api_key_here"
    ```

### Running the Application

You need to run both the backend API and the frontend application in separate terminals.

1.  **Start the FastAPI Backend:**
    ```bash
    uvicorn api:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000`.

2.  **Run the Streamlit Frontend:**
    ```bash
    streamlit run app.py
    ```
    The web app will open in your browser, usually at `http://127.0.0.1:8501`.

## 💻 Technologies Used

-   **Backend:** FastAPI, Uvicorn, LangChain
-   **Frontend:** Streamlit
-   **Video Processing:** yt-dlp
-   **Transcription:** faster-whisper
-   **AI & Q&A:** Google Generative AI
