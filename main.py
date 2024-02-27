# Importar os módulos necessários
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QProgressBar, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from ytmusicapi import YTMusic
import yt_dlp
import re
import os
import subprocess
from PyQt5.QtWidgets import QTextEdit
import mediafiregrabber
import urllib.request
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QComboBox

# Criar uma classe para o thread de download
class DownloadThread(QThread):

    title_signal = pyqtSignal(str)
    artist_signal = pyqtSignal(str)
    videoId_signal = pyqtSignal(str)

    # Definir um sinal para atualizar a barra de progresso
    progress = pyqtSignal(int)

    # Definir um sinal para atualizar o status
    status = pyqtSignal(str)

    def __init__(self, query, quality, open_folder_after_download):
        # Inicializar o thread com o nome da música
        QThread.__init__(self)
        self.query = query
        self.quality = quality
        self.open_folder_after_download = open_folder_after_download
        
    def run(self):
        # Executar o código de download no thread
        def __init__(self, query, quality):
            QThread.__init__(self)
            self.query = query
            self.quality = quality
        # Baixar ffmpeg se 
            
        self.baixar_ffmpeg()
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

            self.title_signal.emit(title)
            self.artist_signal.emit(artist)
            self.videoId_signal.emit(videoId)

            # Criar uma instância do yt-dlp
            ydl_opts = {
                'ffmpeg_location': r'./ffmpeg.exe',
                "format": "bestaudio/best",
                "outtmpl": f"./musics\\{title}",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": self.quality,
                }],
                # Definir uma função para atualizar o sinal de progresso
                "progress_hooks": [self.update_progress],
            }

            ydl = yt_dlp.YoutubeDL(ydl_opts)

            # Baixar a música em formato mp3
            ydl.download([f"https://music.youtube.com/watch?v={videoId}"])
            # Abrir a pasta após o download e selecionar o arquivo
            # Abrir a pasta após o download e selecionar o arquivo
            if self.open_folder_after_download:
                file_path = os.path.abspath(f"./musics/{title}.mp3")  # Adicione a extensão .mp3 uma vez aqui
                print(f"File path: {file_path}")
                subprocess.run(f'explorer /select,"{file_path}"', check=True)
        
        except Exception as e:
            import traceback
            print(traceback.format_exc() + str(e))
    
    def baixar_ffmpeg(self):
        # Verifique se o ffmpeg está presente
        ffmpeg_path = r'./ffmpeg.exe'
        if not os.path.exists(ffmpeg_path):
            self.status.emit("FFmpeg, não encontrado na pasta raiz, Baixando o ffmpeg...")
            # Se não estiver presente, baixe-o
            file_mediafire = mediafiregrabber.downloadlink('https://www.mediafire.com/file/dpovs3t1ae1chu7/ffmpeg.exe/file')
            link_direto = file_mediafire
            filename = ffmpeg_path
            # Crie o diretório se ele não existir
            os.makedirs(os.path.dirname(filename), exist_ok=True)

            # Função para atualizar a barra de progresso
            def reporthook(blocknum, blocksize, totalsize):
                readsofar = blocknum * blocksize
                if totalsize > 0:
                    percent = readsofar * 1e2 / totalsize
                    self.progress.emit(int(percent))

            urllib.request.urlretrieve(link_direto, filename, reporthook)
            self.status.emit("FFmpeg baixado com sucesso.")

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

        # Adicione esta linha para criar a caixa de texto
        self.status = QTextEdit()
        self.status.setReadOnly(True)  # torna a caixa de texto somente leitura
        self.status.setVisible(False)  # torna a caixa de texto oculta por padrão
        # Conectar o botão ao método de baixar a música
        self.button.clicked.connect(self.download)

        # Criar a caixa de seleção
        self.quality_combobox = QComboBox()
        self.quality_combobox.addItem("192 (Padrão)")
        self.quality_combobox.addItem("128 (Baixa)")
        self.quality_combobox.addItem("320 (Alta)")

        # Criar um layout vertical para organizar os widgets
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.progress)
        self.layout.addWidget(self.quality_combobox)
        
         # Adicione esta linha para adicionar a caixa de texto ao layout
        self.layout.addWidget(self.status)

        # Definir o layout da janela
        self.setLayout(self.layout)

        # Criar a caixa de seleção
        self.details_checkbox = QCheckBox("Detalhes")
        self.details_checkbox.stateChanged.connect(self.toggle_status)
        
        # Adicionar a caixa de seleção ao layout
        self.layout.addWidget(self.details_checkbox)
        
        # Criar a caixa de seleção parar a opção de mostrar na pasta depois que baixar
        self.mostrar_pasta_checkbox = QCheckBox("Mostrar na pasta após o download")
        
        # Adicionar a caixa de seleção ao layout
        self.layout.addWidget(self.mostrar_pasta_checkbox)

    def toggle_status(self, state):
        # Mostrar ou ocultar a caixa de texto de status
        self.status.setVisible(state == Qt.Checked)
        self.adjustSize()  # Ajustar o tamanho da janela
        
    def download(self):
        # Obter o nome da música do campo de entrada
        query = self.input.text()
        # Obter a qualidade selecionada
        quality = self.quality_combobox.currentText().split(" ")[0]

        # Criar um thread de download com o nome da música e a qualidade
        self.thread = DownloadThread(query, quality, self.mostrar_pasta_checkbox.isChecked())

        self.thread.title_signal.connect(self.update_title)
        self.thread.artist_signal.connect(self.update_artist)
        self.thread.videoId_signal.connect(self.update_videoId)
        self.thread.progress.connect(self.update_progress)
        self.thread.status.connect(self.update_status)

        # Verificar se o campo de entrada não está vazio
        if query:
            
            # Desabilitar o botão e o campo de entrada
            self.button.setEnabled(False)
            self.input.setEnabled(False)

             # Atualizar a caixa de status
            self.status.append("Iniciando o download...")
            
            # Iniciar o thread de download
            self.thread.start()

    def update_title(self, title):
        self.status.append(f"Titulo: {title}")

    def update_artist(self, artist):
        self.status.append(f"Artista: {artist}")

    def update_videoId(self, videoId):
        self.status.append(f"ID: {videoId}")

    def update_progress(self, value):
        # Atualizar o valor da barra de progresso
        self.progress.setValue(value)

        # Se o valor for 100, habilitar o botão e o campo de entrada
        if value == 100:
            self.button.setEnabled(True)
            self.input.setEnabled(True)
            self.status.append("Download concluído.")
    def update_status(self, message):
        # Atualizar a caixa de status
        self.status.append(message)

# Criar uma instância da aplicação
app = QApplication(sys.argv)

# Criar uma instância da janela principal
window = MainWindow()

# Mostrar a janela
window.show()

# Executar a aplicação
sys.exit(app.exec_())