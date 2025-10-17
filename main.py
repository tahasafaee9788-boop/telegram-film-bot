آخfrom telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
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
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
SPONSOR_CHANNEL = "@marcosrabert"  # آی‌دی کانال اسپانسر

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton("🎬 دریافت فیلم", callback_data="get_film")],
        [InlineKeyboardButton("📞 تماس با ما", url="https://t.me/mts9788")]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.message.reply_text("سلام! لطفاً یکی از گزینه‌های زیر را انتخاب کنید:", reply_markup=keyboard)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "get_film":
        user_id = query.from_user.id
        member = await context.bot.get_chat_member(SPONSOR_CHANNEL, user_id)

        if member.status in ["member", "administrator", "creator"]:
            await query.message.reply_text("🎬 لینک فیلم: https://example.com/film.mp4")
        else:
            buttons = [[InlineKeyboardButton("عضویت در کانال اسپانسر", url=f"https://t.me/{SPONSOR_CHANNEL[1:]}")]]
            keyboard = InlineKeyboardMarkup(buttons)
            await query.message.reply_text("برای دریافت فیلم، ابتدا عضو کانال اسپانسر شوید:", reply_markup=keyboard)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.run_polling()
