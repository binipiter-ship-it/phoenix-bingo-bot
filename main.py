import os
import threading
import http.server
import telebot

# የቦትዎን ቶከን እዚህ ያስገቡ
TOKEN = '8970603591:AAFc45JppRrV6t3Kd4392u0JCuvJ_ATVUpA'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "ሰላም! ወደ ፊኒክс ቢንጎ (Phoenix Bingo) እንኳን በደህና መጡ! 🎮")

# Render የሚፈልገውን ፖርት (Port) የሚያዘጋጅ ሰርቨር
PORT = int(os.environ.get("PORT", 10000))

class SimpleHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive and running!")

def run_server():
    server = http.server.HTTPServer(("", PORT), SimpleHandler)
    print(f"HTTP server running on port {PORT}")
    server.serve_forever()

# ሰርቨሩን ከበስተጀርባ እናስጀምራለን
server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

print("ቦቱ ስራ ጀምሯል...")
bot.infinity_polling()
