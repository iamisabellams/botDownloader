import os
import telebot
from telebot import types
from dotenv import load_dotenv
from services.downloader import download_video

# CARREGA O TOKEN
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

if not TOKEN:
    print("ERRO: Token não encontrado no .env")
    exit()

bot = telebot.TeleBot(TOKEN)

#  COMANDO /START 
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    nome = message.from_user.first_name
    markup = types.InlineKeyboardMarkup()
    btn_sobre = types.InlineKeyboardButton("ℹ️ Sobre", callback_data='botao_sobre')
    markup.add(btn_sobre)
    
    texto = (
        f"Fala, **{nome}**! 👋\n\n"
        f"Mande o link (YouTube, Instagram, TikTok...) e eu baixo pra você."
    )
    bot.reply_to(message, texto, parse_mode="Markdown", reply_markup=markup)

# BOTÃO SOBRE 
@bot.callback_query_handler(func=lambda call: call.data == 'botao_sobre')
def callback_sobre(call):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, "Projeto Individual de uma aluna de TIC. Feito com Python, telebot e yt-dlp.")

# LÓGICA DE DOWNLOAD 
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    
    # Se tiver "http" (link), tenta baixar
    if "http" in url:
        msg_wait = bot.reply_to(message, "Analisando link...")
        
        try:
            caminho = download_video(url)
            
            if caminho and os.path.exists(caminho):
                bot.edit_message_text("⬇Baixando e enviando...", 
                                      chat_id=message.chat.id, 
                                      message_id=msg_wait.message_id)
                
                with open(caminho, 'rb') as video:
                    bot.send_video(message.chat.id, video, caption="Aqui está!")
                
                # Limpa o arquivo do pc para não pesar
                os.remove(caminho)
            else:
                bot.edit_message_text("Não consegui baixar esse link.", 
                                      chat_id=message.chat.id, 
                                      message_id=msg_wait.message_id)
        except Exception as e:
            print(f"Erro: {e}")
            bot.edit_message_text("Erro ao enviar. Este arquivo pode ser maior do que 50MB, sinto muito.", 
                                  chat_id=message.chat.id, 
                                  message_id=msg_wait.message_id)
            if caminho and os.path.exists(caminho):
                os.remove(caminho)

# CTRL + C PARA PARAR O BOT
if __name__ == "__main__":
    print("Bot rodando...")
    bot.polling()