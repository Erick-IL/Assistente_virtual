# Interpretar Perguntas ->
import google.generativeai as genai
from dotenv import load_dotenv
import os

class Ia_Intepreter():
    def __init__(self):     
        load_dotenv()
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.response_params = '''\n(Responda de forma educada, empática e humanizada. 
        Use uma linguagem clara, acolhedora e simples, como se estivesse conversando diretamente com a pessoa. 
        Explique com exemplos, se necessário e não precisa se extender muito se for uma pergunta simples)'''

        self.resume_params = """
            Analise a mensagem abaixo e determine:
            O tipo de mensagem ('comando', 'pergunta/conversa').
            Extraia apenas as palavras-chave principais da mensagem, limitando a no máximo 5 palavras.
            Caso for uma pergunta retorne a pergunta normalmente sem palavra chave
            Responda no seguinte formato para comando:
            Tipo: [tipo da mensagem]
            Palavras-chave: [palavra1, palavra2, palavra3]
            Responda no seguinte formato para pergunta/conversa:
            Tipo: [tipo da mensagem]

            mensagem para analisar: 
            """

    def response(self, question: str) -> str:
        '''receive user input and give a response'''
        response = self.model.generate_content(
            question + self.response_params,
        )
        return response.text
    
    def resume_and_classify_input(self, user_input: str) -> str:
        ''' receive user input and classify in comand or question and separete '''
        response = self.model.generate_content(
            self.resume_params + user_input
        )
        return response.text
    
if __name__ == '__main__':
    ia = Ia_Intepreter()
    print(ia.resume_and_classify_input('Jeep CIC a nova Inteligência Artificial da China'))
