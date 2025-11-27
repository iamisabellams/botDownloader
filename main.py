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
    return "Bot Online e Operante! 🤖"

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
    btn_sobre = types.InlineKeyboardButton("ℹ️ Sobre", callback_data='botao_sobre')
    markup.add(btn_sobre)
    
    texto = (
        f"Olá, **{message.from_user.first_name}**! 👋\n\n"
        f"Eu baixo vídeos e fotos (Instagram, TikTok, Pinterest, YouTube).\n"
        f"Mande o link e aguarde."
    )
    bot.reply_to(message, texto, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'botao_sobre')
def callback_sobre(call):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, "Bot desenvolvido para facilitar downloads.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    
    if "http" in url:
        msg = None
        try:
            msg = bot.reply_to(message, "🔎 Analisando link...")
        except:
            return

        try:
            lista_arquivos = download_video(url)
            
            if lista_arquivos:
                bot.edit_message_text(f"Baixando {len(lista_arquivos)} arquivo(s)... 🚀", 
                                      chat_id=message.chat.id, 
                                      message_id=msg.message_id)
                
                for path in lista_arquivos:
                    if os.path.exists(path):
                        enviar_arquivo(bot, message.chat.id, path)
                        os.remove(path) 
                try:
                    bot.delete_message(message.chat.id, msg.message_id)
                except:
                    pass
            else:
                bot.edit_message_text("Não consegui baixar. Verifique se o perfil é público ou se o link é válido.", 
                                      chat_id=message.chat.id, 
                                      message_id=msg.message_id)

        except Exception as e:
            print(f"Erro Crítico no Handler: {e}")
            try:
                bot.edit_message_text("Erro interno ao processar.", chat_id=message.chat.id, message_id=msg.message_id)
            except:
                pass

def enviar_arquivo(bot, chat_id, path):
    extensao = os.path.splitext(path)[1].lower()
    
    try:
        with open(path, 'rb') as arquivo:
            # imagens
            if extensao in ['.jpg', '.jpeg', '.png', '.webp', '.heic']:
                bot.send_photo(chat_id, arquivo)
            # áudios
            elif extensao in ['.mp3', '.m4a', '.wav', '.ogg']:
                bot.send_audio(chat_id, arquivo)
            # vídeos 
            else:
                bot.send_video(chat_id, arquivo, supports_streaming=True)
    except Exception as e:
        print(f"Erro ao enviar arquivo {path}: {e}")
        bot.send_message(chat_id, f"Não foi possível enviar este arquivo: {os.path.basename(path)}")

if __name__ == "__main__":
    print("Bot Iniciado...")
    bot.infinity_polling(timeout=20, long_polling_timeout=10)