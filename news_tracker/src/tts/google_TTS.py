import os
import time
import logging
import re
from google.cloud import texttospeech
import pygame
from src.utils import remove_links

# Configure logging
logging.basicConfig(
    filename="log.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class TextToSpeechProcessor:
    def __init__(self, credentials_path, language_code="ko-KR", gender=texttospeech.SsmlVoiceGender.FEMALE, speaking_rate=1.55):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        self.language_code = language_code
        self.gender = gender
        self.speaking_rate = speaking_rate
        self.client = texttospeech.TextToSpeechClient()

    @staticmethod
    def sanitize_filename(filename):
        """Replaces invalid characters in the filename with underscores using regex."""
        filename = re.sub(r'[<>:"/\\|?*\n\'\(\)]', '_', str(filename) if filename else "")
        return filename.strip()[:255]  # Limit length

    def text_to_speech(self, text):
        """Converts text to speech, saves it as an MP3 file, and plays it using pygame."""
        if not text:
            logging.error("Empty text passed for synthesis.")
            return None

        synthesis_input = texttospeech.SynthesisInput(text=str(text))  # Ensure text is a string

        voice = texttospeech.VoiceSelectionParams(
            language_code=self.language_code,
            ssml_gender=self.gender,
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=self.speaking_rate
        )

        try:
            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config,
            )
        except Exception as e:
            logging.error(f"Error synthesizing speech: {e}")
            return None

        # Saving the MP3 file with date-based naming
        os.makedirs("audio", exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join("audio", f"audio_{timestamp}.mp3")

        try:
            with open(file_path, "wb") as out:
                out.write(response.audio_content)
        except Exception as e:
            logging.error(f"Error saving audio file {file_path}: {e}")
            return None

        # Playing the audio file using pygame
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)  # Wait for playback to finish
            pygame.mixer.quit()
        except Exception as e:
            logging.error(f"Error playing audio file {file_path}: {e}")
            pygame.mixer.quit()

        return file_path

    def process_texts(self, texts):
        """Processes a list of texts, generates speech, and plays them."""
        for text in texts:
            text = remove_links(text)
            if len(text) > 200:
                logging.warning("Text is too long, skipping.")
                continue
            logging.info("Adding text for speech processing.")
            file_path = self.text_to_speech(text)
            logging.info(f"Processed text: {text}")
            if file_path:
                logging.info(f"Speech file created and played: {file_path}")

def run_text_to_speech_processor(texts):
    """Runs the text-to-speech processing with the provided texts."""
    credentials_path = os.path.join(os.getcwd(), "config/google_TTS_credentials.json")
    logging.info("Initializing TextToSpeechProcessor...")
    processor = TextToSpeechProcessor(credentials_path)
    processor.process_texts(texts)
    logging.info("Text-to-speech processing completed.")

if __name__ == "__main__":
    # Example usage
    texts = ["안녕하세요. 이것은 테스트입니다.", "또 하나의 테스트 문장입니다."]
    run_text_to_speech_processor(texts)
