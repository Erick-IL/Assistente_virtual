import speech_recognition as sr
from Assistente.core.intepreter import Ia_Intepreter
from Assistente.core.tts import TTS

# analizar (se possivel trocar lib)

class recognizer():
     def __init__(self):
          self.rec = sr.Recognizer()
          self.it = Ia_Intepreter()
          self.TTS = TTS()       
             
     def wait_question(self) -> str:
        ''' wait user input '''
        with sr.Microphone() as mic: 
                 self.rec.adjust_for_ambient_noise(mic)
                 audio = self.rec.listen(mic, timeout=20, phrase_time_limit=10)
                 try:
                    text = self.rec.recognize_google(audio, language="pt-BR")
                    print(text)
                    return text
                 except:
                      return 'Desculpe, não entendi'

     def wait_key_word(self) -> str:
        ''' wait for a key word and return a question/str '''
        with sr.Microphone() as mic:
            self.rec.adjust_for_ambient_noise(mic) # remove ambient noise
            while True:
                audio = self.rec.listen(mic) # record audio
                try:
                    text = self.rec.recognize_google(audio, language="pt-BR")
                    print(text) # rev

                    if 'bom dia' in text.lower():
                        self.TTS.play_tts_audio('Olá! Como posso ajudar você hoje?')
                        question = self.wait_question()
                        return question
                  
                except sr.UnknownValueError:
                        continue
                except sr.RequestError:
                        print("Erro de comunicação")
                        break   

