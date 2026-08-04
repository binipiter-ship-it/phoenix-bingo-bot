import os
import threading
import http.server
import telebot
import random

# የቦትዎን ቶከን እዚህ ያስገቡ
TOKEN = '8970603591:AAFc45JppRrV6t3Kd4392u0JCuvJ_ATVUpA'
bot = telebot.TeleBot(TOKEN)

# --- 1. የቢንጎ ሎጂክ (Bingo Logic) ---
def generate_bingo_card():
    """ባለ 5x5 ሙሉ የቢንጎ ካርድ ማመንጫ"""
    b = random.sample(range(1, 16), 5)
    i = random.sample(range(16, 31), 5)
    n = random.sample(range(31, 46), 5)
    g = random.sample(range(46, 61), 5)
    o = random.sample(range(61, 76), 5)

    n[2] = "FREE"

    card = []
    for row in range(5):
        card.append([b[row], i[row], n[row], g[row], o[row]])
    return card

def format_card_to_text(card):
    """ካርዱን ቴሌግራም ላይ በሚያምር ሁኔታ ለማሳየት"""
    text = "🎯 **የእርስዎ የቢንጎ ካርድ** 🎯\n\n"
    text += "<code> B | I | N | G | O \n"
    text += "-" * 22 + "\n"
    for row in card:
        formatted_row = []
        for cell in row:
            if cell == "FREE":
                formatted_row.append(" 🆓 ")
            else:
                formatted_row.append(f"{cell:2d} ")
        text += "|".join(formatted_row) + "\n"
    text += "</code>"
    return text

# --- 2. የቴሌግራም ቦት ትዕዛዞች (Bot Handlers) ---
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
import json
import time
import threading

# የተጠቃሚዎችን የተመረጠ ካርድ ለመያዝ
user_cards = {}

from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
import json
import time
import threading

# የተጠቃሚዎችን የተመረጠ ካርድ ለመያዝ
user_cards = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    # እዚህ ጋር የራስዎን ሚኒ-አፕ ሊንክ በትክክል ያስገቡ
    web_app_url = "https://binipiter-ship-it.github.io/phoenix-bingo/" 
    
    markup.add(KeyboardButton(text="🎲 ፊኒክስ ቢንጎ ለመክፈት እዚህ ይጫኑ", web_app=WebAppInfo(url=web_app_url)))
    
    bot.send_message(
        message.chat.id, 
        "ደህና መጡ! ወደ ፊኒክስ ቢንጎ ጨዋታ ለመቀላቀል ከታች ያለውን ቁልፍ ይጫኑ፦", 
        reply_markup=markup
    )

def send_welcome(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    # እዚህ ጋር የራስዎን ሚኒ-አፕ ሊንክ በትክክል ያስገቡ
    web_app_url = "https://binipiter-ship-it.github.io/phoenix-bingo/" 
    
    markup.add(KeyboardButton(text="🎲 ፊኒክስ ቢንጎ ለመክፈት እዚህ ይጫኑ", web_app=WebAppInfo(url=web_app_url)))
    
    bot.send_message(
        message.chat.id, 
        "ደህና መጡ! ወደ ፊኒክስ ቢንጎ ጨዋታ ለመቀላቀል ከታች ያለውን ቁልፍ ይጫኑ፦", 
        reply_markup=markup
    )

import json

# ... (ከላይ ያሉ ሌሎች ኮዶችዎ እንዳሉ ሆነው) ...

@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    """ከሚኒ-አፑ የሚመጣውን የካርድ ምርጫ መቀበያ"""
    try:
        # ከ ሚኒ-አፑ (script.js) የተላከውን ዳታ ማንበብ
        data = json.loads(message.web_app_data.data)
        action = data.get('action')
        card_id = data.get('card_id')

        if action == 'card_selected':
            # 1. መምረጡን ማረጋገጫ መልዕክት መላክ
            bot.send_message(message.chat.id, f"✅ በተሳካ ሁኔታ ካርድ ቁጥር #{card_id} መርጠዋል!")

            # 2. ለተጫዋቹ የካርዱን 5x5 ሰንጠረዥ አውጥቶ መላክ
            new_card = generate_bingo_card()
            card_text = format_card_to_text(new_card)
            bot.send_message(message.chat.id, card_text, parse_mode='HTML')

    except Exception as e:
        bot.send_message(message.chat.id, "❌ ይቅርታ፣ መረጃውን መቀበል አልተቻለም።")

# ... (ከስር ያሉት የ Render ሰርቨር ኮዶች እንዳሉ ይቀጥላሉ) ...

def send_welcome(message):
    welcome_text = "ሰላም! ወደ ፊኒክስ ቢንጎ (Phoenix Bingo) እንኳን በደህና መጡ! 🎮\nእነሆ የሙከራ ካርድዎ፦"
    bot.reply_to(message, welcome_text)
    
    # አዲስ ካርድ አምርቶ ለተጫዋቹ መላክ
    new_card = generate_bingo_card()
    card_text = format_card_to_text(new_card)
    bot.send_message(message.chat.id, card_text, parse_mode='HTML')

# --- 3. Render Web Server (Port Binding) ---
PORT = int(os.environ.get("PORT", 10000))
class SimpleHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Phoenix Bingo Bot is running!")

def run_server():
    server = http.server.HTTPServer(("", PORT), SimpleHandler)
    server.serve_forever()

server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

print("ቦቱ ስራ ጀምሯል...")
bot.infinity_polling()
