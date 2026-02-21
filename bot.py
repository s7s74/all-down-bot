import os
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥 Welcome to all down\nSend a video link.")

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["url"] = update.message.text
    
    keyboard = [
        [
            InlineKeyboardButton("🎥 Video", callback_data="video"),
            InlineKeyboardButton("🎵 Audio", callback_data="audio"),
        ]
    ]
    
    await update.message.reply_text(
        "Choose type:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    url = context.user_data.get("url")
    
    await query.edit_message_text("⏳ Downloading...")
    
    if query.data == "audio":
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'file.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
        }
    else:
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': 'file.%(ext)s',
            'merge_output_format': 'mp4',
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    await query.message.reply_document(open("file.mp4", "rb"))

    os.remove("file.mp4")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()
