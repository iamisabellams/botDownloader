import yt_dlp
import os
import time

def download_video(url):
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    nome_base = f"video_{int(time.time())}"
    arquivo_cookies = 'cookies.txt'
    usar_cookies = True
    if "youtube.com" in url or "youtu.be" in url:
        usar_cookies = False

    options = {
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'outtmpl': f'downloads/{nome_base}.%(ext)s',
        'noplaylist': True,
        'quiet': True,
        'writethumbnail': False,
        'cookiefile': arquivo_cookies if usar_cookies else None,
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            if options.get('merge_output_format') == 'mp4' and not filename.endswith('.mp4'):
                base, ext = os.path.splitext(filename)
                return base + ".mp4"
                
            return filename

    except Exception as e:
        print(f"Erro no download: {e}")
        return None