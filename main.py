from Assistente.core.recognition import recognizer
from Assistente.core.intepreter import Ia_Intepreter
from Assistente.features.spotfiy_control import SpotifyController 
from Assistente.core.tts import TTS
# Executar comandos do sistema → Usar os, pyautogui, e subprocess.
class virtual_assistant():
    def __init__(self):       
        self.rz = recognizer()
        self.it = Ia_Intepreter()
        self.tts = TTS()
        self.sp = SpotifyController()

    def choose_response(self, user_input: str):
        classified_input = self.it.resume_and_classify_input(user_input)
        if 'comando' in classified_input:
            classified_input.replace('Tipo: [comando]', '')
            self.sp.treat_cmd(classified_input)
        elif 'pergunta/conversa' in classified_input:
            classified_input.replace('Tipo: [pergunta/conversa]', '')
            response = self.it.response(user_input)
            self.tts.play_tts_audio(response)
            print(response)

    def inicializate(self):
        self.tts.play_tts_audio('Olá meu nome é jucelino, seu assistente virtual.')
        while True:
            question = self.rz.wait_key_word()
            self.choose_response(question)
            

if __name__ == '__main__':
    va = virtual_assistant()
    va.inicializate()

