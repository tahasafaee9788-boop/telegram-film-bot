from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

SPONSOR_CHANNELS = ['@marcosrabert'] 
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    member = True
    for channel in SPONSOR_CHANNELS:
        chat_member = await context.bot.get_chat_member(channel, user_id)
        if chat_member.status not in ['member', 'administrator', 'creator']:
            member = False
            break

    if member:
        await update.message.reply_text("🎬 لینک فیلم: https://example.com/film.mp4")
    else:
        buttons = [[InlineKeyboardButton("عضویت در کانال‌ها", url=f"https://t.me/{channel[1:]}")] for channel in SPONSOR_CHANNELS]
        await update.message.reply_text("برای دریافت فیلم، ابتدا عضو کانال‌های زیر شوید:", reply_markup=InlineKeyboardMarkup(buttons))

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
