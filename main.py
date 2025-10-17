from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

import os
BOT_TOKEN = os.getenv("BOT_TOKEN")
SPONSOR_CHANNELS = ['@marcosrabert']
VIDEO_URL = 'https://yourserver.com/video.mp4'
ADMIN_LINK = 'https://t.me/your_admin'

def main_menu():
    keyboard = [
        [InlineKeyboardButton("🎬 دریافت فیلم", callback_data='get_video')],
        [InlineKeyboardButton("📢 عضویت در کانال‌های اسپانسر", callback_data='join_channels')],
        [InlineKeyboardButton("ℹ️ راهنما و قوانین", callback_data='help')],
        [InlineKeyboardButton("🛠 پشتیبانی", url=ADMIN_LINK)]
    ]
    return InlineKeyboardMarkup(keyboard)

async def check_membership(user_id, bot):
    for channel in SPONSOR_CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                return False
        except:
            return False
    return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام 👋 به ربات ارسال فیلم خوش آمدید!", reply_markup=main_menu())

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data

    if data == 'get_video':
        if await check_membership(user_id, context.bot):
            await query.message.reply_video(video=VIDEO_URL)
        else:
            buttons = [
                [InlineKeyboardButton("📢 عضویت در کانال ۱", url='https://t.me/channel1')],
                [InlineKeyboardButton("📢 عضویت در کانال ۲", url='https://t.me/channel2')]
            ]
            await query.message.reply_text("برای دریافت فیلم، ابتدا عضو کانال‌های زیر شوید:", reply_markup=InlineKeyboardMarkup(buttons))

    elif data == 'join_channels':
        buttons = [
            [InlineKeyboardButton("📢 عضویت در کانال ۱", url='https://t.me/channel1')],
            [InlineKeyboardButton("📢 عضویت در کانال ۲", url='https://t.me/channel2')]
        ]
        await query.message.reply_text("برای دریافت فیلم، لطفاً عضو کانال‌های اسپانسر شوید:", reply_markup=InlineKeyboardMarkup(buttons))

    elif data == 'help':
        await query.message.reply_text("📖 راهنما:\n- برای دریافت فیلم، باید عضو کانال‌های اسپانسر باشید.\n- پس از عضویت، روی «🎬 دریافت فیلم» کلیک کنید.\n- در صورت مشکل، از دکمه «🛠 پشتیبانی» استفاده کنید.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_buttons))
app.run_polling()
