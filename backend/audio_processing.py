import io
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def process_audio(audio_data):
    recognizer = sr.Recognizer()

    try:
        # Save the BytesIO object to a temporary file in the persistent /tmp directory
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".webm", dir="/tmp"
        ) as temp_file:
            temp_file.write(audio_data)
            temp_filename = temp_file.name

        logger.info(f"Temporary file created at {temp_filename}")

        # Verify the temporary file size to check if it's written correctly
        file_size = os.path.getsize(temp_filename)
        logger.info(f"Temporary file size: {file_size} bytes")

        # Convert the webm audio data to wav format
        audio_segment = AudioSegment.from_file(temp_filename, format="webm")
        wav_io = io.BytesIO()
        audio_segment.export(wav_io, format="wav")
        wav_io.seek(0)

        # Remove the temporary file
        os.remove(temp_filename)

        with sr.AudioFile(wav_io) as source:
            audio_content = recognizer.record(source)
        text = recognizer.recognize_google(audio_content)
        return text
    except sr.UnknownValueError as e:
        logger.error(f"Google Speech Recognition could not understand audio: {str(e)}")
        raise ValueError(
            f"Google Speech Recognition could not understand audio: {str(e)}"
        )
    except sr.RequestError as e:
        logger.error(
            f"Could not request results from Google Speech Recognition service; {str(e)}"
        )
        raise ValueError(
            f"Could not request results from Google Speech Recognition service; {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error processing audio file: {str(e)}")
        raise ValueError(f"Error processing audio file: {str(e)}")
