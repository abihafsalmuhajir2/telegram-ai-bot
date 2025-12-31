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

# ================== TOKENS ==================
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ================== AI SETUP ==================
openai.api_key = OPENAI_API_KEY
genai.configure(api_key=GEMINI_API_KEY)

# ================== USER MODE ==================
user_mode = {}

# ================== COMMANDS ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 أهلاً بك في البوت الذكي\n\n"
        "📌 اختر المجال من قائمة Menu بالأسفل 👇\n\n"
        "📘 المرحلة الأولى: تعليم + برمجة\n"
        "💬 المرحلة الثانية: أسئلة عامة"
    )

async def stage1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_mode[update.message.from_user.id] = "gpt"
    await update.message.reply_text(
        "✅ تم اختيار المرحلة الأولى (تعليم + برمجة)\n"
        "✍️ اكتب سؤالك الآن"
    )

async def stage2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_mode[update.message.from_user.id] = "gemini"
    await update.message.reply_text(
        "✅ تم اختيار المرحلة الثانية (أسئلة عامة)\n"
        "✍️ اكتب سؤالك الآن"
    )

# ================== MESSAGES ==================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    if user_id not in user_mode:
        await update.message.reply_text(
            "❗ من فضلك اختر المرحلة من قائمة Menu أولاً"
        )
        return

    try:
        if user_mode[user_id] == "gpt":
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "أنت أستاذ جامعي ومبرمج محترف، تشرح بأسلوب مبسط وواضح مع أمثلة."
                    },
                    {
                        "role": "user",
                        "content": text
                    }
                ]
            )
            reply = response.choices[0].message.content

        else:
            model = genai.GenerativeModel("gemini-pro")
            reply = model.generate_content(text).text

        await update.message.reply_text(reply)

    except Exception:
        await update.message.reply_text(
            "⚠️ حدث خطأ مؤقت، حاول مرة أخرى"
        )

# ================== MAIN ==================
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stage1", stage1))
    app.add_handler(CommandHandler("stage2", stage2))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()
