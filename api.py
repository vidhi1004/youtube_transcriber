import os
from fastapi import FastAPI
from pydantic import BaseModel
from downloader import download_audio
from transcriber import transcribe
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


load_dotenv()

app = FastAPI()


class VideoRequest(BaseModel):
    url: str

class QuestionRequest(BaseModel):
    video_id: str
    question: str


@app.post("/transcribe")
def transcribe_video(request: VideoRequest):
    audio_path, video_id = download_audio(request.url, output_dir="data")

    print("DEBUG - audio_path returned from downloader:", audio_path)
    print("DEBUG - does file exist?", os.path.exists(audio_path))

    if not audio_path.endswith(".mp3"):
        base, _ = os.path.splitext(audio_path)
        audio_path = base + ".mp3"
        print("DEBUG - corrected audio_path to:", audio_path)

    video_dir = os.path.join("data", video_id)
    os.makedirs(video_dir, exist_ok=True)

    txt_path, srt_path = transcribe(audio_path, video_dir, model_size="small")

    return {
        "video_id": video_id,
        "audio_path": audio_path,
        "transcript_txt": txt_path,
        "transcript_srt": srt_path,
    }


@app.get("/transcript/{video_id}")
def get_transcript(video_id: str):
    txt_path = os.path.join("data", video_id, "transcript.txt")
    if not os.path.exists(txt_path):
        return {"error": "Transcript not found"}
    with open(txt_path, "r", encoding="utf-8") as f:
        content = f.read()
    return {"video_id": video_id, "transcript": content}


@app.post("/ask")
def ask_question(req: QuestionRequest):
    txt_path = os.path.join("data", req.video_id, "transcript.txt")
    if not os.path.exists(txt_path):
        return {"error": "Transcript not found"}

    with open(txt_path, "r", encoding="utf-8") as f:
        transcript = f.read()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200)
    docs = splitter.create_documents([transcript])

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db = FAISS.from_documents(docs, embeddings)

    retriever = db.as_retriever()
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    answer = qa.invoke(req.question)

    return {"video_id": req.video_id, "question": req.question, "answer": answer}
