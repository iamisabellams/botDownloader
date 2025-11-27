import yt_dlp
import os
import time

def setup_cookies():
    cookies_content = os.getenv('COOKIES_CONTENT')
    if cookies_content:
        with open('cookies.txt', 'w') as f:
            f.write(cookies_content)
        print("Arquivo cookies.txt criado via variável de ambiente.")

if __name__ == "__main__":
    setup_cookies() 
    print("Bot Iniciado...")
    bot.infinity_polling(...)

def download_video(url):
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    
    timestamp = int(time.time())
    nome_base = f"midia_{timestamp}"
    
    arquivo_cookies = 'cookies.txt' 

    options = {
        # 'best' é o mais seguro para misturar fotos e vídeos do ig
        'format': 'best', 
        
        'outtmpl': f'downloads/{nome_base}_%(playlist_index)s.%(ext)s',
        'quiet': True,
        'noplaylist': False,
        'writethumbnail': False,
        'ignoreerrors': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
        }
    }
    if os.path.exists(arquivo_cookies):
        options['cookiefile'] = arquivo_cookies

    arquivos_baixados = []

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            try:
                info = ydl.extract_info(url, download=True)
            except yt_dlp.utils.DownloadError as e:
                if "No video formats found" in str(e):
                    print("Erro de formato: Tentando forçar extração genérica...")
                    options['format'] = 'best'
                    return [] 
                raise e 
            if 'entries' in info:
                for entry in info['entries']:
                    if entry:
                        filename = ydl.prepare_filename(entry)
                        arquivos_baixados.append(filename)
            else:
                filename = ydl.prepare_filename(info)
                arquivos_baixados.append(filename)
                
            return arquivos_baixados

    except Exception as e:
        print(f"Erro no download downloader.py: {e}")
        return []