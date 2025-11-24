import yt_dlp
import os
import time

def download_video(url):
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    nome_arquivo = f"midia_{int(time.time())}"
    arquivo_cookies = 'cookies.txt'

    options = {
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'outtmpl': f'downloads/{nome_arquivo}.%(ext)s',
        'noplaylist': True,
        'quiet': True,
        'writethumbnail': False,
        'cookiefile': arquivo_cookies,
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if options.get('merge_output_format') == 'mp4' and not filename.endswith('.mp4'):
                pre, ext = os.path.splitext(filename)
                filename = pre + ".mp4"
                
            return filename
            
    except Exception as e:
        print(f"Erro no download: {e}")
        return None