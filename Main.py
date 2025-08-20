import os
import asyncio
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters
from telegram import Update
from deep_translator import GoogleTranslator

BOT_TOKEN = os.getenv("BOT_TOKEN", "7516386110:AAHIXej7iI-mbVpUU6iaaN3_LqISh7pT_80")

translator = GoogleTranslator(source='auto', target='sw')

# Function ya Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        message = (
            "👋 Karibu kwenye *Mtranslator Bot!*\n\n"
            "📌 Tuma maandishi, picha, au video yenye maandishi (caption) — bot hii itatafsiri moja kwa moja kwenda *Kiswahili*.\n\n"
            "💬 Hakikisha ujumbe wako hauanzi na alama ya `/` ili bot isijaribu kuchukulia kama amri.\n\n"
            "🤖 Imetengenezwa kwa kutumia *Python* + *Deep Translator* + *Telegram Bot API*.\n\n"
            "🚀 Jaribu sasa kutuma ujumbe au picha!"
        )
        await update.message.reply_text(message, parse_mode="Markdown")
    except Exception as e:
        await context.bot.send_message(chat_id=-1002158955567, text=f"Hitilafu kwenye /start: {str(e)}")

# Handler ya ujumbe
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        if update.message.text:
            await tr_text(update)
        else:
            await tr_picha_video(update)
    except Exception as e:
        await context.bot.send_message(chat_id=-1002158955567, text=f"Hitilafu kwenye message handler: {str(e)}")

# Tafsiri maandishi
async def tr_text(update: Update) -> None:
    message = update.message.text
    if message.startswith('/'):
        return
    translation_text = translator.translate(message).replace("Mwenyezi Mungu", "Allah")
    if message != translation_text:
        await update.message.reply_text(translation_text, disable_web_page_preview=True)

# Tafsiri picha au video
async def tr_picha_video(update: Update) -> None:
    caption = update.message.caption
    if not caption:
        return
    translation_text = translator.translate(caption).replace("Mwenyezi Mungu", "Allah")
    if update.message.photo:
        await update.message.reply_photo(photo=update.message.photo[-1].file_id, caption=translation_text)
    elif update.message.video:
        await update.message.reply_video(video=update.message.video.file_id, caption=translation_text)
    elif update.message.animation:
        await update.message.reply_animation(animation=update.message.animation.file_id, caption=translation_text)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
