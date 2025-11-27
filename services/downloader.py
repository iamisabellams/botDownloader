import yt_dlp
import os
import time

def download_video(url):
    # garante que a pasta existe
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    
    timestamp = int(time.time())
    nome_base = f"midia_{timestamp}"
    arquivo_cookies = 'cookies.txt' 
    options = {
        'format': 'best/bestvideo+bestaudio', 
        'outtmpl': f'downloads/{nome_base}_%(playlist_index)s.%(ext)s',
        'quiet': True,
        'noplaylist': False,
        'writethumbnail': False,
        'ignoreerrors': True, 
    }

    if os.path.exists(arquivo_cookies):
        options['cookiefile'] = arquivo_cookies

    arquivos_baixados = []

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            # extrai informações sem baixar primeiro para analisar
            info = ydl.extract_info(url, download=True)
            
            # lógica para coletar os nomes dos arquivos baixados
            if 'entries' in info:
                # é uma playlist ou carrossel 
                for entry in info['entries']:
                    if entry:
                        filename = ydl.prepare_filename(entry)
                        arquivos_baixados.append(filename)
            else:
                # é um arquivo único
                filename = ydl.prepare_filename(info)
                arquivos_baixados.append(filename)
                
            return arquivos_baixados

    except Exception as e:
        print(f"Erro no download: {e}")
        return []