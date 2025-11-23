# uma imagem slim (leve) do python, 3.10 é a versão que eu estou usando
FROM python:3.10-slim

# instala o FFmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# define a pasta de trabalho
WORKDIR /app

# copia os arquivos do seu projeto para o servidor
COPY . .

# instalando as bibliotecas do python no servidor
RUN pip install --no-cache-dir -r requirements.txt

# aqui o comando para iniciar o bot
CMD ["python", "main.py"]