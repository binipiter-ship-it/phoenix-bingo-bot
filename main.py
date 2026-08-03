import telebot

# ከ BotFather ያገኙትን ቶከን ከታች ባለው ቦታ ያስገቡ
TOKEN = '8970603591:AAGWxqJ7Kfu_r2R5d8VjMstT2jt7R2ua-fI'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "ሰላም! ወደ ፊኒክስ ቢንጎ (Phoenix Bingo) እንኳን በደህና መጡ! 🎮")

print("ሰርቨሩ ስራ ጀምሯል... ቦቱ መልእክት እየጠበቀ ነው!")
bot.infinity_polling()
