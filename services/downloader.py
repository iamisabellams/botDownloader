import yt_dlp
import os
import time

def download_video(url):
    # Cria a pasta se não existir
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    # Nome base com timestamp para evitar conflitos
    nome_base = f"midia_{int(time.time())}"
    arquivo_cookies = 'cookies.txt'

    options = {
        # Tenta baixar o melhor vídeo + melhor áudio e junta (resolve o quadrado).
        # Se não der (ex: é foto), baixa o 'best' normal.
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        
        # CARROSSÉIS 
        'noplaylist': False,  # Permite baixar carrossel 
        
        # CONFIGURAÇÕES GERAIS
        'outtmpl': f'downloads/{nome_base}_%(playlist_index)s.%(ext)s', # Adiciona índice para carrosséis não se sobrescreverem
        'quiet': True,
        'writethumbnail': False,
        'cookiefile': arquivo_cookies,
        'ignoreerrors': True, # Se uma foto do carrossel falhar, continua as outras
    }

    arquivos_baixados = []

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            # 1. Extrai informações e baixa
            info = ydl.extract_info(url, download=True)
            
            # 2. Lógica para pegar os nomes dos arquivos
            if 'entries' in info:
                for entry in info['entries']:
                    if entry: 
                        filename = ydl.prepare_filename(entry)
                        arquivos_baixados.append(corrigir_extensao(filename, options))
            else:
                # É um arquivo ÚNICO (Vídeo ou Foto solta)
                filename = ydl.prepare_filename(info)
                arquivos_baixados.append(corrigir_extensao(filename, options))
                
            return arquivos_baixados # Retorna uma LISTA de arquivos agora

    except Exception as e:
        print(f"Erro no download: {e}")
        return []

def corrigir_extensao(filename, options):
    # O FFmpeg muda a extensão para mp4 ao juntar, precisamos ajustar o nome
    if options.get('merge_output_format') == 'mp4' and filename.endswith('.webm'):
        return filename.replace('.webm', '.mp4')
    if options.get('merge_output_format') == 'mp4' and filename.endswith('.mkv'):
        return filename.replace('.mkv', '.mp4')
    return filename