import yt_dlp
import os
import time

def download_video(url):
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    nome_base = f"video_{int(time.time())}"
    
    is_youtube = "youtube.com" in url or "youtu.be" in url

    options = {
        'format': 'bestvideo+bestaudio/best', 
        'merge_output_format': 'mp4',
        'outtmpl': f'downloads/{nome_base}.%(ext)s',
        'noplaylist': True,
        'quiet': True,
        'writethumbnail': False,
    }

    if not is_youtube:
        options['cookiefile'] = 'cookies.txt'

    try:
        print(f"Tentando baixar: {url} (YouTube: {is_youtube})")
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return corrigir_nome(filename)

    except Exception as e:
        print(f"Erro na Tentativa 1 (Qualidade Máxima): {e}")
        if is_youtube:
            print("Tentando Plano B (720p)...")
            options['format'] = 'best[height<=720]/best'
            try:
                with yt_dlp.YoutubeDL(options) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    return corrigir_nome(filename)
            except Exception as e2:
                print(f"Erro na Tentativa 2: {e2}")
                return None
        return None

def corrigir_nome(filename):
    if not filename.endswith('.mp4'):
        base, ext = os.path.splitext(filename)
        if os.path.exists(filename):
            novo_nome = base + ".mp4"
            try:
                os.rename(filename, novo_nome)
                return novo_nome
            except:
                return filename
    return filename