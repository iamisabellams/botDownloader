import yt_dlp
import os
import time

def download_video(url):
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    nome_arquivo = f"video_{int(time.time())}"
    arquivo_cookies = 'cookies.txt'

    options = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': f'downloads/{nome_arquivo}.%(ext)s',
        'noplaylist': True,
        'quiet': True,
        'cookiefile': arquivo_cookies,
    }

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