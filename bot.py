import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
import openai
import google.generativeai as genai

# ---------------- CONFIG ----------------
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

openai.api_key = OPENAI_API_KEY
genai.configure(api_key=GEMINI_API_KEY)

logging.basicConfig(level=logging.INFO)

# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🎓 المرحلة الأولى (GPT)"],
        ["💬 المرحلة الثانية (Gemini)"]
    ]
    await update.message.reply_text(
        "اختر المجال:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# ---------------- GPT ----------------
async def gpt_reply(text: str):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": text}]
    )
    return response.choices[0].message.content

# ---------------- GEMINI ----------------
async def gemini_reply(text: str):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(text)
    return response.text

# ---------------- MESSAGE ----------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if "المرحلة الأولى" in text:
        context.user_data["mode"] = "gpt"
        await update.message.reply_text("📘 تم اختيار GPT (تعليم + برمجة)")
        return

    if "المرحلة الثانية" in text:
        context.user_data["mode"] = "gemini"
        await update.message.reply_text("💬 تم اختيار Gemini (محادثات عامة)")
        return

    mode = context.user_data.get("mode")

    if mode == "gpt":
        reply = await gpt_reply(text)
    elif mode == "gemini":
        reply = await gemini_reply(text)
    else:
        reply = "⚠️ اختر المرحلة أولاً"

    await update.message.reply_text(reply)

# ---------------- MAIN ----------------
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()
