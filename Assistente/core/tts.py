import pygame
import asyncio
import edge_tts
import os

class TTS:
    def __init__(self):
        self.output_file = "audio.mp3"
        pygame.mixer.init()

    async def generate_tts_audio(self, text) -> None:
        communicate = edge_tts.Communicate(text, "pt-BR-AntonioNeural", rate="+20%")
        await communicate.save(self.output_file)

    def play_tts_audio(self, text):
        # Gera o áudio com Edge TTS
        asyncio.run(self.generate_tts_audio(text))

        pygame.mixer.music.load(self.output_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.music.unload()
        os.remove(self.output_file)

if __name__ == "__main__":
    tts = TTS()
    tts.play_tts_audio("Olá, meu nome é Jucelino, seu assistente virtual!")
