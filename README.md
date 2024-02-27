*upgradeyt*
Este é um projeto em Python que cria uma interface gráfica para baixar músicas do YouTube Music usando as APIs do YouTube Music e do yt-dlp.

Como funciona?

O programa usa a biblioteca ytmusicapi para pesquisar músicas no YouTube Music e obter os links dos vídeos correspondentes. Em seguida, ele usa a biblioteca yt-dlp para baixar os arquivos de áudio dos vídeos e salvá-los em uma pasta especificada pelo usuário. A interface gráfica é criada usando a biblioteca tkinter e permite ao usuário digitar o nome da música, escolher a qualidade do áudio e iniciar o download.

Como instalar
Para executar este projeto, você precisa ter o Python 3 e o FFMPEG instalados em seu computador. Você também precisa instalar as seguintes bibliotecas usando o pip:

ytmusicapi
yt-dlp
pyqt5

Você pode instalar as bibliotecas com o seguinte comando:

python3 -m pip install ytmusicapi yt-dlp pyqt5

Como usar
Para usar este projeto, você precisa clonar este repositório em seu computador e executar o arquivo main.py. Você verá uma janela como esta:

Você pode digitar o nome da música que deseja baixar na caixa de texto e clicar no botão Pesquisar.Você também pode escolher a qualidade do áudio que deseja baixar no menu suspenso. Por fim, você pode clicar no botão Baixar e escolher uma pasta para salvar o arquivo de áudio. O programa irá mostrar o progresso do download e uma mensagem de confirmação quando terminar.
