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
                with open(path, 'rb') as v:
                    bot.send_video(message.chat.id, v)
                os.remove(path)
            else:
                bot.edit_message_text("Falha no download.", chat_id=message.chat.id, message_id=msg.message_id)
        except Exception as e:
            print(e)
            bot.edit_message_text("Erro interno.", chat_id=message.chat.id, message_id=msg.message_id)

if __name__ == "__main__":
    print("Bot rodando...")
    bot.polling()