import requests
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- CONFIG ---
BOT_TOKEN = "8686575510:AAGqx6ddYDeGE5ZxMb14zvUwFRGhidlPjyA" # <---
# --- CONFIG END ---

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "👋 **Welcome to TikSave Pro**\n\n"
        "The fastest TikTok video downloader bot.\n\n"
        "✅ No Watermark\n"
        "✅ High Quality\n"
        "✅ 100% Free & Fast\n\n"
        "Just send me a TikTok link to get started."
    )
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "❓ **How to use?**\n\n"
        "1. Copy any TikTok video link\n"
        "2. Paste it here\n"
        "3. Get your video instantly\n\n"
        "If you face any issue, make sure the video is public."
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if "tiktok.com" not in url:
        await update.message.reply_text("Please send a valid TikTok link. 🔗")
        return

    status_msg = await update.message.reply_text("⏳ Processing your link, please wait...")

    try:
        api_url = f"https://www.tikwm.com/api/?url={url}"
        response = requests.get(api_url, timeout=15).json()

        if response.get('code') == 0:
            data = response.get('data', {})
            video_url = data.get('play')
            title = data.get('title', 'Here is your video!')

            if video_url:
                await status_msg.delete()
                await update.message.reply_video(
                    video=video_url,
                    caption=f"✅ **Done!**\n\n{title}\n\nDownloaded via @YourBotUsername",
                    parse_mode='Markdown'
                )
            else:
                await status_msg.edit_text("❌ Could not find video URL. The video might be private.")
        else:
            await status_msg.edit_text("❌ Invalid link or private video. Please try another link.")

    except Exception as e:
        logging.error(f"Error: {e}")
        await status_msg.edit_text("⚠️ Server is busy, please try again in a moment.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
