from github import Github
from config import VERSION
from tkinter import messagebox

USERNAME = 'usuario_do_github'
REPO_NAME = 'repositorio'

g = Github()

def version_checker():
    # Buscar usuario
    user = g.get_user(USERNAME)

    # Buscar repositorio
    repo = user.get_repo(REPO_NAME)

    # Obter a última release
    latest_release = repo.get_latest_release()

    # Obter a tag associada à última release
    latest_tag = latest_release.tag_name
    
    # Informar nova versão se caso a atual for diferente
    # da ultima lançada
    if latest_tag != VERSION:
        messege = 'Atualizações disponíveis\nExiste uma nova versão do programa. Deseja baixá-la?'
        response = messagebox.askyesno('Atualizações diponiveis', messege)
    else:
        response = False
    return response
