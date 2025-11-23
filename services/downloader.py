import yt_dlp
import os
import time

def download_video(url):
    # cria pasta se não existir
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    nome_arquivo = f"video_{int(time.time())}"
    
    # caminho do arquivo de cookies
    # o bot vai procurar o arquivo 'cookies.txt' na mesma pasta onde ele está rodando
    arquivo_cookies = 'cookies.txt'

    options = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': f'downloads/{nome_arquivo}.%(ext)s',
        'noplaylist': True,
        'quiet': True,
        
        # aqui diz: use as chaves de acesso que estão neste arquivo texto
        'cookiefile': arquivo_cookies,
    }
    
    # verificação de segurança: se o arquivo cookies.txt não existir, avisa no terminal
    if not os.path.exists(arquivo_cookies):
        print(f"AVISO: O arquivo '{arquivo_cookies}' não foi encontrado! O TikTok pode falhar.")

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return filename

    except Exception as e:
        print(f"Erro no download: {e}")
        return None