import os
import telebot
import threading
from flask import Flask # Import novo
from telebot import types
from dotenv import load_dotenv
from services.downloader import download_video

# site falso para o render manter o bot 100% do tempo vivo
app = Flask(__name__)

@app.route('/')
def home():
    return "Estou vivo! O Bot está rodando."

def run_web_server():
    # pega a porta que o render der ou usa a 8080 padrão
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# inicia o site falso por trás do bot
t = threading.Thread(target=run_web_server)
t.start()
# -----------------------------------------

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

if not TOKEN:
    print("ERRO: Token não encontrado")
    # sem exit() para não derrubar o site falso, mas o bot não funciona sem o token
    
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    btn_sobre = types.InlineKeyboardButton("ℹ️ Sobre", callback_data='botao_sobre')
    markup.add(btn_sobre)
    bot.reply_to(message, f"Olá, {message.from_user.first_name}! Mande o link e eu baixo.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'botao_sobre')
def callback_sobre(call):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, "Feito por uma editora que sofre para baixar videos e por uma aluna de TI curiosa.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if "http" in url:
        msg = bot.reply_to(message, "Analisando...")
        try:
            path = download_video(url)
            if path and os.path.exists(path):
                bot.edit_message_text("Enviando...", chat_id=message.chat.id, message_id=msg.message_id)

                extensao = os.path.splitext(path)[1].lower()

                with open(path, 'rb') as arquivo:
                    if extensao in ['.jpg', '.jpeg', '.png', '.gif']:
                        # se for imagem vai enviar a foto
                        bot.send_photo(message.chat.id, arquivo, caption="Aqui está sua imagem!")
                    elif extensao in ['mp3', '.wav', '.m4a']:
                        
                        # se for áudio vai enviar o áudio
                        bot.send_audio(message.chat.id, arquivo, caption="Aqui está o seu áudio!")

                    else:
                        # se for video envia como video
                        bot.send_video(message.chat.id, arquivo, caption="Aqui está seu vídeo!")

                # remove o arquivo depois de enviar)
                os.remove(path)
                
            else:
                bot.edit_message_text("Falha no download.", chat_id=message.chat.id, message_id=msg.message_id)

        except Exception as e:
            print(e)
            bot.edit_message_text("Erro interno.", chat_id=message.chat.id, message_id=msg.message_id)

if __name__ == "__main__":
    print("Bot rodando...")
    # O infinity_polling reconecta automaticamente se a internet cair
    # timeout=10 e long_polling_timeout=5 ajudam a manter a conexão estável
    bot.infinity_polling(timeout=10, long_polling_timeout=5)