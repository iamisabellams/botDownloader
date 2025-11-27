import os
import telebot
import threading
from flask import Flask
from telebot import types
from dotenv import load_dotenv
from services.downloader import download_video

app = Flask(__name__)

@app.route('/')
def home():
    return "<h3>Bot de Vídeo Online 🤖</h3>"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

t = threading.Thread(target=run_web_server)
t.start()

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()

    btn_git = types.InlineKeyboardButton("GitHub", url="https://github.com/iamisabellams") 
    btn_sobre = types.InlineKeyboardButton("Sobre ℹ️", callback_data='botao_sobre')
    
    markup.add(btn_git, btn_sobre)
    
    bot.reply_to(message, 
                 f"Olá, {message.from_user.first_name}! 👋\n\n"
                 f"Mande um link de **Vídeo** (TikTok, Insta, YouTube) e eu baixo.", 
                 reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'botao_sobre')
def callback_sobre(call):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, "Editora que sofre pra baixar videos e uma aluna de TI curiosa demais.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if "http" in url:
        try:
            msg = bot.reply_to(message, "Procurando vídeo...")
        except:
            return 

        try:
            caminho = download_video(url)
            if caminho and os.path.exists(caminho):
                try:
                    bot.edit_message_text("Baixando...", chat_id=message.chat.id, message_id=msg.message_id)
                except:
                    pass
                with open(caminho, 'rb') as video:
                    bot.send_video(message.chat.id, video, caption="Aqui está!")
                os.remove(caminho)
            else:
                bot.edit_message_text("Erro. Link privado ou não é vídeo.", chat_id=message.chat.id, message_id=msg.message_id)

        except Exception as e:
            print(f"Erro no processo: {e}")
            try:
                bot.edit_message_text("Ocorreu um erro interno.", chat_id=message.chat.id, message_id=msg.message_id)
                if caminho and os.path.exists(caminho):
                    os.remove(caminho)
            except:
                pass

if __name__ == "__main__":
    print("Bot Rodando...")
    bot.infinity_polling(timeout=20, long_polling_timeout=10)