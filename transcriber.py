from faster_whisper import WhisperModel
import os
def transcribe(audio_path: str, output_dir: str, model_size: str = "small"):
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, info = model.transcribe(
        audio_path, beam_size=5, task="translate", language="en")

    txt_path = os.path.join(output_dir, "transcript.txt")
    srt_path = os.path.join(output_dir, "transcript.srt")

    with open(txt_path, "w", encoding="utf-8") as txt, open(srt_path, "w", encoding="utf-8") as srt:
        for i, segment in enumerate(segments, start=1):
            txt.write(segment.text.strip()+"\n")

            start = format_timestamp(segment.start)
            end = format_timestamp(segment.end)
            srt.write(f"{i}\n{start}-->{end}\n{segment.text.strip()}\n\n")

        return txt_path, srt_path


def format_timestamp(seconds: float) -> str:
    ms = int((seconds % 1)*1000)
    h = int((seconds//3600))
    m = int((seconds % 3600)//60)
    s = int(seconds % 60)
    return f"{h:02}:{m:02}:{s:02}.{ms:03}"
