"""
🤖 مساعد مشروع التخرج مع Hugging Face AI
نسخة مجانية تعمل على Render
"""
import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import requests

# تحميل المتغيرات
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

# إعداد التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ========== الذكاء الاصطناعي المجاني ==========

class FreeAI:
    def __init__(self):
        self.models = {
            "ar": "aubmindlab/aragpt2-base",
            "en": "gpt2",
            "chat": "microsoft/DialoGPT-small"
        }
    
    def get_ai_response(self, message):
        if not HF_TOKEN:
            return self.get_smart_response(message)
        
        try:
            url = "https://api-inference.huggingface.co/models/aubmindlab/aragpt2-base"
            headers = {"Authorization": f"Bearer {HF_TOKEN}"}
            payload = {"inputs": f"المستخدم: {message}\nالمساعد:"}
            
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    ai_text = result[0].get('generated_text', '')
                    if "المساعد:" in ai_text:
                        return ai_text.split("المساعد:")[-1].strip()[:400]
                    return ai_text[:400]
            
            return self.get_smart_response(message)
            
        except:
            return self.get_smart_response(message)
    
    def get_smart_response(self, message):
        msg = message.lower()
        
        if any(word in msg for word in ["مشروع", "فكرة", "اقتراح"]):
            ideas = [
                "🤖 نظام توصية للكتب باستخدام الذكاء الاصطناعي",
                "📱 تطبيق للتعرف على النباتات بالصورة",
                "🌐 موقع لإدارة مشاريع التخرج",
                "🔍 محرك بحث للأبحاث العربية",
                "💬 بوت ذكي للدعم التعليمي"
            ]
            import random
            return f"💡 {random.choice(ideas)}\n\n📋 الخطوات: 1. البحث 2. التصميم 3. التنفيذ 4. الاختبار 5. التوثيق"
        
        elif any(word in msg for word in ["برمجة", "كود", "برنامج"]):
            return "💻 لغات مقترحة:\n🐍 Python للمشاريع البحثية\n🌐 JavaScript للويب\n📱 Flutter للتطبيقات\n\n🛠️ أدوات: GitHub, VS Code, Trello"
        
        elif any(word in msg for word in ["بحث", "مراجع", "دراسة"]):
            return "🔍 مصادر البحث:\n• Google Scholar\n• arXiv\n• IEEE Xplore\n\n📚 نصيحة: ركز على الأوراق الحديثة (آخر 5 سنوات)"
        
        elif any(word in msg for word in ["مساعدة", "help", "ماذا تفعل"]):
            return "🤖 أنا مساعد مشروع التخرج. اسألني عن:\n• أفكار المشاريع\n• المشاكل البرمجية\n• البحث العلمي\n• إدارة المشروع"
        
        else:
            return f"🧐 أرى أنك تسأل عن: '{message}'\n\nهل تريد مساعدة في:\n• فكرة مشروع؟\n• مشكلة برمجية؟\n• بحث علمي؟"

ai_bot = FreeAI()

# ========== أوامر البوت ==========

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"🎓 مرحباً {user.first_name}!\n\n"
        "أنا مساعد مشروع التخرج الذكي 🤖\n"
        "استخدم Hugging Face AI المجاني\n\n"
        "💡 **جرب:**\n"
        "- 'فكرة مشروع'\n"
        "- 'مشكلة برمجية'\n"
        "- 'بحث علمي'\n"
        "- 'مساعده'"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 **كيف تستخدم البوت:**\n\n"
        "💬 **اكتب مباشرة:**\n"
        "- 'فكرة مشروع'\n"
        "- 'برمجة'\n"
        "- 'بحث'\n"
        "- 'مساعدة'\n\n"
        "⚡ **الأوامر:**\n"
        "/start - بدء البوت\n"
        "/help - هذه الرسالة\n"
        "/status - حالة الذكاء الاصطناعي\n\n"
        "🔗 **AI:** Hugging Face (مجاني)"
    )

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status = "✅ متصل بـ Hugging Face AI" if HF_TOKEN else "⚠️ الردود المسبقة فقط"
    await update.message.reply_text(
        f"📊 **حالة البوت:**\n\n"
        f"🤖 الذكاء الاصطناعي: {status}\n"
        "⚡ الخدمة: Render (مجاني)\n"
        "💬 اللغة: العربية\n\n"
        f"{'🔑 لديك 100 طلب يومياً مجاناً' if HF_TOKEN else '⭐ أضف HUGGINGFACE_TOKEN لمزيد من الذكاء'}"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.chat.send_action(action="typing")
    
    # الحصول على رد
    response = ai_bot.get_ai_response(user_message)
    
    # إضافة تذييل إذا كان من AI
    if HF_TOKEN and len(response) > 50 and "Hugging" not in response:
        response += "\n\n🤖 *باستخدام Hugging Face AI المجاني*"
    
    await update.message.reply_text(response)

# ========== التشغيل الرئيسي ==========

def main():
    if not TOKEN:
        print("❌ خطأ: TELEGRAM_BOT_TOKEN غير موجود")
        print("✅ الحل: أضفه في Render → Environment Variables")
        return
    
    app = Application.builder().token(TOKEN).build()
    
    # الأوامر
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("status", status_command))
    
    # الرسائل
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("=" * 50)
    print("🚀 بوت مشروع التخرج الذكي")
    print("🤖 مع Hugging Face AI (مجاني)")
    print("=" * 50)
    print(f"🔗 Hugging Face: {'✅' if HF_TOKEN else '❌'}")
    print("💬 أرسل /start في Telegram")
    print("=" * 50)
    
    app.run_polling()

if __name__ == "__main__":
    main()
