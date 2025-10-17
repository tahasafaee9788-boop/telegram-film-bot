from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton("عضویت در کانال اسپانسر", url="https://t.me/marcosrabert")]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.message.reply_text("برای دریافت فیلم، ابتدا عضو کانال زیر شوید:", reply_markup=keyboard)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
