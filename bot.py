import os import openai import google.generativeai as genai from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

====== المفاتيح البيئية ======

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN") OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

تهيئة الذكاء الاصطناعي

openai.api_key = OPENAI_API_KEY genai.configure(api_key=GEMINI_API_KEY) gemini_model = genai.GenerativeModel("gemini-pro")

تخزين اختيار كل مستخدم

user_choice = {}

====== أمر البداية /start ======

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): keyboard = [ [InlineKeyboardButton("المرحلة الأولى", callback_data="مرحلة_أولى")], [InlineKeyboardButton("المرحلة الثانية", callback_data="مرحلة_ثانية")] ] await update.message.reply_text("اختر المرحلة:", reply_markup=InlineKeyboardMarkup(keyboard))

====== اختيار المرحلة ======

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE): query = update.callback_query await query.answer()

if query.data == "مرحلة_أولى":
    user_choice[query.from_user.id] = "gpt"
    await query.edit_message_text("✅ تم اختيار المرحلة الأولى (تعليم و برمجة)")
elif query.data == "مرحلة_ثانية":
    user_choice[query.from_user.id] = "gemini"
    await query.edit_message_text("✅ تم اختيار المرحلة الثانية (أسئلة ومحادثة)")

====== استقبال الرسائل ======

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE): text = update.message.text uid = update.effective_user.id

model = user_choice.get(uid)
if not model:
    await update.message.reply_text("⚠️ اختر المرحلة أولاً باستخدام الأزرار.")
    return

if model == "gpt":
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "أنت أستاذ ومبرمج تشرح خطوة خطوة"},
            {"role": "user", "content": text}
        ]
    )
    reply = response.choices[0].message.content
else:
    response = gemini_model.generate_content(f"تحدث بأسلوب ودود مع المستخدم: {text}")
    reply = response.text

await update.message.reply_text(reply)

====== تشغيل البوت ======

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start)) app.add_handler(CallbackQueryHandler(button_handler)) app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot is running...") app.run_polling()
