import os
import threading
import http.server
import socketserver
import telebot

# የራስዎን የ BotFather ቶከን እዚህ በትክክል ያስገቡ
TOKEN = '8970603591:AAGWxqJ7Kfu_r2R5d8VjMstT2jt7R2ua-fI'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "ሰላም! ወደ ፊኒክс ቢንጎ (Phoenix Bingo) እንኳን በደህና መጡ! 🎮")

# Render የሚጠይቀውን ፖርት (Port) ክፍት የሚያደርግ ትንሽ ሰርቨር
PORT = int(os.environ.get("PORT", 10000))

class HealthCheckHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive and running!")

def run_server():
    with socketserver.TCPServer(("", PORT), ) as httpd:
        print(f"Serving HTTP on port {PORT}")
        httpd.serve_forever()

# ሰርቨሩን ከበስተጀርባ (Background) እናስጀምራለን
server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

print("ሰርቨሩ ስራ ጀምሯል... ቦቱ መልእክት እየጠበቀ ነው!")
bot.infinity_polling()
