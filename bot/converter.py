import os
import speech_recognition as sr
import subprocess
from langcodes import standardize_tag, LanguageTagError
from configuration import BOT_CONFIG


class Converter():

    def __init__(self, path_to_file: str):
        self.r = sr.Recognizer()
        subprocess.run(['ffmpeg', '-v', 'quiet', '-i',
                       path_to_file, path_to_file.replace(".ogg", ".wav")])
        self.wav_file = path_to_file.replace(".ogg", ".wav")

    def audio_to_text(self, language_code: str) -> str:
        try:
            language_code = standardize_tag(language_code, macro=True)
            print(language_code)
            with sr.AudioFile(self.wav_file) as source:
                audio = self.r.record(source)
                self.r.adjust_for_ambient_noise(source)

            return self.r.recognize_google(audio, language=language_code)
        except LanguageTagError:
            return BOT_CONFIG.LANGUAGE_NOT_SUPPORTED_MESSAGE.get(
                language_code)

    def __del__(self):
        os.remove(self.wav_file)
