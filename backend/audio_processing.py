import io
import speech_recognition as sr
from pydub import AudioSegment


def process_audio(audio_data):
    recognizer = sr.Recognizer()

    try:
        audio_file = io.BytesIO(audio_data)
        audio_segment = AudioSegment.from_file(audio_file, format="webm")
        wav_io = io.BytesIO()
        audio_segment.export(wav_io, format="wav")
        wav_io.seek(0)

        with sr.AudioFile(wav_io) as source:
            audio_content = recognizer.record(source)
        text = recognizer.recognize_google(audio_content)
        return text
    except Exception as e:
        raise ValueError(f"Error processing audio file: {str(e)}")