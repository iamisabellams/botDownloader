import os
import telebot
import threading
from flask import Flask
from telebot import types
from dotenv import load_dotenv
from services.downloader import download_video

# --- SITE FALSO (MANTÉM O RENDER ACORDADO) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Online e Operante! 🤖"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

t = threading.Thread(target=run_web_server)
t.start()
# ---------------------------------------------

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

# Configuração de reconexão automática
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    btn_sobre = types.InlineKeyboardButton("ℹ️ Sobre", callback_data='botao_sobre')
    markup.add(btn_sobre)
    
    texto = (
        f"Olá, **{message.from_user.first_name}**! 👋\n\n"
        f"Eu baixo algumas coisas, youtube, tiktok, pinterest, instagram.\n"
        f"Mande o link e aguarde o envio."
    )
    bot.reply_to(message, texto, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'botao_sobre')
def callback_sobre(call):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, "Feito por uma editora com dificuldade para baixar videos e uma aluna de TI curiosa demais.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    
    if "http" in url:
        try:
            msg = bot.reply_to(message, "Analisando link e baixando...")
        except:
            return # Se não conseguiu responder, aborta

        try:
            # Chama o downloader 
            lista_arquivos = download_video(url)
            
            if lista_arquivos:
                bot.edit_message_text(f"Encontrei {len(lista_arquivos)} arquivo(s). Enviando...", 
                                      chat_id=message.chat.id, 
                                      message_id=msg.message_id)
                
                # Loop para enviar cada arquivo do carrossel
                for path in lista_arquivos:
                    if os.path.exists(path):
                        enviar_arquivo(bot, message.chat.id, path)
                        os.remove(path) # Limpa cada arquivo após enviar
                
            else:
                bot.edit_message_text("Não consegui baixar nada. Verifique se o perfil é público.", 
                                      chat_id=message.chat.id, 
                                      message_id=msg.message_id)

        except Exception as e:
            print(f"Erro Crítico: {e}")
            try:
                bot.edit_message_text("Ocorreu um erro no processamento.", chat_id=message.chat.id, message_id=msg.message_id)
            except:
                pass

def enviar_arquivo(bot, chat_id, path):
    """Função auxiliar para decidir se manda foto, vídeo ou áudio"""
    extensao = os.path.splitext(path)[1].lower()
    
    try:
        with open(path, 'rb') as arquivo:
            if extensao in ['.jpg', '.jpeg', '.png', '.webp']:
                bot.send_photo(chat_id, arquivo)
            elif extensao in ['.mp3', '.m4a', '.wav']:
                bot.send_audio(chat_id, arquivo)
            else:
                # Vídeo (mp4, mkv, mov)
                bot.send_video(chat_id, arquivo)
    except Exception as e:
        print(f"Erro ao enviar arquivo {path}: {e}")

if __name__ == "__main__":
    print("Bot Iniciado...")
    bot.infinity_polling(timeout=20, long_polling_timeout=10)