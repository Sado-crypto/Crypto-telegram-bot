import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# تنظیمات
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# دستور استارت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! 👋 من ربات تحلیل‌گر کریپتو هستم!\n\nدستورات:\n/price [اسم ارز] - دریافت قیمت\n/analysis - تحلیل بازار")

# دریافت قیمت ارز
async def get_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        coin = context.args[0].lower() if context.args else "bitcoin"
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()
        
        if coin in data:
            price = data[coin]["usd"]
            await update.message.reply_text(f"💰 قیمت {coin.upper()}: ${price:,.2f}")
        else:
            await update.message.reply_text("❌ ارز پیدا نشد! نام صحیح وارد کنید")
    except Exception as e:
        await update.message.reply_text("❌ خطا در دریافت قیمت")

# تحلیل بازار
async def market_analysis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    analysis_text = """
📊 تحلیل بازار کریپتو:

🔸 بیت‌کوین: روند صعودی
🔸 اتریوم: ثبات نسبی  
🔸 بازار کلی: نوسان متوسط

💡 پیشنهاد: سرمایه‌گذاری با احتیاط
    """
    await update.message.reply_text(analysis_text)

# اجرای ربات
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    # handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", get_price))
    app.add_handler(CommandHandler("analysis", market_analysis))
    
    # شروع ربات
    app.run_polling()

if __name__ == "__main__":
    main()
