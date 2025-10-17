from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
SPONSOR_CHANNELS = ["@marcosrabert"]  # آی‌دی کانال‌های اسپانسر

# حافظه موقت برای وضعیت کاربران
user_state = {}

# مرحله ۱: شروع و بررسی عضویت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_state[user_id] = {"step": "check_membership"}

    buttons = [
        [InlineKeyboardButton("عضویت در کانال اول", url="https://t.me/marcosrabert")]
        [InlineKeyboardButton("✅ بررسی عضویت", callback_data="check_membership")]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.message.reply_text("برای ادامه، لطفاً در کانال‌های اسپانسر عضو شوید:", reply_markup=keyboard)

# مرحله ۲: بررسی عضویت
async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    for channel in SPONSOR_CHANNELS:
        member = await context.bot.get_chat_member(channel, user_id)
        if member.status not in ["member", "administrator", "creator"]:
            await query.message.reply_text("❌ هنوز عضو همه کانال‌ها نیستید.")
            return

    user_state[user_id]["step"] = "await_video"
    await query.message.reply_text("✅ عضویت تأیید شد. لطفاً یک ویدئو برای من ارسال کنید.")

# مرحله ۳: دریافت ویدئو
async def receive_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_state.get(user_id, {}).get("step") != "await_video":
        return

    video = update.message.video
    if video:
        user_state[user_id]["video_id"] = video.file_id
        user_state[user_id]["step"] = "await_caption"
        await update.message.reply_text("🎬 ویدئو دریافت شد. حالا لطفاً یک متن توضیحی برای این ویدئو بنویسید.")

# مرحله ۴: دریافت متن و نمایش منوی تنظیمات
async def receive_caption(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_state.get(user_id, {}).get("step") != "await_caption":
        return

    user_state[user_id]["caption"] = update.message.text
    user_state[user_id]["step"] = "settings"

    buttons = [
        [InlineKeyboardButton("✅ متنو بگو", callback_data="apply_text"),
         InlineKeyboardButton("❌ بدون متن", callback_data="no_text")],
        [InlineKeyboardButton("<< متن گیف", callback_data="text_left"),
         InlineKeyboardButton("جای متن >>", callback_data="text_right")],
        [InlineKeyboardButton("IRANSans", callback_data="font_iransans"),
         InlineKeyboardButton("🎨 فیلتر", callback_data="apply_filter")],
        [InlineKeyboardButton("🔙 لغو", callback_data="cancel")]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.message.reply_text("تنظیمات متن را انتخاب کنید:", reply_markup=keyboard)

# مرحله ۵: هندلر دکمه‌های تنظیمات
async def settings_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    action = query.data
    video_id = user_state[user_id].get("video_id")
    caption = user_state[user_id].get("caption", "")

    if action == "apply_text":
        await query.message.reply_video(video_id, caption=caption)
        await query.message.reply_text("✅ متن روی ویدئو اعمال شد.")

    elif action == "no_text":
        await query.message.reply_video(video_id)
        await query.message.reply_text("❌ ویدئو بدون متن ارسال شد.")

    elif action == "text_left":
        await query.message.reply_text("📍 متن به سمت چپ منتقل شد. (نمادین)")

    elif action == "text_right":
        await query.message.reply_text("📍 متن به سمت راست منتقل شد. (نمادین)")

    elif action == "font_iransans":
        await query.message.reply_text("🔤 فونت IRANSans انتخاب شد. (نمادین)")

    elif action == "apply_filter":
        await query.message.reply_text("🎨 فیلتر رنگی اعمال شد. (نمادین)")

    elif action == "cancel":
        user_state[user_id]["step"] = "await_video"
        await query.message.reply_text("🔙 عملیات لغو شد. لطفاً دوباره ویدئو ارسال کنید.")

# اجرای ربات
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(check_membership, pattern="check_membership"))
app.add_handler(CallbackQueryHandler(settings_handler))
app.add_handler(MessageHandler(filters.VIDEO, receive_video))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_caption))
app.run_polling()
