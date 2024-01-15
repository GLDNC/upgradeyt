# Importar os módulos necessários
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QProgressBar, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from ytmusicapi import YTMusic
import yt_dlp
import re
import os
import subprocess
import time

# Criar uma classe para o thread de download
class DownloadThread(QThread):
    # Definir um sinal para atualizar a barra de progresso
    progress = pyqtSignal(int)

    def __init__(self, query):
        # Inicializar o thread com o nome da música
        QThread.__init__(self)
        self.query = query

    def run(self):
        # Executar o código de download no thread
        try:
            # Inicializar a API do YouTube Music
            ytmusic = YTMusic()

            # Pesquisar uma música pelo título
            results = ytmusic.search(self.query, filter="songs")

            # Obter o primeiro resultado da pesquisa
            song = results[0]

            # Obter o título, o artista e o vídeoId da música
            title = song["title"]
            artist = song["artists"][0]["name"]
            videoId = song["videoId"]

            # Criar uma instância do yt-dlp
            ydl_opts = {
                'ffmpeg_location': r'./ffmpeg-6.1.1-essentials_build\\bin\\ffmpeg.exe',
                "format": "bestaudio/best",
                "outtmpl": f"./musics\\{title}",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
                # Definir uma função para atualizar o sinal de progresso
                "progress_hooks": [self.update_progress],
            }

            ydl = yt_dlp.YoutubeDL(ydl_opts)

            # Baixar a música em formato mp3
            ydl.download([f"https://music.youtube.com/watch?v={videoId}"])
            # Abrir a pasta após o download e selecionar o arquivo
            # Abrir a pasta após o download e selecionar o arquivo
            file_path = os.path.abspath(f"./musics/{title}.mp3")  # Adicione a extensão .mp3 uma vez aqui
            subprocess.Popen(f'explorer /select,"{file_path}"')
        except Exception as e:
            # Se ocorrer algum erro, imprimir na tela
            print(e)

    def update_progress(self, d):
        # Atualizar o sinal de progresso com o percentual do download
        if d["status"] == "downloading":
            # Remover os códigos de escape ANSI da string do percentual
            p_str = re.sub(r'\x1b\[.*?m', '', d["_percent_str"])
            # Remover o símbolo de percentagem e converter para um inteiro
            p = int(float(p_str.replace("%", "")))
            self.progress.emit(p)


# Criar uma classe para a janela principal
class MainWindow(QWidget):
    def __init__(self):
        # Inicializar a janela
        QWidget.__init__(self)
        self.setWindowTitle("Baixar Música")
        self.resize(300, 100)

        # Criar os widgets da interface gráfica
        self.label = QLabel("Digite o nome da música:")
        self.input = QLineEdit()
        self.button = QPushButton("Baixar")
        self.progress = QProgressBar()

        # Conectar o botão ao método de baixar a música
        self.button.clicked.connect(self.download)

        # Criar um layout vertical para organizar os widgets
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.progress)

        # Definir o layout da janela
        self.setLayout(self.layout)

    def download(self):
        # Obter o nome da música do campo de entrada
        query = self.input.text()

        # Verificar se o campo de entrada não está vazio
        if query:
            # Desabilitar o botão e o campo de entrada
            self.button.setEnabled(False)
            self.input.setEnabled(False)

            # Criar um thread de download com o nome da música
            self.thread = DownloadThread(query)

            # Conectar o sinal de progresso do thread à barra de progresso
            self.thread.progress.connect(self.update_progress)

            # Iniciar o thread de download
            self.thread.start()

    def update_progress(self, value):
        # Atualizar o valor da barra de progresso
        self.progress.setValue(value)

        # Se o valor for 100, habilitar o botão e o campo de entrada
        if value == 100:
            self.button.setEnabled(True)
            self.input.setEnabled(True)


# Criar uma instância da aplicação
app = QApplication(sys.argv)

# Criar uma instância da janela principal
window = MainWindow()

# Mostrar a janela
window.show()

# Executar a aplicação
sys.exit(app.exec_())
