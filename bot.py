import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
import openai
import google.generativeai as genai

# ===== TOKENS =====
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

openai.api_key = OPENAI_API_KEY
genai.configure(api_key=GEMINI_API_KEY)

user_mode = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 أهلاً بك\n"
        "اختر المجال من قائمة Menu 👇\n\n"
        "📘 المرحلة الأولى: تعليم + برمجة\n"
        "💬 المرحلة الثانية: أسئلة عامة"
    )

async def stage1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_mode[update.message.from_user.id] = "gemini"
    await update.message.reply_text("✅ المرحلة الأولى مفعلة")

async def stage2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_mode[update.message.from_user.id] = "gemini"
    await update.message.reply_text("✅ المرحلة الثانية مفعلة")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    if user_id not in user_mode:
        await update.message.reply_text("❗ اختر مرحلة من Menu أولاً")
        return

    model = genai.GenerativeModel("gemini-pro")
    reply = model.generate_content(text).text
    await update.message.reply_text(reply)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stage1", stage1))
    app.add_handler(CommandHandler("stage2", stage2))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()
