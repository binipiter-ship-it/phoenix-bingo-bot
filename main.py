import os
import threading
import http.server
import telebot
import random

# የቦትዎን ቶከን እዚህ ያስገቡ
TOKEN = 'የእርስዎን_ቶከን_እዚህ_ያስገቡ'
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
@bot.message_handler(commands=['start'])
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
