import os 
import subprocess

# criar/excluir/modificar/abrir arquivos
# abrir aplicativos
# 

class control_pc():
    def __init__(self):
        pass 
    
    def open_app(self, user_input: str):
        for root, dirs, files in os.walk("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs"):
            for file in files:
                if user_input.lower() in file.lower():
                    app_path = os.path.join(root, file)
                    subprocess.run(['start', app_path], shell=True)
                    return f'abrindo {file} para teste app_path: {app_path}'
        return 'app não encontrado'
    
a = control_pc()
print(a.open_app('Gerenciador de Tarefas'))