import ttkbootstrap as tb
from github import Github
import requests
import os
import threading
import zipfile
import time

USERNAME = 'usuario_do_github'
REPO_NAME = 'repositorio'
NEW_FILES = 'new_files.zip'
FILES_DELETE = 'files_delete.txt'

g = Github()
# Buscar usuario
user = g.get_user(USERNAME)
# buscar repositorio
repo = user.get_repo(REPO_NAME)
# Obter a última release
latest_release = repo.get_latest_release()
# Obter a tag associada à última release
latest_tag = latest_release.tag_name
# Obter a lista de assets da última release
assets = latest_release.get_assets()

class ThreadDownload(threading.Thread):
    def __init__(self, root):
        super().__init__(daemon=True)
        self.root = root
    
    def run(self):
        self.start_update()

    def start_update(self):
        self.download_assets()
        self.delete_old_version_files()
        self.install_new_files()

    def download_assets(self):

        for asset in assets:
            # obter a url de download do asset
            download_url = asset.browser_download_url
            # Baixar o asset
            response = requests.get(download_url, timeout=200)
            
            # Preparar o caminho do arquivo para salvar no disco
            file_path = os.path.join('.', asset.name)
            # Salvar o arquivo no disco
            with open(file_path, 'wb') as file:
                file.write(response.content)

        label_step['text'] = 'Atualização concluida!'
        time.sleep(3)
        self.root.destroy()

    def delete_old_version_files(self):
        # Lista de nomes de arquivos a serem excluídos
        time.sleep(1)

        files_delete = []
        with open(FILES_DELETE, 'r') as file:
            # Lê cada linha do arquivo e adiciona à lista
            for line in file:
                # Remove espaços em branco extras e quebras de linha
                clean_line = line.strip()
                files_delete.append(clean_line)

        # Iterar sobre a lista de arquivos e excluí-los
        for file in files_delete:
            path_file = os.path.join('.', file)

            # Verificar se o arquivo existe antes de excluí-lo
            if os.path.exists(path_file):
                os.remove(path_file)

    def install_new_files(self):
        with zipfile.ZipFile(NEW_FILES, 'r') as zip_ref:
            zip_ref.extractall('.')

def start_thread_dowload(root):
    thread_download_new_version = ThreadDownload(root)
    thread_download_new_version.start()

root = tb.Window()

 # Definir o titulo da janela
root.title('Atualizador')

# Impede o redimensionamento da janela
root.resizable(width=False, height=False)

# Criar variaveis para tamanho da janela
window_width = 400
window_height = 100

# Calculo para centralizar janela na tela
scree_width = root.winfo_screenwidth()
scree_height = root.winfo_screenheight()
axis_x = (int(scree_width) // 2) - (int(window_width) // 2)
axis_y = (int(scree_height) // 2) - (int(window_height) // 2)
axis_x = (int(scree_width) // 2) - (int(window_width) // 2)
axis_y = (int(scree_height) // 2) - (int(window_height) // 2)

# Setar Tamanho e posição na tela
root.geometry(f'{window_width}x{window_height}+{axis_x}+{axis_y}')

label_step = tb.Label(root, text='Atualizando AutoZap')
label_step.pack(pady=20)

# Iniciar a barra de progresso ao iniciar o programa
progrees_bar = tb.Progressbar(root, maximum=100, mode='indeterminate', length=200, value=0)
progrees_bar.pack(pady=10)
progrees_bar.start(10)

# Iniciar o processo em uma nova threard para não travar a interface
root.after(2000, start_thread_dowload, root)

root.mainloop()
